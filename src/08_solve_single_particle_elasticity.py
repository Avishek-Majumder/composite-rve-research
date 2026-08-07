"""Solve the first single-particle 2D composite elasticity model."""

from pathlib import Path
import math

import gmsh
import numpy as np
import ufl
import yaml
from dolfinx import fem, mesh
from dolfinx.fem.petsc import LinearProblem
from dolfinx.io import gmsh as gmshio
from mpi4py import MPI
from petsc4py import PETSc


def main() -> None:
    """Solve single-particle composite uniaxial tension."""

    # ------------------------------------------------------------------
    # 1. Load configuration
    # ------------------------------------------------------------------
    config_path = Path("configs/02_single_particle.yaml")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    width = float(config["geometry"]["width"])
    height = float(config["geometry"]["height"])

    matrix_E = float(config["matrix"]["youngs_modulus"])
    matrix_nu = float(config["matrix"]["poissons_ratio"])

    particle_E = float(config["particle"]["youngs_modulus"])
    particle_nu = float(config["particle"]["poissons_ratio"])

    cx = float(config["particle"]["center_x"])
    cy = float(config["particle"]["center_y"])
    radius = float(config["particle"]["radius"])

    prescribed_ux = float(
        config["loading"]["prescribed_x_displacement"]
    )

    mesh_size = float(config["mesh"]["global_size"])

    # ------------------------------------------------------------------
    # 2. Create tagged matrix + particle mesh with Gmsh
    # ------------------------------------------------------------------
    expected_particle_area = math.pi * radius**2

    matrix_physical_tag = 1
    particle_physical_tag = 2

    gmsh.initialize()

    try:
        gmsh.option.setNumber("General.Terminal", 0)

        gmsh.model.add("single_particle_composite_elasticity")

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
            tag=matrix_physical_tag,
            name="matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            [particle_tag],
            tag=particle_physical_tag,
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
        raise RuntimeError(
            "DOLFINx did not receive material cell tags."
        )

    physical_groups = mesh_data.physical_groups

    if "matrix" not in physical_groups:
        raise RuntimeError(
            "Matrix physical group was not transferred."
        )

    if "particle" not in physical_groups:
        raise RuntimeError(
            "Particle physical group was not transferred."
        )

    matrix_tag = physical_groups["matrix"].tag
    particle_tag = physical_groups["particle"].tag

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
    # 4. Plane-stress elastic constants for both materials
    # ------------------------------------------------------------------
    def plane_stress_constants(E, nu):
        """Return shear modulus and plane-stress lambda."""
        mu = E / (2.0 * (1.0 + nu))

        lambda_3d = (
            E * nu
            / ((1.0 + nu) * (1.0 - 2.0 * nu))
        )

        lambda_ps = (
            2.0 * mu * lambda_3d
            / (lambda_3d + 2.0 * mu)
        )

        return mu, lambda_ps

    matrix_mu, matrix_lambda_ps = plane_stress_constants(
        matrix_E,
        matrix_nu,
    )

    particle_mu, particle_lambda_ps = plane_stress_constants(
        particle_E,
        particle_nu,
    )

    def epsilon(displacement):
        """Small-strain tensor."""
        return ufl.sym(ufl.grad(displacement))

    def sigma(displacement, mu, lambda_ps):
        """2D isotropic plane-stress stress tensor."""
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

    # Material-tagged integration measure
    dx = ufl.Measure(
        "dx",
        domain=domain,
        subdomain_data=cell_tags,
    )

    # Internal virtual work:
    # matrix contribution + particle contribution
    a = (
        ufl.inner(
            sigma(
                u,
                matrix_mu,
                matrix_lambda_ps,
            ),
            epsilon(v),
        )
        * dx(matrix_tag)
        + ufl.inner(
            sigma(
                u,
                particle_mu,
                particle_lambda_ps,
            ),
            epsilon(v),
        )
        * dx(particle_tag)
    )

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
        petsc_options_prefix="single_particle_elasticity_",
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
    # 10. Domain-averaged strain and two-material stress
    # ------------------------------------------------------------------
    solved_strain = epsilon(uh)

    matrix_stress = sigma(
        uh,
        matrix_mu,
        matrix_lambda_ps,
    )

    particle_stress = sigma(
        uh,
        particle_mu,
        particle_lambda_ps,
    )

    matrix_area_local = fem.assemble_scalar(
        fem.form(1.0 * dx(matrix_tag))
    )

    particle_area_local = fem.assemble_scalar(
        fem.form(1.0 * dx(particle_tag))
    )

    exx_local = fem.assemble_scalar(
        fem.form(solved_strain[0, 0] * dx)
    )

    eyy_local = fem.assemble_scalar(
        fem.form(solved_strain[1, 1] * dx)
    )

    sxx_local = fem.assemble_scalar(
        fem.form(
            matrix_stress[0, 0] * dx(matrix_tag)
            + particle_stress[0, 0] * dx(particle_tag)
        )
    )

    syy_local = fem.assemble_scalar(
        fem.form(
            matrix_stress[1, 1] * dx(matrix_tag)
            + particle_stress[1, 1] * dx(particle_tag)
        )
    )

    matrix_area = domain.comm.allreduce(
        matrix_area_local,
        op=MPI.SUM,
    )

    particle_area = domain.comm.allreduce(
        particle_area_local,
        op=MPI.SUM,
    )

    area = matrix_area + particle_area

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
    # 11. Composite-response verification
    # ------------------------------------------------------------------
    expected_area = width * height
    expected_exx = prescribed_ux / width

    analytical_particle_fraction = (
        expected_particle_area / expected_area
    )

    numerical_particle_fraction = (
        particle_area / area
    )

    fraction_error = abs(
        numerical_particle_fraction
        - analytical_particle_fraction
    )

    effective_modulus = average_sxx / average_exx

    effective_poissons_ratio = (
        -average_eyy / average_exx
    )

    strain_tolerance = 1.0e-8

    finite_response = np.all(
        np.isfinite(
            [
                average_exx,
                average_eyy,
                average_sxx,
                average_syy,
                effective_modulus,
                effective_poissons_ratio,
            ]
        )
    )

    validation_checks = {
        "solver_converged": int(solver_reason) > 0,
        "positive_material_areas": (
            matrix_area > 0.0
            and particle_area > 0.0
        ),
        "total_area": math.isclose(
            area,
            expected_area,
            abs_tol=1.0e-10,
            rel_tol=0.0,
        ),
        "particle_fraction": fraction_error <= 0.005,
        "average_epsilon_xx": np.isclose(
            average_exx,
            expected_exx,
            atol=strain_tolerance,
            rtol=0.0,
        ),
        "finite_response": bool(finite_response),
        "positive_effective_modulus": (
            effective_modulus > 0.0
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
            "Composite verification failed: "
            + ", ".join(failed_checks)
        )

    if domain.comm.rank == 0:
        print("Model:", config["model"]["name"])
        print("Assumption:", config["model"]["assumption"])
        print("Interface:", config["model"]["interface"])
        print()

        print("Matrix physical tag:", matrix_tag)
        print("Particle physical tag:", particle_tag)
        print()

        print("Matrix Young's modulus:", matrix_E)
        print("Matrix Poisson's ratio:", matrix_nu)
        print(
            "Matrix plane-stress lambda*:",
            matrix_lambda_ps,
        )
        print("Matrix shear modulus mu:", matrix_mu)
        print()

        print("Particle Young's modulus:", particle_E)
        print("Particle Poisson's ratio:", particle_nu)
        print(
            "Particle plane-stress lambda*:",
            particle_lambda_ps,
        )
        print("Particle shear modulus mu:", particle_mu)
        print()

        print("Matrix area:", matrix_area)
        print("Particle area:", particle_area)
        print("Total area:", area)
        print(
            "Analytical particle fraction:",
            analytical_particle_fraction,
        )
        print(
            "Meshed particle fraction:",
            numerical_particle_fraction,
        )
        print(
            "Particle-fraction error:",
            fraction_error,
        )
        print()

        print(
            "Solver convergence reason:",
            solver_reason,
        )
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

        print(
            "Expected average epsilon_xx:",
            expected_exx,
        )
        print(
            "Effective axial modulus:",
            effective_modulus,
        )
        print(
            "Effective Poisson's ratio:",
            effective_poissons_ratio,
        )
        print()

        print(
            "Solver convergence check:",
            validation_checks["solver_converged"],
        )
        print(
            "Material-area check:",
            validation_checks["positive_material_areas"],
        )
        print(
            "Total-area check:",
            validation_checks["total_area"],
        )
        print(
            "Particle-fraction check:",
            validation_checks["particle_fraction"],
        )
        print(
            "Average epsilon_xx check:",
            validation_checks["average_epsilon_xx"],
        )
        print(
            "Finite-response check:",
            validation_checks["finite_response"],
        )
        print(
            "Positive effective-modulus check:",
            validation_checks[
                "positive_effective_modulus"
            ],
        )

        print()
        print("Composite-response verification: PASSED")
        print()
        print(
            "Single-particle composite elasticity solve completed."
        )


if __name__ == "__main__":
    main()
