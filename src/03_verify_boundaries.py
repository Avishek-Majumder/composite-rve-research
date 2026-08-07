"""Verify boundary locations for the homogeneous tension benchmark."""

import numpy as np
from dolfinx import fem, mesh
from mpi4py import MPI


def main() -> None:
    width = 1.0

    domain = mesh.create_unit_square(
        MPI.COMM_WORLD,
        nx=8,
        ny=8,
        cell_type=mesh.CellType.triangle,
    )

    gdim = domain.geometry.dim

    # Vector displacement field: [u_x, u_y]
    V = fem.functionspace(
        domain,
        ("Lagrange", 1, (gdim,)),
    )

    fdim = domain.topology.dim - 1

    left_facets = mesh.locate_entities_boundary(
        domain,
        fdim,
        lambda x: np.isclose(x[0], 0.0),
    )

    right_facets = mesh.locate_entities_boundary(
        domain,
        fdim,
        lambda x: np.isclose(x[0], width),
    )

    left_x_dofs = fem.locate_dofs_topological(
        V.sub(0),
        fdim,
        left_facets,
    )

    right_x_dofs = fem.locate_dofs_topological(
        V.sub(0),
        fdim,
        right_facets,
    )

    V_y, _ = V.sub(1).collapse()

    bottom_left_y_dofs = fem.locate_dofs_geometrical(
        (V.sub(1), V_y),
        lambda x: (
            np.isclose(x[0], 0.0)
            & np.isclose(x[1], 0.0)
        ),
    )

    if MPI.COMM_WORLD.rank == 0:
        print("Left boundary facets:", len(left_facets))
        print("Right boundary facets:", len(right_facets))
        print("Left ux DOFs:", len(left_x_dofs))
        print("Right ux DOFs:", len(right_x_dofs))
        print(
            "Bottom-left uy DOFs:",
            len(bottom_left_y_dofs[0]),
        )

        print("Expected left facets: 8")
        print("Expected right facets: 8")
        print("Expected left ux DOFs: 9")
        print("Expected right ux DOFs: 9")
        print("Expected bottom-left uy DOFs: 1")

        print("Boundary-location verification completed.")


if __name__ == "__main__":
    main()
