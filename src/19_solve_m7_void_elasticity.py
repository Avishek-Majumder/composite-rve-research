"""Solve M7 circular-void RVEs with the verified elasticity model.

This solver consumes valid M7 void geometry metadata and uses the committed
M7 void-capable conformal mesher while preserving the validated M5/M6
mechanics: 2D small-strain isotropic linear elasticity, plane stress,
perfect matrix-particle bonding, and the established displacement boundary
conditions.

Void-aware response normalization is adapted separately and explicitly.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
import sys
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
    / "18_generate_m7_void_mesh.py"
)


def load_m7_mesher():
    """Load the committed M7 void mesher from its source path."""

    module_name = (
        "m7_void_mesher_for_solver"
    )

    spec = importlib.util.spec_from_file_location(
        module_name,
        MESHER_PATH,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not construct import specification "
            "for the M7 void mesher."
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[
        module_name
    ] = module

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

    m7_mesher = load_m7_mesher()

    geometry = (
        m7_mesher.load_geometry(
            args.geometry_json
        )
    )

    (
        mesh_data,
        topology_diagnostics,
    ) = m7_mesher.build_m7_mesh_data(
        geometry=geometry,
        mesh_size=mesh_size,
    )

    mesh_diagnostics = (
        m7_mesher.verify_m7_dolfinx_mesh(
            mesh_data=mesh_data,
            topology_diagnostics=(
                topology_diagnostics
            ),
            geometry=geometry,
            mesh_size=mesh_size,
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
            "m7_void_elasticity_"
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

    solid_area = (
        matrix_area
        + particle_area
    )

    gross_rve_area = (
        width
        * height
    )

    expected_gross_rve_area = float(
        mesh_diagnostics[
            "area"
        ][
            "expected_gross_rve_area"
        ]
    )

    expected_void_area = float(
        mesh_diagnostics[
            "area"
        ][
            "expected_void_area"
        ]
    )

    meshed_void_area = (
        gross_rve_area
        - solid_area
    )

    exx_integral = float(
        domain.comm.allreduce(
            exx_local,
            op=MPI.SUM,
        )
    )

    eyy_integral = float(
        domain.comm.allreduce(
            eyy_local,
            op=MPI.SUM,
        )
    )

    sxx_integral = float(
        domain.comm.allreduce(
            sxx_local,
            op=MPI.SUM,
        )
    )

    syy_integral = float(
        domain.comm.allreduce(
            syy_local,
            op=MPI.SUM,
        )
    )

    # --------------------------------------------------------
    # M6-style solid-domain averages retained ONLY as
    # regression/diagnostic quantities.
    # --------------------------------------------------------

    solid_average_exx = (
        exx_integral
        / solid_area
    )

    solid_average_eyy = (
        eyy_integral
        / solid_area
    )

    solid_average_sxx = (
        sxx_integral
        / solid_area
    )

    solid_average_syy = (
        syy_integral
        / solid_area
    )

    solid_domain_modulus_diagnostic = (
        solid_average_sxx
        / solid_average_exx
    )

    solid_domain_poisson_diagnostic = (
        -solid_average_eyy
        / solid_average_exx
    )

    # --------------------------------------------------------
    # M7 Version-1 provisional porous macroscopic response.
    #
    # Stress uses the gross RVE reference area. The void has
    # no material cells and therefore contributes zero stress.
    #
    # Axial macro strain remains the imposed displacement
    # divided by RVE width.
    # --------------------------------------------------------

    macro_epsilon_xx = (
        prescribed_ux
        / width
    )

    macro_sigma_xx = (
        sxx_integral
        / gross_rve_area
    )

    macro_sigma_yy = (
        syy_integral
        / gross_rve_area
    )

    apparent_axial_modulus = (
        macro_sigma_xx
        / macro_epsilon_xx
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

    void_count = int(
        geometry[
            "generated_geometry"
        ][
            "void_count"
        ]
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
            and solid_area > 0.0
        ),

        "gross_rve_area_matches_config": (
            math.isclose(
                gross_rve_area,
                expected_gross_rve_area,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        ),

        "solid_plus_void_equals_gross": (
            math.isclose(
                solid_area
                + expected_void_area,
                gross_rve_area,
                rel_tol=0.0,
                abs_tol=5.0e-3,
            )
        ),

        "meshed_void_area_matches_mesher": (
            math.isclose(
                meshed_void_area,
                float(
                    mesh_diagnostics[
                        "area"
                    ][
                        "meshed_void_area"
                    ]
                ),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        ),

        "macro_epsilon_definition": (
            math.isclose(
                macro_epsilon_xx,
                prescribed_ux
                / width,
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
        ),

        "finite_response": all(
            math.isfinite(value)
            for value in [
                solid_average_exx,
                solid_average_eyy,
                solid_average_sxx,
                solid_average_syy,
                solid_domain_modulus_diagnostic,
                solid_domain_poisson_diagnostic,
                macro_epsilon_xx,
                macro_sigma_xx,
                macro_sigma_yy,
                apparent_axial_modulus,
            ]
        ),

        "positive_apparent_axial_modulus": (
            apparent_axial_modulus
            > 0.0
        ),
    }

    if void_count == 0:

        verification.update(
            {
                "zero_void_solid_area_equals_gross": (
                    math.isclose(
                        solid_area,
                        gross_rve_area,
                        rel_tol=0.0,
                        abs_tol=1.0e-10,
                    )
                ),

                "zero_void_macro_sigma_equals_solid_average": (
                    math.isclose(
                        macro_sigma_xx,
                        solid_average_sxx,
                        rel_tol=0.0,
                        abs_tol=1.0e-10,
                    )
                ),

                "zero_void_macro_strain_equals_solid_average": (
                    math.isclose(
                        macro_epsilon_xx,
                        solid_average_exx,
                        rel_tol=0.0,
                        abs_tol=1.0e-8,
                    )
                ),

                "zero_void_apparent_modulus_equals_solid_diagnostic": (
                    math.isclose(
                        apparent_axial_modulus,
                        solid_domain_modulus_diagnostic,
                        rel_tol=0.0,
                        abs_tol=1.0e-6,
                    )
                ),
            }
        )

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
            "M7 void-aware solver verification failed: "
            + ", ".join(
                failed
            )
        )

    result = {
        "schema": (
            "m7_void_elasticity_v1"
        ),

        "response_definition": (
            "m7_gross_rve_axial_v1"
        ),

        "geometry": {
            "schema": (
                geometry[
                    "schema"
                ]
            ),

            "source_m6_geometry_schema": (
                geometry[
                    "source_m6_geometry"
                ][
                    "schema"
                ]
            ),

            "source_m6_geometry_sha256": (
                geometry[
                    "source_m6_geometry"
                ][
                    "sha256"
                ]
            ),

            "particle_seed": int(
                geometry[
                    "source_m6_geometry"
                ][
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
                    geometry[
                        "particles"
                    ]
                )
            ),

            "void_count": int(
                len(
                    geometry[
                        "voids"
                    ]
                )
            ),

            "particle_area_fraction": float(
                geometry[
                    "generated_geometry"
                ][
                    "particle_area_fraction"
                ]
            ),

            "void_area_fraction": float(
                geometry[
                    "generated_geometry"
                ][
                    "void_area_fraction"
                ]
            ),
        },

        "model": {
            "dimension": int(
                model_dimension
            ),

            "assumption": (
                model_assumption
            ),

            "interface": (
                interface_assumption
            ),
        },

        "rve": {
            "width": float(
                width
            ),

            "height": float(
                height
            ),
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
            "schema": (
                mesh_diagnostics[
                    "schema"
                ]
            ),

            "mesh_size": float(
                mesh_size
            ),

            "cell_count": int(
                mesh_diagnostics[
                    "mesh"
                ][
                    "cell_count"
                ]
            ),

            "tagged_cell_count": int(
                mesh_diagnostics[
                    "mesh"
                ][
                    "tagged_cell_count"
                ]
            ),

            "void_boundary_facet_count": int(
                mesh_diagnostics[
                    "mesh"
                ][
                    "void_boundary_facet_count"
                ]
            ),

            "checks_passed": all(
                mesh_diagnostics[
                    "checks"
                ].values()
            ),
        },

        "area": {
            "gross_rve_area": float(
                gross_rve_area
            ),

            "matrix_area": float(
                matrix_area
            ),

            "particle_area": float(
                particle_area
            ),

            "solid_area": float(
                solid_area
            ),

            "expected_void_area": float(
                expected_void_area
            ),

            "meshed_void_area": float(
                meshed_void_area
            ),
        },

        "boundary_dofs": {
            "left_x": int(
                len(
                    left_x_dofs
                )
            ),

            "right_x": int(
                len(
                    right_x_dofs
                )
            ),

            "bottom_left_y": int(
                len(
                    bottom_left_y_dofs
                )
            ),
        },

        "response": {
            # Provisional M7 porous macroscopic response.
            "macro_epsilon_xx": float(
                macro_epsilon_xx
            ),

            "macro_sigma_xx": float(
                macro_sigma_xx
            ),

            "macro_sigma_yy": float(
                macro_sigma_yy
            ),

            "apparent_axial_modulus": float(
                apparent_axial_modulus
            ),

            # Explicitly diagnostic M6-style solid averages.
            "solid_domain_average_epsilon_xx": float(
                solid_average_exx
            ),

            "solid_domain_average_epsilon_yy": float(
                solid_average_eyy
            ),

            "solid_domain_average_sigma_xx": float(
                solid_average_sxx
            ),

            "solid_domain_average_sigma_yy": float(
                solid_average_syy
            ),

            "solid_domain_modulus_diagnostic": float(
                solid_domain_modulus_diagnostic
            ),

            "solid_domain_poisson_diagnostic": float(
                solid_domain_poisson_diagnostic
            ),

            "ux_min": float(
                ux_min
            ),

            "ux_max": float(
                ux_max
            ),

            "uy_min": float(
                uy_min
            ),

            "uy_max": float(
                uy_max
            ),
        },

        "solver": {
            "convergence_reason": int(
                solver_reason
            ),

            "converged": (
                solver_reason > 0
            ),
        },

        "verification": {
            key: bool(
                value
            )
            for key, value
            in verification.items()
        },

        "status": "valid",
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
