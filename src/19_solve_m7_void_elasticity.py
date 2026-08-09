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


def area_weighted_upper_tail_statistics(
    values,
    areas,
    tail_fraction: float,
) -> dict:
    """Return exact physical-area-weighted upper-tail statistics.

    Values are ranked from highest to lowest. Physical area is
    accumulated until exactly ``tail_fraction`` of total area has
    contributed. If the cutoff falls inside the final cell, only the
    required fractional area of that cell is used.

    This helper contains no FEM- or DOLFINx-specific logic.
    """

    stress_values = np.asarray(
        values,
        dtype=np.float64,
    )

    cell_areas = np.asarray(
        areas,
        dtype=np.float64,
    )

    if stress_values.ndim != 1:
        raise ValueError(
            "values must be one-dimensional."
        )

    if cell_areas.ndim != 1:
        raise ValueError(
            "areas must be one-dimensional."
        )

    if stress_values.size == 0:
        raise ValueError(
            "At least one value is required."
        )

    if (
        stress_values.size
        != cell_areas.size
    ):
        raise ValueError(
            "values and areas must have identical lengths."
        )

    if not np.all(
        np.isfinite(
            stress_values
        )
    ):
        raise ValueError(
            "All values must be finite."
        )

    if not np.all(
        np.isfinite(
            cell_areas
        )
    ):
        raise ValueError(
            "All areas must be finite."
        )

    if not np.all(
        cell_areas > 0.0
    ):
        raise ValueError(
            "All cell areas must be strictly positive."
        )

    tail_fraction = float(
        tail_fraction
    )

    if (
        not math.isfinite(
            tail_fraction
        )
        or tail_fraction <= 0.0
        or tail_fraction > 1.0
    ):
        raise ValueError(
            "tail_fraction must satisfy "
            "0 < tail_fraction <= 1."
        )

    total_area = float(
        np.sum(
            cell_areas,
            dtype=np.float64,
        )
    )

    if (
        not math.isfinite(
            total_area
        )
        or total_area <= 0.0
    ):
        raise ValueError(
            "Total physical area must be finite and positive."
        )

    target_tail_area = (
        tail_fraction
        * total_area
    )

    # Stable indirect sorting provides deterministic ordering of
    # equal-valued entries while ranking stress from high to low.
    order = np.argsort(
        -stress_values,
        kind="stable",
    )

    accumulated_area = 0.0
    weighted_sum = 0.0

    contributing_cell_count = 0
    fractional_cutoff_used = False

    area_tolerance = (
        64.0
        * np.finfo(
            np.float64
        ).eps
        * total_area
    )

    for index in order:

        remaining_area = (
            target_tail_area
            - accumulated_area
        )

        if (
            remaining_area
            <= area_tolerance
        ):
            break

        available_area = float(
            cell_areas[
                index
            ]
        )

        included_area = min(
            available_area,
            remaining_area,
        )

        if included_area <= 0.0:
            continue

        weighted_sum += (
            float(
                stress_values[
                    index
                ]
            )
            * included_area
        )

        accumulated_area += (
            included_area
        )

        contributing_cell_count += 1

        if (
            included_area
            < available_area
            - area_tolerance
        ):
            fractional_cutoff_used = True

    if not math.isclose(
        accumulated_area,
        target_tail_area,
        rel_tol=0.0,
        abs_tol=area_tolerance,
    ):
        raise RuntimeError(
            "Upper-tail area accumulation did not reach "
            "the requested physical area."
        )

    # Normalize the accumulated value using the mathematically
    # requested target area rather than the floating accumulated sum.
    tail_mean = (
        weighted_sum
        / target_tail_area
    )

    area_weighted_mean = float(
        np.sum(
            stress_values
            * cell_areas,
            dtype=np.float64,
        )
        / total_area
    )

    raw_max = float(
        stress_values[
            order[0]
        ]
    )

    outputs = (
        tail_mean,
        raw_max,
        area_weighted_mean,
        weighted_sum,
        accumulated_area,
    )

    if not all(
        math.isfinite(
            float(value)
        )
        for value in outputs
    ):
        raise RuntimeError(
            "Upper-tail calculation produced "
            "a non-finite output."
        )

    return {
        "tail_fraction": float(
            tail_fraction
        ),

        "total_area": float(
            total_area
        ),

        "target_tail_area": float(
            target_tail_area
        ),

        "effective_tail_area": float(
            accumulated_area
        ),

        "tail_mean": float(
            tail_mean
        ),

        "raw_max": float(
            raw_max
        ),

        "area_weighted_mean": float(
            area_weighted_mean
        ),

        "contributing_cell_count": int(
            contributing_cell_count
        ),

        "fractional_cutoff_used": bool(
            fractional_cutoff_used
        ),
    }


