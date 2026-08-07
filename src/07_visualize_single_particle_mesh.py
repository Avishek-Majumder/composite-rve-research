"""Visualize matrix and particle material tags in the DOLFINx mesh."""

from pathlib import Path
import math

import gmsh
import numpy as np
import pyvista as pv
import yaml

from dolfinx import plot
from dolfinx.io import gmsh as gmshio
from mpi4py import MPI


def main() -> None:
    """Generate and visualize the tagged single-particle mesh."""

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

    gmsh.initialize()

    try:
        gmsh.option.setNumber("General.Terminal", 0)

        gmsh.model.add("single_particle_visualization")

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

        gmsh.model.addPhysicalGroup(
            2,
            [matrix_tag],
            tag=1,
            name="matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            [particle_tag],
            tag=2,
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

    domain = mesh_data.mesh
    cell_tags = mesh_data.cell_tags

    if cell_tags is None:
        raise RuntimeError("Material cell tags are missing.")

    topology, cell_types, geometry = plot.vtk_mesh(
        domain,
        domain.topology.dim,
    )

    grid = pv.UnstructuredGrid(
        topology,
        cell_types,
        geometry,
    )

    material_ids = np.zeros(
        grid.n_cells,
        dtype=np.int32,
    )

    material_ids[cell_tags.indices] = cell_tags.values

    grid.cell_data["Material ID"] = material_ids

    unique_material_ids = np.unique(material_ids)

    output_file = Path(
        "figures/02_single_particle_material_tags.png"
    )

    plotter = pv.Plotter(
        off_screen=True,
        window_size=(900, 900),
    )

    plotter.add_mesh(
        grid,
        scalars="Material ID",
        categories=True,
        show_edges=True,
        line_width=0.5,
        scalar_bar_args={
            "title": "Material ID",
        },
    )

    plotter.view_xy()
    plotter.enable_parallel_projection()

    plotter.show(
        screenshot=str(output_file),
        auto_close=True,
    )

    print("Grid points:", grid.n_points)
    print("Grid cells:", grid.n_cells)
    print(
        "Material IDs present:",
        unique_material_ids.tolist(),
    )
    print("Matrix material ID: 1")
    print("Particle material ID: 2")
    print("Image path:", output_file.resolve())
    print("Image exists:", output_file.exists())

    if output_file.exists():
        print(
            "Image size:",
            output_file.stat().st_size,
            "bytes",
        )

    print("Tagged material visualization generated.")


if __name__ == "__main__":
    main()
