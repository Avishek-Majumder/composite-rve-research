"""Build and verify a tagged DOLFINx mesh from M6 particle metadata.

This script consumes a valid geometry record produced by
14_generate_m6_random_microstructure.py.

It creates a conformal matrix/particle mesh only.
It does not introduce defects or solve the elasticity problem.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import gmsh
import numpy as np
import ufl
from dolfinx import fem
from dolfinx.io import gmsh as gmshio
from mpi4py import MPI


MATRIX_PHYSICAL_TAG = 1
PARTICLE_PHYSICAL_TAG = 2

EXPECTED_GEOMETRY_SCHEMA = "m6_random_microstructure_v1"
MESH_DIAGNOSTICS_SCHEMA = "m6_multi_particle_mesh_diagnostics_v1"

CAD_ABS_TOL = 1.0e-10
TOTAL_AREA_ABS_TOL = 1.0e-10
PARTICLE_FRACTION_TOL = 0.005


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Create and verify a conformal tagged DOLFINx mesh "
            "from valid M6 multi-particle geometry metadata."
        )
    )

    parser.add_argument(
        "--geometry-json",
        type=Path,
        required=True,
        help=(
            "Path to a valid JSON geometry record produced by "
            "14_generate_m6_random_microstructure.py."
        ),
    )

    parser.add_argument(
        "--mesh-size",
        type=float,
        default=0.02048,
        help=(
            "Uniform Gmsh target mesh size. "
            "Defaults to the verified M5 production size 0.02048."
        ),
    )

    return parser.parse_args()


def load_geometry(path: Path) -> dict:
    """Load and validate the required M6 geometry metadata."""

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if data.get("schema") != EXPECTED_GEOMETRY_SCHEMA:
        raise ValueError(
            "Unsupported geometry schema: "
            f"{data.get('schema')!r}. "
            f"Expected {EXPECTED_GEOMETRY_SCHEMA!r}."
        )

    if data.get("status") != "valid":
        raise ValueError(
            "Only geometry records with status='valid' "
            "may be meshed."
        )

    if "rve" not in data:
        raise ValueError("Geometry record is missing 'rve'.")

    if "particles" not in data:
        raise ValueError(
            "Geometry record is missing 'particles'."
        )

    width = float(data["rve"]["width"])
    height = float(data["rve"]["height"])

    if (
        not np.isfinite(width)
        or not np.isfinite(height)
        or width <= 0.0
        or height <= 0.0
    ):
        raise ValueError(
            "RVE width and height must be finite and positive."
        )

    particles = data["particles"]

    requested_count = int(
        data["requested_geometry"]["particle_count"]
    )

    generated_count = int(
        data["generated_geometry"]["particle_count"]
    )

    if len(particles) != requested_count:
        raise ValueError(
            "Particle list length does not match "
            "requested particle count."
        )

    if len(particles) != generated_count:
        raise ValueError(
            "Particle list length does not match "
            "generated particle count."
        )

    if len(particles) <= 0:
        raise ValueError(
            "At least one particle is required."
        )

    expected_ids = list(
        range(1, len(particles) + 1)
    )

    actual_ids = [
        int(particle["particle_id"])
        for particle in particles
    ]

    if actual_ids != expected_ids:
        raise ValueError(
            "Particle IDs must be consecutive and ordered "
            "from 1 through particle_count."
        )

    for particle in particles:
        center_x = float(particle["center_x"])
        center_y = float(particle["center_y"])
        radius = float(particle["radius"])

        if (
            not np.isfinite(center_x)
            or not np.isfinite(center_y)
        ):
            raise ValueError(
                "Particle centers must be finite."
            )

        if (
            not np.isfinite(radius)
            or radius <= 0.0
        ):
            raise ValueError(
                "Particle radii must be finite and positive."
            )

        if not (
            center_x - radius > 0.0
            and center_x + radius < width
            and center_y - radius > 0.0
            and center_y + radius < height
        ):
            raise ValueError(
                f"Particle {particle['particle_id']} "
                "does not lie strictly inside the RVE."
            )

    return data


def build_mesh(
    geometry: dict,
    mesh_size: float,
):
    """Create the conformal Gmsh model and convert it to DOLFINx."""

    if (
        not np.isfinite(mesh_size)
        or mesh_size <= 0.0
    ):
        raise ValueError(
            "mesh-size must be finite and positive."
        )

    width = float(geometry["rve"]["width"])
    height = float(geometry["rve"]["height"])

    particles = geometry["particles"]

    expected_particle_area = sum(
        math.pi * float(particle["radius"]) ** 2
        for particle in particles
    )

    expected_total_area = width * height

    expected_matrix_area = (
        expected_total_area
        - expected_particle_area
    )

    metadata_particle_area = float(
        geometry["generated_geometry"]["particle_area"]
    )

    if not math.isclose(
        expected_particle_area,
        metadata_particle_area,
        rel_tol=0.0,
        abs_tol=CAD_ABS_TOL,
    ):
        raise ValueError(
            "Particle areas reconstructed from radii "
            "do not match the geometry metadata."
        )

    gmsh.initialize()

    try:
        gmsh.option.setNumber(
            "General.Terminal",
            0,
        )

        gmsh.model.add(
            "m6_multi_particle_mesh"
        )

        rectangle_tag = (
            gmsh.model.occ.addRectangle(
                0.0,
                0.0,
                0.0,
                width,
                height,
            )
        )

        disk_tags: list[int] = []

        for particle in particles:
            disk_tag = gmsh.model.occ.addDisk(
                float(particle["center_x"]),
                float(particle["center_y"]),
                0.0,
                float(particle["radius"]),
                float(particle["radius"]),
            )

            disk_tags.append(disk_tag)

        (
            _fragmented_entities,
            fragment_map,
        ) = gmsh.model.occ.fragment(
            [(2, rectangle_tag)],
            [
                (2, disk_tag)
                for disk_tag in disk_tags
            ],
            removeObject=True,
            removeTool=True,
        )

        gmsh.model.occ.synchronize()

        expected_map_count = (
            1 + len(particles)
        )

        if len(fragment_map) != expected_map_count:
            raise RuntimeError(
                "Unexpected Gmsh fragment-map length."
            )

        particle_surface_tags: list[int] = []

        for particle_index, mapping in enumerate(
            fragment_map[1:],
            start=1,
        ):
            mapped_surfaces = [
                tag
                for dim, tag in mapping
                if dim == 2
            ]

            if len(mapped_surfaces) != 1:
                raise RuntimeError(
                    "Particle "
                    f"{particle_index} mapped to "
                    f"{len(mapped_surfaces)} surfaces; "
                    "exactly one was expected."
                )

            particle_surface_tags.append(
                mapped_surfaces[0]
            )

        if (
            len(set(particle_surface_tags))
            != len(particles)
        ):
            raise RuntimeError(
                "Particle surfaces are not unique."
            )

        all_surface_tags = sorted(
            tag
            for dim, tag
            in gmsh.model.getEntities(2)
        )

        matrix_candidates = sorted(
            set(all_surface_tags)
            - set(particle_surface_tags)
        )

        if len(matrix_candidates) != 1:
            raise RuntimeError(
                "Exactly one matrix surface was expected."
            )

        matrix_surface_tag = (
            matrix_candidates[0]
        )

        if len(all_surface_tags) != (
            len(particles) + 1
        ):
            raise RuntimeError(
                "Expected one matrix surface plus "
                "one surface for every particle."
            )

        calculated_cad_particle_area = 0.0

        particle_cad_checks = []

        for particle, surface_tag in zip(
            particles,
            particle_surface_tags,
            strict=True,
        ):
            radius = float(
                particle["radius"]
            )

            expected_area = (
                math.pi * radius**2
            )

            actual_area = (
                gmsh.model.occ.getMass(
                    2,
                    surface_tag,
                )
            )

            center_of_mass = (
                gmsh.model.occ.getCenterOfMass(
                    2,
                    surface_tag,
                )
            )

            expected_x = float(
                particle["center_x"]
            )

            expected_y = float(
                particle["center_y"]
            )

            area_ok = math.isclose(
                actual_area,
                expected_area,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            center_x_ok = math.isclose(
                center_of_mass[0],
                expected_x,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            center_y_ok = math.isclose(
                center_of_mass[1],
                expected_y,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            center_z_ok = math.isclose(
                center_of_mass[2],
                0.0,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            particle_cad_checks.append(
                {
                    "particle_id": int(
                        particle["particle_id"]
                    ),
                    "surface_tag": int(
                        surface_tag
                    ),
                    "area_ok": bool(area_ok),
                    "center_x_ok": bool(
                        center_x_ok
                    ),
                    "center_y_ok": bool(
                        center_y_ok
                    ),
                    "center_z_ok": bool(
                        center_z_ok
                    ),
                }
            )

            if not all(
                [
                    area_ok,
                    center_x_ok,
                    center_y_ok,
                    center_z_ok,
                ]
            ):
                raise RuntimeError(
                    "CAD verification failed for "
                    f"particle {particle['particle_id']}."
                )

            calculated_cad_particle_area += (
                actual_area
            )

        actual_matrix_cad_area = (
            gmsh.model.occ.getMass(
                2,
                matrix_surface_tag,
            )
        )

        if not math.isclose(
            calculated_cad_particle_area,
            expected_particle_area,
            rel_tol=0.0,
            abs_tol=CAD_ABS_TOL,
        ):
            raise RuntimeError(
                "Combined CAD particle area mismatch."
            )

        if not math.isclose(
            actual_matrix_cad_area,
            expected_matrix_area,
            rel_tol=0.0,
            abs_tol=CAD_ABS_TOL,
        ):
            raise RuntimeError(
                "CAD matrix area mismatch."
            )

        matrix_boundary_curves = {
            tag
            for dim, tag
            in gmsh.model.getBoundary(
                [(2, matrix_surface_tag)],
                combined=False,
                oriented=False,
                recursive=False,
            )
            if dim == 1
        }

        particle_boundary_curves: set[int] = set()

        for surface_tag in particle_surface_tags:
            particle_boundary_curves.update(
                tag
                for dim, tag
                in gmsh.model.getBoundary(
                    [(2, surface_tag)],
                    combined=False,
                    oriented=False,
                    recursive=False,
                )
                if dim == 1
            )

        shared_interface_curves = (
            matrix_boundary_curves
            & particle_boundary_curves
        )

        outer_boundary_curves = (
            matrix_boundary_curves
            - particle_boundary_curves
        )

        if (
            particle_boundary_curves
            != shared_interface_curves
        ):
            raise RuntimeError(
                "Particle boundaries are not fully shared "
                "with the matrix."
            )

        if len(outer_boundary_curves) != 4:
            raise RuntimeError(
                "Expected four external RVE boundary curves."
            )

        gmsh.model.addPhysicalGroup(
            2,
            [matrix_surface_tag],
            tag=MATRIX_PHYSICAL_TAG,
            name="matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            particle_surface_tags,
            tag=PARTICLE_PHYSICAL_TAG,
            name="particle",
        )

        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMin",
            mesh_size,
        )

        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMax",
            mesh_size,
        )

        gmsh.model.mesh.generate(2)

        mesh_data = gmshio.model_to_mesh(
            gmsh.model,
            MPI.COMM_WORLD,
            rank=0,
            gdim=2,
        )

    finally:
        gmsh.finalize()

    topology_diagnostics = {
        "matrix_surface_tag": int(
            matrix_surface_tag
        ),
        "particle_surface_tags": [
            int(tag)
            for tag in particle_surface_tags
        ],
        "particle_cad_checks": (
            particle_cad_checks
        ),
        "cad_matrix_area": float(
            actual_matrix_cad_area
        ),
        "cad_particle_area": float(
            calculated_cad_particle_area
        ),
        "outer_boundary_curve_count": int(
            len(outer_boundary_curves)
        ),
        "shared_interface_curve_count": int(
            len(shared_interface_curves)
        ),
    }

    return (
        mesh_data,
        topology_diagnostics,
        expected_total_area,
        expected_particle_area,
    )


def verify_dolfinx_mesh(
    mesh_data,
    expected_total_area: float,
    expected_particle_area: float,
    mesh_size: float,
    geometry: dict,
    topology_diagnostics: dict,
) -> dict:
    """Verify material tags and numerical mesh areas in DOLFINx."""

    domain = mesh_data.mesh
    cell_tags = mesh_data.cell_tags

    if cell_tags is None:
        raise RuntimeError(
            "DOLFINx did not receive material cell tags."
        )

    physical_groups = (
        mesh_data.physical_groups
    )

    if "matrix" not in physical_groups:
        raise RuntimeError(
            "Matrix physical group was not transferred."
        )

    if "particle" not in physical_groups:
        raise RuntimeError(
            "Particle physical group was not transferred."
        )

    matrix_tag = int(
        physical_groups["matrix"].tag
    )

    particle_tag = int(
        physical_groups["particle"].tag
    )

    if matrix_tag != MATRIX_PHYSICAL_TAG:
        raise RuntimeError(
            "Unexpected DOLFINx matrix physical tag."
        )

    if particle_tag != PARTICLE_PHYSICAL_TAG:
        raise RuntimeError(
            "Unexpected DOLFINx particle physical tag."
        )

    tdim = domain.topology.dim

    owned_cell_count = (
        domain.topology.index_map(
            tdim
        ).size_local
    )

    total_cell_count = (
        domain.comm.allreduce(
            owned_cell_count,
            op=MPI.SUM,
        )
    )

    matrix_cells = (
        cell_tags.find(matrix_tag)
    )

    particle_cells = (
        cell_tags.find(particle_tag)
    )

    matrix_owned_cells = matrix_cells[
        matrix_cells < owned_cell_count
    ]

    particle_owned_cells = particle_cells[
        particle_cells < owned_cell_count
    ]

    tagged_cell_count = (
        domain.comm.allreduce(
            len(matrix_owned_cells)
            + len(particle_owned_cells),
            op=MPI.SUM,
        )
    )

    dx = ufl.Measure(
        "dx",
        domain=domain,
        subdomain_data=cell_tags,
    )

    matrix_area_local = (
        fem.assemble_scalar(
            fem.form(
                1.0 * dx(matrix_tag)
            )
        )
    )

    particle_area_local = (
        fem.assemble_scalar(
            fem.form(
                1.0 * dx(particle_tag)
            )
        )
    )

    matrix_area = (
        domain.comm.allreduce(
            matrix_area_local,
            op=MPI.SUM,
        )
    )

    particle_area = (
        domain.comm.allreduce(
            particle_area_local,
            op=MPI.SUM,
        )
    )

    total_area = (
        matrix_area + particle_area
    )

    analytical_particle_fraction = (
        expected_particle_area
        / expected_total_area
    )

    meshed_particle_fraction = (
        particle_area / total_area
    )

    particle_fraction_error = abs(
        meshed_particle_fraction
        - analytical_particle_fraction
    )

    checks = {
        "all_cells_tagged": (
            tagged_cell_count
            == total_cell_count
        ),
        "positive_matrix_area": (
            matrix_area > 0.0
        ),
        "positive_particle_area": (
            particle_area > 0.0
        ),
        "total_area": math.isclose(
            total_area,
            expected_total_area,
            rel_tol=0.0,
            abs_tol=TOTAL_AREA_ABS_TOL,
        ),
        "particle_fraction": (
            particle_fraction_error
            <= PARTICLE_FRACTION_TOL
        ),
        "matrix_physical_tag": (
            matrix_tag
            == MATRIX_PHYSICAL_TAG
        ),
        "particle_physical_tag": (
            particle_tag
            == PARTICLE_PHYSICAL_TAG
        ),
    }

    if not all(checks.values()):
        failed_checks = [
            name
            for name, passed
            in checks.items()
            if not passed
        ]

        raise RuntimeError(
            "DOLFINx mesh verification failed: "
            + ", ".join(failed_checks)
        )

    return {
        "schema": MESH_DIAGNOSTICS_SCHEMA,
        "geometry_schema": geometry["schema"],
        "geometry_seed": int(
            geometry["rng"]["seed"]
        ),
        "particle_count": int(
            len(geometry["particles"])
        ),
        "mesh_size": float(mesh_size),
        "physical_tags": {
            "matrix": matrix_tag,
            "particle": particle_tag,
        },
        "topology": topology_diagnostics,
        "mesh": {
            "cell_count": int(
                total_cell_count
            ),
            "tagged_cell_count": int(
                tagged_cell_count
            ),
            "matrix_cell_count": int(
                domain.comm.allreduce(
                    len(matrix_owned_cells),
                    op=MPI.SUM,
                )
            ),
            "particle_cell_count": int(
                domain.comm.allreduce(
                    len(particle_owned_cells),
                    op=MPI.SUM,
                )
            ),
        },
        "area": {
            "expected_total_area": float(
                expected_total_area
            ),
            "meshed_total_area": float(
                total_area
            ),
            "expected_particle_area": float(
                expected_particle_area
            ),
            "meshed_particle_area": float(
                particle_area
            ),
            "meshed_matrix_area": float(
                matrix_area
            ),
            "analytical_particle_area_fraction": float(
                analytical_particle_fraction
            ),
            "meshed_particle_area_fraction": float(
                meshed_particle_fraction
            ),
            "particle_area_fraction_error": float(
                particle_fraction_error
            ),
        },
        "checks": {
            name: bool(passed)
            for name, passed
            in checks.items()
        },
        "status": "valid",
    }


def main() -> int:
    """Build and verify one multi-particle mesh."""

    args = parse_args()

    geometry = load_geometry(
        args.geometry_json
    )

    (
        mesh_data,
        topology_diagnostics,
        expected_total_area,
        expected_particle_area,
    ) = build_mesh(
        geometry,
        float(args.mesh_size),
    )

    diagnostics = verify_dolfinx_mesh(
        mesh_data=mesh_data,
        expected_total_area=(
            expected_total_area
        ),
        expected_particle_area=(
            expected_particle_area
        ),
        mesh_size=float(args.mesh_size),
        geometry=geometry,
        topology_diagnostics=(
            topology_diagnostics
        ),
    )

    if MPI.COMM_WORLD.rank == 0:
        print(
            json.dumps(
                diagnostics,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
