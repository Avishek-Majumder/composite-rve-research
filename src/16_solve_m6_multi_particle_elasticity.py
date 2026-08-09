"""Solve M6 multi-particle RVEs with the verified elasticity model.

This solver consumes valid M6 geometry metadata and uses the committed
M6 conformal mesher while preserving the validated M5 mechanics:
2D small-strain isotropic linear elasticity, plane stress, perfect
matrix-particle bonding, and the established displacement boundary
conditions and global effective-property definitions.

Circular void defects are not supported here; they belong to M7.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path

import numpy as np
import ufl
import yaml
from dolfinx import fem, mesh
from dolfinx.fem.petsc import LinearProblem
from mpi4py import MPI
from petsc4py import PETSc


MESHER_PATH = (
    Path(__file__).resolve().parent
    / "15_generate_m6_multi_particle_mesh.py"
)


def load_m6_mesher():
    """Load the committed M6 mesher without modifying the repository."""

    spec = importlib.util.spec_from_file_location(
        "m6_step520_mesher",
        MESHER_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Could not construct import specification "
            "for the M6 mesher."
        )

    module = importlib.util.module_from_spec(
        spec
    )

    spec.loader.exec_module(
        module
    )

    return module


def plane_stress_constants(
    E: float,
    nu: float,
) -> tuple[float, float]:
    """Return shear modulus and verified plane-stress lambda."""

    mu = (
        E
        / (
            2.0
            * (1.0 + nu)
        )
    )

    lambda_3d = (
        E
        * nu
        / (
            (1.0 + nu)
            * (1.0 - 2.0 * nu)
        )
    )

    lambda_ps = (
        2.0
        * mu
        * lambda_3d
        / (
            lambda_3d
            + 2.0 * mu
        )
    )

    return (
        mu,
        lambda_ps,
    )


def main() -> int:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--config",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--geometry-json",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--mesh-size",
        type=float,
        required=True,
    )

    parser.add_argument(
        "--results-file",
        type=Path,
        required=True,
    )

    args = parser.parse_args()

    with args.config.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(
            file
        )

    model_dimension = int(
        config["model"]["dimension"]
    )

    model_assumption = str(
        config["model"]["assumption"]
    )

    interface_assumption = str(
        config["model"]["interface"]
    )

    if model_dimension != 2:
        raise ValueError(
            "Only the locked 2D model is allowed."
        )

    if model_assumption != "plane_stress":
        raise ValueError(
            "Only the locked plane-stress model is allowed."
        )

    if interface_assumption != "perfect_bonding":
        raise ValueError(
            "Only the locked perfect-bonding interface is allowed."
        )

    width = float(
        config["geometry"]["width"]
    )

    height = float(
        config["geometry"]["height"]
    )

    matrix_E = float(
        config["matrix"]["youngs_modulus"]
    )

    matrix_nu = float(
        config["matrix"]["poissons_ratio"]
    )

    particle_E = float(
        config["particle"]["youngs_modulus"]
    )

    particle_nu = float(
        config["particle"]["poissons_ratio"]
    )

    prescribed_ux = float(
        config["loading"][
            "prescribed_x_displacement"
        ]
    )

    mesh_size = float(
        args.mesh_size
    )

    m6_mesher = load_m6_mesher()

    geometry = (
        m6_mesher.load_geometry(
            args.geometry_json
        )
    )

    (
        mesh_data,
        topology_diagnostics,
        expected_total_area,
        expected_particle_area,
    ) = m6_mesher.build_mesh(
        geometry,
        mesh_size,
    )

    mesh_diagnostics = (
        m6_mesher.verify_dolfinx_mesh(
            mesh_data=mesh_data,
            expected_total_area=(
                expected_total_area
            ),
            expected_particle_area=(
                expected_particle_area
            ),
            mesh_size=mesh_size,
            geometry=geometry,
            topology_diagnostics=(
                topology_diagnostics
            ),
        )
    )

    domain = mesh_data.mesh

    cell_tags = mesh_data.cell_tags

    if cell_tags is None:
        raise RuntimeError(
            "Material cell tags are missing."
        )

    physical_groups = (
        mesh_data.physical_groups
    )

    matrix_tag = int(
        physical_groups[
            "matrix"
        ].tag
    )

    particle_tag = int(
        physical_groups[
            "particle"
        ].tag
    )

    gdim = domain.geometry.dim
    tdim = domain.topology.dim
    fdim = tdim - 1

    if gdim != 2:
        raise RuntimeError(
            "Expected 2D geometric dimension."
        )

    V = fem.functionspace(
        domain,
        (
            "Lagrange",
            1,
            (gdim,),
        ),
    )

    (
        matrix_mu,
        matrix_lambda_ps,
    ) = plane_stress_constants(
        matrix_E,
        matrix_nu,
    )

    (
        particle_mu,
        particle_lambda_ps,
    ) = plane_stress_constants(
        particle_E,
        particle_nu,
    )

    def epsilon(displacement):
        return ufl.sym(
            ufl.grad(
                displacement
            )
        )

    def sigma(
        displacement,
        mu,
        lambda_ps,
    ):
        strain = epsilon(
            displacement
        )

        return (
            2.0
            * mu
            * strain
            + lambda_ps
            * ufl.tr(strain)
            * ufl.Identity(gdim)
        )

    u = ufl.TrialFunction(
        V
    )

    v = ufl.TestFunction(
        V
    )

    dx = ufl.Measure(
        "dx",
        domain=domain,
        subdomain_data=cell_tags,
    )

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

    zero_force = fem.Constant(
        domain,
        np.zeros(
            gdim,
            dtype=PETSc.ScalarType,
        ),
    )

    L = (
        ufl.inner(
            zero_force,
            v,
        )
        * ufl.dx
    )

    left_facets = (
        mesh.locate_entities_boundary(
            domain,
            fdim,
            lambda x: np.isclose(
                x[0],
                0.0,
            ),
        )
    )

    right_facets = (
        mesh.locate_entities_boundary(
            domain,
            fdim,
            lambda x: np.isclose(
                x[0],
                width,
            ),
        )
    )

    left_x_dofs = (
        fem.locate_dofs_topological(
            V.sub(0),
            fdim,
            left_facets,
        )
    )

    right_x_dofs = (
        fem.locate_dofs_topological(
            V.sub(0),
            fdim,
            right_facets,
        )
    )

    bottom_left_vertices = (
        mesh.locate_entities_boundary(
            domain,
            0,
            lambda x: (
                np.isclose(
                    x[0],
                    0.0,
                )
                & np.isclose(
                    x[1],
                    0.0,
                )
            ),
        )
    )

    bottom_left_y_dofs = (
        fem.locate_dofs_topological(
            V.sub(1),
            0,
            bottom_left_vertices,
        )
    )

    if len(left_x_dofs) == 0:
        raise RuntimeError(
            "No left-boundary x DOFs found."
        )

    if len(right_x_dofs) == 0:
        raise RuntimeError(
            "No right-boundary x DOFs found."
        )

    if len(bottom_left_y_dofs) == 0:
        raise RuntimeError(
            "No bottom-left y DOF found."
        )

    bc_left = fem.dirichletbc(
        PETSc.ScalarType(
            0.0
        ),
        left_x_dofs,
        V.sub(0),
    )

    bc_right = fem.dirichletbc(
        PETSc.ScalarType(
            prescribed_ux
        ),
        right_x_dofs,
        V.sub(0),
    )

    bc_bottom_left = (
        fem.dirichletbc(
            PETSc.ScalarType(
                0.0
            ),
            bottom_left_y_dofs,
            V.sub(1),
        )
    )

    problem = LinearProblem(
        a,
        L,
        bcs=[
            bc_left,
            bc_right,
            bc_bottom_left,
        ],
        petsc_options_prefix=(
            "m6_multi_particle_elasticity_"
        ),
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "ksp_error_if_not_converged": True,
        },
    )

    uh = problem.solve()

    uh.x.scatter_forward()

    solver_reason = int(
        problem.solver.getConvergedReason()
    )

    solved_strain = epsilon(
        uh
    )

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

    matrix_area_local = (
        fem.assemble_scalar(
            fem.form(
                1.0
                * dx(matrix_tag)
            )
        )
    )

    particle_area_local = (
        fem.assemble_scalar(
            fem.form(
                1.0
                * dx(particle_tag)
            )
        )
    )

    exx_local = (
        fem.assemble_scalar(
            fem.form(
                solved_strain[
                    0,
                    0,
                ]
                * dx
            )
        )
    )

    eyy_local = (
        fem.assemble_scalar(
            fem.form(
                solved_strain[
                    1,
                    1,
                ]
                * dx
            )
        )
    )

    sxx_local = (
        fem.assemble_scalar(
            fem.form(
                matrix_stress[
                    0,
                    0,
                ]
                * dx(matrix_tag)
                + particle_stress[
                    0,
                    0,
                ]
                * dx(particle_tag)
            )
        )
    )

    syy_local = (
        fem.assemble_scalar(
            fem.form(
                matrix_stress[
                    1,
                    1,
                ]
                * dx(matrix_tag)
                + particle_stress[
                    1,
                    1,
                ]
                * dx(particle_tag)
            )
        )
    )

    matrix_area = float(
        domain.comm.allreduce(
            matrix_area_local,
            op=MPI.SUM,
        )
    )

    particle_area = float(
        domain.comm.allreduce(
            particle_area_local,
            op=MPI.SUM,
        )
    )

    total_area = (
        matrix_area
        + particle_area
    )

    average_exx = float(
        domain.comm.allreduce(
            exx_local,
            op=MPI.SUM,
        )
        / total_area
    )

    average_eyy = float(
        domain.comm.allreduce(
            eyy_local,
            op=MPI.SUM,
        )
        / total_area
    )

    average_sxx = float(
        domain.comm.allreduce(
            sxx_local,
            op=MPI.SUM,
        )
        / total_area
    )

    average_syy = float(
        domain.comm.allreduce(
            syy_local,
            op=MPI.SUM,
        )
        / total_area
    )

    effective_modulus = (
        average_sxx
        / average_exx
    )

    effective_poissons_ratio = (
        -average_eyy
        / average_exx
    )

    expected_exx = (
        prescribed_ux
        / width
    )

    _, ux_to_parent = (
        V.sub(0).collapse()
    )

    _, uy_to_parent = (
        V.sub(1).collapse()
    )

    local_ux = (
        uh.x.array[
            ux_to_parent
        ]
    )

    local_uy = (
        uh.x.array[
            uy_to_parent
        ]
    )

    ux_min = float(
        domain.comm.allreduce(
            np.min(local_ux),
            op=MPI.MIN,
        )
    )

    ux_max = float(
        domain.comm.allreduce(
            np.max(local_ux),
            op=MPI.MAX,
        )
    )

    uy_min = float(
        domain.comm.allreduce(
            np.min(local_uy),
            op=MPI.MIN,
        )
    )

    uy_max = float(
        domain.comm.allreduce(
            np.max(local_uy),
            op=MPI.MAX,
        )
    )

    verification = {
        "solver_converged": (
            solver_reason > 0
        ),
        "mesh_checks_passed": all(
            mesh_diagnostics[
                "checks"
            ].values()
        ),
        "positive_material_areas": (
            matrix_area > 0.0
            and particle_area > 0.0
        ),
        "total_area": math.isclose(
            total_area,
            width * height,
            rel_tol=0.0,
            abs_tol=1.0e-10,
        ),
        "average_epsilon_xx": (
            math.isclose(
                average_exx,
                expected_exx,
                rel_tol=0.0,
                abs_tol=1.0e-8,
            )
        ),
        "finite_response": all(
            math.isfinite(value)
            for value in [
                average_exx,
                average_eyy,
                average_sxx,
                average_syy,
                effective_modulus,
                effective_poissons_ratio,
            ]
        ),
        "positive_effective_modulus": (
            effective_modulus > 0.0
        ),
    }

    if not all(
        verification.values()
    ):
        failed = [
            key
            for key, value
            in verification.items()
            if not value
        ]

        raise RuntimeError(
            "Temporary M6 solver verification failed: "
            + ", ".join(failed)
        )

    result = {
        "schema": (
            "m6_multi_particle_elasticity_v1"
        ),
        "model": {
            "dimension": (
                model_dimension
            ),
            "assumption": (
                model_assumption
            ),
            "interface": (
                interface_assumption
            ),
        },
        "geometry": {
            "width": width,
            "height": height,
            "particle_count": len(
                geometry["particles"]
            ),
            "arrangement": geometry[
                "arrangement"
            ],
        },
        "matrix": {
            "youngs_modulus": (
                matrix_E
            ),
            "poissons_ratio": (
                matrix_nu
            ),
        },
        "particle": {
            "youngs_modulus": (
                particle_E
            ),
            "poissons_ratio": (
                particle_nu
            ),
        },
        "loading": {
            "prescribed_x_displacement": (
                prescribed_ux
            ),
        },
        "mesh": {
            "global_size": (
                mesh_size
            ),
            "cell_count": (
                mesh_diagnostics[
                    "mesh"
                ][
                    "cell_count"
                ]
            ),
            "tagged_cell_count": (
                mesh_diagnostics[
                    "mesh"
                ][
                    "tagged_cell_count"
                ]
            ),
            "meshed_particle_fraction": (
                mesh_diagnostics[
                    "area"
                ][
                    "meshed_particle_area_fraction"
                ]
            ),
            "analytical_particle_fraction": (
                mesh_diagnostics[
                    "area"
                ][
                    "analytical_particle_area_fraction"
                ]
            ),
            "particle_fraction_error": (
                mesh_diagnostics[
                    "area"
                ][
                    "particle_area_fraction_error"
                ]
            ),
        },
        "boundary_dofs": {
            "left_x": int(
                len(left_x_dofs)
            ),
            "right_x": int(
                len(right_x_dofs)
            ),
            "bottom_left_y": int(
                len(
                    bottom_left_y_dofs
                )
            ),
        },
        "response": {
            "average_epsilon_xx": (
                average_exx
            ),
            "average_epsilon_yy": (
                average_eyy
            ),
            "average_sigma_xx": (
                average_sxx
            ),
            "average_sigma_yy": (
                average_syy
            ),
            "effective_modulus": (
                effective_modulus
            ),
            "effective_poissons_ratio": (
                effective_poissons_ratio
            ),
            "ux_min": ux_min,
            "ux_max": ux_max,
            "uy_min": uy_min,
            "uy_max": uy_max,
        },
        "solver": {
            "convergence_reason": (
                solver_reason
            ),
        },
        "verification": (
            verification
        ),
    }

    if domain.comm.rank == 0:
        args.results_file.write_text(
            json.dumps(
                result,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
            + "\n",
            encoding="utf-8",
        )

        print(
            json.dumps(
                result,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
