"""Solve the first homogeneous 2D plane-stress elasticity benchmark."""

from pathlib import Path

import numpy as np
import ufl
import yaml
from dolfinx import fem, mesh
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc


def main() -> None:
    """Solve homogeneous uniaxial tension using linear elasticity."""

    # ------------------------------------------------------------------
    # 1. Load configuration
    # ------------------------------------------------------------------
    config_path = Path("configs/01_homogeneous_elasticity.yaml")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    width = float(config["geometry"]["width"])
    height = float(config["geometry"]["height"])

    E = float(config["material"]["youngs_modulus"])
    nu = float(config["material"]["poissons_ratio"])

    prescribed_ux = float(
        config["loading"]["prescribed_x_displacement"]
    )

    nx = int(config["mesh"]["nx"])
    ny = int(config["mesh"]["ny"])

    # ------------------------------------------------------------------
    # 2. Create rectangular triangular mesh
    # ------------------------------------------------------------------
    domain = mesh.create_rectangle(
        MPI.COMM_WORLD,
        [
            np.array([0.0, 0.0]),
            np.array([width, height]),
        ],
        [nx, ny],
        cell_type=mesh.CellType.triangle,
    )

    gdim = domain.geometry.dim
    tdim = domain.topology.dim
    fdim = tdim - 1

    # ------------------------------------------------------------------
    # 3. Vector displacement function space [ux, uy]
    # ------------------------------------------------------------------
    V = fem.functionspace(
        domain,
        ("Lagrange", 1, (gdim,)),
    )

    # ------------------------------------------------------------------
    # 4. Plane-stress elastic constants
    # ------------------------------------------------------------------
    mu = E / (2.0 * (1.0 + nu))

    lambda_3d = (
        E * nu
        / ((1.0 + nu) * (1.0 - 2.0 * nu))
    )

    lambda_ps = (
        2.0 * mu * lambda_3d
        / (lambda_3d + 2.0 * mu)
    )

    def epsilon(displacement):
        """Small-strain tensor."""
        return ufl.sym(ufl.grad(displacement))

    def sigma(displacement):
        """2D isotropic plane-stress tensor."""
        strain = epsilon(displacement)

        return (
            2.0 * mu * strain
            + lambda_ps
            * ufl.tr(strain)
            * ufl.Identity(gdim)
        )

    # ------------------------------------------------------------------
    # 5. Trial and test functions
    # ------------------------------------------------------------------
    u = ufl.TrialFunction(V)
    v = ufl.TestFunction(V)

    # Internal virtual work
    a = ufl.inner(
        sigma(u),
        epsilon(v),
    ) * ufl.dx

    # No body force
    # Use a DOLFINx Constant so the zero vector is tied to this mesh domain.
    zero_force = fem.Constant(
        domain,
        np.zeros(gdim, dtype=PETSc.ScalarType),
    )

    L = ufl.inner(
        zero_force,
        v,
    ) * ufl.dx

    # ------------------------------------------------------------------
    # 6. Locate boundaries
    # ------------------------------------------------------------------
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

    # Bottom-left vertex removes rigid vertical translation
    bottom_left_vertices = mesh.locate_entities_boundary(
        domain,
        0,
        lambda x: (
            np.isclose(x[0], 0.0)
            & np.isclose(x[1], 0.0)
        ),
    )

    bottom_left_y_dofs = fem.locate_dofs_topological(
        V.sub(1),
        0,
        bottom_left_vertices,
    )

    # ------------------------------------------------------------------
    # 7. Dirichlet boundary conditions
    # ------------------------------------------------------------------
    bc_left = fem.dirichletbc(
        PETSc.ScalarType(0.0),
        left_x_dofs,
        V.sub(0),
    )

    bc_right = fem.dirichletbc(
        PETSc.ScalarType(prescribed_ux),
        right_x_dofs,
        V.sub(0),
    )

    bc_bottom_left = fem.dirichletbc(
        PETSc.ScalarType(0.0),
        bottom_left_y_dofs,
        V.sub(1),
    )

    boundary_conditions = [
        bc_left,
        bc_right,
        bc_bottom_left,
    ]

    # ------------------------------------------------------------------
    # 8. Solve the linear FEM system
    # ------------------------------------------------------------------
    problem = LinearProblem(
        a,
        L,
        bcs=boundary_conditions,
        petsc_options_prefix="homogeneous_elasticity_",
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "ksp_error_if_not_converged": True,
        },
    )

    uh = problem.solve()
    uh.x.scatter_forward()

    # ------------------------------------------------------------------
    # 9. Extract displacement-component ranges
    # ------------------------------------------------------------------
    _, ux_to_parent = V.sub(0).collapse()
    _, uy_to_parent = V.sub(1).collapse()

    local_ux = uh.x.array[ux_to_parent]
    local_uy = uh.x.array[uy_to_parent]

    ux_min = domain.comm.allreduce(
        np.min(local_ux),
        op=MPI.MIN,
    )

    ux_max = domain.comm.allreduce(
        np.max(local_ux),
        op=MPI.MAX,
    )

    uy_min = domain.comm.allreduce(
        np.min(local_uy),
        op=MPI.MIN,
    )

    uy_max = domain.comm.allreduce(
        np.max(local_uy),
        op=MPI.MAX,
    )

    solver_reason = problem.solver.getConvergedReason()

    # ------------------------------------------------------------------
    # 10. Domain-averaged strain and stress verification
    # ------------------------------------------------------------------
    dx = ufl.Measure("dx", domain=domain)

    solved_strain = epsilon(uh)
    solved_stress = sigma(uh)

    area_local = fem.assemble_scalar(
        fem.form(1.0 * dx)
    )

    exx_local = fem.assemble_scalar(
        fem.form(solved_strain[0, 0] * dx)
    )

    eyy_local = fem.assemble_scalar(
        fem.form(solved_strain[1, 1] * dx)
    )

    sxx_local = fem.assemble_scalar(
        fem.form(solved_stress[0, 0] * dx)
    )

    syy_local = fem.assemble_scalar(
        fem.form(solved_stress[1, 1] * dx)
    )

    area = domain.comm.allreduce(
        area_local,
        op=MPI.SUM,
    )

    average_exx = domain.comm.allreduce(
        exx_local,
        op=MPI.SUM,
    ) / area

    average_eyy = domain.comm.allreduce(
        eyy_local,
        op=MPI.SUM,
    ) / area

    average_sxx = domain.comm.allreduce(
        sxx_local,
        op=MPI.SUM,
    ) / area

    average_syy = domain.comm.allreduce(
        syy_local,
        op=MPI.SUM,
    ) / area

    # ------------------------------------------------------------------
    # 11. Automatic analytical benchmark validation
    # ------------------------------------------------------------------
    expected_exx = prescribed_ux / width
    expected_eyy = -nu * expected_exx
    expected_sxx = E * expected_exx
    expected_syy = 0.0

    tolerance = 1.0e-10

    validation_checks = {
        "epsilon_xx": np.isclose(
            average_exx,
            expected_exx,
            atol=tolerance,
            rtol=0.0,
        ),
        "epsilon_yy": np.isclose(
            average_eyy,
            expected_eyy,
            atol=tolerance,
            rtol=0.0,
        ),
        "sigma_xx": np.isclose(
            average_sxx,
            expected_sxx,
            atol=tolerance,
            rtol=0.0,
        ),
        "sigma_yy": np.isclose(
            average_syy,
            expected_syy,
            atol=tolerance,
            rtol=0.0,
        ),
    }

    validation_passed = all(validation_checks.values())

    if not validation_passed:
        failed_checks = [
            name
            for name, passed in validation_checks.items()
            if not passed
        ]

        raise RuntimeError(
            "Analytical benchmark failed: "
            + ", ".join(failed_checks)
        )

    if domain.comm.rank == 0:
        print("Model:", config["model"]["name"])
        print("Assumption:", config["model"]["assumption"])
        print("Young's modulus:", E)
        print("Poisson's ratio:", nu)
        print("Plane-stress lambda*:", lambda_ps)
        print("Shear modulus mu:", mu)
        print()
        print("Solver convergence reason:", solver_reason)
        print("ux minimum:", ux_min)
        print("ux maximum:", ux_max)
        print("uy minimum:", uy_min)
        print("uy maximum:", uy_max)
        print()
        print("Average epsilon_xx:", average_exx)
        print("Average epsilon_yy:", average_eyy)
        print("Average sigma_xx:", average_sxx)
        print("Average sigma_yy:", average_syy)
        print()
        print("Expected epsilon_xx: 0.01")
        print("Expected epsilon_yy: -0.003")
        print("Expected sigma_xx: 10.0")
        print("Expected sigma_yy: 0.0")
        print()
        print("Expected ux range: 0.0 to 0.01")
        print("Expected uy range: approximately -0.003 to 0.0")
        print("Validation tolerance:", tolerance)
        print("epsilon_xx check:", validation_checks["epsilon_xx"])
        print("epsilon_yy check:", validation_checks["epsilon_yy"])
        print("sigma_xx check:", validation_checks["sigma_xx"])
        print("sigma_yy check:", validation_checks["sigma_yy"])
        print("Analytical benchmark validation: PASSED")
        print()
        print("Homogeneous elasticity solve completed.")


if __name__ == "__main__":
    main()
