"""Solve one M9 Step-9 defective periodized true-hole PBC load case.

This source is lineage-adapted from the authenticated M8 defective PBC solver
while consuming the Step-9 single-state geometry and mesh-diagnostics schemas.
The validated periodic MPC, deterministic gauge, heterogeneous plane-stress FEM,
PETSc, homogenized-response, Hill-Mandel, and permanent src/26 quadrature-local
mechanisms are preserved. The permanent X-load path evaluates the locked local
metric at quadrature degree 8.

This is Step-9 transfer-validation code only. It does not own production design
IDs, production realization IDs, production pilot-sampling RNG, or raw-root
layout. Merely importing or statically compiling this source performs no solve.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
from pathlib import Path

import yaml


GEOMETRY_SCHEMA = "m9_step9_void_microstructure_v1"
MESH_SCHEMA = "m9_step9_void_mesh_diagnostics_v1"
PBC_LOAD_SCHEMA = "m9_step9_void_pbc_load_validation_v1"
STEP9_VALIDATION_SEED_NAMESPACE = (
    "composite-rve-m9-step9-transfer-validation-v1"
)
STEP9_ALLOWED_VOID_COUNTS = frozenset({1, 2, 4})
STEP9_PHYSICAL_PARTICLE_COUNT = 16
STEP9_RVE_LENGTH = 1.0
STEP9_MATRIX_E = 1000.0
STEP9_EP_OVER_EM_MIN = 2.0
STEP9_EP_OVER_EM_MAX = 30.0
STEP9_NU_MATRIX_MIN = 0.25
STEP9_NU_MATRIX_MAX = 0.40
STEP9_NU_PARTICLE_MIN = 0.15
STEP9_NU_PARTICLE_MAX = 0.30
STEP9_PRODUCTION_QUADRATURE_DEGREE = 8
STEP9_LOCAL_METRIC_ID = "m8_matrix_vm_annulus_quadrature_tail10_v1"

GEOM_TOL = 1.0e-10
MESH_AUDIT_TOL = 5.0e-3
MPC_TOL = 1.0e-12

EXPECTED_PHYSICAL_TAGS = {
    "matrix": 1,
    "particle": 2,
    "void_boundary": 3,
    "left": 11,
    "right": 12,
    "bottom": 13,
    "top": 14,
}
AUTHORITIES = {
    "M8_TARGET_MESH_PROTOCOL.md":
        "0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f",
    "src/22_solve_m8_periodized_pbc.py":
        "90079e56df7f2a74cac3b301e81cbaa0ea520ebcd1987f1ac7f81f4a6ee12e5b",
    "src/25_solve_m8_periodized_void_pbc.py":
        "b97f5add78d712dee1dc7564e6dce3f6cf08e7c1bee9562522e3344483e230dc",
    "src/26_m8_local_response.py":
        "d73423d4e41fdc686e8bfd0825c0bead0c82103ec423fceb91e8b60d001bbaae",
    "src/28_generate_m9_step9_void_microstructure.py":
        "20c2d56b734518bf6bf18f867652d562778290e146c47be961e3a416645af160",
    "src/29_generate_m9_step9_void_mesh.py":
        "15fce610f15b7e54eb81142b459788e83dab1079d56d8253bd6b942d9ea57a30",
}

def must(
    condition: bool,
    message: str,
) -> None:
    if condition:
        print(
            f"PASS — {message}"
        )
        return

    print(
        f"FAIL — DO NOT CONTINUE: {message}"
    )

    raise RuntimeError(
        message
    )


def sha256_file(
    path: Path,
) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def canonical_sha256(
    value: str,
    label: str,
) -> str:
    normalized = (
        value.strip().lower()
    )

    must(
        len(normalized) == 64
        and all(
            character
            in "0123456789abcdef"
            for character
            in normalized
        ),
        f"{label} is canonical SHA256 text",
    )

    return normalized


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate or solve one authenticated M9 Step-9 "
            "single-state defective true-hole PBC load case."
        )
    )

    parser.add_argument(
        "--mesh",
        type=Path,
        required=True,
        help=(
            "Authenticated Step-9 periodized true-hole "
            "Gmsh mesh from src/29."
        ),
    )

    parser.add_argument(
        "--expected-mesh-sha256",
        required=True,
    )

    parser.add_argument(
        "--mesh-diagnostics",
        type=Path,
        required=True,
        help=(
            "Authenticated m9_step9_void_mesh_"
            "diagnostics_v1 JSON from src/29."
        ),
    )

    parser.add_argument(
        "--expected-mesh-diagnostics-sha256",
        required=True,
    )

    parser.add_argument(
        "--geometry-json",
        type=Path,
        required=True,
        help=(
            "Authenticated single-state defective "
            "Step-9 geometry JSON from src/28."
        ),
    )

    parser.add_argument(
        "--expected-geometry-sha256",
        required=True,
    )

    parser.add_argument(
        "--config",
        type=Path,
        default=Path(
            "configs/03_parametric_rve_base.yaml"
        ),
    )

    parser.add_argument(
        "--load-case",
        required=True,
        choices=[
            "X",
            "Y",
            "XY",
        ],
    )

    parser.add_argument(
        "--macro-amplitude",
        type=float,
        default=0.01,
    )

    parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help=(
            "Permanent Step-9 per-load validation JSON path. "
            "Preflight-only modes never write it."
        ),
    )

    parser.add_argument(
        "--mpc-preflight-only",
        action="store_true",
        help=(
            "Import the authenticated true-hole mesh in the isolated "
            "DOLFINx-MPC environment, construct and authenticate the "
            "periodic MPC topology and deterministic interior gauge "
            "candidate, but do not assemble or solve FEM."
        ),
    )

    parser.add_argument(
        "--gauge-preflight-only",
        action="store_true",
        help=(
            "Construct and authenticate the deterministic zero-displacement "
            "interior gauge Dirichlet BC after the periodic MPC topology, "
            "without creating UFL forms, assembling, or solving FEM."
        ),
    )

    parser.add_argument(
        "--form-preflight-only",
        action="store_true",
        help=(
            "Reconstruct the authenticated periodic MPC and gauge, "
            "create and compile the heterogeneous plane-stress UFL "
            "bilinear/linear forms for the requested X/Y/XY load, "
            "but do not assemble or solve FEM."
        ),
    )

    parser.add_argument(
        "--linear-problem-preflight-only",
        action="store_true",
        help=(
            "Reconstruct the authenticated MPC, gauge and heterogeneous "
            "UFL forms, then construct the MPC-aware LinearProblem and "
            "audit its PETSc algebraic structures without calling solve()."
        ),
    )

    parser.add_argument(
        "--solve-preflight-only",
        action="store_true",
        help=(
            "Reconstruct the authenticated MPC, deterministic gauge, "
            "heterogeneous plane-stress forms and MPC-aware LinearProblem, "
            "then perform exactly one requested-load solve and audit only the "
            "solution/algebraic/periodic constraints. No stress recovery, "
            "homogenization, tensor reconstruction or output write occurs."
        ),
    )

    parser.add_argument(
        "--response-preflight-only",
        action="store_true",
        help=(
            "Reconstruct and solve the authenticated requested-load true-hole "
            "PBC system, then evaluate discrete phase areas, homogenized "
            "stress, the single X stiffness column, Hill-Mandel consistency "
            "and weak stationarity without writing the permanent output."
        ),
    )

    parser.add_argument(
        "--cell-local-preflight-only",
        action="store_true",
        help=(
            "Reconstruct and solve exactly one authenticated X-load "
            "true-hole PBC system, evaluate the existing homogenized "
            "response, then extract only the M8 matrix-cell local "
            "response using permanent src/26. No permanent output "
            "is written."
        ),
    )

    parser.add_argument(
        "--quadrature-local-preflight-only",
        action="store_true",
        help=(
            "Solve exactly one authenticated X-load true-hole PBC system, "
            "evaluate the existing response, then extract the M8 matrix "
            "quadrature local response using permanent src/26. An explicit "
            "--quadrature-degree is required. No permanent output is written."
        ),
    )
    parser.add_argument(
        "--quadrature-degree",
        type=int,
        default=None,
        help=(
            "Explicit validation degree for --quadrature-local-preflight-only; "
            "None otherwise. Permanent Step-9 X-load output uses degree 8."
        ),
    )

    return parser.parse_args()



def plane_stress_constants(
    young: float,
    poisson: float,
) -> tuple[float, float]:
    """Return shear modulus and effective plane-stress Lamé parameter."""

    must(
        math.isfinite(
            young
        )
        and young > 0.0,
        "plane-stress Young's modulus is finite and positive",
    )

    must(
        math.isfinite(
            poisson
        )
        and -1.0 < poisson < 0.5,
        "plane-stress Poisson ratio is physically admissible",
    )

    mu = (
        young
        / (
            2.0
            * (
                1.0
                + poisson
            )
        )
    )

    lambda_3d = (
        young
        * poisson
        / (
            (
                1.0
                + poisson
            )
            * (
                1.0
                - 2.0
                * poisson
            )
        )
    )

    lambda_ps = (
        2.0
        * mu
        * lambda_3d
        / (
            lambda_3d
            + 2.0
            * mu
        )
    )

    must(
        math.isfinite(
            mu
        )
        and mu > 0.0,
        "plane-stress shear modulus is finite and positive",
    )

    must(
        math.isfinite(
            lambda_ps
        ),
        "effective plane-stress Lamé parameter is finite",
    )

    return (
        float(
            mu
        ),
        float(
            lambda_ps
        ),
    )


def run_mpc_topology_preflight(
    mesh_path: Path,
    mesh_diag: dict,
    width: float,
    height: float,
    create_gauge_bc: bool = False,
    create_forms: bool = False,
    create_linear_problem: bool = False,
    solve_problem: bool = False,
    evaluate_response: bool = False,
    load_case: str | None = None,
    macro_amplitude: float | None = None,
    matrix_E: float | None = None,
    matrix_nu: float | None = None,
    particle_E: float | None = None,
    particle_nu: float | None = None,
    evaluate_local_response: bool = False,
    physical_voids: list[dict] | None = None,
    evaluate_quadrature_local_response: bool = False,
    quadrature_degree: int | None = None,
) -> dict:
    """Authenticate DOLFINx import and periodic MPC topology only.

    Imports are deliberately lazy so the input-contract-only path remains
    runnable inside the protected composite-sim environment, where
    dolfinx_mpc must remain absent.
    """

    import numpy as np
    from mpi4py import MPI

    import dolfinx
    import dolfinx_mpc
    from dolfinx import fem, mesh
    from dolfinx.io import gmsh as gmshio

    if evaluate_local_response:
        must(
            evaluate_response,
            "cell-local extraction requires authenticated response evaluation",
        )
        must(
            load_case == "X",
            "cell-local extraction is restricted to the M8 X PBC load",
        )
        must(
            isinstance(
                physical_voids,
                list,
            ),
            "cell-local extraction received the selected physical-void list",
        )

    if evaluate_quadrature_local_response:
        must(evaluate_response, "quadrature-local extraction requires response evaluation")
        must(load_case == "X", "quadrature-local extraction is restricted to X load")
        must(isinstance(physical_voids, list), "quadrature-local extraction received physical voids")
        must(
            isinstance(quadrature_degree, int)
            and not isinstance(quadrature_degree, bool)
            and 1 <= quadrature_degree <= 8,
            "quadrature-local extraction requires explicit validation degree 1..8",
        )

    must(
        dolfinx.__version__ == "0.11.0",
        "MPC preflight uses DOLFINx 0.11.0",
    )

    must(
        MPI.COMM_WORLD.size == 1,
        "MPC preflight remains single-rank",
    )

    must(
        hasattr(
            dolfinx_mpc,
            "MultiPointConstraint",
        ),
        "dolfinx_mpc MultiPointConstraint API is available",
    )

    print()
    print(
        "Importing authenticated periodized true-hole mesh "
        "for MPC-topology preflight..."
    )

    mesh_data = gmshio.read_from_msh(
        mesh_path,
        MPI.COMM_WORLD,
        rank=0,
        gdim=2,
    )

    domain = mesh_data.mesh
    cell_tags = mesh_data.cell_tags
    facet_tags = mesh_data.facet_tags

    must(
        cell_tags is not None,
        "MPC preflight imported material cell tags",
    )

    must(
        facet_tags is not None,
        "MPC preflight imported boundary facet tags",
    )

    physical_groups = {
        str(name): (
            int(group.dim),
            int(group.tag),
        )
        for name, group
        in mesh_data.physical_groups.items()
    }

    expected_groups = {
        "matrix": (2, 1),
        "particle": (2, 2),
        "void_boundary": (1, 3),
        "left": (1, 11),
        "right": (1, 12),
        "bottom": (1, 13),
        "top": (1, 14),
    }

    must(
        physical_groups == expected_groups,
        "DOLFINx named physical groups are exact",
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
            cell_tags.values == 1
        )
    )

    particle_cells = int(
        np.count_nonzero(
            cell_tags.values == 2
        )
    )

    cell_values = {
        int(v)
        for v in np.unique(
            cell_tags.values
        )
    }

    facet_values = {
        int(v)
        for v in np.unique(
            facet_tags.values
        )
    }

    print()
    print(
        "DOLFINx cell count =",
        cell_count,
    )

    print(
        "DOLFINx matrix cells =",
        matrix_cells,
    )

    print(
        "DOLFINx particle cells =",
        particle_cells,
    )

    print(
        "DOLFINx cell-tag values =",
        sorted(
            cell_values
        ),
    )

    print(
        "DOLFINx facet-tag values =",
        sorted(
            facet_values
        ),
    )

    must(
        cell_count
        == int(
            mesh_diag[
                "mesh"
            ][
                "cell_count"
            ]
        ),
        "DOLFINx cell count matches authenticated mesh diagnostics",
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
        "DOLFINx matrix-cell count matches mesh diagnostics",
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
        "DOLFINx particle-cell count matches mesh diagnostics",
    )

    must(
        len(
            cell_tags.indices
        )
        == cell_count,
        "every DOLFINx cell has a material tag",
    )

    must(
        cell_values == {1, 2},
        "only matrix and particle material-cell tags are present",
    )

    must(
        facet_values
        == {
            3,
            11,
            12,
            13,
            14,
        },
        (
            "only void-boundary and four external "
            "facet tags are present"
        ),
    )

    # --------------------------------------------------------
    # P1 vector fluctuation space.
    # --------------------------------------------------------

    V = fem.functionspace(
        domain,
        (
            "Lagrange",
            1,
            (2,),
        ),
    )

    bs = int(
        V.dofmap.bs
    )

    must(
        bs == 2,
        "P1 fluctuation space has exactly two displacement components",
    )

    # --------------------------------------------------------
    # Same protected periodic topology as src/22.
    # The true holes are interior/periodized geometric boundaries and
    # receive no displacement Dirichlet condition.
    # --------------------------------------------------------

    def right_except_top_right(
        x: np.ndarray,
    ) -> np.ndarray:
        return np.logical_and(
            np.isclose(
                x[0],
                width,
                atol=GEOM_TOL,
                rtol=0.0,
            ),
            ~np.isclose(
                x[1],
                height,
                atol=GEOM_TOL,
                rtol=0.0,
            ),
        )

    def right_to_left(
        x: np.ndarray,
    ) -> np.ndarray:
        out = np.array(
            x,
            copy=True,
        )

        out[0] -= width

        return out

    def top_except_top_right(
        x: np.ndarray,
    ) -> np.ndarray:
        return np.logical_and(
            np.isclose(
                x[1],
                height,
                atol=GEOM_TOL,
                rtol=0.0,
            ),
            ~np.isclose(
                x[0],
                width,
                atol=GEOM_TOL,
                rtol=0.0,
            ),
        )

    def top_to_bottom(
        x: np.ndarray,
    ) -> np.ndarray:
        out = np.array(
            x,
            copy=True,
        )

        out[1] -= height

        return out

    def top_right_only(
        x: np.ndarray,
    ) -> np.ndarray:
        return np.logical_and(
            np.isclose(
                x[0],
                width,
                atol=GEOM_TOL,
                rtol=0.0,
            ),
            np.isclose(
                x[1],
                height,
                atol=GEOM_TOL,
                rtol=0.0,
            ),
        )

    def top_right_to_bottom_left(
        x: np.ndarray,
    ) -> np.ndarray:
        out = np.array(
            x,
            copy=True,
        )

        out[0] -= width
        out[1] -= height

        return out

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
        int(value)
        for value in slaves
    }

    must(
        len(slaves) > 0,
        "periodic MPC contains scalar slave DOFs",
    )

    must(
        len(slaves) % bs == 0,
        "periodic scalar slave count aligns with vector block size",
    )

    slave_blocks = {
        int(value) // bs
        for value in slaves
    }

    must(
        len(
            slave_blocks
        )
        * bs
        == len(
            slaves
        ),
        (
            "both displacement components are constrained "
            "for every periodic slave block"
        ),
    )

    expected_slave_blocks = (
        int(
            mesh_diag[
                "mesh"
            ][
                "right_node_count"
            ]
        )
        + int(
            mesh_diag[
                "mesh"
            ][
                "top_node_count"
            ]
        )
        - 1
    )

    must(
        len(
            slave_blocks
        )
        == expected_slave_blocks,
        (
            "periodic slave-block count matches "
            "right+top boundary-node topology"
        ),
    )

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

    master_set: set[int] = set()

    max_coefficient_error = 0.0
    min_master_count = 10**9
    max_master_count = 0
    component_mismatch_count = 0
    mapping_max_error = 0.0

    coordinates = np.asarray(
        V.tabulate_dof_coordinates(),
        dtype=float,
    )

    allowed_translations = (
        np.array(
            [
                width,
                0.0,
            ],
            dtype=float,
        ),
        np.array(
            [
                0.0,
                height,
            ],
            dtype=float,
        ),
        np.array(
            [
                width,
                height,
            ],
            dtype=float,
        ),
    )

    for slave in slaves:
        slave = int(
            slave
        )

        masters = np.asarray(
            mpc.masters.links(
                slave
            ),
            dtype=np.int64,
        )

        master_count = int(
            len(
                masters
            )
        )

        min_master_count = min(
            min_master_count,
            master_count,
        )

        max_master_count = max(
            max_master_count,
            master_count,
        )

        must(
            master_count == 1,
            (
                f"periodic slave {slave} "
                "has exactly one master"
            ),
        )

        master = int(
            masters[0]
        )

        master_set.add(
            master
        )

        if (
            slave % bs
            != master % bs
        ):
            component_mismatch_count += 1

        c0 = int(
            offsets[
                slave
            ]
        )

        c1 = int(
            offsets[
                slave + 1
            ]
        )

        local_coeffs = coeffs[
            c0:c1
        ]

        must(
            len(
                local_coeffs
            )
            == 1,
            (
                f"periodic slave {slave} "
                "has exactly one coefficient"
            ),
        )

        max_coefficient_error = max(
            max_coefficient_error,
            abs(
                float(
                    local_coeffs[0]
                )
                - 1.0
            ),
        )

        slave_block = (
            slave // bs
        )

        master_block = (
            master // bs
        )

        delta = (
            coordinates[
                slave_block
            ][:2]
            - coordinates[
                master_block
            ][:2]
        )

        translation_error = min(
            float(
                np.max(
                    np.abs(
                        delta
                        - translation
                    )
                )
            )
            for translation
            in allowed_translations
        )

        mapping_max_error = max(
            mapping_max_error,
            translation_error,
        )

    overlap = sorted(
        slave_set
        & master_set
    )

    print()
    print(
        "MPC scalar slave count =",
        len(
            slaves
        ),
    )

    print(
        "MPC periodic slave-block count =",
        len(
            slave_blocks
        ),
    )

    print(
        "Expected periodic slave-block count =",
        expected_slave_blocks,
    )

    print(
        "MPC unique master count =",
        len(
            master_set
        ),
    )

    print(
        "MPC master-count range =",
        (
            min_master_count,
            max_master_count,
        ),
    )

    print(
        "MPC maximum coefficient error =",
        max_coefficient_error,
    )

    print(
        "MPC component mismatch count =",
        component_mismatch_count,
    )

    print(
        "MPC slave/master overlap =",
        overlap,
    )

    print(
        "MPC maximum geometric translation error =",
        mapping_max_error,
    )

    must(
        min_master_count == 1
        and max_master_count == 1,
        "every periodic slave has exactly one master",
    )

    must(
        max_coefficient_error
        <= MPC_TOL,
        "all periodic MPC coefficients equal one",
    )

    must(
        component_mismatch_count == 0,
        "periodic MPC preserves displacement component identity",
    )

    must(
        overlap == [],
        "periodic MPC has zero slave/master chaining",
    )

    must(
        mapping_max_error
        <= GEOM_TOL,
        "periodic MPC master/slave coordinates satisfy translation maps",
    )

    # --------------------------------------------------------
    # Deterministic interior gauge candidate only.
    # Do not create the Dirichlet BC yet.
    # --------------------------------------------------------

    occupied = (
        slave_set
        | master_set
    )

    center = np.array(
        [
            0.5 * width,
            0.5 * height,
        ],
        dtype=float,
    )

    candidates = []

    for block, xyz in enumerate(
        coordinates
    ):
        x = float(
            xyz[0]
        )

        y = float(
            xyz[1]
        )

        if not (
            0.10 * width
            < x
            < 0.90 * width
            and
            0.10 * height
            < y
            < 0.90 * height
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
                    np.asarray(
                        [
                            x,
                            y,
                        ],
                        dtype=float,
                    )
                    - center
                )
                ** 2
            )
        )

        candidates.append(
            (
                distance2,
                int(
                    block
                ),
                np.asarray(
                    xyz,
                    dtype=float,
                ),
                scalar_dofs,
            )
        )

    must(
        len(
            candidates
        )
        > 0,
        "strict-interior MPC-independent gauge candidate exists",
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
        gauge_coordinate,
        gauge_dofs,
    ) = candidates[0]

    must(
        not (
            set(
                gauge_dofs
            )
            & slave_set
        ),
        "gauge candidate intersects no MPC slave",
    )

    must(
        not (
            set(
                gauge_dofs
            )
            & master_set
        ),
        "gauge candidate intersects no MPC master",
    )

    print()
    print(
        "MPC_PREFLIGHT_GAUGE_BLOCK=",
        gauge_block,
    )

    print(
        "MPC_PREFLIGHT_GAUGE_COORDINATE=",
        gauge_coordinate.tolist(),
    )

    print(
        "MPC_PREFLIGHT_GAUGE_SCALAR_DOFS=",
        gauge_dofs,
    )

    gauge_bc_created = False
    gauge_bc_scalar_dofs: list[int] = []

    if create_gauge_bc:
        from petsc4py import PETSc

        gauge_blocks = np.array(
            [
                gauge_block,
            ],
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

        gauge_bc_scalar_dofs = [
            int(value)
            for value in np.asarray(
                bc_dofs,
                dtype=np.int64,
            )
        ]

        print()
        print(
            "GAUGE_PREFLIGHT_DIRICHLET_SCALAR_DOFS=",
            gauge_bc_scalar_dofs,
        )

        print(
            "GAUGE_PREFLIGHT_VALUE=",
            [
                0.0,
                0.0,
            ],
        )

        must(
            len(
                gauge_bc_scalar_dofs
            )
            == 2,
            "Dirichlet gauge contains exactly two scalar DOFs",
        )

        must(
            set(
                gauge_bc_scalar_dofs
            )
            == set(
                gauge_dofs
            ),
            "Dirichlet gauge targets exactly the deterministic gauge components",
        )

        must(
            not (
                set(
                    gauge_bc_scalar_dofs
                )
                & slave_set
            ),
            "Dirichlet gauge intersects no MPC slave",
        )

        must(
            not (
                set(
                    gauge_bc_scalar_dofs
                )
                & master_set
            ),
            "Dirichlet gauge intersects no MPC master",
        )

        must(
            np.all(
                np.asarray(
                    gauge_value,
                    dtype=float,
                )
                == 0.0
            ),
            "Dirichlet gauge value is exactly zero in both components",
        )

        gauge_bc_created = True

    forms_created = False
    forms_compiled = False
    linear_problem_created = False
    linear_problem_matrix_size: list[int] = []
    linear_problem_rhs_size = 0
    linear_problem_solution_size = 0
    linear_problem_solver_type = ""
    linear_problem_pc_type = ""
    linear_problem_options_prefix = ""
    system_assembled = False
    bilinear_argument_count = 0
    linear_argument_count = 0
    bilinear_cell_subdomain_ids: list[int] = []
    linear_cell_subdomain_ids: list[int] = []
    matrix_mu = math.nan
    matrix_lambda_ps = math.nan
    particle_mu = math.nan
    particle_lambda_ps = math.nan
    macro_strain_matrix: list[list[float]] = []
    macro_strain_voigt: list[float] = []

    if create_forms:
        must(
            create_gauge_bc,
            "UFL-form preflight requires the authenticated gauge-BC layer",
        )

        must(
            load_case
            in {
                "X",
                "Y",
                "XY",
            },
            "UFL-form preflight load case belongs to X/Y/XY",
        )

        must(
            macro_amplitude is not None
            and math.isfinite(
                float(
                    macro_amplitude
                )
            )
            and float(
                macro_amplitude
            )
            > 0.0,
            "UFL-form preflight macro amplitude is finite and positive",
        )

        for value, label in (
            (
                matrix_E,
                "matrix Young's modulus",
            ),
            (
                matrix_nu,
                "matrix Poisson ratio",
            ),
            (
                particle_E,
                "particle Young's modulus",
            ),
            (
                particle_nu,
                "particle Poisson ratio",
            ),
        ):
            must(
                value is not None,
                f"UFL-form preflight received {label}",
            )

        import ufl

        matrix_mu, matrix_lambda_ps = (
            plane_stress_constants(
                float(
                    matrix_E
                ),
                float(
                    matrix_nu
                ),
            )
        )

        particle_mu, particle_lambda_ps = (
            plane_stress_constants(
                float(
                    particle_E
                ),
                float(
                    particle_nu
                ),
            )
        )

        amplitude = float(
            macro_amplitude
        )

        if load_case == "X":
            e_bar_numpy = np.array(
                [
                    [
                        amplitude,
                        0.0,
                    ],
                    [
                        0.0,
                        0.0,
                    ],
                ],
                dtype=float,
            )

            expected_macro_strain = np.array(
                [
                    amplitude,
                    0.0,
                    0.0,
                ],
                dtype=float,
            )

        elif load_case == "Y":
            e_bar_numpy = np.array(
                [
                    [
                        0.0,
                        0.0,
                    ],
                    [
                        0.0,
                        amplitude,
                    ],
                ],
                dtype=float,
            )

            expected_macro_strain = np.array(
                [
                    0.0,
                    amplitude,
                    0.0,
                ],
                dtype=float,
            )

        else:
            e_bar_numpy = np.array(
                [
                    [
                        0.0,
                        0.5
                        * amplitude,
                    ],
                    [
                        0.5
                        * amplitude,
                        0.0,
                    ],
                ],
                dtype=float,
            )

            expected_macro_strain = np.array(
                [
                    0.0,
                    0.0,
                    amplitude,
                ],
                dtype=float,
            )

        macro_strain_matrix = (
            e_bar_numpy.tolist()
        )

        macro_strain_voigt = (
            expected_macro_strain.tolist()
        )

        print()
        print(
            "FORM_PREFLIGHT_MATRIX_MU=",
            matrix_mu,
        )

        print(
            "FORM_PREFLIGHT_MATRIX_LAMBDA_PS=",
            matrix_lambda_ps,
        )

        print(
            "FORM_PREFLIGHT_PARTICLE_MU=",
            particle_mu,
        )

        print(
            "FORM_PREFLIGHT_PARTICLE_LAMBDA_PS=",
            particle_lambda_ps,
        )

        print(
            "FORM_PREFLIGHT_MACRO_STRAIN_CASE=",
            load_case,
        )

        print(
            "FORM_PREFLIGHT_MACRO_STRAIN_MATRIX=",
            macro_strain_matrix,
        )

        print(
            "FORM_PREFLIGHT_MACRO_STRAIN_VOIGT=",
            macro_strain_voigt,
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
                * ufl.tr(
                    strain
                )
                * ufl.Identity(
                    2
                )
            )

        matrix_tag = 1
        particle_tag = 2

        dx = ufl.Measure(
            "dx",
            domain=domain,
            subdomain_data=cell_tags,
        )

        E_bar = ufl.as_matrix(
            (
                (
                    float(
                        e_bar_numpy[
                            0,
                            0,
                        ]
                    ),
                    float(
                        e_bar_numpy[
                            0,
                            1,
                        ]
                    ),
                ),
                (
                    float(
                        e_bar_numpy[
                            1,
                            0,
                        ]
                    ),
                    float(
                        e_bar_numpy[
                            1,
                            1,
                        ]
                    ),
                ),
            )
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
            * dx(
                matrix_tag
            )
            +
            ufl.inner(
                sigma_trial_particle,
                eps_test,
            )
            * dx(
                particle_tag
            )
        )

        L = (
            -ufl.inner(
                sigma_macro_matrix,
                eps_test,
            )
            * dx(
                matrix_tag
            )
            -
            ufl.inner(
                sigma_macro_particle,
                eps_test,
            )
            * dx(
                particle_tag
            )
        )

        bilinear_argument_count = len(
            a.arguments()
        )

        linear_argument_count = len(
            L.arguments()
        )

        must(
            bilinear_argument_count
            == 2,
            "heterogeneous bilinear UFL form has exactly two arguments",
        )

        must(
            linear_argument_count
            == 1,
            "heterogeneous linear UFL form has exactly one argument",
        )

        def cell_subdomain_ids(
            form,
        ) -> list[int]:
            ids: list[int] = []

            for integral in form.integrals():
                must(
                    integral.integral_type()
                    == "cell",
                    "UFL mechanics preflight contains only cell integrals",
                )

                subdomain_id = (
                    integral.subdomain_id()
                )

                if isinstance(
                    subdomain_id,
                    tuple,
                ):
                    ids.extend(
                        int(
                            value
                        )
                        for value
                        in subdomain_id
                    )
                else:
                    ids.append(
                        int(
                            subdomain_id
                        )
                    )

            return sorted(
                set(
                    ids
                )
            )

        bilinear_cell_subdomain_ids = (
            cell_subdomain_ids(
                a
            )
        )

        linear_cell_subdomain_ids = (
            cell_subdomain_ids(
                L
            )
        )

        print(
            "FORM_PREFLIGHT_BILINEAR_CELL_SUBDOMAIN_IDS=",
            bilinear_cell_subdomain_ids,
        )

        print(
            "FORM_PREFLIGHT_LINEAR_CELL_SUBDOMAIN_IDS=",
            linear_cell_subdomain_ids,
        )

        must(
            bilinear_cell_subdomain_ids
            == [
                1,
                2,
            ],
            "bilinear mechanics integrates matrix and particle only",
        )

        must(
            linear_cell_subdomain_ids
            == [
                1,
                2,
            ],
            "linear mechanics integrates matrix and particle only",
        )

        must(
            3
            not in bilinear_cell_subdomain_ids
            and 3
            not in linear_cell_subdomain_ids,
            "void-boundary physical tag is absent from volume mechanics",
        )

        # Compile only. No matrix/vector assembly and no solve.
        compiled_a = fem.form(
            a
        )

        compiled_L = fem.form(
            L
        )

        must(
            compiled_a is not None,
            "DOLFINx bilinear form compilation succeeded",
        )

        must(
            compiled_L is not None,
            "DOLFINx linear form compilation succeeded",
        )

        forms_created = True
        forms_compiled = True

    fem_solve_performed = False
    solve_petsc_convergence_reason = None
    solve_petsc_iterations = None
    solve_algebraic_residual_norm = None
    solve_rhs_norm = None
    solve_algebraic_relative_residual = None
    solve_fluctuation_dof_count = 0
    solve_fluctuation_linf = None
    solve_gauge_max_abs = None
    solve_periodic_max_abs_error = None
    solve_periodic_reference_scale = None
    solve_periodic_normalized_error = None

    if create_linear_problem:
        must(
            create_forms,
            "LinearProblem preflight requires compiled heterogeneous forms",
        )

        must(
            create_gauge_bc,
            "LinearProblem preflight requires the authenticated gauge BC",
        )

        linear_problem_options_prefix = (
            "m8_periodized_void_pbc_"
        )

        problem = dolfinx_mpc.LinearProblem(
            a,
            L,
            mpc,
            bcs=[
                bc_gauge,
            ],
            petsc_options_prefix=(
                linear_problem_options_prefix
            ),
            petsc_options={
                "ksp_type": "preonly",
                "pc_type": "lu",
                "ksp_error_if_not_converged": True,
            },
        )

        must(
            problem.A is not None,
            "LinearProblem created an MPC-compatible PETSc matrix structure",
        )

        must(
            problem.b is not None,
            "LinearProblem created an MPC-compatible PETSc RHS vector structure",
        )

        must(
            problem.x is not None,
            "LinearProblem created an MPC-compatible PETSc solution vector structure",
        )

        must(
            problem.solver is not None,
            "LinearProblem created a PETSc KSP object",
        )

        matrix_size = tuple(
            int(value)
            for value in problem.A.getSize()
        )

        rhs_size = int(
            problem.b.getSize()
        )

        solution_size = int(
            problem.x.getSize()
        )

        must(
            len(
                matrix_size
            )
            == 2
            and matrix_size[0] > 0
            and matrix_size[1] > 0,
            "LinearProblem matrix structure has positive dimensions",
        )

        must(
            matrix_size[0]
            == matrix_size[1],
            "LinearProblem matrix structure is square",
        )

        must(
            rhs_size
            == matrix_size[0],
            "LinearProblem RHS size matches matrix row dimension",
        )

        must(
            solution_size
            == matrix_size[1],
            "LinearProblem solution-vector size matches matrix column dimension",
        )

        linear_problem_matrix_size = [
            matrix_size[0],
            matrix_size[1],
        ]

        linear_problem_rhs_size = rhs_size
        linear_problem_solution_size = solution_size

        linear_problem_solver_type = str(
            problem.solver.getType()
        )

        pc = problem.solver.getPC()

        linear_problem_pc_type = str(
            pc.getType()
        )

        must(
            linear_problem_solver_type
            == "preonly",
            "LinearProblem KSP type is locked to preonly",
        )

        must(
            linear_problem_pc_type
            == "lu",
            "LinearProblem PC type is locked to LU",
        )

        must(
            problem.solver.getOptionsPrefix()
            == linear_problem_options_prefix,
            "LinearProblem PETSc options prefix is dedicated to void-capable PBC",
        )

        print()
        print(
            "LINEAR_PROBLEM_PREFLIGHT_MATRIX_SIZE=",
            linear_problem_matrix_size,
        )

        print(
            "LINEAR_PROBLEM_PREFLIGHT_RHS_SIZE=",
            linear_problem_rhs_size,
        )

        print(
            "LINEAR_PROBLEM_PREFLIGHT_SOLUTION_SIZE=",
            linear_problem_solution_size,
        )

        print(
            "LINEAR_PROBLEM_PREFLIGHT_KSP_TYPE=",
            linear_problem_solver_type,
        )

        print(
            "LINEAR_PROBLEM_PREFLIGHT_PC_TYPE=",
            linear_problem_pc_type,
        )

        print(
            "LINEAR_PROBLEM_PREFLIGHT_OPTIONS_PREFIX=",
            linear_problem_options_prefix,
        )

        linear_problem_created = True

        # Important: LinearProblem.solve() is deliberately not called here.
        # In DOLFINx-MPC, actual matrix/vector assembly occurs in solve().
        system_assembled = False

    response_evaluated = False

    response_runtime_matrix_area = None
    response_runtime_particle_area = None
    response_runtime_material_area = None
    response_runtime_void_area = None

    response_stress_tensor = []
    response_stress_voigt = []
    response_stiffness_column = []
    response_stiffness_column_normalized = []
    response_positive_component_index = None

    response_micro_energy_density = None
    response_macro_energy_density = None
    response_hill_mandel_relative_mismatch = None

    response_weak_stationarity_value = None
    response_weak_stationarity_relative = None

    local_response_evaluated = False
    local_response = None
    local_response_matrix_owned_cell_count = 0
    local_response_matrix_area_from_cells = None
    quadrature_local_response_evaluated = False
    quadrature_local_response = None
    quadrature_local_degree = None
    quadrature_local_reference_point_count = 0
    quadrature_local_matrix_owned_cell_count = 0
    quadrature_local_contribution_count = 0
    quadrature_local_matrix_area_from_weights = None

    if solve_problem:
        from petsc4py import PETSc

        must(
            create_linear_problem,
            "solve preflight requires the authenticated LinearProblem layer",
        )

        must(
            create_forms,
            "solve preflight requires compiled heterogeneous forms",
        )

        must(
            create_gauge_bc,
            "solve preflight requires the deterministic gauge BC",
        )



        print()
        print(
            "Solving requested-load heterogeneous true-hole PBC fluctuation problem..."
        )

        fluctuation = problem.solve()
        fluctuation.x.scatter_forward()

        fem_solve_performed = True
        system_assembled = True

        solve_petsc_convergence_reason = int(
            problem.solver.getConvergedReason()
        )

        solve_petsc_iterations = int(
            problem.solver.getIterationNumber()
        )

        print(
            "SOLVE_PREFLIGHT_PETSC_CONVERGENCE_REASON=",
            solve_petsc_convergence_reason,
        )

        print(
            "SOLVE_PREFLIGHT_PETSC_ITERATIONS=",
            solve_petsc_iterations,
        )

        must(
            solve_petsc_convergence_reason > 0,
            "PETSc requested-load solve converged",
        )

        fluctuation_values = np.asarray(
            fluctuation.x.array
        )

        must(
            fluctuation_values.ndim == 1,
            "returned fluctuation field has a one-dimensional scalar-DOF array",
        )

        must(
            fluctuation_values.size > 0,
            "returned fluctuation field contains scalar DOFs",
        )

        must(
            bool(
                np.all(
                    np.isfinite(
                        fluctuation_values
                    )
                )
            ),
            "every returned fluctuation DOF is finite",
        )

        solve_fluctuation_dof_count = int(
            fluctuation_values.size
        )

        solve_fluctuation_linf = float(
            np.max(
                np.abs(
                    fluctuation_values
                )
            )
        )

        print(
            "SOLVE_PREFLIGHT_FLUCTUATION_DOF_COUNT=",
            solve_fluctuation_dof_count,
        )

        print(
            "SOLVE_PREFLIGHT_FLUCTUATION_LINF=",
            solve_fluctuation_linf,
        )

        must(
            all(
                0 <= int(dof) < fluctuation_values.size
                for dof in gauge_dofs
            ),
            "deterministic gauge DOFs are valid returned-field indices",
        )

        solve_gauge_max_abs = float(
            max(
                abs(
                    fluctuation_values[
                        int(dof)
                    ]
                )
                for dof in gauge_dofs
            )
        )

        print(
            "SOLVE_PREFLIGHT_GAUGE_MAX_ABS=",
            solve_gauge_max_abs,
        )

        must(
            solve_gauge_max_abs <= 1.0e-12,
            "deterministic zero-displacement gauge remains zero after solve",
        )

        periodic_errors: list[float] = []

        coefficient_values, coefficient_offsets = (
            mpc.coefficients()
        )

        master_adjacency = mpc.masters

        for slave in slaves:
            slave_index = int(
                slave
            )

            master_links = np.asarray(
                master_adjacency.links(
                    slave_index
                ),
                dtype=np.int64,
            )

            must(
                master_links.size == 1,
                (
                    "solved periodic slave "
                    f"{slave_index} has exactly one master"
                ),
            )

            coefficient_start = int(
                coefficient_offsets[
                    slave_index
                ]
            )

            coefficient_end = int(
                coefficient_offsets[
                    slave_index + 1
                ]
            )

            solved_coefficients = np.asarray(
                coefficient_values[
                    coefficient_start:
                    coefficient_end
                ]
            )

            must(
                solved_coefficients.size == 1,
                (
                    "solved periodic slave "
                    f"{slave_index} has exactly one coefficient"
                ),
            )

            master_index = int(
                master_links[
                    0
                ]
            )

            must(
                0 <= slave_index < fluctuation_values.size,
                "periodic slave index is valid in returned fluctuation field",
            )

            must(
                0 <= master_index < fluctuation_values.size,
                "periodic master index is valid in returned fluctuation field",
            )

            periodic_errors.append(
                float(
                    abs(
                        fluctuation_values[
                            slave_index
                        ]
                        -
                        solved_coefficients[
                            0
                        ]
                        * fluctuation_values[
                            master_index
                        ]
                    )
                )
            )

        must(
            len(
                periodic_errors
            )
            == len(
                slaves
            ),
            "every periodic scalar slave was audited after backsubstitution",
        )

        solve_periodic_max_abs_error = float(
            max(
                periodic_errors,
                default=0.0,
            )
        )

        solve_periodic_reference_scale = float(
            max(
                solve_fluctuation_linf,
                abs(
                    float(
                        macro_amplitude
                    )
                ),
                1.0e-30,
            )
        )

        solve_periodic_normalized_error = float(
            solve_periodic_max_abs_error
            / solve_periodic_reference_scale
        )

        print(
            "SOLVE_PREFLIGHT_PERIODIC_MAX_ABS_ERROR=",
            solve_periodic_max_abs_error,
        )

        print(
            "SOLVE_PREFLIGHT_PERIODIC_REFERENCE_SCALE=",
            solve_periodic_reference_scale,
        )

        print(
            "SOLVE_PREFLIGHT_PERIODIC_NORMALIZED_ERROR=",
            solve_periodic_normalized_error,
        )

        must(
            solve_periodic_normalized_error <= 1.0e-10,
            "back-substituted fluctuation field satisfies periodic equality",
        )

        residual = problem.b.duplicate()

        try:
            problem.A.mult(
                problem.x,
                residual,
            )

            residual.axpy(
                PETSc.ScalarType(
                    -1.0
                ),
                problem.b,
            )

            solve_algebraic_residual_norm = float(
                residual.norm(
                    PETSc.NormType.NORM_2
                )
            )

            solve_rhs_norm = float(
                problem.b.norm(
                    PETSc.NormType.NORM_2
                )
            )

        finally:
            residual.destroy()

        solve_algebraic_relative_residual = float(
            solve_algebraic_residual_norm
            / max(
                solve_rhs_norm,
                1.0,
            )
        )

        print(
            "SOLVE_PREFLIGHT_CONSTRAINED_RESIDUAL_NORM=",
            solve_algebraic_residual_norm,
        )

        print(
            "SOLVE_PREFLIGHT_CONSTRAINED_RHS_NORM=",
            solve_rhs_norm,
        )

        print(
            "SOLVE_PREFLIGHT_CONSTRAINED_RELATIVE_RESIDUAL=",
            solve_algebraic_relative_residual,
        )

        must(
            math.isfinite(
                solve_algebraic_relative_residual
            ),
            "constrained algebraic relative residual is finite",
        )

        must(
            solve_algebraic_relative_residual <= 1.0e-10,
            "constrained algebraic relative residual passes hard solve gate",
        )

        print(
            "PASS — requested-load solve used public MPC-aware LinearProblem.solve exactly once"
        )

        print(
            "PASS — returned fluctuation field is finite"
        )

        print(
            "PASS — deterministic gauge remains exactly constrained"
        )

        print(
            "PASS — periodic fluctuation equality survives MPC backsubstitution"
        )

        print(
            "PASS — constrained algebraic residual passes the hard gate"
        )

    if evaluate_response:
        must(
            solve_problem,
            "response preflight requires the authenticated solved fluctuation field",
        )

        must(
            create_linear_problem,
            "response preflight requires the authenticated LinearProblem layer",
        )

        must(
            create_forms,
            "response preflight requires the heterogeneous constitutive forms",
        )

        must(
            create_gauge_bc,
            "response preflight requires the deterministic gauge BC",
        )



        must(
            macro_amplitude is not None
            and math.isfinite(
                float(
                    macro_amplitude
                )
            )
            and float(
                macro_amplitude
            )
            > 0.0,
            "response preflight macro amplitude is finite and positive",
        )

        must(
            matrix_E is not None
            and math.isfinite(
                float(
                    matrix_E
                )
            )
            and float(
                matrix_E
            )
            > 0.0,
            "response preflight matrix modulus is finite and positive",
        )

        print()
        print(
            "Evaluating requested-load true-hole homogenized response..."
        )

        def response_integrate(
            expression,
        ) -> float:
            local_value = fem.assemble_scalar(
                fem.form(
                    expression
                )
            )

            global_value = MPI.COMM_WORLD.allreduce(
                local_value,
                op=MPI.SUM,
            )

            return float(
                global_value
            )

        gross_area = float(
            mesh_diag[
                "gross_area"
            ]
        )

        must(
            math.isfinite(
                gross_area
            )
            and gross_area > 0.0,
            "response gross RVE area is finite and positive",
        )

        mesh_area_authority = mesh_diag[
            "mesh"
        ]

        expected_meshed_matrix_area = float(
            mesh_area_authority[
                "meshed_matrix_area"
            ]
        )

        expected_meshed_particle_area = float(
            mesh_area_authority[
                "meshed_particle_area"
            ]
        )

        expected_meshed_material_area = float(
            mesh_area_authority[
                "meshed_material_area"
            ]
        )

        expected_meshed_void_area = float(
            mesh_area_authority[
                "meshed_void_area"
            ]
        )

        response_runtime_matrix_area = response_integrate(
            1.0
            * dx(
                matrix_tag
            )
        )

        response_runtime_particle_area = response_integrate(
            1.0
            * dx(
                particle_tag
            )
        )

        response_runtime_material_area = float(
            response_runtime_matrix_area
            + response_runtime_particle_area
        )

        response_runtime_void_area = float(
            gross_area
            - response_runtime_material_area
        )

        print()
        print(
            "RESPONSE_PREFLIGHT_RUNTIME_MATRIX_AREA=",
            response_runtime_matrix_area,
        )

        print(
            "RESPONSE_PREFLIGHT_RUNTIME_PARTICLE_AREA=",
            response_runtime_particle_area,
        )

        print(
            "RESPONSE_PREFLIGHT_RUNTIME_MATERIAL_AREA=",
            response_runtime_material_area,
        )

        print(
            "RESPONSE_PREFLIGHT_RUNTIME_VOID_AREA=",
            response_runtime_void_area,
        )

        area_tolerance = 1.0e-10

        must(
            abs(
                response_runtime_matrix_area
                - expected_meshed_matrix_area
            )
            <= area_tolerance,
            "runtime matrix area matches discrete meshed matrix-area authority",
        )

        must(
            abs(
                response_runtime_particle_area
                - expected_meshed_particle_area
            )
            <= area_tolerance,
            "runtime particle area matches discrete meshed particle-area authority",
        )

        must(
            abs(
                response_runtime_material_area
                - expected_meshed_material_area
            )
            <= area_tolerance,
            "runtime material area matches discrete meshed material-area authority",
        )

        must(
            abs(
                response_runtime_void_area
                - expected_meshed_void_area
            )
            <= area_tolerance,
            "runtime inferred true-hole area matches discrete meshed void-area authority",
        )

        must(
            response_runtime_void_area > 0.0,
            "runtime response domain retains positive true-hole area",
        )

        must(
            response_runtime_material_area < gross_area,
            "true-hole runtime material area is strictly less than gross RVE area",
        )

        eps_fluct_response = ufl.sym(
            ufl.grad(
                fluctuation
            )
        )

        eps_total_response = (
            eps_fluct_response
            + E_bar
        )

        identity_2d_response = ufl.Identity(
            2
        )

        sigma_matrix_response = (
            2.0
            * matrix_mu
            * eps_total_response
            +
            matrix_lambda_ps
            * ufl.tr(
                eps_total_response
            )
            * identity_2d_response
        )

        sigma_particle_response = (
            2.0
            * particle_mu
            * eps_total_response
            +
            particle_lambda_ps
            * ufl.tr(
                eps_total_response
            )
            * identity_2d_response
        )

        def integrate_material_stress_component(
            component_i: int,
            component_j: int,
        ) -> float:
            return response_integrate(
                sigma_matrix_response[
                    component_i,
                    component_j,
                ]
                * dx(
                    matrix_tag
                )
                +
                sigma_particle_response[
                    component_i,
                    component_j,
                ]
                * dx(
                    particle_tag
                )
            )

        response_sigma_11 = float(
            integrate_material_stress_component(
                0,
                0,
            )
            / gross_area
        )

        response_sigma_22 = float(
            integrate_material_stress_component(
                1,
                1,
            )
            / gross_area
        )

        response_sigma_12 = float(
            integrate_material_stress_component(
                0,
                1,
            )
            / gross_area
        )

        response_stress_tensor_numpy = np.array(
            [
                [
                    response_sigma_11,
                    response_sigma_12,
                ],
                [
                    response_sigma_12,
                    response_sigma_22,
                ],
            ],
            dtype=float,
        )

        response_stress_voigt_numpy = np.array(
            [
                response_sigma_11,
                response_sigma_22,
                response_sigma_12,
            ],
            dtype=float,
        )

        must(
            bool(
                np.all(
                    np.isfinite(
                        response_stress_voigt_numpy
                    )
                )
            ),
            "requested-load homogenized true-hole stress is finite",
        )

        response_stiffness_column_numpy = (
            response_stress_voigt_numpy
            / float(
                macro_amplitude
            )
        )

        must(
            bool(
                np.all(
                    np.isfinite(
                        response_stiffness_column_numpy
                    )
                )
            ),
            "requested-load true-hole stiffness column is finite",
        )

        response_positive_component_map = {
            "X": 0,
            "Y": 1,
            "XY": 2,
        }

        must(
            load_case in response_positive_component_map,
            "response load-direction component mapping covers X/Y/XY",
        )

        response_positive_component_index = int(
            response_positive_component_map[
                load_case
            ]
        )

        print(
            "RESPONSE_PREFLIGHT_POSITIVE_COMPONENT_INDEX=",
            response_positive_component_index,
        )

        must(
            float(
                response_stiffness_column_numpy[response_positive_component_index]
            )
            > 0.0,
            "requested-load load-direction stiffness candidate is positive",
        )

        response_stiffness_column_normalized_numpy = (
            response_stiffness_column_numpy
            / float(
                matrix_E
            )
        )

        response_stress_tensor = (
            response_stress_tensor_numpy.tolist()
        )

        response_stress_voigt = (
            response_stress_voigt_numpy.tolist()
        )

        response_stiffness_column = (
            response_stiffness_column_numpy.tolist()
        )

        response_stiffness_column_normalized = (
            response_stiffness_column_normalized_numpy.tolist()
        )

        print()
        print(
            "RESPONSE_PREFLIGHT_MACROSCOPIC_STRESS_TENSOR=",
            response_stress_tensor,
        )

        print(
            "RESPONSE_PREFLIGHT_MACROSCOPIC_STRESS_VOIGT=",
            response_stress_voigt,
        )

        print(
            "RESPONSE_PREFLIGHT_STIFFNESS_COLUMN=",
            response_stiffness_column,
        )

        print(
            "RESPONSE_PREFLIGHT_STIFFNESS_COLUMN_NORMALIZED_BY_E_MATRIX=",
            response_stiffness_column_normalized,
        )

        response_micro_energy_density = float(
            response_integrate(
                ufl.inner(
                    sigma_matrix_response,
                    eps_total_response,
                )
                * dx(
                    matrix_tag
                )
                +
                ufl.inner(
                    sigma_particle_response,
                    eps_total_response,
                )
                * dx(
                    particle_tag
                )
            )
            / gross_area
        )

        response_macro_energy_density = float(
            np.sum(
                response_stress_tensor_numpy
                * e_bar_numpy
            )
        )

        must(
            math.isfinite(
                response_micro_energy_density
            ),
            "true-hole microscopic energy density is finite",
        )

        must(
            math.isfinite(
                response_macro_energy_density
            ),
            "true-hole macroscopic energy density is finite",
        )

        response_hill_mandel_relative_mismatch = float(
            abs(
                response_micro_energy_density
                - response_macro_energy_density
            )
            /
            max(
                abs(
                    response_micro_energy_density
                ),
                abs(
                    response_macro_energy_density
                ),
                1.0e-30,
            )
        )

        print()
        print(
            "RESPONSE_PREFLIGHT_MICRO_ENERGY_DENSITY=",
            response_micro_energy_density,
        )

        print(
            "RESPONSE_PREFLIGHT_MACRO_ENERGY_DENSITY=",
            response_macro_energy_density,
        )

        print(
            "RESPONSE_PREFLIGHT_HILL_MANDEL_RELATIVE_MISMATCH=",
            response_hill_mandel_relative_mismatch,
        )

        must(
            math.isfinite(
                response_hill_mandel_relative_mismatch
            ),
            "true-hole Hill-Mandel relative mismatch is finite",
        )

        must(
            response_hill_mandel_relative_mismatch
            <= 1.0e-5,
            "true-hole Hill-Mandel relative mismatch <= 1e-5",
        )

        response_weak_stationarity_value = float(
            response_integrate(
                ufl.inner(
                    sigma_matrix_response,
                    eps_fluct_response,
                )
                * dx(
                    matrix_tag
                )
                +
                ufl.inner(
                    sigma_particle_response,
                    eps_fluct_response,
                )
                * dx(
                    particle_tag
                )
            )
            / gross_area
        )

        response_weak_stationarity_relative = float(
            abs(
                response_weak_stationarity_value
            )
            /
            max(
                abs(
                    response_micro_energy_density
                ),
                abs(
                    response_macro_energy_density
                ),
                1.0,
            )
        )

        print()
        print(
            "RESPONSE_PREFLIGHT_WEAK_STATIONARITY_VALUE=",
            response_weak_stationarity_value,
        )

        print(
            "RESPONSE_PREFLIGHT_WEAK_STATIONARITY_RELATIVE=",
            response_weak_stationarity_relative,
        )

        must(
            math.isfinite(
                response_weak_stationarity_relative
            ),
            "true-hole weak-stationarity diagnostic is finite",
        )

        must(
            response_weak_stationarity_relative
            <= 1.0e-8,
            "true-hole weak-stationarity diagnostic passes <= 1e-8 gate",
        )

        response_evaluated = True

        if evaluate_local_response:
            must(
                physical_voids is not None,
                "cell-local extraction has physical void input",
            )

            matrix_cells_all_local = np.asarray(
                cell_tags.find(
                    int(
                        matrix_tag
                    )
                ),
                dtype=np.int32,
            )

            owned_cell_count_local = int(
                cell_map.size_local
            )

            matrix_owned_cells_local = np.asarray(
                matrix_cells_all_local[
                    matrix_cells_all_local
                    < owned_cell_count_local
                ],
                dtype=np.int32,
            )

            must(
                matrix_owned_cells_local.size > 0,
                "cell-local extraction contains owned matrix cells",
            )

            matrix_midpoints_xyz_local = (
                mesh.compute_midpoints(
                    domain,
                    tdim,
                    matrix_owned_cells_local,
                )
            )

            must(
                matrix_midpoints_xyz_local.ndim == 2
                and matrix_midpoints_xyz_local.shape[0]
                == matrix_owned_cells_local.size
                and matrix_midpoints_xyz_local.shape[1] >= 2,
                "cell-local physical matrix-cell midpoints have valid shape",
            )

            matrix_midpoints_local = np.asarray(
                matrix_midpoints_xyz_local[
                    :,
                    :2,
                ],
                dtype=np.float64,
            )

            sigma_xx_local = (
                sigma_matrix_response[
                    0,
                    0,
                ]
            )
            sigma_yy_local = (
                sigma_matrix_response[
                    1,
                    1,
                ]
            )
            tau_xy_local = (
                sigma_matrix_response[
                    0,
                    1,
                ]
            )

            sigma_vm_local = ufl.sqrt(
                sigma_xx_local
                * sigma_xx_local
                - sigma_xx_local
                * sigma_yy_local
                + sigma_yy_local
                * sigma_yy_local
                + 3.0
                * tau_xy_local
                * tau_xy_local
            )

            reference_midpoint_local = np.array(
                [
                    [
                        1.0 / 3.0,
                        1.0 / 3.0,
                    ]
                ],
                dtype=np.float64,
            )

            vm_expression_local = fem.Expression(
                sigma_vm_local,
                reference_midpoint_local,
            )

            area_expression_local = fem.Expression(
                ufl.CellVolume(
                    domain
                ),
                reference_midpoint_local,
            )

            local_vm_values = np.asarray(
                vm_expression_local.eval(
                    domain,
                    matrix_owned_cells_local,
                ),
                dtype=np.float64,
            ).reshape(
                matrix_owned_cells_local.size,
                -1,
            )[
                :,
                0,
            ]

            local_cell_areas = np.asarray(
                area_expression_local.eval(
                    domain,
                    matrix_owned_cells_local,
                ),
                dtype=np.float64,
            ).reshape(
                matrix_owned_cells_local.size,
                -1,
            )[
                :,
                0,
            ]

            must(
                bool(
                    np.all(
                        np.isfinite(
                            local_vm_values
                        )
                    )
                ),
                "cell-local matrix von-Mises values are finite",
            )

            must(
                bool(
                    np.all(
                        local_vm_values >= 0.0
                    )
                ),
                "cell-local matrix von-Mises values are non-negative",
            )

            must(
                bool(
                    np.all(
                        np.isfinite(
                            local_cell_areas
                        )
                    )
                    and np.all(
                        local_cell_areas > 0.0
                    )
                ),
                "cell-local physical matrix-cell areas are finite and positive",
            )

            local_response_matrix_area_from_cells = float(
                np.sum(
                    local_cell_areas
                )
            )

            must(
                math.isclose(
                    local_response_matrix_area_from_cells,
                    float(
                        response_runtime_matrix_area
                    ),
                    rel_tol=1.0e-10,
                    abs_tol=1.0e-10,
                ),
                "cell-local physical cell areas reproduce runtime matrix area",
            )

            local_module_path = (
                Path(__file__)
                .resolve()
                .with_name(
                    "26_m8_local_response.py"
                )
            )

            local_spec = (
                importlib.util.spec_from_file_location(
                    "_m8_local_response_runtime",
                    local_module_path,
                )
            )

            must(
                local_spec is not None
                and local_spec.loader is not None,
                "permanent src/26 module specification is loadable",
            )

            local_module = (
                importlib.util.module_from_spec(
                    local_spec
                )
            )

            local_spec.loader.exec_module(
                local_module
            )

            local_evaluator = getattr(
                local_module,
                "evaluate_m8_matrix_vm_annulus_cell_tail10",
                None,
            )

            must(
                callable(
                    local_evaluator
                ),
                "permanent src/26 cell evaluator is callable",
            )

            local_metric_authority = getattr(
                local_module,
                "M8_CELL_METRIC_ID",
                None,
            )

            must(
                isinstance(
                    local_metric_authority,
                    str,
                )
                and len(
                    local_metric_authority
                ) > 0,
                "permanent src/26 cell metric identifier is available",
            )

            local_response = local_evaluator(
                matrix_cell_midpoints=(
                    matrix_midpoints_local
                ),
                sigma_vm_values=(
                    local_vm_values
                ),
                cell_areas=(
                    local_cell_areas
                ),
                physical_voids=(
                    physical_voids
                ),
                width=width,
                height=height,
                macro_sigma_11=(
                    response_sigma_11
                ),
            )

            must(
                isinstance(
                    local_response,
                    dict,
                ),
                "cell-local evaluator returned a diagnostics dictionary",
            )

            must(
                local_response.get(
                    "metric_id"
                )
                == local_metric_authority,
                "cell-local metric identifier matches permanent src/26 authority",
            )

            must(
                local_response.get(
                    "status"
                )
                == "valid",
                "positive-void cell-local response status is valid",
            )

            local_K = float(
                local_response[
                    "K_vm_tail10"
                ]
            )

            must(
                math.isfinite(
                    local_K
                )
                and local_K >= 0.0,
                "cell-local K_vm_tail10 is finite and non-negative",
            )

            must(
                math.isclose(
                    float(
                        local_response[
                            "normalization_abs_Sigma_11"
                        ]
                    ),
                    abs(
                        float(
                            response_sigma_11
                        )
                    ),
                    rel_tol=0.0,
                    abs_tol=1.0e-12,
                ),
                "cell-local normalization uses exact gross-RVE abs(Sigma_11)",
            )

            local_response_matrix_owned_cell_count = int(
                matrix_owned_cells_local.size
            )

            local_response_evaluated = True

            print()
            print(
                "CELL_LOCAL_PREFLIGHT_MATRIX_OWNED_CELL_COUNT=",
                local_response_matrix_owned_cell_count,
            )
            print(
                "CELL_LOCAL_PREFLIGHT_MATRIX_AREA_FROM_CELLS=",
                local_response_matrix_area_from_cells,
            )
            print(
                "CELL_LOCAL_PREFLIGHT_SIGMA_VM_TAIL10=",
                local_response[
                    "sigma_vm_tail10"
                ],
            )
            print(
                "CELL_LOCAL_PREFLIGHT_K_VM_TAIL10=",
                local_response[
                    "K_vm_tail10"
                ],
            )

            print(
                "PASS — permanent src/26 cell-local evaluator completed on the authenticated solved response"
            )

        if evaluate_quadrature_local_response:
            import basix

            matrix_cells_all_q = np.asarray(cell_tags.find(int(matrix_tag)), dtype=np.int32)
            owned_cell_count_q = int(cell_map.size_local)
            matrix_owned_cells_q = np.asarray(
                matrix_cells_all_q[matrix_cells_all_q < owned_cell_count_q],
                dtype=np.int32,
            )
            must(matrix_owned_cells_q.size > 0, "quadrature-local extraction contains owned matrix cells")

            q_points, q_weights_ref = basix.make_quadrature(
                domain.basix_cell(),
                int(quadrature_degree),
            )
            q_points = np.asarray(q_points, dtype=np.float64)
            q_weights_ref = np.asarray(q_weights_ref, dtype=np.float64).reshape(-1)
            must(
                q_points.ndim == 2 and q_points.shape[1] == 2 and q_points.shape[0] > 0,
                "quadrature-local reference points have valid triangle shape",
            )
            quadrature_local_reference_point_count = int(q_points.shape[0])
            must(
                q_weights_ref.shape == (quadrature_local_reference_point_count,),
                "quadrature-local reference weights match reference-point count",
            )
            must(
                bool(np.all(np.isfinite(q_points)))
                and bool(np.all(np.isfinite(q_weights_ref)))
                and bool(np.all(q_weights_ref > 0.0)),
                "quadrature-local reference points/weights are finite and positive",
            )

            sigma_xx_q = sigma_matrix_response[0, 0]
            sigma_yy_q = sigma_matrix_response[1, 1]
            tau_xy_q = sigma_matrix_response[0, 1]
            sigma_vm_q = ufl.sqrt(
                sigma_xx_q * sigma_xx_q
                - sigma_xx_q * sigma_yy_q
                + sigma_yy_q * sigma_yy_q
                + 3.0 * tau_xy_q * tau_xy_q
            )

            coord_expr_q = fem.Expression(ufl.SpatialCoordinate(domain), q_points)
            detj_expr_q = fem.Expression(ufl.JacobianDeterminant(domain), q_points)
            vm_expr_q = fem.Expression(sigma_vm_q, q_points)

            coords_q = np.asarray(
                coord_expr_q.eval(domain, matrix_owned_cells_q), dtype=np.float64
            )
            detj_q = np.asarray(
                detj_expr_q.eval(domain, matrix_owned_cells_q), dtype=np.float64
            )
            vm_q = np.asarray(
                vm_expr_q.eval(domain, matrix_owned_cells_q), dtype=np.float64
            )
            expected_scalar_shape_q = (
                int(matrix_owned_cells_q.size),
                quadrature_local_reference_point_count,
            )
            must(
                coords_q.shape == expected_scalar_shape_q + (2,),
                "quadrature-local physical-coordinate Expression shape is exact",
            )
            must(
                detj_q.shape == expected_scalar_shape_q,
                "quadrature-local detJ Expression shape is exact",
            )
            must(
                vm_q.shape == expected_scalar_shape_q,
                "quadrature-local von-Mises Expression shape is exact",
            )

            physical_weights_q = np.abs(detj_q) * q_weights_ref[None, :]
            must(
                bool(np.all(np.isfinite(coords_q)))
                and bool(np.all(np.isfinite(detj_q)))
                and bool(np.all(np.isfinite(vm_q)))
                and bool(np.all(np.isfinite(physical_weights_q))),
                "quadrature-local physical coordinates/stress/weights are finite",
            )
            must(
                bool(np.all(vm_q >= 0.0))
                and bool(np.all(physical_weights_q > 0.0)),
                "quadrature-local stress is non-negative and physical weights are positive",
            )

            quadrature_local_matrix_area_from_weights = float(np.sum(physical_weights_q))
            must(
                math.isclose(
                    quadrature_local_matrix_area_from_weights,
                    float(response_runtime_matrix_area),
                    rel_tol=1.0e-10,
                    abs_tol=1.0e-10,
                ),
                "quadrature-local physical weights reproduce runtime matrix area",
            )

            coords_flat_q = np.asarray(coords_q.reshape(-1, 2), dtype=np.float64)
            vm_flat_q = np.asarray(vm_q.reshape(-1), dtype=np.float64)
            weights_flat_q = np.asarray(physical_weights_q.reshape(-1), dtype=np.float64)
            quadrature_local_contribution_count = int(vm_flat_q.size)
            must(
                coords_flat_q.shape[0]
                == quadrature_local_contribution_count
                == weights_flat_q.size,
                "quadrature-local flattened contributions align",
            )

            q_module_path = Path(__file__).resolve().with_name("26_m8_local_response.py")
            q_spec = importlib.util.spec_from_file_location(
                "_m8_quadrature_local_response_runtime",
                q_module_path,
            )
            must(
                q_spec is not None and q_spec.loader is not None,
                "permanent src/26 quadrature module specification is loadable",
            )
            q_module = importlib.util.module_from_spec(q_spec)
            q_spec.loader.exec_module(q_module)
            q_evaluator = getattr(
                q_module,
                "evaluate_m8_matrix_vm_annulus_quadrature_tail10",
                None,
            )
            q_metric_id = getattr(q_module, "M8_QUADRATURE_METRIC_ID", None)
            must(callable(q_evaluator), "permanent src/26 quadrature evaluator is callable")
            must(
                isinstance(q_metric_id, str) and len(q_metric_id) > 0,
                "permanent src/26 quadrature metric identifier is available",
            )

            quadrature_local_response = q_evaluator(
                quadrature_point_coordinates=coords_flat_q,
                sigma_vm_values=vm_flat_q,
                quadrature_area_weights=weights_flat_q,
                physical_voids=physical_voids,
                width=width,
                height=height,
                macro_sigma_11=response_sigma_11,
            )
            must(
                isinstance(quadrature_local_response, dict),
                "quadrature-local evaluator returned diagnostics",
            )
            must(
                quadrature_local_response.get("metric_id") == q_metric_id,
                "quadrature-local metric identifier matches permanent src/26 authority",
            )
            must(
                quadrature_local_response.get("status") == "valid",
                "positive-void quadrature-local response status is valid",
            )
            q_K = float(quadrature_local_response["K_vm_tail10"])
            must(
                math.isfinite(q_K) and q_K >= 0.0,
                "quadrature-local K_vm_tail10 is finite and non-negative",
            )
            must(
                math.isclose(
                    float(quadrature_local_response["normalization_abs_Sigma_11"]),
                    abs(float(response_sigma_11)),
                    rel_tol=0.0,
                    abs_tol=1.0e-12,
                ),
                "quadrature-local normalization uses exact gross-RVE abs(Sigma_11)",
            )

            quadrature_local_degree = int(quadrature_degree)
            quadrature_local_matrix_owned_cell_count = int(matrix_owned_cells_q.size)
            quadrature_local_response_evaluated = True
            print()
            print("QUADRATURE_LOCAL_PREFLIGHT_DEGREE=", quadrature_local_degree)
            print(
                "QUADRATURE_LOCAL_PREFLIGHT_REFERENCE_POINT_COUNT=",
                quadrature_local_reference_point_count,
            )
            print(
                "QUADRATURE_LOCAL_PREFLIGHT_MATRIX_OWNED_CELL_COUNT=",
                quadrature_local_matrix_owned_cell_count,
            )
            print(
                "QUADRATURE_LOCAL_PREFLIGHT_CONTRIBUTION_COUNT=",
                quadrature_local_contribution_count,
            )
            print(
                "QUADRATURE_LOCAL_PREFLIGHT_MATRIX_AREA_FROM_WEIGHTS=",
                quadrature_local_matrix_area_from_weights,
            )
            print(
                "QUADRATURE_LOCAL_PREFLIGHT_SIGMA_VM_TAIL10=",
                quadrature_local_response["sigma_vm_tail10"],
            )
            print(
                "QUADRATURE_LOCAL_PREFLIGHT_K_VM_TAIL10=",
                quadrature_local_response["K_vm_tail10"],
            )
            print(
                "PASS — permanent src/26 quadrature-local evaluator completed on the authenticated solved response"
            )

        print()
        print(
            "PASS — discrete runtime phase areas match the authenticated FE mesh authority"
        )

        print(
            "PASS — prescribed requested-load E_bar remains the macroscopic strain authority"
        )

        print(
            "PASS — no material-only recovered-strain hard gate was evaluated"
        )

        print(
            "PASS — homogenized material stress was normalized by gross RVE area"
        )

        print(
            "PASS — positive requested-load single-load stiffness column was reconstructed"
        )

        print(
            "PASS — true-hole Hill-Mandel consistency passes the hard gate"
        )

        print(
            "PASS — true-hole weak stationarity passes the hard gate"
        )

    return {
        "dolfinx_version":
            dolfinx.__version__,
        "cell_count":
            cell_count,
        "matrix_cell_count":
            matrix_cells,
        "particle_cell_count":
            particle_cells,
        "scalar_slave_count":
            len(
                slaves
            ),
        "periodic_slave_block_count":
            len(
                slave_blocks
            ),
        "expected_periodic_slave_block_count":
            expected_slave_blocks,
        "unique_master_count":
            len(
                master_set
            ),
        "minimum_master_count":
            min_master_count,
        "maximum_master_count":
            max_master_count,
        "maximum_coefficient_error":
            max_coefficient_error,
        "component_mismatch_count":
            component_mismatch_count,
        "slave_master_overlap_count":
            len(
                overlap
            ),
        "maximum_mapping_error":
            mapping_max_error,
        "gauge_block":
            gauge_block,
        "gauge_coordinate":
            gauge_coordinate.tolist(),
        "gauge_scalar_dofs":
            gauge_dofs,
        "dirichlet_gauge_created":
            gauge_bc_created,
        "gauge_bc_scalar_dofs":
            gauge_bc_scalar_dofs,
        "gauge_bc_value":
            (
                [
                    0.0,
                    0.0,
                ]
                if gauge_bc_created
                else []
            ),
        "fem_forms_created":
            forms_created,
        "fem_forms_compiled":
            forms_compiled,
        "bilinear_argument_count":
            bilinear_argument_count,
        "linear_argument_count":
            linear_argument_count,
        "bilinear_cell_subdomain_ids":
            bilinear_cell_subdomain_ids,
        "linear_cell_subdomain_ids":
            linear_cell_subdomain_ids,
        "matrix_mu":
            matrix_mu,
        "matrix_lambda_ps":
            matrix_lambda_ps,
        "particle_mu":
            particle_mu,
        "particle_lambda_ps":
            particle_lambda_ps,
        "macro_strain_matrix":
            macro_strain_matrix,
        "macro_strain_voigt":
            macro_strain_voigt,
        "linear_problem_created":
            linear_problem_created,
        "linear_problem_matrix_size":
            linear_problem_matrix_size,
        "linear_problem_rhs_size":
            linear_problem_rhs_size,
        "linear_problem_solution_size":
            linear_problem_solution_size,
        "linear_problem_solver_type":
            linear_problem_solver_type,
        "linear_problem_pc_type":
            linear_problem_pc_type,
        "linear_problem_options_prefix":
            linear_problem_options_prefix,
        "system_assembled":
            system_assembled,
        "fem_solve_performed":
            fem_solve_performed,
        "response_evaluated":
            response_evaluated,
        "response_runtime_matrix_area":
            response_runtime_matrix_area,
        "response_runtime_particle_area":
            response_runtime_particle_area,
        "response_runtime_material_area":
            response_runtime_material_area,
        "response_runtime_void_area":
            response_runtime_void_area,
        "response_stress_tensor":
            response_stress_tensor,
        "response_stress_voigt":
            response_stress_voigt,
        "response_stiffness_column":
            response_stiffness_column,
        "response_stiffness_column_normalized_by_E_matrix":
            response_stiffness_column_normalized,
        "response_positive_component_index":
            response_positive_component_index,
        "response_micro_energy_density":
            response_micro_energy_density,
        "response_macro_energy_density":
            response_macro_energy_density,
        "response_hill_mandel_relative_mismatch":
            response_hill_mandel_relative_mismatch,
        "response_weak_stationarity_value":
            response_weak_stationarity_value,
        "response_weak_stationarity_relative":
            response_weak_stationarity_relative,
        "local_response_evaluated":
            local_response_evaluated,
        "local_response":
            local_response,
        "local_response_matrix_owned_cell_count":
            local_response_matrix_owned_cell_count,
        "local_response_matrix_area_from_cells":
            local_response_matrix_area_from_cells,
        "quadrature_local_response_evaluated":
            quadrature_local_response_evaluated,
        "quadrature_local_response":
            quadrature_local_response,
        "quadrature_local_degree":
            quadrature_local_degree,
        "quadrature_local_reference_point_count":
            quadrature_local_reference_point_count,
        "quadrature_local_matrix_owned_cell_count":
            quadrature_local_matrix_owned_cell_count,
        "quadrature_local_contribution_count":
            quadrature_local_contribution_count,
        "quadrature_local_matrix_area_from_weights":
            quadrature_local_matrix_area_from_weights,
        "solve_petsc_convergence_reason":
            solve_petsc_convergence_reason,
        "solve_petsc_iterations":
            solve_petsc_iterations,
        "solve_algebraic_residual_norm":
            solve_algebraic_residual_norm,
        "solve_rhs_norm":
            solve_rhs_norm,
        "solve_algebraic_relative_residual":
            solve_algebraic_relative_residual,
        "solve_fluctuation_dof_count":
            solve_fluctuation_dof_count,
        "solve_fluctuation_linf":
            solve_fluctuation_linf,
        "solve_gauge_max_abs":
            solve_gauge_max_abs,
        "solve_periodic_max_abs_error":
            solve_periodic_max_abs_error,
        "solve_periodic_reference_scale":
            solve_periodic_reference_scale,
        "solve_periodic_normalized_error":
            solve_periodic_normalized_error,
    }


def main() -> int:
    args = parse_args()

    selected_preflight_modes = sum(
        int(value)
        for value in (
            args.mpc_preflight_only,
            args.gauge_preflight_only,
            args.form_preflight_only,
            args.linear_problem_preflight_only,
            args.solve_preflight_only,
            args.response_preflight_only,
            args.cell_local_preflight_only,
            args.quadrature_local_preflight_only,
        )
    )

    must(
        selected_preflight_modes <= 1,
        (
            "MPC, gauge, UFL-form and LinearProblem "
            "preflight modes are mutually exclusive"
        ),
    )


    if args.quadrature_local_preflight_only:
        must(
            args.quadrature_degree is not None and 1 <= args.quadrature_degree <= 8,
            "quadrature-local preflight requires explicit validation degree 1..8",
        )
    else:
        must(
            args.quadrature_degree is None,
            "--quadrature-degree is accepted only with --quadrature-local-preflight-only",
        )


    repo = (
        Path(__file__)
        .resolve()
        .parents[1]
    )

    print(
        "=== M9 STEP-9 VOID PBC INPUT CONTRACT ==="
    )

    # --------------------------------------------------------
    # Permanent implementation lineage.
    # --------------------------------------------------------

    for relative, expected in AUTHORITIES.items():
        path = (
            repo
            / relative
        )

        must(
            path.is_file(),
            f"authority exists: {relative}",
        )

        actual = sha256_file(
            path
        )

        print(
            f"{relative} SHA256 = {actual}"
        )

        must(
            actual == expected,
            (
                "authority SHA authenticated: "
                f"{relative}"
            ),
        )

    # --------------------------------------------------------
    # Runtime input existence and immutable SHA provenance.
    # --------------------------------------------------------

    for path, label in (
        (
            args.mesh,
            "runtime true-hole mesh",
        ),
        (
            args.mesh_diagnostics,
            "runtime mesh diagnostics",
        ),
        (
            args.geometry_json,
            "runtime Step-9 defective geometry",
        ),
        (
            args.config,
            "runtime material config",
        ),
    ):
        must(
            path.is_file(),
            f"{label} exists",
        )

    must(
        not args.output.exists(),
        "future PBC output does not already exist",
    )

    expected_mesh_sha = canonical_sha256(
        args.expected_mesh_sha256,
        "expected mesh SHA256",
    )

    expected_diag_sha = canonical_sha256(
        args.expected_mesh_diagnostics_sha256,
        "expected mesh-diagnostics SHA256",
    )

    expected_geometry_sha = canonical_sha256(
        args.expected_geometry_sha256,
        "expected Step-9 geometry SHA256",
    )

    actual_mesh_sha = sha256_file(
        args.mesh
    )

    actual_diag_sha = sha256_file(
        args.mesh_diagnostics
    )

    actual_geometry_sha = sha256_file(
        args.geometry_json
    )

    config_sha = sha256_file(
        args.config
    )

    print(
        "mesh SHA256 =",
        actual_mesh_sha,
    )

    print(
        "mesh diagnostics SHA256 =",
        actual_diag_sha,
    )

    print(
        "Step-9 geometry SHA256 =",
        actual_geometry_sha,
    )

    print(
        "material config SHA256 =",
        config_sha,
    )

    must(
        actual_mesh_sha
        == expected_mesh_sha,
        "runtime mesh SHA256 authenticated",
    )

    must(
        actual_diag_sha
        == expected_diag_sha,
        "runtime mesh-diagnostics SHA256 authenticated",
    )

    must(
        actual_geometry_sha
        == expected_geometry_sha,
        "runtime Step-9 geometry SHA256 authenticated",
    )

    # --------------------------------------------------------
    # Step-9 single defective geometry contract.
    # --------------------------------------------------------

    geometry = json.loads(
        args.geometry_json.read_text(
            encoding="utf-8"
        )
    )

    must(
        geometry.get(
            "schema"
        )
        == GEOMETRY_SCHEMA,
        "Step-9 defective geometry schema authenticated",
    )

    must(
        geometry.get(
            "status"
        )
        == "valid"
        and geometry.get(
            "failure_reason"
        )
        is None,
        "Step-9 defective geometry status is valid",
    )

    must(
        all(
            value is True
            for value
            in geometry[
                "checks"
            ].values()
        ),
        "all Step-9 geometry checks PASS",
    )

    geometry_scope = geometry[
        "scope_guard"
    ]

    must(
        geometry_scope[
            "source_particle_geometry_regenerated"
        ]
        is False,
        "Step-9 geometry reused authenticated particle geometry",
    )

    must(
        geometry_scope[
            "protected_pristine_m8_schema_mutated"
        ]
        is False,
        "protected pristine M8 schema remains unmutated",
    )

    must(
        geometry_scope[
            "mpc_constructed"
        ]
        is False,
        "Step-9 geometry artifact predates MPC",
    )

    must(
        geometry_scope[
            "fem_solve_performed"
        ]
        is False,
        "Step-9 geometry artifact predates FEM",
    )

    must(
        geometry_scope[
            "m9_step9_transfer_validation"
        ] is True,
        "geometry belongs to Step-9 transfer validation",
    )

    must(
        geometry_scope[
            "m9_stochastic_pilot_production"
        ] is False,
        "geometry is not stochastic-pilot production evidence",
    )

    must(
        geometry_scope[
            "production_design_id_created"
        ] is False,
        "geometry created no production design ID",
    )

    must(
        geometry_scope[
            "production_realization_id_created"
        ] is False,
        "geometry created no production realization ID",
    )

    must(
        geometry_scope[
            "production_pilot_sampling_rng_consumed"
        ] is False,
        "geometry consumed no production pilot sampling RNG",
    )

    state = geometry[
        "state"
    ]

    must(
        state[
            "state"
        ]
        == "defective",
        "single Step-9 geometry state is defective",
    )

    must(
        all(
            value is True
            for value
            in state[
                "checks"
            ].values()
        ),
        "selected geometry-state checks all PASS",
    )

    physical_voids = state[
        "voids"
    ]

    must(
        isinstance(physical_voids, list),
        "Step-9 state exposes physical void records",
    )

    void_count = len(physical_voids)

    must(
        void_count in STEP9_ALLOWED_VOID_COUNTS,
        "physical void count belongs to locked Step-9 set {1,2,4}",
    )

    must(
        int(state["void_count"]) == void_count,
        "state void count matches physical void records",
    )

    must(
        len(geometry["particles"]) == STEP9_PHYSICAL_PARTICLE_COUNT,
        "Step-9 geometry contains 16 physical particles",
    )

    geometry_rng = geometry["rng"]

    must(
        geometry_rng["bit_generator"] == "PCG64",
        "Step-9 geometry records explicit PCG64",
    )

    must(
        geometry_rng["rng_namespace"] == STEP9_VALIDATION_SEED_NAMESPACE,
        "Step-9 validation-seed namespace authenticated",
    )

    must(
        geometry_rng["void_seed_status"] == "applicable",
        "defective Step-9 geometry has an applicable void seed",
    )

    width = float(
        geometry[
            "rve"
        ][
            "width"
        ]
    )

    height = float(
        geometry[
            "rve"
        ][
            "height"
        ]
    )

    gross_area = (
        width
        * height
    )

    must(
        math.isclose(
            width, STEP9_RVE_LENGTH,
            rel_tol=0.0, abs_tol=1.0e-12,
        )
        and math.isclose(
            height, STEP9_RVE_LENGTH,
            rel_tol=0.0, abs_tol=1.0e-12,
        ),
        "Step-9 RVE side length is locked to 1.0",
    )

    must(
        math.isfinite(
            width
        )
        and width > 0.0
        and math.isfinite(
            height
        )
        and height > 0.0,
        "RVE dimensions are finite and positive",
    )

    must(
        math.isclose(
            float(
                geometry[
                    "rve"
                ][
                    "area"
                ]
            ),
            gross_area,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "RVE area is consistent with width*height",
    )

    must(
        math.isclose(
            float(
                state[
                    "gross_rve_area"
                ]
            ),
            gross_area,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "selected state gross area matches RVE",
    )

    particle_identity = str(
        geometry[
            "source_particle_geometry"
        ][
            "geometry_identity_sha256"
        ]
    )

    geometry_identity = str(
        state[
            "geometry_identity"
        ][
            "sha256"
        ]
    )

    # --------------------------------------------------------
    # Mesh-diagnostics contract.
    # --------------------------------------------------------

    mesh_diag = json.loads(
        args.mesh_diagnostics.read_text(
            encoding="utf-8"
        )
    )

    must(
        mesh_diag.get(
            "schema"
        )
        == MESH_SCHEMA,
        "periodized true-hole mesh schema authenticated",
    )

    must(
        mesh_diag.get(
            "status"
        )
        == "valid",
        "mesh diagnostics status is valid",
    )

    must(
        mesh_diag[
            "state"
        ]
        == "defective",
        "mesh state matches single defective geometry state",
    )

    must(
        mesh_diag[
            "source_geometry_sha256"
        ]
        == actual_geometry_sha,
        "mesh provenance points to authenticated Step-9 geometry",
    )

    must(
        mesh_diag[
            "artifacts"
        ][
            "mesh"
        ]
        == str(
            args.mesh
        ),
        "mesh diagnostics record exact runtime mesh path",
    )

    must(
        mesh_diag[
            "artifacts"
        ][
            "diagnostics"
        ]
        == str(
            args.mesh_diagnostics
        ),
        "mesh diagnostics record their exact runtime path",
    )

    must(
        mesh_diag[
            "physical_tags"
        ]
        == EXPECTED_PHYSICAL_TAGS,
        "void-capable material/boundary physical tags are exact",
    )

    must(
        mesh_diag[
            "periodic_geometric_pairing_ready"
        ]
        is True,
        "input mesh passed periodic CAD pairing",
    )

    must(
        mesh_diag[
            "periodic_mesh_constraints_applied"
        ]
        is True,
        "input mesh contains authenticated periodic constraints",
    )

    must(
        mesh_diag[
            "mesh_generated"
        ]
        is True,
        "input true-hole mesh was generated",
    )

    mesh_scope = mesh_diag[
        "scope_guard"
    ]

    must(
        mesh_scope["m9_step9_transfer_validation"] is True,
        "mesh belongs to Step-9 transfer validation",
    )

    must(
        mesh_scope["m9_stochastic_pilot_production"] is False,
        "mesh is not stochastic-pilot production evidence",
    )

    must(
        mesh_scope["production_design_id_created"] is False,
        "mesh created no production design ID",
    )

    must(
        mesh_scope["production_realization_id_created"] is False,
        "mesh created no production realization ID",
    )

    must(
        mesh_scope["production_pilot_sampling_rng_consumed"] is False,
        "mesh consumed no production pilot sampling RNG",
    )

    must(
        mesh_scope[
            "source_geometry_regenerated"
        ]
        is False,
        "mesh construction did not regenerate geometry",
    )

    must(
        mesh_scope[
            "mpc_constructed"
        ]
        is False,
        "input mesh predates MPC construction",
    )

    must(
        mesh_scope[
            "fem_solve_performed"
        ]
        is False,
        "input mesh predates FEM solve",
    )

    must(
        mesh_scope[
            "tensor_reconstructed"
        ]
        is False,
        "input mesh predates tensor reconstruction",
    )

    must(
        mesh_scope[
            "machine_learning_performed"
        ]
        is False,
        "input mesh predates ML",
    )

    must(
        mesh_scope[
            "protected_pristine_m8_schema_mutated"
        ]
        is False,
        "mesh did not mutate protected pristine M8 schema",
    )

    mesh_size = float(
        mesh_diag[
            "mesh_size"
        ]
    )

    must(
        math.isfinite(
            mesh_size
        )
        and mesh_size > 0.0,
        "runtime mesh size is finite and positive",
    )

    mesh = mesh_diag[
        "mesh"
    ]

    must(
        mesh[
            "element_policy"
        ]
        == "first_order_triangles",
        "runtime mesh uses first-order triangles",
    )

    must(
        int(
            mesh[
                "cell_count"
            ]
        )
        > 0,
        "runtime mesh contains cells",
    )

    must(
        int(
            mesh[
                "matrix_cell_count"
            ]
        )
        > 0,
        "runtime mesh contains matrix cells",
    )

    must(
        int(
            mesh[
                "particle_cell_count"
            ]
        )
        > 0,
        "runtime mesh contains particle cells",
    )

    must(
        int(
            mesh[
                "matrix_cell_count"
            ]
        )
        + int(
            mesh[
                "particle_cell_count"
            ]
        )
        == int(
            mesh[
                "cell_count"
            ]
        ),
        "matrix and particle cells cover every 2D cell",
    )

    must(
        int(
            mesh[
                "void_boundary_element_count"
            ]
        )
        > 0,
        "runtime mesh retains true-hole boundary elements",
    )

    must(
        mesh[
            "periodic_master_entities_ok"
        ]
        is True,
        "runtime Gmsh periodic master entities are authenticated",
    )

    must(
        float(
            mesh[
                "periodic_transform_max_error"
            ]
        )
        <= GEOM_TOL,
        "runtime periodic transform error passes hard gate",
    )

    for key, label in (
        (
            "particle_fraction_absolute_error",
            "particle-fraction mesh error",
        ),
        (
            "void_fraction_absolute_error",
            "void-fraction mesh error",
        ),
        (
            "material_area_absolute_error",
            "material-area mesh error",
        ),
    ):
        must(
            float(
                mesh[
                    key
                ]
            )
            <= MESH_AUDIT_TOL,
            f"{label} <= 0.005",
        )

    expected_particle_area = float(
        geometry[
            "generated_geometry"
        ][
            "particle_area"
        ]
    )

    must(
        math.isclose(
            float(
                mesh_diag[
                    "expected_particle_area"
                ]
            ),
            expected_particle_area,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "mesh analytical particle area matches Step-9 geometry",
    )

    must(
        math.isclose(
            float(
                mesh_diag[
                    "expected_void_area"
                ]
            ),
            float(
                state[
                    "void_area"
                ]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "mesh analytical void area matches selected state",
    )

    must(
        math.isclose(
            float(
                mesh_diag[
                    "expected_matrix_area"
                ]
            ),
            float(
                state[
                    "matrix_area"
                ]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "mesh analytical matrix area matches selected state",
    )

    must(
        math.isclose(
            float(
                mesh_diag[
                    "gross_area"
                ]
            ),
            gross_area,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "mesh gross area matches Step-9 geometry",
    )

    # --------------------------------------------------------
    # Locked material/mechanics model contract.
    # --------------------------------------------------------

    config = yaml.safe_load(
        args.config.read_text(
            encoding="utf-8"
        )
    )

    must(
        config[
            "model"
        ][
            "dimension"
        ]
        == 2,
        "material config dimension = 2",
    )

    must(
        config[
            "model"
        ][
            "assumption"
        ]
        == "plane_stress",
        "material config assumption = plane stress",
    )

    must(
        config[
            "model"
        ][
            "interface"
        ]
        == "perfect_bonding",
        "material config interface = perfect bonding",
    )

    matrix_E = float(
        config[
            "matrix"
        ][
            "youngs_modulus"
        ]
    )

    matrix_nu = float(
        config[
            "matrix"
        ][
            "poissons_ratio"
        ]
    )

    particle_E = float(
        config[
            "particle"
        ][
            "youngs_modulus"
        ]
    )

    particle_nu = float(
        config[
            "particle"
        ][
            "poissons_ratio"
        ]
    )

    must(
        math.isfinite(matrix_E)
        and math.isclose(
            matrix_E, STEP9_MATRIX_E,
            rel_tol=0.0, abs_tol=0.0,
        ),
        "Step-9 matrix reference modulus remains exactly 1000",
    )

    must(
        math.isfinite(particle_E) and particle_E > 0.0,
        "Step-9 particle modulus is finite and positive",
    )

    ep_over_em = particle_E / matrix_E

    must(
        math.isfinite(ep_over_em)
        and STEP9_EP_OVER_EM_MIN <= ep_over_em <= STEP9_EP_OVER_EM_MAX,
        "Step-9 particle/matrix stiffness ratio lies in [2, 30]",
    )

    must(
        math.isclose(
            particle_E, ep_over_em * matrix_E,
            rel_tol=1.0e-12, abs_tol=0.0,
        ),
        "Step-9 particle modulus equals Ep_over_Em * E_matrix",
    )

    must(
        math.isfinite(matrix_nu)
        and STEP9_NU_MATRIX_MIN <= matrix_nu <= STEP9_NU_MATRIX_MAX,
        "Step-9 matrix Poisson ratio lies in [0.25, 0.40]",
    )

    must(
        math.isfinite(particle_nu)
        and STEP9_NU_PARTICLE_MIN <= particle_nu <= STEP9_NU_PARTICLE_MAX,
        "Step-9 particle Poisson ratio lies in [0.15, 0.30]",
    )

    macro_amplitude = float(
        args.macro_amplitude
    )

    must(
        math.isfinite(
            macro_amplitude
        )
        and macro_amplitude > 0.0,
        "future macroscopic strain amplitude is finite and positive",
    )

    must(
        args.load_case
        in {
            "X",
            "Y",
            "XY",
        },
        "future load case belongs to permanent X/Y/XY set",
    )

    # --------------------------------------------------------
    # Contract summary only — deliberately no mechanics.
    # --------------------------------------------------------

    print()
    print(
        "particle identity =",
        particle_identity,
    )

    print(
        "defective geometry identity =",
        geometry_identity,
    )

    print(
        "state =",
        "defective",
    )

    print(
        "mesh size =",
        mesh_size,
    )

    print(
        "load case =",
        args.load_case,
    )

    print(
        "macro amplitude =",
        macro_amplitude,
    )

    print(
        "Ep/Em =",
        ep_over_em,
    )

    print(
        "reserved PBC load schema =",
        PBC_LOAD_SCHEMA,
    )

    print(
        "future output =",
        args.output,
    )

    print(
        "PASS — protected pristine src/22 remains a separate solver lineage"
    )

    if selected_preflight_modes == 0:
        must(
            not args.output.exists(),
            "permanent load-validation output does not already exist",
        )

        print()
        print(
            "Executing permanent true-hole PBC load validation..."
        )

        permanent_local_response_required = (
            args.load_case == "X"
        )

        permanent_response = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            create_linear_problem=True,
            solve_problem=True,
            evaluate_response=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
            physical_voids=(
                physical_voids
                if permanent_local_response_required
                else None
            ),
            evaluate_quadrature_local_response=(
                permanent_local_response_required
            ),
            quadrature_degree=(
                STEP9_PRODUCTION_QUADRATURE_DEGREE
                if permanent_local_response_required
                else None
            ),
        )

        must(
            permanent_response[
                "fem_solve_performed"
            ]
            is True,
            "permanent load validation requires an authenticated FEM solve",
        )

        must(
            permanent_response[
                "response_evaluated"
            ]
            is True,
            "permanent load validation requires an authenticated homogenized response",
        )

        must(
            permanent_response[
                "response_positive_component_index"
            ]
            in (
                0,
                1,
                2,
            ),
            "permanent response carries a valid generalized load-direction component index",
        )

        protected_positive_component_map = {
            "X": 0,
            "Y": 1,
            "XY": 2,
        }

        must(
            permanent_response[
                "response_positive_component_index"
            ]
            ==
            protected_positive_component_map[
                args.load_case
            ],
            "permanent response positivity index matches protected X/Y/XY mapping",
        )

        permanent_rve_level = "R1"

        permanent_gross_area = float(
            width
            * height
        )

        must(
            permanent_gross_area > 0.0,
            "permanent output gross RVE area is positive",
        )

        permanent_source_sha256 = (
            hashlib.sha256(
                Path(
                    __file__
                ).read_bytes()
            ).hexdigest()
        )

        permanent_config_sha256 = (
            hashlib.sha256(
                args.config.read_bytes()
            ).hexdigest()
        )

        if permanent_local_response_required:
            must(
                permanent_response["quadrature_local_response_evaluated"] is True,
                "permanent Step-9 X load evaluated quadrature local response",
            )
            must(
                permanent_response["quadrature_local_degree"]
                == STEP9_PRODUCTION_QUADRATURE_DEGREE,
                "permanent Step-9 X local response uses quadrature degree 8",
            )
            permanent_local_response = permanent_response[
                "quadrature_local_response"
            ]
            must(
                isinstance(permanent_local_response, dict)
                and permanent_local_response.get("status") == "valid",
                "permanent Step-9 X local response is valid",
            )
            must(
                permanent_local_response.get("metric_id") == STEP9_LOCAL_METRIC_ID,
                "permanent Step-9 X local metric identifier is exact",
            )
            must(
                int(permanent_local_response["physical_void_count"]) == void_count,
                "permanent Step-9 X local response uses all physical voids",
            )
            must(
                math.isclose(
                    float(permanent_local_response["normalization_abs_Sigma_11"]),
                    abs(float(permanent_response["response_stress_voigt"][0])),
                    rel_tol=0.0, abs_tol=1.0e-12,
                ),
                "permanent Step-9 X local normalization uses exact abs(Sigma_11)",
            )
        else:
            must(
                permanent_response["quadrature_local_response_evaluated"] is False,
                "Y/XY permanent loads do not invent an X-only local metric",
            )
            permanent_local_response = None

        permanent_output = {
            "schema":
                PBC_LOAD_SCHEMA,

            "status":
                "validated",

            "case": {
                "rve_level":
                    permanent_rve_level,

                "state":
                    "defective",

                "void_count":
                    void_count,

                "load_case":
                    args.load_case,

                "macro_amplitude":
                    float(
                        macro_amplitude
                    ),

                "macroscopic_strain_authority":
                    "prescribed_E_bar",

                "macroscopic_strain_matrix":
                    permanent_response[
                        "macro_strain_matrix"
                    ],

                "macroscopic_strain_voigt":
                    permanent_response[
                        "macro_strain_voigt"
                    ],
            },

            "provenance": {
                "solver_source":
                    str(
                        Path(
                            __file__
                        )
                    ),

                "solver_source_sha256":
                    permanent_source_sha256,

                "mesh":
                    str(
                        args.mesh
                    ),

                "mesh_sha256":
                    args.expected_mesh_sha256,

                "mesh_diagnostics":
                    str(
                        args.mesh_diagnostics
                    ),

                "mesh_diagnostics_sha256":
                    args.expected_mesh_diagnostics_sha256,

                "geometry_json":
                    str(
                        args.geometry_json
                    ),

                "geometry_sha256":
                    args.expected_geometry_sha256,

                "geometry_identity_sha256":
                    geometry_identity,

                "geometry_state":
                    "defective",

                "material_config":
                    str(
                        args.config
                    ),

                "material_config_sha256":
                    permanent_config_sha256,

                "requested_output":
                    str(
                        args.output
                    ),
            },

            "model": {
                "dimension":
                    2,

                "assumption":
                    "plane_stress",

                "interface":
                    "perfect_bonding",

                "matrix": {
                    "youngs_modulus":
                        float(
                            matrix_E
                        ),

                    "poissons_ratio":
                        float(
                            matrix_nu
                        ),
                },

                "particle": {
                    "youngs_modulus":
                        float(
                            particle_E
                        ),

                    "poissons_ratio":
                        float(
                            particle_nu
                        ),

                    "stiffness_ratio_to_matrix":
                        float(
                            ep_over_em
                        ),
                },

                "void": {
                    "representation":
                        "true_hole",

                    "constitutive_volume_phase":
                        False,

                    "constitutive_stress_contribution":
                        False,

                    "constitutive_energy_contribution":
                        False,
                },
            },

            "mesh": {
                "cells":
                    permanent_response[
                        "cell_count"
                    ],

                "matrix_cells":
                    permanent_response[
                        "matrix_cell_count"
                    ],

                "particle_cells":
                    permanent_response[
                        "particle_cell_count"
                    ],

                "matrix_area":
                    permanent_response[
                        "response_runtime_matrix_area"
                    ],

                "particle_area":
                    permanent_response[
                        "response_runtime_particle_area"
                    ],

                "material_area":
                    permanent_response[
                        "response_runtime_material_area"
                    ],

                "void_area":
                    permanent_response[
                        "response_runtime_void_area"
                    ],

                "gross_area":
                    permanent_gross_area,

                "area_authority":
                    "discrete_FE_mesh",
            },

            "mpc": {
                "scalar_slave_dofs":
                    permanent_response[
                        "scalar_slave_count"
                    ],

                "periodic_slave_blocks":
                    permanent_response[
                        "periodic_slave_block_count"
                    ],

                "unique_master_dofs":
                    permanent_response[
                        "unique_master_count"
                    ],

                "minimum_master_count":
                    permanent_response[
                        "minimum_master_count"
                    ],

                "maximum_master_count":
                    permanent_response[
                        "maximum_master_count"
                    ],

                "slave_master_overlap":
                    permanent_response[
                        "slave_master_overlap_count"
                    ],

                "component_mismatch_count":
                    permanent_response[
                        "component_mismatch_count"
                    ],

                "max_coefficient_error":
                    permanent_response[
                        "maximum_coefficient_error"
                    ],

                "max_mapping_error":
                    permanent_response[
                        "maximum_mapping_error"
                    ],
            },

            "gauge": {
                "block":
                    permanent_response[
                        "gauge_block"
                    ],

                "coordinate":
                    permanent_response[
                        "gauge_coordinate"
                    ],

                "scalar_dofs":
                    permanent_response[
                        "gauge_scalar_dofs"
                    ],

                "bc_scalar_dofs":
                    permanent_response[
                        "gauge_bc_scalar_dofs"
                    ],

                "values":
                    permanent_response[
                        "gauge_bc_value"
                    ],

                "max_abs":
                    permanent_response[
                        "solve_gauge_max_abs"
                    ],
            },

            "solver": {
                "solver_type":
                    permanent_response[
                        "linear_problem_solver_type"
                    ],

                "pc_type":
                    permanent_response[
                        "linear_problem_pc_type"
                    ],

                "convergence_reason":
                    permanent_response[
                        "solve_petsc_convergence_reason"
                    ],

                "iterations":
                    permanent_response[
                        "solve_petsc_iterations"
                    ],

                "algebraic_residual_norm":
                    permanent_response[
                        "solve_algebraic_residual_norm"
                    ],

                "rhs_norm":
                    permanent_response[
                        "solve_rhs_norm"
                    ],

                "algebraic_relative_residual":
                    permanent_response[
                        "solve_algebraic_relative_residual"
                    ],
            },

            "periodicity": {
                "checked_slave_blocks":
                    permanent_response[
                        "periodic_slave_block_count"
                    ],

                "fluctuation_max_abs_mismatch":
                    permanent_response[
                        "solve_periodic_max_abs_error"
                    ],

                "reference_scale":
                    permanent_response[
                        "solve_periodic_reference_scale"
                    ],

                "normalized_error":
                    permanent_response[
                        "solve_periodic_normalized_error"
                    ],
            },

            "response": {
                "macroscopic_strain_authority":
                    "prescribed_E_bar",

                "stress_tensor":
                    permanent_response[
                        "response_stress_tensor"
                    ],

                "stress_voigt":
                    permanent_response[
                        "response_stress_voigt"
                    ],

                "stiffness_column":
                    permanent_response[
                        "response_stiffness_column"
                    ],

                "response_stiffness_column_normalized_by_E_matrix":
                    permanent_response[
                        "response_stiffness_column_normalized_by_E_matrix"
                    ],

                "positive_component_index":
                    permanent_response[
                        "response_positive_component_index"
                    ],

                "positive_component_mapping":
                    protected_positive_component_map,

                "isotropy_projection_applied":
                    False,
            },

            "energy": {
                "micro_energy_density":
                    permanent_response[
                        "response_micro_energy_density"
                    ],

                "macro_energy_density":
                    permanent_response[
                        "response_macro_energy_density"
                    ],

                "hill_mandel_relative_mismatch":
                    permanent_response[
                        "response_hill_mandel_relative_mismatch"
                    ],

                "weak_stationarity_value":
                    permanent_response[
                        "response_weak_stationarity_value"
                    ],

                "weak_stationarity_relative":
                    permanent_response[
                        "response_weak_stationarity_relative"
                    ],
            },

            "local_response": {
                "applicable": permanent_local_response_required,
                "load_case_authority": "X",
                "quadrature_degree": (
                    STEP9_PRODUCTION_QUADRATURE_DEGREE
                    if permanent_local_response_required
                    else None
                ),
                "metric": permanent_local_response,
            },

            "scope_guard": {
                "m9_step9_transfer_validation": True,
                "m9_stochastic_pilot_production": False,
                "production_design_id_created": False,
                "production_realization_id_created": False,
                "production_pilot_sampling_rng_consumed": False,
                "step9_raw_root_owned": False,
                "production_raw_root_owned": False,
                "geometry_regenerated": False,
                "mesh_generated": False,
                "mpc_constructed": True,
                "fem_solve_performed": True,
                "tensor_reconstructed": False,
                "machine_learning_performed": False,
            },

            "deferred_until_all_three_loads": {
                "full_homogenized_stiffness_tensor":
                    True,

                "compliance_tensor":
                    True,

                "engineering_constants":
                    True,

                "cross_load_symmetry_audit":
                    True,

                "isotropy_projection":
                    False,
            },

            "raw_sigma_h_n_is_hard_gate":
                False,

            "fem_solve_performed":
                permanent_response[
                    "fem_solve_performed"
                ],

            "response_evaluated":
                permanent_response[
                    "response_evaluated"
                ],

            "stochastic_pilot_authorized_by_this_output":
                False,

            "machine_learning_performed":
                False,

            "repository_files_created": [
                str(
                    args.output
                ),
            ],
        }

        must(
            abs(
                (
                    float(
                        permanent_output[
                            "mesh"
                        ][
                            "matrix_area"
                        ]
                    )
                    +
                    float(
                        permanent_output[
                            "mesh"
                        ][
                            "particle_area"
                        ]
                    )
                )
                -
                float(
                    permanent_output[
                        "mesh"
                    ][
                        "material_area"
                    ]
                )
            )
            <= 1.0e-10,
            "permanent output matrix + particle area closes to material area",
        )

        must(
            abs(
                (
                    float(
                        permanent_output[
                            "mesh"
                        ][
                            "material_area"
                        ]
                    )
                    +
                    float(
                        permanent_output[
                            "mesh"
                        ][
                            "void_area"
                        ]
                    )
                )
                -
                float(
                    permanent_output[
                        "mesh"
                    ][
                        "gross_area"
                    ]
                )
            )
            <= 1.0e-10,
            "permanent output material + void area closes to gross area",
        )

        must(
            float(
                permanent_output[
                    "mesh"
                ][
                    "void_area"
                ]
            )
            > 0.0,
            "permanent true-hole output retains positive void area",
        )

        permanent_json_text = (
            json.dumps(
                permanent_output,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
            + "\n"
        )

        must(
            not args.output.exists(),
            "permanent output remains absent immediately before exclusive creation",
        )

        args.output.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with args.output.open(
            "x",
            encoding="utf-8",
        ) as permanent_handle:
            permanent_handle.write(
                permanent_json_text
            )

        permanent_output_sha256 = (
            hashlib.sha256(
                args.output.read_bytes()
            ).hexdigest()
        )

        print()
        print(
            "PERMANENT_LOAD_VALIDATION_PATH=",
            args.output,
        )

        print(
            "PERMANENT_LOAD_VALIDATION_SHA256=",
            permanent_output_sha256,
        )

        print(
            "PASS — permanent result was created using exclusive non-overwrite semantics"
        )

        print(
            "PASS — permanent result uses deterministic strict JSON serialization"
        )

        print(
            "PASS — permanent result represents exactly one requested load case"
        )

        print(
            "PASS — prescribed E_bar remains the macroscopic strain authority"
        )

        print(
            "PASS — true-hole matrix/particle/void FE area accounting is retained"
        )

        print(
            "PASS — no full stiffness tensor or compliance was reconstructed in the per-load writer"
        )

        print(
            "PASS — no isotropy projection or ML occurred"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_LOAD_VALIDATION_OK"
        )

    elif args.quadrature_local_preflight_only:
        must(
            args.load_case == "X",
            "quadrature-local preflight is restricted to the Step-9 X PBC load",
        )
        must(
            isinstance(state.get("voids"), list),
            "selected geometry state exposes physical void records",
        )
        q_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            create_linear_problem=True,
            solve_problem=True,
            evaluate_response=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
            physical_voids=state["voids"],
            evaluate_quadrature_local_response=True,
            quadrature_degree=args.quadrature_degree,
        )
        must(
            q_preflight["fem_solve_performed"] is True,
            "quadrature-local preflight reused exactly one authenticated FEM solve path",
        )
        must(
            q_preflight["response_evaluated"] is True,
            "quadrature-local preflight reused authenticated response evaluation",
        )
        must(
            q_preflight["quadrature_local_response_evaluated"] is True,
            "quadrature-local preflight evaluated the M8 quadrature response",
        )
        must(
            q_preflight["quadrature_local_degree"] == args.quadrature_degree,
            "quadrature-local diagnostics retain the explicit requested degree",
        )
        must(
            isinstance(q_preflight["quadrature_local_response"], dict)
            and q_preflight["quadrature_local_response"]["status"] == "valid",
            "quadrature-local preflight returned valid diagnostics",
        )
        print()
        print(
            "True-hole quadrature local-response preflight diagnostics = "
            + json.dumps(q_preflight["quadrature_local_response"], sort_keys=True)
        )
        print()
        print("PASS — explicit validation quadrature degree was supplied")
        print("PASS — authoritative physical void records were used")
        print("PASS — physical quadrature coordinates and area weights were used")
        print("PASS — quadrature weights reproduce runtime matrix area")
        print("PASS — local normalization used gross-RVE abs(Sigma_11)")
        print("PASS — permanent load-validation JSON was not written")
        print("PASS — no production quadrature degree/order was selected")
        print("PASS — no twelve-case local target-mesh study was executed")
        print("PASS — no machine learning occurred")
        print()
        print("M9_STEP9_VOID_PBC_QUADRATURE_LOCAL_PREFLIGHT_OK")

    elif args.cell_local_preflight_only:
        must(
            args.load_case == "X",
            "cell-local preflight is restricted to the Step-9 X PBC load",
        )

        must(
            isinstance(
                state.get(
                    "voids"
                ),
                list,
            ),
            "selected geometry state exposes physical void records",
        )

        cell_local_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            create_linear_problem=True,
            solve_problem=True,
            evaluate_response=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
            evaluate_local_response=True,
            physical_voids=state[
                "voids"
            ],
        )

        must(
            cell_local_preflight[
                "fem_solve_performed"
            ]
            is True,
            "cell-local preflight reused exactly one authenticated FEM solve path",
        )

        must(
            cell_local_preflight[
                "response_evaluated"
            ]
            is True,
            "cell-local preflight reused authenticated homogenized response evaluation",
        )

        must(
            cell_local_preflight[
                "local_response_evaluated"
            ]
            is True,
            "cell-local preflight evaluated the M8 cell local response",
        )

        must(
            isinstance(
                cell_local_preflight[
                    "local_response"
                ],
                dict,
            ),
            "cell-local preflight returned local-response diagnostics",
        )

        must(
            cell_local_preflight[
                "local_response"
            ][
                "status"
            ]
            == "valid",
            "cell-local preflight local-response status is valid",
        )

        print()
        print(
            "True-hole cell local-response preflight diagnostics = "
            + json.dumps(
                cell_local_preflight[
                    "local_response"
                ],
                sort_keys=True,
            )
        )

        print()
        print(
            "PASS — selected physical void records were handed to permanent src/26"
        )
        print(
            "PASS — periodic computational void representations were not used"
        )
        print(
            "PASS — owned matrix-cell midpoint von-Mises extraction used physical cell areas"
        )
        print(
            "PASS — local normalization used gross-RVE abs(Sigma_11)"
        )
        print(
            "PASS — permanent load-validation JSON was not written"
        )
        print(
            "PASS — quadrature implementation/order remains deferred"
        )
        print(
            "PASS — no twelve-case local target-mesh study was executed"
        )
        print(
            "PASS — no machine learning occurred"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_CELL_LOCAL_PREFLIGHT_OK"
        )

    elif args.response_preflight_only:
        response_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            create_linear_problem=True,
            solve_problem=True,
            evaluate_response=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
        )

        print()
        print(
            "True-hole homogenized response preflight diagnostics = "
            + json.dumps(
                response_preflight,
                sort_keys=True,
            )
        )

        print(
            "PASS — authenticated requested-load MPC/FEM solve was reconstructed"
        )

        print(
            "PASS — discrete matrix/particle/void FE areas were authenticated"
        )

        print(
            "PASS — requested-load gross-area homogenized stress response was evaluated"
        )

        print(
            "PASS — only the single requested-load stiffness column was reconstructed"
        )

        print(
            "PASS — Hill-Mandel and weak-stationarity response gates were evaluated"
        )

        print(
            "PASS — no full homogenized stiffness tensor was reconstructed"
        )

        print(
            "PASS — no other load case or expanded scientific scope was executed"
        )

        print(
            "PASS — no permanent load-validation JSON was written"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_RESPONSE_PREFLIGHT_OK"
        )

    elif args.solve_preflight_only:



        solve_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            create_linear_problem=True,
            solve_problem=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
        )

        print()
        print(
            "Void-PBC solve preflight diagnostics = "
            + json.dumps(
                solve_preflight,
                sort_keys=True,
            )
        )

        print(
            "PASS — authenticated MPC/gauge/forms/LinearProblem layers were reconstructed"
        )

        print(
            "PASS — exactly one requested-load public LinearProblem solve was performed"
        )

        print(
            "PASS — PETSc convergence, finite solution, gauge and periodicity were authenticated"
        )

        print(
            "PASS — constrained algebraic residual was authenticated"
        )

        print(
            "PASS — no constitutive stress response was evaluated"
        )

        print(
            "PASS — no homogenized stress or stiffness tensor was reconstructed"
        )

        print(
            "PASS — no local-response extraction or ML occurred"
        )

        print(
            "PASS — reserved load-validation JSON was not written"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_SOLVE_PREFLIGHT_OK"
        )

    elif args.linear_problem_preflight_only:
        linear_problem_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            create_linear_problem=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
        )

        print()
        print(
            "LinearProblem construction preflight diagnostics = "
            + json.dumps(
                linear_problem_preflight,
                sort_keys=True,
            )
        )

        print(
            "PASS — periodic MPC, deterministic gauge and heterogeneous forms were reconstructed"
        )

        print(
            "PASS — MPC-aware LinearProblem was constructed"
        )

        print(
            "PASS — PETSc matrix/RHS/solution structures are dimensionally consistent"
        )

        print(
            "PASS — dedicated preonly/LU solver configuration was installed"
        )

        print(
            "PASS — LinearProblem.solve was not called"
        )

        print(
            "PASS — no FEM system values were assembled or solved"
        )

        print(
            "PASS — no stress recovery or stiffness tensor reconstruction occurred"
        )

        print(
            "PASS — no local-response extraction or ML occurred"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_LINEAR_PROBLEM_PREFLIGHT_OK"
        )

    elif args.form_preflight_only:
        form_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
            create_forms=True,
            load_case=args.load_case,
            macro_amplitude=macro_amplitude,
            matrix_E=matrix_E,
            matrix_nu=matrix_nu,
            particle_E=particle_E,
            particle_nu=particle_nu,
        )

        print()
        print(
            "Material/UFL form preflight diagnostics = "
            + json.dumps(
                form_preflight,
                sort_keys=True,
            )
        )

        print(
            "PASS — periodic MPC topology and deterministic gauge were reconstructed"
        )

        print(
            "PASS — plane-stress matrix/particle constitutive constants were created"
        )

        print(
            "PASS — requested engineering X/Y/XY macro strain was constructed"
        )

        print(
            "PASS — heterogeneous matrix/particle UFL forms were created and compiled"
        )

        print(
            "PASS — true-hole void boundary contributes no material volume term"
        )

        print(
            "PASS — no PETSc matrix/vector was assembled"
        )

        print(
            "PASS — no LinearProblem was created"
        )

        print(
            "PASS — no FEM solve was performed"
        )

        print(
            "PASS — no stiffness tensor was reconstructed"
        )

        print(
            "PASS — no local-response extraction or ML occurred"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_FORM_PREFLIGHT_OK"
        )

    elif args.gauge_preflight_only:
        gauge_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
            create_gauge_bc=True,
        )

        print()
        print(
            "Gauge BC preflight diagnostics = "
            + json.dumps(
                gauge_preflight,
                sort_keys=True,
            )
        )

        print(
            "PASS — periodic MPC topology was reconstructed and authenticated"
        )

        print(
            "PASS — deterministic interior gauge candidate was reconstructed"
        )

        print(
            "PASS — zero-displacement Dirichlet gauge BC was created"
        )

        print(
            "PASS — Dirichlet gauge targets exactly both deterministic gauge components"
        )

        print(
            "PASS — no UFL/FEM constitutive form was created"
        )

        print(
            "PASS — no FEM system was assembled or solved"
        )

        print(
            "PASS — no stiffness tensor was reconstructed"
        )

        print(
            "PASS — no local-response extraction or ML occurred"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_GAUGE_PREFLIGHT_OK"
        )

    elif args.mpc_preflight_only:
        mpc_preflight = run_mpc_topology_preflight(
            args.mesh,
            mesh_diag,
            width,
            height,
        )

        print()
        print(
            "MPC topology preflight diagnostics = "
            + json.dumps(
                mpc_preflight,
                sort_keys=True,
            )
        )

        print(
            "PASS — periodic MPC topology was constructed and authenticated"
        )

        print(
            "PASS — deterministic interior gauge candidate was identified"
        )

        print(
            "PASS — no Dirichlet gauge BC was created"
        )

        print(
            "PASS — no UFL/FEM constitutive form was created"
        )

        print(
            "PASS — no FEM system was assembled or solved"
        )

        print(
            "PASS — no stiffness tensor was reconstructed"
        )

        print(
            "PASS — no local-response extraction or ML occurred"
        )

        print()
        print(
            "M9_STEP9_VOID_PBC_MPC_TOPOLOGY_PREFLIGHT_OK"
        )

    else:
        print(
            "PASS — no DOLFINx import was performed by src/30 input-contract path"
        )

        print(
            "PASS — no dolfinx_mpc import or MPC construction was performed"
        )

        print(
            "PASS — no FEM form was assembled or solved"
        )

        print(
            "PASS — no stiffness tensor was reconstructed"
        )

        print(
            "PASS — no local-response extraction or ML occurred"
        )

    print()
    print(
        "M9_STEP9_VOID_PBC_INPUT_CONTRACT_OK"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