def extract_m7_matrix_vm_annulus_tail10(
    domain,
    cell_tags,
    displacement,
    geometry: dict,
    matrix_tag: int,
    matrix_E: float,
    matrix_nu: float,
    macro_sigma_xx: float,
) -> dict:
    """Extract the locked M7 matrix von-Mises annulus candidate.

    The Version-1 discrete neighborhood is the union of MATRIX cells
    whose physical cell midpoint satisfies, for at least one void,

        r < distance(midpoint, void_center) <= 2*r.

    Each qualifying matrix cell is counted once.

    The upper-tail statistic is the physical-area-weighted highest
    10 percent of neighborhood matrix area.
    """

    metric_id = (
        "m7_matrix_vm_annulus_tail10_v1"
    )

    tail_fraction = 0.10

    voids = geometry.get(
        "voids"
    )

    if not isinstance(
        voids,
        list,
    ):
        raise ValueError(
            "M7 geometry must contain a void list."
        )

    if len(voids) == 0:

        return {
            "metric_id": metric_id,
            "status": "not_applicable",
            "reason": "zero_void_geometry",
            "tail_fraction": float(
                tail_fraction
            ),
            "neighborhood_matrix_cell_count": 0,
            "neighborhood_matrix_area": None,
            "upper_tail_effective_area": None,
            "upper_tail_contributing_cell_count": 0,
            "fractional_cutoff_used": None,
            "raw_max_sigma_vm": None,
            "area_weighted_neighborhood_mean_sigma_vm": None,
            "sigma_vm_tail10": None,
            "normalization_abs_macro_sigma_xx": None,
            "K_vm_tail10": None,
        }

    macro_sigma_xx = float(
        macro_sigma_xx
    )

    if (
        not math.isfinite(
            macro_sigma_xx
        )
        or abs(
            macro_sigma_xx
        ) <= 0.0
    ):
        raise ValueError(
            "Positive-void local metric requires finite, "
            "non-zero macro_sigma_xx."
        )

    matrix_E = float(
        matrix_E
    )

    matrix_nu = float(
        matrix_nu
    )

    if (
        not math.isfinite(
            matrix_E
        )
        or matrix_E <= 0.0
    ):
        raise ValueError(
            "Matrix Young's modulus must be finite and positive."
        )

    if (
        not math.isfinite(
            matrix_nu
        )
        or matrix_nu <= -1.0
        or matrix_nu >= 0.5
    ):
        raise ValueError(
            "Matrix Poisson ratio must be finite and satisfy "
            "-1 < nu < 0.5."
        )

    if cell_tags is None:
        raise ValueError(
            "M7 local metric requires material cell tags."
        )

    tdim = int(
        domain.topology.dim
    )

    if tdim != 2:
        raise ValueError(
            "M7 Version-1 local metric requires a 2D mesh."
        )

    owned_cell_count = int(
        domain.topology.index_map(
            tdim
        ).size_local
    )

    matrix_cells_all = np.asarray(
        cell_tags.find(
            int(
                matrix_tag
            )
        ),
        dtype=np.int32,
    )

    matrix_cells = np.asarray(
        matrix_cells_all[
            matrix_cells_all
            < owned_cell_count
        ],
        dtype=np.int32,
    )

    if matrix_cells.size > 0:

        matrix_midpoints = (
            mesh.compute_midpoints(
                domain,
                tdim,
                matrix_cells,
            )
        )

        neighborhood_mask = np.zeros(
            matrix_cells.size,
            dtype=bool,
        )

        for void in voids:

            center_x = float(
                void[
                    "center_x"
                ]
            )

            center_y = float(
                void[
                    "center_y"
                ]
            )

            radius = float(
                void[
                    "radius"
                ]
            )

            if (
                not math.isfinite(
                    center_x
                )
                or not math.isfinite(
                    center_y
                )
                or not math.isfinite(
                    radius
                )
                or radius <= 0.0
            ):
                raise ValueError(
                    "Void centers/radii must be finite and "
                    "void radii strictly positive."
                )

            dx = (
                matrix_midpoints[
                    :,
                    0
                ]
                - center_x
            )

            dy = (
                matrix_midpoints[
                    :,
                    1
                ]
                - center_y
            )

            distances = np.sqrt(
                dx * dx
                + dy * dy
            )

            neighborhood_mask |= (
                (distances > radius)
                & (
                    distances
                    <= 2.0 * radius
                )
            )

        neighborhood_cells = np.asarray(
            matrix_cells[
                neighborhood_mask
            ],
            dtype=np.int32,
        )

    else:

        neighborhood_cells = np.empty(
            0,
            dtype=np.int32,
        )


    local_neighborhood_count = int(
        neighborhood_cells.size
    )

    global_neighborhood_count = int(
        domain.comm.allreduce(
            local_neighborhood_count,
            op=MPI.SUM,
        )
    )

    if global_neighborhood_count <= 0:
        raise RuntimeError(
            "Positive-void geometry produced no eligible "
            "matrix cells in the locked annulus neighborhood."
        )


    if local_neighborhood_count > 0:

        mu_matrix, lambda_matrix = (
            plane_stress_constants(
                matrix_E,
                matrix_nu,
            )
        )

        strain = ufl.sym(
            ufl.grad(
                displacement
            )
        )

        matrix_sigma = (
            2.0
            * mu_matrix
            * strain
            + lambda_matrix
            * ufl.tr(
                strain
            )
            * ufl.Identity(
                2
            )
        )

        sigma_xx = (
            matrix_sigma[
                0,
                0
            ]
        )

        sigma_yy = (
            matrix_sigma[
                1,
                1
            ]
        )

        tau_xy = (
            matrix_sigma[
                0,
                1
            ]
        )

        sigma_vm = ufl.sqrt(
            sigma_xx
            * sigma_xx
            - sigma_xx
            * sigma_yy
            + sigma_yy
            * sigma_yy
            + 3.0
            * tau_xy
            * tau_xy
        )

        # Reference midpoint of the triangular reference cell.
        reference_midpoint = np.array(
            [
                [
                    1.0 / 3.0,
                    1.0 / 3.0,
                ]
            ],
            dtype=np.float64,
        )

        vm_expression = fem.Expression(
            sigma_vm,
            reference_midpoint,
        )

        area_expression = fem.Expression(
            ufl.CellVolume(
                domain
            ),
            reference_midpoint,
        )

        local_vm = np.asarray(
            vm_expression.eval(
                domain,
                neighborhood_cells,
            ),
            dtype=np.float64,
        ).reshape(
            local_neighborhood_count,
            -1,
        )[
            :,
            0
        ]

        local_areas = np.asarray(
            area_expression.eval(
                domain,
                neighborhood_cells,
            ),
            dtype=np.float64,
        ).reshape(
            local_neighborhood_count,
            -1,
        )[
            :,
            0
        ]

        if not np.all(
            np.isfinite(
                local_vm
            )
        ):
            raise RuntimeError(
                "Non-finite matrix von Mises stress encountered."
            )

        if not np.all(
            local_vm >= 0.0
        ):
            raise RuntimeError(
                "Negative von Mises stress encountered."
            )

        if (
            not np.all(
                np.isfinite(
                    local_areas
                )
            )
            or not np.all(
                local_areas > 0.0
            )
        ):
            raise RuntimeError(
                "Neighborhood cell areas must be finite "
                "and strictly positive."
            )

    else:

        local_vm = np.empty(
            0,
            dtype=np.float64,
        )

        local_areas = np.empty(
            0,
            dtype=np.float64,
        )


    gathered_vm = domain.comm.gather(
        local_vm,
        root=0,
    )

    gathered_areas = domain.comm.gather(
        local_areas,
        root=0,
    )


    result = None

    if domain.comm.rank == 0:

        global_vm = np.concatenate(
            gathered_vm
        )

        global_areas = np.concatenate(
            gathered_areas
        )

        if (
            global_vm.size
            != global_neighborhood_count
        ):
            raise RuntimeError(
                "Gathered neighborhood stress count mismatch."
            )

        if (
            global_areas.size
            != global_neighborhood_count
        ):
            raise RuntimeError(
                "Gathered neighborhood area count mismatch."
            )

        statistics = (
            area_weighted_upper_tail_statistics(
                values=global_vm,
                areas=global_areas,
                tail_fraction=tail_fraction,
            )
        )

        normalization = abs(
            macro_sigma_xx
        )

        K_vm_tail10 = (
            statistics[
                "tail_mean"
            ]
            / normalization
        )

        if (
            not math.isfinite(
                K_vm_tail10
            )
            or K_vm_tail10 < 0.0
        ):
            raise RuntimeError(
                "Normalized local defect metric is invalid."
            )

        result = {
            "metric_id": metric_id,
            "status": "valid",
            "reason": None,
            "tail_fraction": float(
                tail_fraction
            ),
            "neighborhood_matrix_cell_count": int(
                global_neighborhood_count
            ),
            "neighborhood_matrix_area": float(
                statistics[
                    "total_area"
                ]
            ),
            "upper_tail_effective_area": float(
                statistics[
                    "effective_tail_area"
                ]
            ),
            "upper_tail_contributing_cell_count": int(
                statistics[
                    "contributing_cell_count"
                ]
            ),
            "fractional_cutoff_used": bool(
                statistics[
                    "fractional_cutoff_used"
                ]
            ),
            "raw_max_sigma_vm": float(
                statistics[
                    "raw_max"
                ]
            ),
            "area_weighted_neighborhood_mean_sigma_vm": float(
                statistics[
                    "area_weighted_mean"
                ]
            ),
            "sigma_vm_tail10": float(
                statistics[
                    "tail_mean"
                ]
            ),
            "normalization_abs_macro_sigma_xx": float(
                normalization
            ),
            "K_vm_tail10": float(
                K_vm_tail10
            ),
        }


    result = domain.comm.bcast(
        result,
        root=0,
    )

    return result


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

    local_response = (
        extract_m7_matrix_vm_annulus_tail10(
            domain=domain,
            cell_tags=cell_tags,
            displacement=uh,
            geometry=geometry,
            matrix_tag=matrix_tag,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            macro_sigma_xx=macro_sigma_xx,
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

    verification[
        "local_response_metric_id"
    ] = (
        local_response[
            "metric_id"
        ]
        == "m7_matrix_vm_annulus_tail10_v1"
    )

    if void_count > 0:

        verification.update(
            {
                "local_response_status_valid": (
                    local_response[
                        "status"
                    ]
                    == "valid"
                ),

                "local_response_positive_neighborhood": (
                    local_response[
                        "neighborhood_matrix_cell_count"
                    ]
                    > 0
                    and local_response[
                        "neighborhood_matrix_area"
                    ]
                    > 0.0
                    and local_response[
                        "upper_tail_contributing_cell_count"
                    ]
                    > 0
                ),

                "local_response_finite": all(
                    math.isfinite(
                        float(value)
                    )
                    for value in [
                        local_response[
                            "neighborhood_matrix_area"
                        ],
                        local_response[
                            "upper_tail_effective_area"
                        ],
                        local_response[
                            "raw_max_sigma_vm"
                        ],
                        local_response[
                            "area_weighted_neighborhood_mean_sigma_vm"
                        ],
                        local_response[
                            "sigma_vm_tail10"
                        ],
                        local_response[
                            "normalization_abs_macro_sigma_xx"
                        ],
                        local_response[
                            "K_vm_tail10"
                        ],
                    ]
                ),

                "local_response_tail_area_identity": (
                    math.isclose(
                        local_response[
                            "upper_tail_effective_area"
                        ],
                        local_response[
                            "tail_fraction"
                        ]
                        * local_response[
                            "neighborhood_matrix_area"
                        ],
                        rel_tol=0.0,
                        abs_tol=1.0e-12,
                    )
                ),

                "local_response_normalization_matches_macro": (
                    math.isclose(
                        local_response[
                            "normalization_abs_macro_sigma_xx"
                        ],
                        abs(
                            macro_sigma_xx
                        ),
                        rel_tol=0.0,
                        abs_tol=1.0e-12,
                    )
                ),

                "local_response_ordering_sanity": (
                    local_response[
                        "raw_max_sigma_vm"
                    ]
                    + 1.0e-12
                    >= local_response[
                        "sigma_vm_tail10"
                    ]
                    and local_response[
                        "sigma_vm_tail10"
                    ]
                    + 1.0e-12
                    >= local_response[
                        "area_weighted_neighborhood_mean_sigma_vm"
                    ]
                ),

                "local_response_nonnegative_K": (
                    local_response[
                        "K_vm_tail10"
                    ]
                    >= 0.0
                ),
            }
        )

    else:

        verification.update(
            {
                "local_response_not_applicable": (
                    local_response[
                        "status"
                    ]
                    == "not_applicable"
                    and local_response[
                        "reason"
                    ]
                    == "zero_void_geometry"
                ),

                "local_response_zero_void_payload": (
                    local_response[
                        "neighborhood_matrix_cell_count"
                    ]
                    == 0
                    and local_response[
                        "neighborhood_matrix_area"
                    ]
                    is None
                    and local_response[
                        "upper_tail_effective_area"
                    ]
                    is None
                    and local_response[
                        "raw_max_sigma_vm"
                    ]
                    is None
                    and local_response[
                        "area_weighted_neighborhood_mean_sigma_vm"
                    ]
                    is None
                    and local_response[
                        "sigma_vm_tail10"
                    ]
                    is None
                    and local_response[
                        "normalization_abs_macro_sigma_xx"
                    ]
                    is None
                    and local_response[
                        "K_vm_tail10"
                    ]
                    is None
                ),
            }
        )

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
            "m7_void_elasticity_v2"
        ),

        "response_definition": (
            "m7_gross_rve_axial_v1"
        ),

        "local_response_definition": (
            "m7_matrix_vm_annulus_tail10_v1"
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

        "local_response": local_response,

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
