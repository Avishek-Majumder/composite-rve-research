from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import numpy as np
import ufl
import yaml
from mpi4py import MPI
from petsc4py import PETSc

import dolfinx
import dolfinx_mpc
from dolfinx import fem
from dolfinx.io import gmsh as gmshio









GEOM_TOL = 1.0e-10
MPC_TOL = 1.0e-12

PERIODIC_TOL = 1.0e-8
GAUGE_TOL = 1.0e-12
ALGEBRAIC_TOL = 1.0e-10
MACRO_STRAIN_TOL = 1.0e-8
HILL_MANDEL_TOL = 1.0e-5
WEAK_IDENTITY_TOL = 1.0e-10




RVE_WIDTH = math.nan
RVE_HEIGHT = math.nan


def must(condition: bool, message: str) -> None:
    if condition:
        print(f"PASS — {message}")
        return

    print(
        f"FAIL — DO NOT CONTINUE: {message}"
    )
    raise RuntimeError(message)


def plane_stress_constants(
    young: float,
    poisson: float,
) -> tuple[float, float]:
    mu = (
        young
        / (
            2.0
            * (1.0 + poisson)
        )
    )

    lambda_3d = (
        young
        * poisson
        / (
            (1.0 + poisson)
            * (1.0 - 2.0 * poisson)
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
        float(mu),
        float(lambda_ps),
    )


def right_except_top_right(
    x: np.ndarray,
) -> np.ndarray:
    return np.logical_and(
        np.isclose(
            x[0],
            RVE_WIDTH,
            atol=GEOM_TOL,
            rtol=0.0,
        ),
        ~np.isclose(
            x[1],
            RVE_HEIGHT,
            atol=GEOM_TOL,
            rtol=0.0,
        ),
    )


def right_to_left(
    x: np.ndarray,
) -> np.ndarray:
    out = np.array(x, copy=True)
    out[0] -= RVE_WIDTH
    return out


def top_except_top_right(
    x: np.ndarray,
) -> np.ndarray:
    return np.logical_and(
        np.isclose(
            x[1],
            RVE_HEIGHT,
            atol=GEOM_TOL,
            rtol=0.0,
        ),
        ~np.isclose(
            x[0],
            RVE_WIDTH,
            atol=GEOM_TOL,
            rtol=0.0,
        ),
    )


def top_to_bottom(
    x: np.ndarray,
) -> np.ndarray:
    out = np.array(x, copy=True)
    out[1] -= RVE_HEIGHT
    return out


def top_right_only(
    x: np.ndarray,
) -> np.ndarray:
    return np.logical_and(
        np.isclose(
            x[0],
            RVE_WIDTH,
            atol=GEOM_TOL,
            rtol=0.0,
        ),
        np.isclose(
            x[1],
            RVE_HEIGHT,
            atol=GEOM_TOL,
            rtol=0.0,
        ),
    )


def top_right_to_bottom_left(
    x: np.ndarray,
) -> np.ndarray:
    out = np.array(x, copy=True)
    out[0] -= RVE_WIDTH
    out[1] -= RVE_HEIGHT
    return out


def find_unique_block(
    coordinates: np.ndarray,
    target: np.ndarray,
) -> int:
    delta = np.max(
        np.abs(
            coordinates
            - target[None, :]
        ),
        axis=1,
    )

    found = np.flatnonzero(
        delta <= GEOM_TOL
    )

    must(
        len(found) == 1,
        (
            "exactly one DOF block exists at "
            f"{target.tolist()}"
        ),
    )

    return int(found[0])


def mpi_sum(
    value: float,
) -> float:
    return float(
        MPI.COMM_WORLD.allreduce(
            float(value),
            op=MPI.SUM,
        )
    )


def main() -> None:
    global RVE_WIDTH, RVE_HEIGHT

    parser = argparse.ArgumentParser(
        description=(
            "Solve one permanent M8 periodized "
            "particle RVE load case using PBC."
        )
    )

    parser.add_argument(
        "--mesh",
        required=True,
        help="Periodic Gmsh .msh file from src/21.",
    )

    parser.add_argument(
        "--mesh-diagnostics",
        required=True,
        help=(
            "Permanent src/21 mesh diagnostics JSON."
        ),
    )

    parser.add_argument(
        "--config",
        default="configs/03_parametric_rve_base.yaml",
        help=(
            "Elastic material configuration YAML."
        ),
    )

    parser.add_argument(
        "--load-case",
        required=True,
        choices=["X", "Y", "XY"],
        help=(
            "Macroscopic engineering-Voigt "
            "strain load case."
        ),
    )

    parser.add_argument(
        "--macro-amplitude",
        type=float,
        default=0.01,
        help=(
            "Engineering strain amplitude."
        ),
    )

    parser.add_argument(
        "--output",
        required=True,
        help=(
            "Output diagnostics JSON path."
        ),
    )

    args = parser.parse_args()

    mesh_path = Path(args.mesh)
    mesh_diag_path = Path(
        args.mesh_diagnostics
    )
    config_path = Path(args.config)
    out_path = Path(args.output)

    load_case = str(args.load_case)
    macro_amplitude = float(
        args.macro_amplitude
    )

    must(
        mesh_path.is_file(),
        "runtime periodic mesh exists",
    )

    must(
        mesh_diag_path.is_file(),
        "runtime mesh diagnostics exist",
    )

    must(
        config_path.is_file(),
        "runtime material config exists",
    )

    must(
        math.isfinite(
            macro_amplitude
        )
        and macro_amplitude > 0.0,
        "macroscopic strain amplitude is finite and positive",
    )

    mesh_diag = json.loads(
        mesh_diag_path.read_text(
            encoding="utf-8"
        )
    )

    must(
        mesh_diag.get("schema")
        == "m8_periodized_particle_mesh_diagnostics_v1",
        "permanent mesh diagnostics schema is valid",
    )

    must(
        mesh_diag.get("status")
        == "valid",
        "permanent mesh diagnostics status is valid",
    )

    must(
        mesh_diag[
            "scope_guard"
        ][
            "fem_solve_performed"
        ]
        is False,
        "input mesh predates FEM solve",
    )

    must(
        mesh_diag[
            "scope_guard"
        ][
            "voids_generated"
        ]
        is False,
        "pristine particle-only M8 mesh supplied",
    )

    must(
        mesh_diag[
            "mesh"
        ][
            "element_policy"
        ]
        == "first_order_triangles",
        "runtime mesh uses validated first-order triangles",
    )

    RVE_WIDTH = float(
        mesh_diag[
            "provenance"
        ][
            "width"
        ]
    )

    RVE_HEIGHT = float(
        mesh_diag[
            "provenance"
        ][
            "height"
        ]
    )

    must(
        math.isfinite(RVE_WIDTH)
        and RVE_WIDTH > 0.0,
        "runtime RVE width is finite and positive",
    )

    must(
        math.isfinite(RVE_HEIGHT)
        and RVE_HEIGHT > 0.0,
        "runtime RVE height is finite and positive",
    )

    must(
        abs(
            RVE_WIDTH
            - RVE_HEIGHT
        )
        <= GEOM_TOL,
        "permanent M8 PBC solver receives a square RVE",
    )

    gross_area_from_dimensions = (
        RVE_WIDTH
        * RVE_HEIGHT
    )

    must(
        abs(
            gross_area_from_dimensions
            - float(
                mesh_diag[
                    "provenance"
                ][
                    "gross_area"
                ]
            )
        )
        <= 1.0e-12,
        "runtime dimensions reproduce mesh gross area",
    )

    matrix_tag = int(
        mesh_diag[
            "physical_tags"
        ][
            "matrix"
        ]
    )

    particle_tag = int(
        mesh_diag[
            "physical_tags"
        ][
            "particle"
        ]
    )

    must(
        matrix_tag != particle_tag,
        "matrix and particle physical tags are distinct",
    )

    must(
        matrix_tag > 0
        and particle_tag > 0,
        "material physical tags are positive",
    )

    geometry_seed = int(
        mesh_diag[
            "source_geometry"
        ][
            "seed"
        ]
    )

    geometry_sha256 = str(
        mesh_diag[
            "source_geometry"
        ][
            "geometry_sha256"
        ]
    )

    must(
        mesh_diag[
            "source_geometry"
        ][
            "schema"
        ]
        == "m8_periodized_particle_microstructure_v1",
        "mesh references permanent M8 periodized geometry",
    )

    mesh_provenance = {
        "provenance": {
            "geometry_seed": geometry_seed,
            "geometry_sha256": geometry_sha256,
            "mesh_size": float(
                mesh_diag[
                    "provenance"
                ][
                    "mesh_size"
                ]
            ),
        },
    }

    mesh_area_reference = {
        "areas": {
            "matrix": float(
                mesh_diag[
                    "meshed_area"
                ][
                    "matrix_area"
                ]
            ),
            "particle": float(
                mesh_diag[
                    "meshed_area"
                ][
                    "particle_area"
                ]
            ),
        },
    }

    if load_case == "X":
        e_bar_numpy = np.array(
            [
                [macro_amplitude, 0.0],
                [0.0, 0.0],
            ],
            dtype=float,
        )

        expected_macro_strain = np.array(
            [
                macro_amplitude,
                0.0,
                0.0,
            ],
            dtype=float,
        )

        positive_component_index = 0

    elif load_case == "Y":
        e_bar_numpy = np.array(
            [
                [0.0, 0.0],
                [0.0, macro_amplitude],
            ],
            dtype=float,
        )

        expected_macro_strain = np.array(
            [
                0.0,
                macro_amplitude,
                0.0,
            ],
            dtype=float,
        )

        positive_component_index = 1

    else:
        e_bar_numpy = np.array(
            [
                [
                    0.0,
                    0.5 * macro_amplitude,
                ],
                [
                    0.5 * macro_amplitude,
                    0.0,
                ],
            ],
            dtype=float,
        )

        expected_macro_strain = np.array(
            [
                0.0,
                0.0,
                macro_amplitude,
            ],
            dtype=float,
        )

        positive_component_index = 2

    out_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    must(
        MPI.COMM_WORLD.size == 1,
        "permanent M8 PBC runs in serial",
    )

    print("DOLFINx version    :", dolfinx.__version__)
    print(
        "DOLFINx-MPC version:",
        getattr(
            dolfinx_mpc,
            "__version__",
            "0.11.0 package",
        ),
    )

    must(
        dolfinx.__version__ == "0.11.0",
        "DOLFINx remains 0.11.0",
    )

    # --------------------------------------------------------
    # Permanent runtime provenance
    # --------------------------------------------------------









    # --------------------------------------------------------
    # Existing protected material configuration
    # --------------------------------------------------------

    config = yaml.safe_load(
        config_path.read_text(
            encoding="utf-8"
        )
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

    print()
    print("Material configuration:")
    print("  E_matrix   =", matrix_E)
    print("  nu_matrix  =", matrix_nu)
    print("  E_particle =", particle_E)
    print("  nu_particle=", particle_nu)
    print(
        "  stiffness ratio =",
        particle_E / matrix_E,
    )

    must(
        config["model"]["dimension"] == 2,
        "material model dimension remains 2D",
    )

    must(
        config["model"]["assumption"]
        == "plane_stress",
        "material model remains plane stress",
    )

    must(
        config["model"]["interface"]
        == "perfect_bonding",
        "material interface remains perfectly bonded",
    )

    must(
        math.isfinite(matrix_E)
        and matrix_E > 0.0,
        "matrix Young's modulus is finite and positive",
    )

    must(
        math.isfinite(particle_E)
        and particle_E > 0.0,
        "particle Young's modulus is finite and positive",
    )

    must(
        math.isfinite(matrix_nu)
        and -1.0 < matrix_nu < 0.5,
        "matrix Poisson ratio is within admissible isotropic range",
    )

    must(
        math.isfinite(particle_nu)
        and -1.0 < particle_nu < 0.5,
        "particle Poisson ratio is within admissible isotropic range",
    )

    must(
        math.isfinite(
            particle_E / matrix_E
        )
        and (
            particle_E / matrix_E
        ) > 0.0,
        "stiffness ratio is finite and positive",
    )





    # --------------------------------------------------------
    # Import runtime permanent M8 mesh
    # --------------------------------------------------------

    print()
    print("Importing runtime permanent M8 mesh...")

    mesh_data = gmshio.read_from_msh(
        mesh_path,
        MPI.COMM_WORLD,
        rank=0,
        gdim=2,
    )

    domain = mesh_data.mesh
    cell_tags = mesh_data.cell_tags

    must(
        cell_tags is not None,
        "material cell tags imported",
    )

    tdim = domain.topology.dim
    cell_map = domain.topology.index_map(
        tdim
    )

    cell_count = int(
        cell_map.size_local
        + cell_map.num_ghosts
    )

    matrix_cells = int(
        np.count_nonzero(
            cell_tags.values
            == matrix_tag
        )
    )

    particle_cells = int(
        np.count_nonzero(
            cell_tags.values
            == particle_tag
        )
    )

    print("Cell count         :", cell_count)
    print("Matrix cell count  :", matrix_cells)
    print("Particle cell count:", particle_cells)

    must(
        cell_count
        == int(
            mesh_diag["mesh"]["cell_count"]
        ),
        "DOLFINx imported runtime cell count matches permanent mesh diagnostics",
    )

    must(
        matrix_cells
        == int(
            mesh_diag[
                "mesh"
            ][
                "matrix_cell_count"
            ]
        ),
        "DOLFINx matrix-cell count matches permanent mesh diagnostics",
    )

    must(
        particle_cells
        == int(
            mesh_diag[
                "mesh"
            ][
                "particle_cell_count"
            ]
        ),
        "DOLFINx particle-cell count matches permanent mesh diagnostics",
    )

    must(
        len(cell_tags.indices)
        == cell_count,
        "every cell has a material tag",
    )

    must(
        set(
            int(v)
            for v
            in np.unique(
                cell_tags.values
            )
        )
        == {
            matrix_tag,
            particle_tag,
        },
        "only intended material tags are present",
    )

    # --------------------------------------------------------
    # Displacement fluctuation space + clean periodic MPC
    # --------------------------------------------------------

    V = fem.functionspace(
        domain,
        (
            "Lagrange",
            1,
            (2,),
        ),
    )

    bs = int(V.dofmap.bs)

    must(
        bs == 2,
        "P1 displacement space has two components",
    )

    mpc = dolfinx_mpc.MultiPointConstraint(
        V
    )

    mpc.create_periodic_constraint_geometrical(
        V,
        right_except_top_right,
        right_to_left,
        [],
        tol=MPC_TOL,
    )

    mpc.create_periodic_constraint_geometrical(
        V,
        top_except_top_right,
        top_to_bottom,
        [],
        tol=MPC_TOL,
    )

    mpc.create_periodic_constraint_geometrical(
        V,
        top_right_only,
        top_right_to_bottom_left,
        [],
        tol=MPC_TOL,
    )

    mpc.finalize()

    slaves = np.asarray(
        mpc.slaves,
        dtype=np.int64,
    )

    slave_set = {
        int(v)
        for v in slaves
    }

    master_set: set[int] = set()

    coeffs, offsets = (
        mpc.coefficients()
    )

    coeffs = np.asarray(
        coeffs,
        dtype=float,
    )

    offsets = np.asarray(
        offsets,
        dtype=np.int64,
    )

    max_coeff_error = 0.0
    max_master_count = 0
    min_master_count = 999999

    for slave in slaves:
        slave = int(slave)

        masters = np.asarray(
            mpc.masters.links(slave),
            dtype=np.int64,
        )

        count = int(len(masters))

        max_master_count = max(
            max_master_count,
            count,
        )

        min_master_count = min(
            min_master_count,
            count,
        )

        must(
            count == 1,
            (
                f"periodic slave {slave} "
                "has exactly one master"
            ),
        )

        master_set.add(
            int(masters[0])
        )

        c0 = int(
            offsets[slave]
        )
        c1 = int(
            offsets[slave + 1]
        )

        local_coeffs = (
            coeffs[c0:c1]
        )

        must(
            len(local_coeffs) == 1,
            (
                f"periodic slave {slave} "
                "has exactly one coefficient"
            ),
        )

        max_coeff_error = max(
            max_coeff_error,
            abs(
                float(
                    local_coeffs[0]
                )
                - 1.0
            ),
        )

    overlap = sorted(
        slave_set
        & master_set
    )

    print()
    print("MPC scalar slave count:", len(slaves))
    print(
        "MPC unique master count:",
        len(master_set),
    )
    print(
        "MPC master-count range:",
        (
            min_master_count,
            max_master_count,
        ),
    )
    print(
        "Maximum coefficient error:",
        max_coeff_error,
    )
    print(
        "Slave/master overlap:",
        overlap,
    )

    must(
        len(slaves) > 0,
        "runtime periodic MPC has scalar slave DOFs",
    )

    must(
        len(slaves) % bs == 0,
        "runtime scalar slave count aligns with displacement block size",
    )

    must(
        len(
            {
                int(v) // bs
                for v in slaves
            }
        )
        * bs
        == len(slaves),
        "both displacement components are constrained for each periodic slave block",
    )

    must(
        overlap == [],
        "periodic MPC has zero slave/master chaining",
    )

    must(
        max_coeff_error <= 1.0e-12,
        "periodic coefficients equal one",
    )

    # --------------------------------------------------------
    # Reproduce deterministic MPC-independent gauge
    # --------------------------------------------------------

    coords = np.asarray(
        V.tabulate_dof_coordinates(),
        dtype=float,
    )

    occupied = (
        slave_set
        | master_set
    )

    candidates = []

    center = np.array(
        [
            0.5 * RVE_WIDTH,
            0.5 * RVE_HEIGHT,
        ],
        dtype=float,
    )

    for block, xyz in enumerate(coords):
        x = float(xyz[0])
        y = float(xyz[1])

        if not (
            0.10 * RVE_WIDTH
            < x
            < 0.90 * RVE_WIDTH
            and
            0.10 * RVE_HEIGHT
            < y
            < 0.90 * RVE_HEIGHT
        ):
            continue

        scalar_dofs = [
            block * bs,
            block * bs + 1,
        ]

        if any(
            dof in occupied
            for dof in scalar_dofs
        ):
            continue

        distance2 = float(
            np.sum(
                (
                    np.array([x, y])
                    - center
                ) ** 2
            )
        )

        candidates.append(
            (
                distance2,
                int(block),
                np.asarray(
                    xyz,
                    dtype=float,
                ),
                scalar_dofs,
            )
        )

    must(
        len(candidates) > 0,
        "strict-interior gauge candidate exists",
    )

    candidates.sort(
        key=lambda item: (
            item[0],
            item[1],
        )
    )

    (
        _,
        gauge_block,
        gauge_coord,
        gauge_dofs,
    ) = candidates[0]


    print()
    print(
        "INTERIOR_GAUGE_BLOCK=",
        gauge_block,
    )
    print(
        "INTERIOR_GAUGE_COORDINATE=",
        gauge_coord.tolist(),
    )
    print(
        "INTERIOR_GAUGE_SCALAR_DOFS=",
        gauge_dofs,
    )



    must(
        not (
            set(gauge_dofs)
            & slave_set
        ),
        "gauge intersects no MPC slave",
    )

    must(
        not (
            set(gauge_dofs)
            & master_set
        ),
        "gauge intersects no MPC master",
    )

    gauge_blocks = np.array(
        [gauge_block],
        dtype=np.int32,
    )

    gauge_value = np.zeros(
        2,
        dtype=PETSc.ScalarType,
    )

    bc_gauge = fem.dirichletbc(
        gauge_value,
        gauge_blocks,
        V,
    )

    bc_dofs, _ = (
        bc_gauge.dof_indices()
    )

    print(
        "Gauge Dirichlet scalar DOFs:",
        bc_dofs.tolist(),
    )

    must(
        set(
            int(v)
            for v in bc_dofs
        )
        == set(gauge_dofs),
        "Dirichlet gauge targets exactly both gauge components",
    )

    # --------------------------------------------------------
    # Material mechanics
    # --------------------------------------------------------

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

    print()
    print(
        "Matrix (mu, lambda_ps):",
        (
            matrix_mu,
            matrix_lambda_ps,
        ),
    )
    print(
        "Particle (mu, lambda_ps):",
        (
            particle_mu,
            particle_lambda_ps,
        ),
    )

    def epsilon(
        displacement,
    ):
        return ufl.sym(
            ufl.grad(
                displacement
            )
        )

    def sigma_from_strain(
        strain,
        mu: float,
        lambda_ps: float,
    ):
        return (
            2.0
            * mu
            * strain
            + lambda_ps
            * ufl.tr(strain)
            * ufl.Identity(2)
        )

    dx = ufl.Measure(
        "dx",
        domain=domain,
        subdomain_data=cell_tags,
    )

    # --------------------------------------------------------
    # Exact macroscopic X strain
    # --------------------------------------------------------

    E_bar = ufl.as_matrix(
        (
            (
                float(e_bar_numpy[0, 0]),
                float(e_bar_numpy[0, 1]),
            ),
            (
                float(e_bar_numpy[1, 0]),
                float(e_bar_numpy[1, 1]),
            ),
        )
    )

    print()
    print(
        f"MACROSCOPIC_STRAIN_CASE={load_case}"
    )
    print(
        "E_BAR=",
        e_bar_numpy.tolist(),
    )

    fluct_trial = ufl.TrialFunction(
        V
    )

    test = ufl.TestFunction(
        V
    )

    eps_trial = epsilon(
        fluct_trial
    )

    eps_test = epsilon(
        test
    )

    sigma_trial_matrix = (
        sigma_from_strain(
            eps_trial,
            matrix_mu,
            matrix_lambda_ps,
        )
    )

    sigma_trial_particle = (
        sigma_from_strain(
            eps_trial,
            particle_mu,
            particle_lambda_ps,
        )
    )

    sigma_macro_matrix = (
        sigma_from_strain(
            E_bar,
            matrix_mu,
            matrix_lambda_ps,
        )
    )

    sigma_macro_particle = (
        sigma_from_strain(
            E_bar,
            particle_mu,
            particle_lambda_ps,
        )
    )

    a = (
        ufl.inner(
            sigma_trial_matrix,
            eps_test,
        )
        * dx(matrix_tag)
        +
        ufl.inner(
            sigma_trial_particle,
            eps_test,
        )
        * dx(particle_tag)
    )

    L = (
        -ufl.inner(
            sigma_macro_matrix,
            eps_test,
        )
        * dx(matrix_tag)
        -
        ufl.inner(
            sigma_macro_particle,
            eps_test,
        )
        * dx(particle_tag)
    )

    # --------------------------------------------------------
    # Solve periodic fluctuation problem
    # --------------------------------------------------------

    print()
    print(
        "Solving heterogeneous PBC fluctuation problem..."
    )

    problem = dolfinx_mpc.LinearProblem(
        a,
        L,
        mpc,
        bcs=[
            bc_gauge,
        ],
        petsc_options_prefix=(
            "m8_periodized_particle_pbc_"
        ),
        petsc_options={
            "ksp_type": "preonly",
            "pc_type": "lu",
            "ksp_error_if_not_converged": True,
        },
    )

    fluctuation = problem.solve()

    fluctuation.x.scatter_forward()

    solver_reason = int(
        problem.solver.getConvergedReason()
    )

    solver_iterations = int(
        problem.solver.getIterationNumber()
    )

    print(
        "PETSc convergence reason:",
        solver_reason,
    )
    print(
        "PETSc iterations:",
        solver_iterations,
    )

    must(
        solver_reason > 0,
        "PETSc solver converged",
    )

    # --------------------------------------------------------
    # HARD GATE: actual constrained algebraic residual
    #
    # problem.x is the solved algebraic system vector.
    # fluctuation is the back-substituted FE field.
    # --------------------------------------------------------

    residual = problem.b.duplicate()

    problem.A.mult(
        problem.x,
        residual,
    )

    residual.axpy(
        PETSc.ScalarType(-1.0),
        problem.b,
    )

    residual_norm = float(
        residual.norm(
            PETSc.NormType.NORM_2
        )
    )

    rhs_norm = float(
        problem.b.norm(
            PETSc.NormType.NORM_2
        )
    )

    algebraic_relative_residual = (
        residual_norm
        / max(
            rhs_norm,
            1.0,
        )
    )

    print()
    print(
        "CONSTRAINED_ALGEBRAIC_RESIDUAL_NORM=",
        residual_norm,
    )
    print(
        "CONSTRAINED_RHS_NORM=",
        rhs_norm,
    )
    print(
        "CONSTRAINED_ALGEBRAIC_RELATIVE_RESIDUAL=",
        algebraic_relative_residual,
    )

    must(
        algebraic_relative_residual
        <= ALGEBRAIC_TOL,
        (
            "constrained algebraic equilibrium "
            "<= 1e-10"
        ),
    )

    residual.destroy()

    # --------------------------------------------------------
    # HARD GATE: gauge exact enforcement
    # --------------------------------------------------------

    solution_values = np.asarray(
        fluctuation.x.array,
        dtype=float,
    )

    gauge_values = np.array(
        [
            solution_values[
                gauge_block * bs
            ],
            solution_values[
                gauge_block * bs + 1
            ],
        ],
        dtype=float,
    )

    gauge_max_abs = float(
        np.max(
            np.abs(
                gauge_values
            )
        )
    )

    print()
    print(
        "GAUGE_VALUES=",
        gauge_values.tolist(),
    )
    print(
        "GAUGE_MAX_ABS=",
        gauge_max_abs,
    )

    must(
        gauge_max_abs
        <= GAUGE_TOL,
        "interior point gauge is exactly enforced",
    )

    # --------------------------------------------------------
    # HARD GATE: periodic fluctuation constraints
    # --------------------------------------------------------

    solution_coords = np.asarray(
        mpc.function_space.tabulate_dof_coordinates(),
        dtype=float,
    )

    periodic_block_count = 0
    periodic_max_abs = 0.0

    slave_block_set = {
        int(value) // bs
        for value in slaves
    }

    checked_periodic_blocks: set[int] = set()

    for block, xyz in enumerate(
        solution_coords
    ):
        x = float(xyz[0])
        y = float(xyz[1])

        is_right = np.isclose(
            x,
            RVE_WIDTH,
            atol=GEOM_TOL,
            rtol=0.0,
        )

        is_top = np.isclose(
            y,
            RVE_HEIGHT,
            atol=GEOM_TOL,
            rtol=0.0,
        )

        if is_right and is_top:
            target = np.array(
                [
                    0.0,
                    0.0,
                    0.0,
                ],
                dtype=float,
            )

        elif is_right:
            target = np.array(
                [
                    0.0,
                    y,
                    0.0,
                ],
                dtype=float,
            )

        elif is_top:
            target = np.array(
                [
                    x,
                    0.0,
                    0.0,
                ],
                dtype=float,
            )

        else:
            continue

        master_block = find_unique_block(
            solution_coords,
            target,
        )

        slave_value = np.array(
            [
                solution_values[
                    block * bs
                ],
                solution_values[
                    block * bs + 1
                ],
            ],
            dtype=float,
        )

        master_value = np.array(
            [
                solution_values[
                    master_block * bs
                ],
                solution_values[
                    master_block * bs + 1
                ],
            ],
            dtype=float,
        )

        mismatch = float(
            np.max(
                np.abs(
                    slave_value
                    - master_value
                )
            )
        )

        periodic_max_abs = max(
            periodic_max_abs,
            mismatch,
        )

        periodic_block_count += 1
        checked_periodic_blocks.add(
            int(block)
        )

    periodic_normalized_error = (
        periodic_max_abs
        / macro_amplitude
    )

    print()
    print(
        "PERIODIC_CHECKED_SLAVE_BLOCKS=",
        periodic_block_count,
    )
    print(
        "PERIODIC_FLUCTUATION_MAX_ABS_MISMATCH=",
        periodic_max_abs,
    )
    print(
        "PERIODIC_FLUCTUATION_NORMALIZED_ERROR=",
        periodic_normalized_error,
    )

    must(
        checked_periodic_blocks
        == slave_block_set,
        "post-solve periodic verification covers exactly all runtime MPC slave blocks",
    )

    must(
        periodic_block_count
        == len(slave_block_set),
        "all runtime periodic slave blocks were checked",
    )

    must(
        periodic_normalized_error
        <= PERIODIC_TOL,
        "periodic fluctuation mismatch <= 1e-8",
    )

    # --------------------------------------------------------
    # Area accounting in solved domain
    # --------------------------------------------------------

    matrix_area = mpi_sum(
        fem.assemble_scalar(
            fem.form(
                1.0
                * dx(matrix_tag)
            )
        )
    )

    particle_area = mpi_sum(
        fem.assemble_scalar(
            fem.form(
                1.0
                * dx(particle_tag)
            )
        )
    )

    gross_area = (
        RVE_WIDTH
        * RVE_HEIGHT
    )

    solid_area = (
        matrix_area
        + particle_area
    )

    print()
    print("Matrix area :", matrix_area)
    print("Particle area:", particle_area)
    print("Solid area  :", solid_area)
    print("Gross area  :", gross_area)

    must(
        abs(
            matrix_area
            - float(
                mesh_area_reference[
                    "areas"
                ][
                    "matrix"
                ]
            )
        )
        <= 1.0e-12,
        "integrated matrix area matches permanent mesh diagnostics",
    )

    must(
        abs(
            particle_area
            - float(
                mesh_area_reference[
                    "areas"
                ][
                    "particle"
                ]
            )
        )
        <= 1.0e-12,
        "integrated particle area matches permanent mesh diagnostics",
    )

    must(
        abs(
            solid_area
            - gross_area
        )
        <= 1.0e-12,
        "pristine solid area equals runtime gross RVE area",
    )

    # --------------------------------------------------------
    # Total strain / stress
    # --------------------------------------------------------

    eps_fluct = epsilon(
        fluctuation
    )

    eps_total = (
        eps_fluct
        + E_bar
    )

    sigma_matrix_total = (
        sigma_from_strain(
            eps_total,
            matrix_mu,
            matrix_lambda_ps,
        )
    )

    sigma_particle_total = (
        sigma_from_strain(
            eps_total,
            particle_mu,
            particle_lambda_ps,
        )
    )

    def integrate_both_phases(
        expression,
    ) -> float:
        return mpi_sum(
            fem.assemble_scalar(
                fem.form(
                    expression
                    * dx(matrix_tag)
                    +
                    expression
                    * dx(particle_tag)
                )
            )
        )

    def integrate_phase_stress(
        component_i: int,
        component_j: int,
    ) -> float:
        return mpi_sum(
            fem.assemble_scalar(
                fem.form(
                    sigma_matrix_total[
                        component_i,
                        component_j,
                    ]
                    * dx(matrix_tag)
                    +
                    sigma_particle_total[
                        component_i,
                        component_j,
                    ]
                    * dx(particle_tag)
                )
            )
        )

    avg_eps_11 = (
        integrate_both_phases(
            eps_total[0, 0]
        )
        / gross_area
    )

    avg_eps_22 = (
        integrate_both_phases(
            eps_total[1, 1]
        )
        / gross_area
    )

    avg_gamma_12 = (
        integrate_both_phases(
            2.0
            * eps_total[0, 1]
        )
        / gross_area
    )

    macro_strain_voigt = np.array(
        [
            avg_eps_11,
            avg_eps_22,
            avg_gamma_12,
        ],
        dtype=float,
    )

    # expected_macro_strain is defined from
    # the runtime X/Y/XY engineering-Voigt load case.

    macro_strain_error = float(
        np.max(
            np.abs(
                macro_strain_voigt
                - expected_macro_strain
            )
        )
    )

    print()
    print(
        "RECOVERED_MACRO_STRAIN_VOIGT=",
        macro_strain_voigt.tolist(),
    )
    print(
        "EXPECTED_MACRO_STRAIN_VOIGT=",
        expected_macro_strain.tolist(),
    )
    print(
        "MACRO_STRAIN_MAX_ABS_ERROR=",
        macro_strain_error,
    )

    must(
        macro_strain_error
        <= MACRO_STRAIN_TOL,
        "imposed macroscopic strain recovered <= 1e-8",
    )

    sigma_11 = (
        integrate_phase_stress(
            0,
            0,
        )
        / gross_area
    )

    sigma_22 = (
        integrate_phase_stress(
            1,
            1,
        )
        / gross_area
    )

    sigma_12 = (
        integrate_phase_stress(
            0,
            1,
        )
        / gross_area
    )

    Sigma = np.array(
        [
            [
                sigma_11,
                sigma_12,
            ],
            [
                sigma_12,
                sigma_22,
            ],
        ],
        dtype=float,
    )

    stress_voigt = np.array(
        [
            sigma_11,
            sigma_22,
            sigma_12,
        ],
        dtype=float,
    )

    stiffness_column = (
        stress_voigt
        / macro_amplitude
    )

    print()
    print(
        "MACROSCOPIC_STRESS_TENSOR=",
        Sigma.tolist(),
    )
    print(
        "MACROSCOPIC_STRESS_VOIGT=",
        stress_voigt.tolist(),
    )
    print(
        "PBC_STIFFNESS_COLUMN=",
        stiffness_column.tolist(),
    )
    print(
        "PBC_STIFFNESS_COLUMN_NORMALIZED_BY_E_MATRIX=",
        (
            stiffness_column
            / matrix_E
        ).tolist(),
    )

    must(
        np.all(
            np.isfinite(
                stress_voigt
            )
        ),
        "macroscopic stress is finite",
    )

    must(
        np.all(
            np.isfinite(
                stiffness_column
            )
        ),
        "PBC stiffness column is finite",
    )

    must(
        float(
            stiffness_column[
                positive_component_index
            ]
        )
        > 0.0,
        "load-direction stiffness candidate is positive",
    )

    # --------------------------------------------------------
    # HARD GATE: Hill-Mandel energetic consistency
    # --------------------------------------------------------

    micro_energy = (
        mpi_sum(
            fem.assemble_scalar(
                fem.form(
                    ufl.inner(
                        sigma_matrix_total,
                        eps_total,
                    )
                    * dx(matrix_tag)
                    +
                    ufl.inner(
                        sigma_particle_total,
                        eps_total,
                    )
                    * dx(particle_tag)
                )
            )
        )
        / gross_area
    )

    macro_energy = float(
        np.sum(
            Sigma
            * e_bar_numpy
        )
    )

    hill_mandel_relative = (
        abs(
            micro_energy
            - macro_energy
        )
        / max(
            abs(micro_energy),
            abs(macro_energy),
            1.0e-30,
        )
    )

    print()
    print(
        "MICRO_ENERGY_DENSITY=",
        micro_energy,
    )
    print(
        "MACRO_ENERGY_DENSITY=",
        macro_energy,
    )
    print(
        "HILL_MANDEL_RELATIVE_MISMATCH=",
        hill_mandel_relative,
    )

    must(
        hill_mandel_relative
        <= HILL_MANDEL_TOL,
        "Hill-Mandel relative mismatch <= 1e-5",
    )

    # --------------------------------------------------------
    # HARD GATE: weak-stationarity identity
    # ∫ sigma(total):epsilon(fluctuation) dA = 0
    # --------------------------------------------------------

    weak_identity = (
        mpi_sum(
            fem.assemble_scalar(
                fem.form(
                    ufl.inner(
                        sigma_matrix_total,
                        eps_fluct,
                    )
                    * dx(matrix_tag)
                    +
                    ufl.inner(
                        sigma_particle_total,
                        eps_fluct,
                    )
                    * dx(particle_tag)
                )
            )
        )
        / gross_area
    )

    weak_identity_error = (
        abs(
            weak_identity
        )
        / max(
            abs(micro_energy),
            abs(macro_energy),
            1.0,
        )
    )

    print()
    print(
        "WEAK_STATIONARITY_IDENTITY_VALUE=",
        weak_identity,
    )
    print(
        "WEAK_STATIONARITY_IDENTITY_ERROR=",
        weak_identity_error,
    )

    must(
        weak_identity_error
        <= WEAK_IDENTITY_TOL,
        "Hill-Mandel/weak-stationarity identity <= 1e-10",
    )

    # --------------------------------------------------------
    # Explicit finite-value audit
    # --------------------------------------------------------

    finite_values = [
        residual_norm,
        rhs_norm,
        algebraic_relative_residual,
        gauge_max_abs,
        periodic_max_abs,
        periodic_normalized_error,
        matrix_area,
        particle_area,
        solid_area,
        avg_eps_11,
        avg_eps_22,
        avg_gamma_12,
        macro_strain_error,
        sigma_11,
        sigma_22,
        sigma_12,
        micro_energy,
        macro_energy,
        hill_mandel_relative,
        weak_identity,
        weak_identity_error,
    ]

    must(
        all(
            math.isfinite(
                float(value)
            )
            for value
            in finite_values
        ),
        "all permanent M8 PBC numerical diagnostics are finite",
    )

    # --------------------------------------------------------
    # Record transient result
    #
    # Symmetry / positive-definiteness are intentionally
    # NOT evaluated from one stiffness column. They require
    # X/Y/XY completion.
    # --------------------------------------------------------

    output = {
        "schema": (
            "m8_periodized_particle_pbc_load_validation_v1"
        ),
        "status": "valid",
        "case": {
            "rve_level": (
                mesh_diag["provenance"]["rve_level"]
            ),
            "geometry_seed": (
                mesh_provenance[
                    "provenance"
                ][
                    "geometry_seed"
                ]
            ),
            "geometry_sha256": (
                mesh_provenance[
                    "provenance"
                ][
                    "geometry_sha256"
                ]
            ),
            "boundary_condition": "PBC",
            "load_case": load_case,
            "macroscopic_strain_voigt": (
                expected_macro_strain.tolist()
            ),
            "mesh_size": (
                mesh_provenance[
                    "provenance"
                ][
                    "mesh_size"
                ]
            ),
        },
        "model": {
            "dimension": 2,
            "assumption": "plane_stress",
            "interface": "perfect_bonding",
            "matrix": {
                "youngs_modulus": matrix_E,
                "poissons_ratio": matrix_nu,
            },
            "particle": {
                "youngs_modulus": particle_E,
                "poissons_ratio": particle_nu,
                "stiffness_ratio": (
                    particle_E
                    / matrix_E
                ),
            },
        },
        "mesh": {
            "cells": cell_count,
            "matrix_cells": matrix_cells,
            "particle_cells": particle_cells,
            "matrix_area": matrix_area,
            "particle_area": particle_area,
            "gross_area": gross_area,
        },
        "mpc": {
            "basis_cutoff_tolerance": MPC_TOL,
            "scalar_slave_dofs": (
                len(slaves)
            ),
            "unique_master_dofs": (
                len(master_set)
            ),
            "slave_master_overlap": overlap,
            "max_coefficient_error": (
                max_coeff_error
            ),
        },
        "gauge": {
            "block": gauge_block,
            "coordinate": (
                gauge_coord.tolist()
            ),
            "scalar_dofs": gauge_dofs,
            "values": (
                gauge_values.tolist()
            ),
            "max_abs": gauge_max_abs,
            "slave_overlap": [],
            "master_overlap": [],
        },
        "solver": {
            "convergence_reason": (
                solver_reason
            ),
            "iterations": (
                solver_iterations
            ),
            "algebraic_residual_norm": (
                residual_norm
            ),
            "rhs_norm": rhs_norm,
            "algebraic_relative_residual": (
                algebraic_relative_residual
            ),
        },
        "periodicity": {
            "checked_slave_blocks": (
                periodic_block_count
            ),
            "fluctuation_max_abs_mismatch": (
                periodic_max_abs
            ),
            "normalized_error": (
                periodic_normalized_error
            ),
        },
        "response": {
            "recovered_strain_voigt": (
                macro_strain_voigt.tolist()
            ),
            "macro_strain_max_abs_error": (
                macro_strain_error
            ),
            "stress_tensor": (
                Sigma.tolist()
            ),
            "stress_voigt": (
                stress_voigt.tolist()
            ),
            "stiffness_column": (
                stiffness_column.tolist()
            ),
            "x_stiffness_column_normalized": (
                (
                    stiffness_column
                    / matrix_E
                ).tolist()
            ),
        },
        "energy": {
            "micro_energy_density": (
                micro_energy
            ),
            "macro_energy_density": (
                macro_energy
            ),
            "hill_mandel_relative_mismatch": (
                hill_mandel_relative
            ),
            "weak_stationarity_value": (
                weak_identity
            ),
            "weak_stationarity_error": (
                weak_identity_error
            ),
        },
        "deferred_until_all_three_loads": {
            "homogenized_stiffness_symmetry": True,
            "positive_definiteness": True,
            "engineering_constants": True,
            "voigt_reuss_tensor_sanity": True,
        },
        "raw_sigma_h_n_is_hard_gate": False,
        "fem_solve_performed": True,
        "repository_files_created": (
            Path.cwd()
            in out_path.resolve().parents
        ),
    }

    out_path.write_text(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
    )

    print()
    print(
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )

    print()
    print(
        "PASS — permanent M8 periodized heterogeneous PBC load validation"
    )


if __name__ == "__main__":
    main()
