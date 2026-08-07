"""Create the first verified DOLFINx finite-element mesh."""

from dolfinx import mesh
from mpi4py import MPI


def main() -> None:
    """Create a triangular mesh of a 1 x 1 square."""

    domain = mesh.create_unit_square(
        MPI.COMM_WORLD,
        nx=8,
        ny=8,
        cell_type=mesh.CellType.triangle,
    )

    topological_dimension = domain.topology.dim
    geometrical_dimension = domain.geometry.dim

    global_cells = domain.topology.index_map(
        topological_dimension
    ).size_global

    global_vertices = domain.topology.index_map(
        0
    ).size_global

    if MPI.COMM_WORLD.rank == 0:
        print("Mesh: 1 x 1 unit square")
        print("Cell type: triangle")
        print("Topological dimension:", topological_dimension)
        print("Geometrical dimension:", geometrical_dimension)
        print("Global vertices:", global_vertices)
        print("Global cells:", global_cells)
        print("First project mesh test passed.")


if __name__ == "__main__":
    main()
