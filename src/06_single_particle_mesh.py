"""Generate and verify the matrix + particle finite-element mesh."""

from pathlib import Path
import math

import gmsh
import numpy as np
import ufl
import yaml
from dolfinx import fem
from dolfinx.io import gmsh as gmshio
from mpi4py import MPI


def main() -> None:
    """Generate the first tagged two-material DOLFINx mesh."""

    config_path = Path("configs/02_single_particle.yaml")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    width = float(config["geometry"]["width"])
    height = float(config["geometry"]["height"])

    cx = float(config["particle"]["center_x"])
    cy = float(config["particle"]["center_y"])
    radius = float(config["particle"]["radius"])

    mesh_size = float(config["mesh"]["global_size"])

    expected_particle_area = math.pi * radius**2
    expected_total_area = width * height

    matrix_physical_tag = 1
    particle_physical_tag = 2

    gmsh.initialize()

    try:
        gmsh.option.setNumber("General.Terminal", 0)

        gmsh.model.add("single_particle_composite_mesh")

        # --------------------------------------------------------------
        # 1. Build CAD geometry
        # --------------------------------------------------------------
        rectangle = gmsh.model.occ.addRectangle(
            0.0,
            0.0,
            0.0,
            width,
            height,
        )

        disk = gmsh.model.occ.addDisk(
            cx,
            cy,
            0.0,
            radius,
            radius,
        )

        gmsh.model.occ.fragment(
            [(2, rectangle)],
            [(2, disk)],
            removeObject=True,
            removeTool=True,
        )

        gmsh.model.occ.synchronize()

        # --------------------------------------------------------------
        # 2. Identify matrix and particle surfaces
        # --------------------------------------------------------------
        surfaces = gmsh.model.getEntities(dim=2)

        surface_areas = {
            tag: gmsh.model.occ.getMass(2, tag)
            for _, tag in surfaces
        }

        particle_tag = min(
            surface_areas,
            key=lambda tag: abs(
                surface_areas[tag]
                - expected_particle_area
            ),
        )

        matrix_tag = next(
            tag
            for tag in surface_areas
            if tag != particle_tag
        )

        # --------------------------------------------------------------
        # 3. Physical material groups
        # --------------------------------------------------------------
        gmsh.model.addPhysicalGroup(
            2,
            [matrix_tag],
            tag=matrix_physical_tag,
            name="matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            [particle_tag],
            tag=particle_physical_tag,
            name="particle",
        )

        # --------------------------------------------------------------
        # 4. Mesh-size control
        # --------------------------------------------------------------
        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMin",
            mesh_size,
        )

        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMax",
            mesh_size,
        )

        # First-order triangular mesh
        gmsh.model.mesh.generate(2)

        # --------------------------------------------------------------
        # 5. Transfer Gmsh model into DOLFINx
        # --------------------------------------------------------------
        mesh_data = gmshio.model_to_mesh(
            gmsh.model,
            MPI.COMM_WORLD,
            rank=0,
            gdim=2,
        )

    finally:
        gmsh.finalize()

    domain = mesh_data.mesh
    cell_tags = mesh_data.cell_tags

    if cell_tags is None:
        raise RuntimeError(
            "DOLFINx did not receive material cell tags."
        )

    # --------------------------------------------------------------
    # 6. Verify physical-group names and tags
    # --------------------------------------------------------------
    physical_groups = mesh_data.physical_groups

    if "matrix" not in physical_groups:
        raise RuntimeError(
            "Matrix physical group was not transferred."
        )

    if "particle" not in physical_groups:
        raise RuntimeError(
            "Particle physical group was not transferred."
        )

    matrix_tag_from_name = physical_groups["matrix"].tag
    particle_tag_from_name = physical_groups["particle"].tag

    # --------------------------------------------------------------
    # 7. Count cells belonging to each material
    # --------------------------------------------------------------
    matrix_cells_local = cell_tags.find(
        matrix_tag_from_name
    )

    particle_cells_local = cell_tags.find(
        particle_tag_from_name
    )

    matrix_cell_count = domain.comm.allreduce(
        len(matrix_cells_local),
        op=MPI.SUM,
    )

    particle_cell_count = domain.comm.allreduce(
        len(particle_cells_local),
        op=MPI.SUM,
    )

    total_cells = domain.comm.allreduce(
        domain.topology.index_map(
            domain.topology.dim
        ).size_local,
        op=MPI.SUM,
    )

    # --------------------------------------------------------------
    # 8. Numerically integrate areas from tagged DOLFINx cells
    # --------------------------------------------------------------
    dx = ufl.Measure(
        "dx",
        domain=domain,
        subdomain_data=cell_tags,
    )

    matrix_area_local = fem.assemble_scalar(
        fem.form(1.0 * dx(matrix_tag_from_name))
    )

    particle_area_local = fem.assemble_scalar(
        fem.form(1.0 * dx(particle_tag_from_name))
    )

    matrix_area = domain.comm.allreduce(
        matrix_area_local,
        op=MPI.SUM,
    )

    particle_area = domain.comm.allreduce(
        particle_area_local,
        op=MPI.SUM,
    )

    total_area = matrix_area + particle_area

    numerical_particle_fraction = (
        particle_area / total_area
    )

    analytical_particle_fraction = (
        expected_particle_area / expected_total_area
    )

    # First-order triangles approximate the circular boundary
    # with straight edges, so the particle area will not be
    # mathematically exact at this mesh resolution.
    fraction_error = abs(
        numerical_particle_fraction
        - analytical_particle_fraction
    )

    # --------------------------------------------------------------
    # 9. Validation
    # --------------------------------------------------------------
    if matrix_cell_count <= 0:
        raise RuntimeError(
            "No matrix cells were found."
        )

    if particle_cell_count <= 0:
        raise RuntimeError(
            "No particle cells were found."
        )

    if matrix_cell_count + particle_cell_count != total_cells:
        raise RuntimeError(
            "Not all cells received a material tag."
        )

    if not math.isclose(
        total_area,
        expected_total_area,
        abs_tol=1.0e-10,
        rel_tol=0.0,
    ):
        raise RuntimeError(
            "Total meshed area does not equal the RVE area."
        )

    # Loose verification only at this initial mesh resolution.
    if fraction_error > 0.005:
        raise RuntimeError(
            "Particle fraction error is unexpectedly large."
        )

    if domain.comm.rank == 0:
        print("DOLFINx mesh dimension:", domain.topology.dim)
        print("DOLFINx geometry dimension:", domain.geometry.dim)
        print()

        print(
            "Matrix physical tag:",
            matrix_tag_from_name,
        )

        print(
            "Particle physical tag:",
            particle_tag_from_name,
        )

        print()

        print("Total cells:", total_cells)
        print("Matrix cells:", matrix_cell_count)
        print("Particle cells:", particle_cell_count)
        print()

        print("Meshed matrix area:", matrix_area)
        print("Meshed particle area:", particle_area)
        print("Total meshed area:", total_area)
        print()

        print(
            "Analytical particle fraction:",
            analytical_particle_fraction,
        )

        print(
            "Meshed particle fraction:",
            numerical_particle_fraction,
        )

        print(
            "Absolute particle-fraction error:",
            fraction_error,
        )

        print()
        print(
            "Two-material Gmsh-to-DOLFINx mesh validation passed."
        )


if __name__ == "__main__":
    main()
