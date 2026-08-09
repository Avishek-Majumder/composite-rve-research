"""Build and verify a tagged DOLFINx mesh from M7 void metadata.

This script consumes a valid geometry record produced by
17_generate_m7_void_microstructure.py.

It preserves matrix and particle material cells while representing
Version-1 circular voids as true geometric holes.
It does not solve the elasticity problem.
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
VOID_BOUNDARY_PHYSICAL_TAG = 3

EXPECTED_GEOMETRY_SCHEMA = "m7_void_microstructure_v1"
SOURCE_M6_GEOMETRY_SCHEMA = "m6_random_microstructure_v1"
MESH_DIAGNOSTICS_SCHEMA = "m7_void_mesh_diagnostics_v1"

CAD_ABS_TOL = 1.0e-10
TOTAL_AREA_ABS_TOL = 1.0e-10
PARTICLE_FRACTION_TOL = 0.005
MATRIX_FRACTION_TOL = 0.005
VOID_FRACTION_TOL = 0.005
SOLID_FRACTION_TOL = 0.005
VOID_BOUNDARY_LENGTH_REL_TOL = 0.05


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Create and verify a conformal tagged DOLFINx mesh "
            "from valid M7 circular-void geometry metadata."
        )
    )

    parser.add_argument(
        "--geometry-json",
        type=Path,
        required=True,
        help=(
            "Path to a valid JSON geometry record produced by "
            "17_generate_m7_void_microstructure.py."
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
    """Load and independently validate required M7 geometry metadata."""

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
            "Only M7 geometry records with status='valid' "
            "may be meshed."
        )

    required_top_level = (
        "rve",
        "source_m6_geometry",
        "rng",
        "requested_void_geometry",
        "generated_geometry",
        "checks",
        "particles",
        "voids",
    )

    missing = [
        key
        for key in required_top_level
        if key not in data
    ]

    if missing:
        raise ValueError(
            "M7 geometry record is missing required fields: "
            + ", ".join(missing)
        )

    source_m6 = data["source_m6_geometry"]

    requested_void_geometry = data[
        "requested_void_geometry"
    ]

    generated = data[
        "generated_geometry"
    ]

    checks = data["checks"]

    if not isinstance(source_m6, dict):
        raise ValueError(
            "'source_m6_geometry' must be a dictionary."
        )

    if (
        source_m6.get("schema")
        != SOURCE_M6_GEOMETRY_SCHEMA
    ):
        raise ValueError(
            "M7 record does not reference the expected "
            "M6 source geometry schema."
        )

    if source_m6.get("status") != "valid":
        raise ValueError(
            "M7 record must reference a valid M6 source geometry."
        )

    if not isinstance(
        requested_void_geometry,
        dict,
    ):
        raise ValueError(
            "'requested_void_geometry' must be a dictionary."
        )

    if not isinstance(generated, dict):
        raise ValueError(
            "'generated_geometry' must be a dictionary."
        )

    if not isinstance(checks, dict):
        raise ValueError(
            "'checks' must be a dictionary."
        )

    if not checks:
        raise ValueError(
            "M7 geometry checks dictionary may not be empty."
        )

    width = float(
        data["rve"]["width"]
    )

    height = float(
        data["rve"]["height"]
    )

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
    voids = data["voids"]

    if not isinstance(particles, list):
        raise ValueError(
            "'particles' must be a list."
        )

    if not isinstance(voids, list):
        raise ValueError(
            "'voids' must be a list."
        )

    if len(particles) <= 0:
        raise ValueError(
            "At least one particle is required."
        )

    generated_particle_count = int(
        generated["particle_count"]
    )

    generated_void_count = int(
        generated["void_count"]
    )

    requested_void_count = int(
        requested_void_geometry[
            "void_count"
        ]
    )

    if len(particles) != generated_particle_count:
        raise ValueError(
            "Particle list length does not match "
            "generated particle count."
        )

    if len(voids) != generated_void_count:
        raise ValueError(
            "Void list length does not match "
            "generated void count."
        )

    if len(voids) != requested_void_count:
        raise ValueError(
            "Void list length does not match "
            "requested void count."
        )

    expected_particle_ids = list(
        range(
            1,
            len(particles) + 1,
        )
    )

    actual_particle_ids = [
        int(
            particle["particle_id"]
        )
        for particle in particles
    ]

    if actual_particle_ids != expected_particle_ids:
        raise ValueError(
            "Particle IDs must be consecutive and ordered "
            "from 1 through particle_count."
        )

    expected_void_ids = list(
        range(
            1,
            len(voids) + 1,
        )
    )

    actual_void_ids = [
        int(
            void["void_id"]
        )
        for void in voids
    ]

    if actual_void_ids != expected_void_ids:
        raise ValueError(
            "Void IDs must be consecutive and ordered "
            "from 1 through void_count."
        )

    def validate_circle(
        circle: dict,
        object_name: str,
        object_id: int,
    ) -> tuple[float, float, float]:

        center_x = float(
            circle["center_x"]
        )

        center_y = float(
            circle["center_y"]
        )

        radius = float(
            circle["radius"]
        )

        if (
            not np.isfinite(center_x)
            or not np.isfinite(center_y)
            or not np.isfinite(radius)
            or radius <= 0.0
        ):
            raise ValueError(
                f"Invalid numerical data for "
                f"{object_name} {object_id}."
            )

        if not (
            center_x - radius > 0.0
            and center_x + radius < width
            and center_y - radius > 0.0
            and center_y + radius < height
        ):
            raise ValueError(
                f"{object_name.capitalize()} "
                f"{object_id} does not lie "
                "strictly inside the RVE."
            )

        return (
            center_x,
            center_y,
            radius,
        )

    particle_circles = [
        validate_circle(
            particle,
            "particle",
            int(
                particle["particle_id"]
            ),
        )
        for particle in particles
    ]

    void_circles = [
        validate_circle(
            void,
            "void",
            int(
                void["void_id"]
            ),
        )
        for void in voids
    ]

    geometry_tolerance = 1.0e-12

    def circle_surface_gap(
        first: tuple[
            float,
            float,
            float,
        ],
        second: tuple[
            float,
            float,
            float,
        ],
    ) -> float:

        return (
            math.hypot(
                first[0] - second[0],
                first[1] - second[1],
            )
            - first[2]
            - second[2]
        )

    # Independently reject particle overlap or tangency.
    for i, first in enumerate(
        particle_circles[:-1]
    ):
        for j, second in enumerate(
            particle_circles[
                i + 1:
            ],
            start=i + 1,
        ):
            if (
                circle_surface_gap(
                    first,
                    second,
                )
                <= geometry_tolerance
            ):
                raise ValueError(
                    "Particles "
                    f"{i + 1} and {j + 1} "
                    "overlap or touch."
                )

    # Independently reject void-particle overlap or tangency.
    for void_index, void_circle in enumerate(
        void_circles,
        start=1,
    ):
        for particle_index, particle_circle in enumerate(
            particle_circles,
            start=1,
        ):
            if (
                circle_surface_gap(
                    void_circle,
                    particle_circle,
                )
                <= geometry_tolerance
            ):
                raise ValueError(
                    f"Void {void_index} and particle "
                    f"{particle_index} overlap or touch."
                )

    # Independently reject void-void overlap or tangency.
    for i, first in enumerate(
        void_circles[:-1]
    ):
        for j, second in enumerate(
            void_circles[
                i + 1:
            ],
            start=i + 1,
        ):
            if (
                circle_surface_gap(
                    first,
                    second,
                )
                <= geometry_tolerance
            ):
                raise ValueError(
                    f"Voids {i + 1} and {j + 1} "
                    "overlap or touch."
                )

    failed_checks = [
        str(name)
        for name, passed
        in checks.items()
        if passed is not True
    ]

    if failed_checks:
        raise ValueError(
            "M7 geometry record contains failed checks: "
            + ", ".join(
                failed_checks
            )
        )

    gross_area = (
        width * height
    )

    particle_area = sum(
        math.pi * radius**2
        for _, _, radius
        in particle_circles
    )

    void_area = sum(
        math.pi * radius**2
        for _, _, radius
        in void_circles
    )

    matrix_area = (
        gross_area
        - particle_area
        - void_area
    )

    solid_area = (
        gross_area
        - void_area
    )

    if matrix_area <= 0.0:
        raise ValueError(
            "Reconstructed matrix area must be positive."
        )

    area_fields = {
        "gross_rve_area": (
            gross_area
        ),
        "particle_area": (
            particle_area
        ),
        "void_area": (
            void_area
        ),
        "matrix_area": (
            matrix_area
        ),
        "solid_area": (
            solid_area
        ),
    }

    for name, reconstructed in area_fields.items():

        metadata_value = float(
            generated[name]
        )

        if not math.isclose(
            reconstructed,
            metadata_value,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise ValueError(
                f"Reconstructed {name} does not match "
                "generated_geometry metadata."
            )

    return data


def build_m7_cad_topology(
    geometry: dict,
) -> dict:
    """Build and verify M7 OCC entities in the current Gmsh model.

    Gmsh must already be initialized and a current model must exist.
    This function creates CAD entities and physical groups only.
    It intentionally does not generate the finite-element mesh.
    """

    width = float(
        geometry["rve"]["width"]
    )

    height = float(
        geometry["rve"]["height"]
    )

    particles = geometry["particles"]
    voids = geometry["voids"]

    generated = geometry[
        "generated_geometry"
    ]

    expected_gross_area = (
        width * height
    )

    expected_particle_area = sum(
        math.pi
        * float(particle["radius"]) ** 2
        for particle in particles
    )

    expected_void_area = sum(
        math.pi
        * float(void["radius"]) ** 2
        for void in voids
    )

    expected_matrix_area = (
        expected_gross_area
        - expected_particle_area
        - expected_void_area
    )

    expected_solid_area = (
        expected_gross_area
        - expected_void_area
    )

    reconstructed = {
        "gross_rve_area": (
            expected_gross_area
        ),
        "particle_area": (
            expected_particle_area
        ),
        "void_area": (
            expected_void_area
        ),
        "matrix_area": (
            expected_matrix_area
        ),
        "solid_area": (
            expected_solid_area
        ),
    }

    for name, expected in reconstructed.items():

        metadata_value = float(
            generated[name]
        )

        if not math.isclose(
            expected,
            metadata_value,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise RuntimeError(
                f"Geometry metadata mismatch for {name}."
            )

    if expected_matrix_area <= 0.0:
        raise RuntimeError(
            "Expected matrix area must be positive."
        )


    # ========================================================
    # 1. Gross RVE rectangle
    # ========================================================

    rectangle_tag = (
        gmsh.model.occ.addRectangle(
            0.0,
            0.0,
            0.0,
            width,
            height,
        )
    )


    # ========================================================
    # 2. True circular void disks
    # ========================================================

    void_disk_tags: list[int] = []

    for void in voids:

        tag = gmsh.model.occ.addDisk(
            float(void["center_x"]),
            float(void["center_y"]),
            0.0,
            float(void["radius"]),
            float(void["radius"]),
        )

        void_disk_tags.append(
            int(tag)
        )


    # ========================================================
    # 3. Subtract voids from material region
    # ========================================================

    if void_disk_tags:

        (
            cut_entities,
            _cut_map,
        ) = gmsh.model.occ.cut(
            [(2, rectangle_tag)],
            [
                (2, tag)
                for tag in void_disk_tags
            ],
            removeObject=True,
            removeTool=True,
        )

        cut_surfaces = [
            int(tag)
            for dim, tag in cut_entities
            if dim == 2
        ]

        if len(cut_surfaces) != 1:
            raise RuntimeError(
                "Void subtraction did not produce exactly "
                "one remaining material surface."
            )

        material_region_tag = (
            cut_surfaces[0]
        )

    else:

        material_region_tag = int(
            rectangle_tag
        )


    # ========================================================
    # 4. Particle disks
    # ========================================================

    particle_disk_tags: list[int] = []

    for particle in particles:

        disk_tag = gmsh.model.occ.addDisk(
            float(
                particle["center_x"]
            ),
            float(
                particle["center_y"]
            ),
            0.0,
            float(
                particle["radius"]
            ),
            float(
                particle["radius"]
            ),
        )

        particle_disk_tags.append(
            int(disk_tag)
        )


    # ========================================================
    # 5. Conformal matrix-particle fragmentation
    # ========================================================

    (
        _fragmented_entities,
        fragment_map,
    ) = gmsh.model.occ.fragment(
        [
            (
                2,
                material_region_tag,
            )
        ],
        [
            (
                2,
                tag,
            )
            for tag
            in particle_disk_tags
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


    # ========================================================
    # 6. Recover particle surfaces from fragment map
    # ========================================================

    particle_surface_tags: list[int] = []

    for particle_index, mapping in enumerate(
        fragment_map[1:],
        start=1,
    ):

        mapped_surfaces = [
            int(tag)
            for dim, tag in mapping
            if dim == 2
        ]

        if len(mapped_surfaces) != 1:
            raise RuntimeError(
                "Expected exactly one surface for "
                f"particle {particle_index}; got "
                f"{mapped_surfaces}."
            )

        particle_surface_tags.append(
            mapped_surfaces[0]
        )

    if (
        len(
            set(
                particle_surface_tags
            )
        )
        != len(particles)
    ):
        raise RuntimeError(
            "Particle surfaces are not unique."
        )


    # ========================================================
    # 7. Matrix surface is the only non-particle 2D surface
    # ========================================================

    all_surface_tags = sorted(
        int(tag)
        for dim, tag
        in gmsh.model.getEntities(2)
        if dim == 2
    )

    matrix_candidates = sorted(
        set(all_surface_tags)
        - set(
            particle_surface_tags
        )
    )

    if len(matrix_candidates) != 1:
        raise RuntimeError(
            "Exactly one matrix surface was expected."
        )

    matrix_surface_tag = int(
        matrix_candidates[0]
    )

    if len(all_surface_tags) != (
        len(particles) + 1
    ):
        raise RuntimeError(
            "A void must not create a 2D material surface. "
            "Expected one matrix surface plus one surface "
            "for every particle."
        )


    # ========================================================
    # 8. CAD material-area and particle-center checks
    # ========================================================

    particle_cad_checks = []

    calculated_cad_particle_area = 0.0

    for particle, surface_tag in zip(
        particles,
        particle_surface_tags,
    ):

        radius = float(
            particle["radius"]
        )

        expected_area = (
            math.pi * radius**2
        )

        actual_area = float(
            gmsh.model.occ.getMass(
                2,
                surface_tag,
            )
        )

        center = (
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
            float(center[0]),
            expected_x,
            rel_tol=0.0,
            abs_tol=CAD_ABS_TOL,
        )

        center_y_ok = math.isclose(
            float(center[1]),
            expected_y,
            rel_tol=0.0,
            abs_tol=CAD_ABS_TOL,
        )

        check = {
            "particle_id": int(
                particle[
                    "particle_id"
                ]
            ),
            "surface_tag": int(
                surface_tag
            ),
            "area_ok": bool(
                area_ok
            ),
            "center_x_ok": bool(
                center_x_ok
            ),
            "center_y_ok": bool(
                center_y_ok
            ),
            "cad_area": float(
                actual_area
            ),
        }

        particle_cad_checks.append(
            check
        )

        if not all(
            (
                area_ok,
                center_x_ok,
                center_y_ok,
            )
        ):
            raise RuntimeError(
                "CAD particle geometry check failed "
                f"for particle "
                f"{particle['particle_id']}."
            )

        calculated_cad_particle_area += (
            actual_area
        )

    actual_matrix_cad_area = float(
        gmsh.model.occ.getMass(
            2,
            matrix_surface_tag,
        )
    )

    actual_solid_cad_area = (
        actual_matrix_cad_area
        + calculated_cad_particle_area
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

    if not math.isclose(
        actual_solid_cad_area,
        expected_solid_area,
        rel_tol=0.0,
        abs_tol=CAD_ABS_TOL,
    ):
        raise RuntimeError(
            "CAD solid area mismatch."
        )


    # ========================================================
    # 9. Recover matrix-particle interface curves
    # ========================================================

    matrix_boundary_curves = {
        int(tag)
        for dim, tag
        in gmsh.model.getBoundary(
            [
                (
                    2,
                    matrix_surface_tag,
                )
            ],
            combined=False,
            oriented=False,
            recursive=False,
        )
        if dim == 1
    }

    particle_boundary_curves: set[int] = set()

    for surface_tag in particle_surface_tags:

        particle_boundary_curves.update(
            int(tag)
            for dim, tag
            in gmsh.model.getBoundary(
                [
                    (
                        2,
                        surface_tag,
                    )
                ],
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

    if (
        particle_boundary_curves
        != shared_interface_curves
    ):
        raise RuntimeError(
            "Particle boundaries are not fully shared "
            "with the matrix."
        )


    # ========================================================
    # 10. Separate circular void boundaries from outer RVE
    #
    # Candidate non-particle matrix boundaries consist only of:
    #   - four outer rectangle curves
    #   - one circular curve per Version-1 void
    #
    # Match each void independently by CAD curve length and COM.
    # ========================================================

    remaining_nonparticle_curves = (
        matrix_boundary_curves
        - particle_boundary_curves
    )

    unmatched_curves = set(
        remaining_nonparticle_curves
    )

    void_boundary_curves: set[int] = set()

    void_boundary_cad_checks = []

    for void in voids:

        void_id = int(
            void["void_id"]
        )

        expected_x = float(
            void["center_x"]
        )

        expected_y = float(
            void["center_y"]
        )

        radius = float(
            void["radius"]
        )

        expected_length = (
            2.0
            * math.pi
            * radius
        )

        matches = []

        for curve_tag in sorted(
            unmatched_curves
        ):

            actual_length = float(
                gmsh.model.occ.getMass(
                    1,
                    curve_tag,
                )
            )

            center = (
                gmsh.model.occ.getCenterOfMass(
                    1,
                    curve_tag,
                )
            )

            length_ok = math.isclose(
                actual_length,
                expected_length,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            center_x_ok = math.isclose(
                float(center[0]),
                expected_x,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            center_y_ok = math.isclose(
                float(center[1]),
                expected_y,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            )

            if (
                length_ok
                and center_x_ok
                and center_y_ok
            ):
                matches.append(
                    (
                        int(curve_tag),
                        actual_length,
                    )
                )

        if len(matches) != 1:
            raise RuntimeError(
                "Could not uniquely identify CAD "
                f"boundary for void {void_id}: "
                f"{matches}."
            )

        curve_tag, actual_length = (
            matches[0]
        )

        void_boundary_curves.add(
            curve_tag
        )

        unmatched_curves.remove(
            curve_tag
        )

        void_boundary_cad_checks.append(
            {
                "void_id": (
                    void_id
                ),
                "curve_tag": int(
                    curve_tag
                ),
                "expected_length": float(
                    expected_length
                ),
                "cad_length": float(
                    actual_length
                ),
                "center_x": float(
                    expected_x
                ),
                "center_y": float(
                    expected_y
                ),
                "radius": float(
                    radius
                ),
            }
        )


    # Everything still unmatched must be the four outer edges.
    outer_boundary_curves = set(
        unmatched_curves
    )

    if len(outer_boundary_curves) != 4:
        raise RuntimeError(
            "Expected exactly four external RVE "
            "boundary curves after removing void boundaries."
        )

    if len(void_boundary_curves) != len(voids):
        raise RuntimeError(
            "Void-boundary curve count does not match "
            "the geometry void count."
        )

    if (
        matrix_boundary_curves
        != (
            shared_interface_curves
            | outer_boundary_curves
            | void_boundary_curves
        )
    ):
        raise RuntimeError(
            "Matrix boundary partition is incomplete."
        )


    # ========================================================
    # 11. Physical groups
    # ========================================================

    gmsh.model.addPhysicalGroup(
        2,
        [
            matrix_surface_tag
        ],
        tag=MATRIX_PHYSICAL_TAG,
        name="matrix",
    )

    gmsh.model.addPhysicalGroup(
        2,
        particle_surface_tags,
        tag=PARTICLE_PHYSICAL_TAG,
        name="particle",
    )

    # For the zero-void regression limit there are no internal
    # hole facets, so no empty physical group is created.
    if void_boundary_curves:

        gmsh.model.addPhysicalGroup(
            1,
            sorted(
                void_boundary_curves
            ),
            tag=(
                VOID_BOUNDARY_PHYSICAL_TAG
            ),
            name="void_boundary",
        )


    # ========================================================
    # 12. Return CAD-only diagnostics
    # ========================================================

    return {
        "matrix_surface_tag": int(
            matrix_surface_tag
        ),
        "particle_surface_tags": [
            int(tag)
            for tag
            in particle_surface_tags
        ],
        "void_boundary_curve_tags": sorted(
            int(tag)
            for tag
            in void_boundary_curves
        ),
        "outer_boundary_curve_tags": sorted(
            int(tag)
            for tag
            in outer_boundary_curves
        ),
        "shared_interface_curve_tags": sorted(
            int(tag)
            for tag
            in shared_interface_curves
        ),
        "particle_cad_checks": (
            particle_cad_checks
        ),
        "void_boundary_cad_checks": (
            void_boundary_cad_checks
        ),
        "surface_count": int(
            len(
                all_surface_tags
            )
        ),
        "outer_boundary_curve_count": int(
            len(
                outer_boundary_curves
            )
        ),
        "shared_interface_curve_count": int(
            len(
                shared_interface_curves
            )
        ),
        "void_boundary_curve_count": int(
            len(
                void_boundary_curves
            )
        ),
        "expected_gross_rve_area": float(
            expected_gross_area
        ),
        "expected_particle_area": float(
            expected_particle_area
        ),
        "expected_void_area": float(
            expected_void_area
        ),
        "expected_matrix_area": float(
            expected_matrix_area
        ),
        "expected_solid_area": float(
            expected_solid_area
        ),
        "cad_particle_area": float(
            calculated_cad_particle_area
        ),
        "cad_matrix_area": float(
            actual_matrix_cad_area
        ),
        "cad_solid_area": float(
            actual_solid_cad_area
        ),
    }


def build_m7_mesh_data(
    geometry: dict,
    mesh_size: float,
):
    """Generate the M7 mesh and transfer physical tags to DOLFINx."""

    if (
        not np.isfinite(mesh_size)
        or mesh_size <= 0.0
    ):
        raise ValueError(
            "mesh-size must be finite and positive."
        )

    gmsh.initialize()

    try:

        gmsh.option.setNumber(
            "General.Terminal",
            0,
        )

        gmsh.model.add(
            "m7_void_mesh"
        )

        topology_diagnostics = (
            build_m7_cad_topology(
                geometry
            )
        )

        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMin",
            mesh_size,
        )

        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMax",
            mesh_size,
        )

        gmsh.model.mesh.generate(
            2
        )

        mesh_data = (
            gmshio.model_to_mesh(
                gmsh.model,
                MPI.COMM_WORLD,
                rank=0,
                gdim=2,
            )
        )

    finally:

        gmsh.finalize()

    return (
        mesh_data,
        topology_diagnostics,
    )


def verify_m7_dolfinx_mesh(
    mesh_data,
    topology_diagnostics: dict,
    geometry: dict,
    mesh_size: float,
) -> dict:
    """Verify M7 material cells, hole facets and mesh geometry."""

    domain = mesh_data.mesh
    cell_tags = mesh_data.cell_tags
    facet_tags = mesh_data.facet_tags
    physical_groups = mesh_data.physical_groups

    if cell_tags is None:
        raise RuntimeError(
            "DOLFINx did not receive M7 material cell tags."
        )

    if "matrix" not in physical_groups:
        raise RuntimeError(
            "Matrix physical group was not transferred."
        )

    if "particle" not in physical_groups:
        raise RuntimeError(
            "Particle physical group was not transferred."
        )

    matrix_group = physical_groups[
        "matrix"
    ]

    particle_group = physical_groups[
        "particle"
    ]

    matrix_tag = int(
        matrix_group.tag
    )

    particle_tag = int(
        particle_group.tag
    )

    if (
        int(matrix_group.dim) != 2
        or matrix_tag
        != MATRIX_PHYSICAL_TAG
    ):
        raise RuntimeError(
            "Unexpected matrix physical group."
        )

    if (
        int(particle_group.dim) != 2
        or particle_tag
        != PARTICLE_PHYSICAL_TAG
    ):
        raise RuntimeError(
            "Unexpected particle physical group."
        )

    void_count = int(
        geometry[
            "generated_geometry"
        ]["void_count"]
    )

    void_group = physical_groups.get(
        "void_boundary"
    )

    if void_count > 0:

        if void_group is None:
            raise RuntimeError(
                "void_boundary physical group "
                "was not transferred."
            )

        if (
            int(void_group.dim) != 1
            or int(void_group.tag)
            != VOID_BOUNDARY_PHYSICAL_TAG
        ):
            raise RuntimeError(
                "Unexpected void_boundary physical group."
            )

        if facet_tags is None:
            raise RuntimeError(
                "Void geometry did not transfer facet tags."
            )

        void_tag = int(
            void_group.tag
        )

    else:

        if void_group is not None:
            raise RuntimeError(
                "Zero-void geometry unexpectedly contains "
                "a void_boundary physical group."
            )

        void_tag = (
            VOID_BOUNDARY_PHYSICAL_TAG
        )


    # ========================================================
    # Cell counts
    # ========================================================

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

    matrix_cells = cell_tags.find(
        matrix_tag
    )

    particle_cells = cell_tags.find(
        particle_tag
    )

    matrix_owned_cells = (
        matrix_cells[
            matrix_cells
            < owned_cell_count
        ]
    )

    particle_owned_cells = (
        particle_cells[
            particle_cells
            < owned_cell_count
        ]
    )

    matrix_cell_count = (
        domain.comm.allreduce(
            len(
                matrix_owned_cells
            ),
            op=MPI.SUM,
        )
    )

    particle_cell_count = (
        domain.comm.allreduce(
            len(
                particle_owned_cells
            ),
            op=MPI.SUM,
        )
    )

    tagged_cell_count = (
        matrix_cell_count
        + particle_cell_count
    )


    # ========================================================
    # Material area integration
    # ========================================================

    dx = ufl.Measure(
        "dx",
        domain=domain,
        subdomain_data=cell_tags,
    )

    matrix_area_local = (
        fem.assemble_scalar(
            fem.form(
                1.0
                * dx(
                    matrix_tag
                )
            )
        )
    )

    particle_area_local = (
        fem.assemble_scalar(
            fem.form(
                1.0
                * dx(
                    particle_tag
                )
            )
        )
    )

    meshed_matrix_area = float(
        domain.comm.allreduce(
            matrix_area_local,
            op=MPI.SUM,
        )
    )

    meshed_particle_area = float(
        domain.comm.allreduce(
            particle_area_local,
            op=MPI.SUM,
        )
    )

    meshed_solid_area = (
        meshed_matrix_area
        + meshed_particle_area
    )


    # ========================================================
    # Analytical reference quantities
    # ========================================================

    generated = geometry[
        "generated_geometry"
    ]

    expected_gross_area = float(
        generated[
            "gross_rve_area"
        ]
    )

    expected_matrix_area = float(
        generated[
            "matrix_area"
        ]
    )

    expected_particle_area = float(
        generated[
            "particle_area"
        ]
    )

    expected_void_area = float(
        generated[
            "void_area"
        ]
    )

    expected_solid_area = float(
        generated[
            "solid_area"
        ]
    )

    if expected_gross_area <= 0.0:
        raise RuntimeError(
            "Expected gross RVE area must be positive."
        )

    meshed_void_area = (
        expected_gross_area
        - meshed_solid_area
    )


    # Gross-RVE-normalized 2D fraction errors.
    particle_fraction_error = abs(
        meshed_particle_area
        - expected_particle_area
    ) / expected_gross_area

    matrix_fraction_error = abs(
        meshed_matrix_area
        - expected_matrix_area
    ) / expected_gross_area

    void_fraction_error = abs(
        meshed_void_area
        - expected_void_area
    ) / expected_gross_area

    solid_fraction_error = abs(
        meshed_solid_area
        - expected_solid_area
    ) / expected_gross_area


    # ========================================================
    # Void-boundary facet transfer and length
    # ========================================================

    void_facet_count = 0

    expected_void_boundary_length = sum(
        2.0
        * math.pi
        * float(
            void[
                "radius"
            ]
        )
        for void
        in geometry["voids"]
    )

    meshed_void_boundary_length = 0.0
    boundary_length_relative_error = 0.0

    if void_count > 0:

        void_facets = facet_tags.find(
            void_tag
        )

        fdim = (
            domain.topology.dim
            - 1
        )

        owned_facet_count = (
            domain.topology.index_map(
                fdim
            ).size_local
        )

        owned_void_facets = (
            void_facets[
                void_facets
                < owned_facet_count
            ]
        )

        void_facet_count = int(
            domain.comm.allreduce(
                len(
                    owned_void_facets
                ),
                op=MPI.SUM,
            )
        )

        ds = ufl.Measure(
            "ds",
            domain=domain,
            subdomain_data=facet_tags,
        )

        boundary_length_local = (
            fem.assemble_scalar(
                fem.form(
                    1.0
                    * ds(
                        void_tag
                    )
                )
            )
        )

        meshed_void_boundary_length = float(
            domain.comm.allreduce(
                boundary_length_local,
                op=MPI.SUM,
            )
        )

        if expected_void_boundary_length <= 0.0:
            raise RuntimeError(
                "Positive void count requires positive "
                "analytical void-boundary length."
            )

        boundary_length_relative_error = (
            abs(
                meshed_void_boundary_length
                - expected_void_boundary_length
            )
            / expected_void_boundary_length
        )

    else:

        if facet_tags is not None:

            zero_void_facets = (
                facet_tags.find(
                    void_tag
                )
            )

            void_facet_count = int(
                len(
                    zero_void_facets
                )
            )


    # ========================================================
    # Permanent M7 mesh checks
    # ========================================================

    checks = {
        "all_cells_tagged": (
            tagged_cell_count
            == total_cell_count
        ),

        "positive_matrix_cell_count": (
            matrix_cell_count > 0
        ),

        "positive_particle_cell_count": (
            particle_cell_count > 0
        ),

        "positive_matrix_area": (
            meshed_matrix_area > 0.0
        ),

        "positive_particle_area": (
            meshed_particle_area > 0.0
        ),

        "positive_solid_area": (
            meshed_solid_area > 0.0
        ),

        "matrix_physical_tag": (
            matrix_tag
            == MATRIX_PHYSICAL_TAG
        ),

        "particle_physical_tag": (
            particle_tag
            == PARTICLE_PHYSICAL_TAG
        ),

        "particle_fraction": (
            particle_fraction_error
            <= PARTICLE_FRACTION_TOL
        ),

        "matrix_fraction": (
            matrix_fraction_error
            <= MATRIX_FRACTION_TOL
        ),

        "void_fraction": (
            void_fraction_error
            <= VOID_FRACTION_TOL
        ),

        "solid_fraction": (
            solid_fraction_error
            <= SOLID_FRACTION_TOL
        ),

        "cad_surface_count": (
            int(
                topology_diagnostics[
                    "surface_count"
                ]
            )
            == (
                len(
                    geometry["particles"]
                )
                + 1
            )
        ),

        "outer_boundary_curve_count": (
            int(
                topology_diagnostics[
                    "outer_boundary_curve_count"
                ]
            )
            == 4
        ),

        "void_boundary_curve_count": (
            int(
                topology_diagnostics[
                    "void_boundary_curve_count"
                ]
            )
            == void_count
        ),
    }

    if void_count > 0:

        checks.update(
            {
                "void_boundary_physical_tag": (
                    int(
                        void_group.tag
                    )
                    == (
                        VOID_BOUNDARY_PHYSICAL_TAG
                    )
                ),

                "positive_void_facet_count": (
                    void_facet_count > 0
                ),

                "void_boundary_length": (
                    boundary_length_relative_error
                    <= (
                        VOID_BOUNDARY_LENGTH_REL_TOL
                    )
                ),
            }
        )

    else:

        checks.update(
            {
                "no_void_physical_group": (
                    void_group is None
                ),

                "zero_void_facet_count": (
                    void_facet_count == 0
                ),

                "zero_void_area": (
                    abs(
                        meshed_void_area
                    )
                    <= TOTAL_AREA_ABS_TOL
                ),
            }
        )

    failed_checks = [
        name
        for name, passed
        in checks.items()
        if not passed
    ]

    if failed_checks:

        raise RuntimeError(
            "M7 DOLFINx mesh verification failed: "
            + ", ".join(
                failed_checks
            )
        )


    # ========================================================
    # Machine-readable diagnostics
    # ========================================================

    source_m6 = geometry[
        "source_m6_geometry"
    ]

    return {
        "schema": (
            MESH_DIAGNOSTICS_SCHEMA
        ),

        "geometry_schema": (
            geometry["schema"]
        ),

        "source_m6_geometry_schema": (
            source_m6[
                "schema"
            ]
        ),

        "source_m6_geometry_sha256": (
            source_m6[
                "sha256"
            ]
        ),

        "particle_seed": int(
            source_m6[
                "particle_seed"
            ]
        ),

        "void_seed": int(
            geometry[
                "rng"
            ][
                "void_seed"
            ]
        ),

        "particle_count": int(
            len(
                geometry["particles"]
            )
        ),

        "void_count": int(
            len(
                geometry["voids"]
            )
        ),

        "mesh_size": float(
            mesh_size
        ),

        "physical_tags": {
            "matrix": int(
                matrix_tag
            ),

            "particle": int(
                particle_tag
            ),

            "void_boundary": (
                int(
                    VOID_BOUNDARY_PHYSICAL_TAG
                )
                if void_count > 0
                else None
            ),
        },

        "topology": (
            topology_diagnostics
        ),

        "mesh": {
            "cell_count": int(
                total_cell_count
            ),

            "tagged_cell_count": int(
                tagged_cell_count
            ),

            "matrix_cell_count": int(
                matrix_cell_count
            ),

            "particle_cell_count": int(
                particle_cell_count
            ),

            "void_boundary_facet_count": int(
                void_facet_count
            ),
        },

        "area": {
            "expected_gross_rve_area": float(
                expected_gross_area
            ),

            "expected_matrix_area": float(
                expected_matrix_area
            ),

            "meshed_matrix_area": float(
                meshed_matrix_area
            ),

            "expected_particle_area": float(
                expected_particle_area
            ),

            "meshed_particle_area": float(
                meshed_particle_area
            ),

            "expected_void_area": float(
                expected_void_area
            ),

            "meshed_void_area": float(
                meshed_void_area
            ),

            "expected_solid_area": float(
                expected_solid_area
            ),

            "meshed_solid_area": float(
                meshed_solid_area
            ),

            "analytical_particle_area_fraction": float(
                expected_particle_area
                / expected_gross_area
            ),

            "meshed_particle_area_fraction": float(
                meshed_particle_area
                / expected_gross_area
            ),

            "analytical_void_area_fraction": float(
                expected_void_area
                / expected_gross_area
            ),

            "meshed_void_area_fraction": float(
                meshed_void_area
                / expected_gross_area
            ),

            "particle_area_fraction_error": float(
                particle_fraction_error
            ),

            "matrix_area_fraction_error": float(
                matrix_fraction_error
            ),

            "void_area_fraction_error": float(
                void_fraction_error
            ),

            "solid_area_fraction_error": float(
                solid_fraction_error
            ),
        },

        "void_boundary": {
            "expected_length": float(
                expected_void_boundary_length
            ),

            "meshed_length": float(
                meshed_void_boundary_length
            ),

            "relative_error": float(
                boundary_length_relative_error
            ),
        },

        "checks": {
            name: bool(
                passed
            )
            for name, passed
            in checks.items()
        },

        "status": "valid",
    }


def main() -> int:
    """Build, verify and report one M7 circular-void mesh."""

    args = parse_args()

    geometry = load_geometry(
        args.geometry_json
    )

    (
        mesh_data,
        topology_diagnostics,
    ) = build_m7_mesh_data(
        geometry=geometry,
        mesh_size=float(
            args.mesh_size
        ),
    )

    diagnostics = verify_m7_dolfinx_mesh(
        mesh_data=mesh_data,
        topology_diagnostics=(
            topology_diagnostics
        ),
        geometry=geometry,
        mesh_size=float(
            args.mesh_size
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
