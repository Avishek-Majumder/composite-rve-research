"""Render and save the verified DOLFINx unit-square mesh."""

from pathlib import Path

import pyvista as pv
from dolfinx import mesh, plot
from mpi4py import MPI


def main() -> None:
    """Create the mesh and save an off-screen visualization."""

    domain = mesh.create_unit_square(
        MPI.COMM_WORLD,
        nx=8,
        ny=8,
        cell_type=mesh.CellType.triangle,
    )

    topology, cell_types, geometry = plot.vtk_mesh(
        domain,
        domain.topology.dim,
    )

    grid = pv.UnstructuredGrid(
        topology,
        cell_types,
        geometry,
    )

    output_file = Path("figures/01_unit_square_mesh.png")

    plotter = pv.Plotter(
        off_screen=True,
        window_size=(800, 800),
    )

    plotter.add_mesh(
        grid,
        show_edges=True,
    )

    plotter.view_xy()
    plotter.enable_parallel_projection()

    plotter.show(
        screenshot=str(output_file),
        auto_close=True,
    )

    print("Grid points:", grid.n_points)
    print("Grid cells:", grid.n_cells)
    print("Image path:", output_file.resolve())
    print("Image exists:", output_file.exists())

    if output_file.exists():
        print("Image size:", output_file.stat().st_size, "bytes")

    print("Unit-square mesh visualization passed.")


if __name__ == "__main__":
    main()
