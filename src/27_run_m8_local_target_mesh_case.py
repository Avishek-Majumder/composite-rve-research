"""Durable per-case Stage-8 local target-mesh writer.

This source executes exactly one authenticated X-load true-hole PBC solve for
one predeclared R1 defect-state/mesh combination, evaluates both permanent M8
local-response methods from the same solved field, and writes one deterministic
JSON result.  It performs no cross-case comparison and no machine learning.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path

import yaml


CASE_SCHEMA = "m8_local_target_mesh_case_v1"
LOAD_CASE = "X"
MACRO_AMPLITUDE = 0.01
PRODUCTION_QUADRATURE_DEGREE = 8
EXPECTED_MESH_SIZES = {
    "h_0p02048": 0.02048,
    "h_0p010": 0.010,
}
MPC_PYTHON = Path(
    "/home/avishek/miniforge3/envs/composite-sim-m8-mpc-compat/bin/python"
)

AUTHORITIES = {
    "M8_TARGET_MESH_PROTOCOL.md":
        "0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f",
    "src/25_solve_m8_periodized_void_pbc.py":
        "b97f5add78d712dee1dc7564e6dce3f6cf08e7c1bee9562522e3344483e230dc",
    "src/26_m8_local_response.py":
        "d73423d4e41fdc686e8bfd0825c0bead0c82103ec423fceb91e8b60d001bbaae",
    "configs/03_parametric_rve_base.yaml":
        "f9dbb565bc2eeaa9166eac4a721de1f1d1f47474ecaf13ec567c5627614351dd",
}


def must(condition: bool, message: str) -> None:
    if condition:
        print(f"PASS — {message}")
        return
    print(f"FAIL — DO NOT CONTINUE: {message}")
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha256(value: str, label: str) -> str:
    normalized = value.strip().lower()
    must(
        len(normalized) == 64
        and all(character in "0123456789abcdef" for character in normalized),
        f"{label} is canonical SHA256 text",
    )
    return normalized


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    must(
        spec is not None and spec.loader is not None,
        f"{name} module specification is loadable",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Run exactly one authenticated Stage-8 R1 defect local target-mesh "
            "case with both permanent local metrics."
        )
    )
    parser.add_argument(
        "--realization",
        type=int,
        choices=range(1, 7),
        required=True,
    )
    parser.add_argument(
        "--state",
        choices=["baseline", "high_severity"],
        required=True,
    )
    parser.add_argument(
        "--mesh-label",
        choices=sorted(EXPECTED_MESH_SIZES),
        required=True,
    )
    parser.add_argument("--mesh", type=Path, required=True)
    parser.add_argument("--expected-mesh-sha256", required=True)
    parser.add_argument("--mesh-diagnostics", type=Path, required=True)
    parser.add_argument(
        "--expected-mesh-diagnostics-sha256",
        required=True,
    )
    parser.add_argument(
        "--geometry-family-json",
        type=Path,
        required=True,
    )
    parser.add_argument("--expected-family-sha256", required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/03_parametric_rve_base.yaml"),
    )
    parser.add_argument(
        "--load-case",
        choices=["X"],
        default="X",
    )
    parser.add_argument(
        "--macro-amplitude",
        type=float,
        default=MACRO_AMPLITUDE,
    )
    parser.add_argument(
        "--quadrature-degree",
        type=int,
        choices=[PRODUCTION_QUADRATURE_DEGREE],
        default=PRODUCTION_QUADRATURE_DEGREE,
    )
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo = Path(__file__).resolve().parents[1]

    print("=== M8 STAGE-8 LOCAL TARGET-MESH CASE ===")

    must(
        Path(sys.executable).resolve() == MPC_PYTHON.resolve(),
        "execution uses exact isolated M8 MPC compatibility Python",
    )
    must(
        os.environ.get("CONDA_DEFAULT_ENV")
        == "composite-sim-m8-mpc-compat",
        "isolated M8 MPC compatibility environment is active",
    )

    for relative, expected in AUTHORITIES.items():
        path = repo / relative
        must(path.is_file(), f"authority exists: {relative}")
        actual = sha256_file(path)
        print(f"{relative} SHA256 = {actual}")
        must(
            actual == expected,
            f"authority SHA authenticated: {relative}",
        )

    expected_mesh_path = (
        Path(
            "results/raw/04_m8_target_mesh/"
            "periodized_void_mesh/R1"
        )
        / f"realization_{args.realization:04d}"
        / args.state
        / args.mesh_label
        / "mesh.msh"
    )
    expected_diag_path = (
        expected_mesh_path.with_name(
            "mesh_diagnostics.json"
        )
    )
    expected_family_path = (
        Path(
            "results/raw/04_m8_target_mesh/"
            "periodized_void_geometry/R1"
        )
        / f"realization_{args.realization:04d}"
        / "geometry_family.json"
    )
    expected_output_path = (
        Path(
            "results/raw/04_m8_target_mesh/"
            "local_target_mesh_cases/R1"
        )
        / f"realization_{args.realization:04d}"
        / args.state
        / args.mesh_label
        / "local_response.json"
    )

    must(
        args.mesh == expected_mesh_path,
        "runtime mesh path is exact for requested case",
    )
    must(
        args.mesh_diagnostics == expected_diag_path,
        "runtime mesh-diagnostics path is exact for requested case",
    )
    must(
        args.geometry_family_json == expected_family_path,
        "runtime geometry-family path is exact for requested realization",
    )
    must(
        args.output == expected_output_path,
        "durable output path is exact for requested case",
    )

    for path, label in (
        (args.mesh, "runtime mesh"),
        (
            args.mesh_diagnostics,
            "runtime mesh diagnostics",
        ),
        (
            args.geometry_family_json,
            "runtime geometry family",
        ),
        (args.config, "runtime material config"),
    ):
        must(
            path.is_file(),
            f"{label} exists",
        )

    must(
        not args.output.exists(),
        "durable case output is absent before execution",
    )

    expected_mesh_sha = canonical_sha256(
        args.expected_mesh_sha256,
        "expected mesh SHA256",
    )
    expected_diag_sha = canonical_sha256(
        args.expected_mesh_diagnostics_sha256,
        "expected mesh-diagnostics SHA256",
    )
    expected_family_sha = canonical_sha256(
        args.expected_family_sha256,
        "expected family SHA256",
    )

    actual_mesh_sha = sha256_file(args.mesh)
    actual_diag_sha = sha256_file(
        args.mesh_diagnostics
    )
    actual_family_sha = sha256_file(
        args.geometry_family_json
    )

    print("mesh SHA256 =", actual_mesh_sha)
    print(
        "mesh diagnostics SHA256 =",
        actual_diag_sha,
    )
    print(
        "geometry family SHA256 =",
        actual_family_sha,
    )

    must(
        actual_mesh_sha == expected_mesh_sha,
        "runtime mesh SHA256 authenticated",
    )
    must(
        actual_diag_sha == expected_diag_sha,
        "runtime mesh-diagnostics SHA256 authenticated",
    )
    must(
        actual_family_sha == expected_family_sha,
        "runtime geometry-family SHA256 authenticated",
    )

    solver_path = (
        repo
        / "src/25_solve_m8_periodized_void_pbc.py"
    )
    solver = load_module(
        solver_path,
        "_m8_stage8_src25",
    )

    must(
        solver.M8_PRODUCTION_QUADRATURE_DEGREE
        == PRODUCTION_QUADRATURE_DEGREE,
        (
            "src/25 production quadrature degree "
            "agrees with Stage-8 writer"
        ),
    )

    for relative, expected in solver.AUTHORITIES.items():
        dependency = repo / relative
        must(
            dependency.is_file(),
            f"src/25 dependency exists: {relative}",
        )
        must(
            sha256_file(dependency) == expected,
            (
                "src/25 dependency SHA authenticated: "
                f"{relative}"
            ),
        )

    family = json.loads(
        args.geometry_family_json.read_text(
            encoding="utf-8"
        )
    )

    must(
        family.get("schema")
        == solver.FAMILY_SCHEMA,
        "geometry-family schema authenticated",
    )
    must(
        family.get("status") == "valid"
        and family.get("failure_reason") is None,
        "geometry-family status is valid",
    )
    must(
        set(
            family.get(
                "states",
                {},
            )
        )
        == {
            "baseline",
            "high_severity",
        },
        (
            "geometry family retains exactly "
            "both paired states"
        ),
    )
    must(
        all(
            value is True
            for value in family[
                "checks"
            ].values()
        ),
        "all geometry-family checks PASS",
    )

    state = family[
        "states"
    ][
        args.state
    ]

    must(
        state["state"] == args.state,
        "selected geometry state is self-consistent",
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
        isinstance(
            physical_voids,
            list,
        ),
        (
            "selected state exposes canonical "
            "state['voids']"
        ),
    )
    must(
        len(
            physical_voids
        )
        == 4,
        (
            "selected state retains exactly "
            "four physical voids"
        ),
    )

    expected_radius = (
        0.025
        if args.state == "baseline"
        else 0.0275
    )

    must(
        all(
            math.isclose(
                float(
                    void[
                        "radius"
                    ]
                ),
                expected_radius,
                rel_tol=0.0,
                abs_tol=0.0,
            )
            for void
            in physical_voids
        ),
        (
            "selected state retains exact "
            "protocol void radius"
        ),
    )

    width = float(
        family[
            "rve"
        ][
            "width"
        ]
    )
    height = float(
        family[
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
                family[
                    "rve"
                ][
                    "area"
                ]
            ),
            gross_area,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "RVE area equals width*height",
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

    mesh_diag = json.loads(
        args.mesh_diagnostics.read_text(
            encoding="utf-8"
        )
    )

    must(
        mesh_diag.get(
            "schema"
        )
        == solver.MESH_SCHEMA,
        "mesh diagnostics schema authenticated",
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
        == args.state,
        (
            "mesh diagnostics state matches "
            "requested state"
        ),
    )
    must(
        mesh_diag[
            "source_family_sha256"
        ]
        == actual_family_sha,
        (
            "mesh diagnostics provenance matches "
            "authenticated family"
        ),
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
        "mesh diagnostics record exact mesh path",
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
        (
            "mesh diagnostics record exact "
            "diagnostics path"
        ),
    )
    must(
        mesh_diag[
            "physical_tags"
        ]
        == solver.EXPECTED_PHYSICAL_TAGS,
        (
            "mesh diagnostics physical-tag "
            "map is exact"
        ),
    )
    must(
        mesh_diag[
            "periodic_geometric_pairing_ready"
        ]
        is True,
        (
            "periodic geometric pairing "
            "is authenticated"
        ),
    )
    must(
        mesh_diag[
            "periodic_mesh_constraints_applied"
        ]
        is True,
        (
            "periodic mesh constraints "
            "are authenticated"
        ),
    )
    must(
        mesh_diag[
            "mesh_generated"
        ]
        is True,
        "runtime true-hole mesh is generated",
    )

    expected_mesh_size = (
        EXPECTED_MESH_SIZES[
            args.mesh_label
        ]
    )
    actual_mesh_size = float(
        mesh_diag[
            "mesh_size"
        ]
    )

    must(
        math.isclose(
            actual_mesh_size,
            expected_mesh_size,
            rel_tol=0.0,
            abs_tol=0.0,
        ),
        (
            "mesh diagnostics size matches "
            "requested mesh label exactly"
        ),
    )

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
        "material config dimension remains 2",
    )
    must(
        config[
            "model"
        ][
            "assumption"
        ]
        == "plane_stress",
        "material config remains plane stress",
    )
    must(
        config[
            "model"
        ][
            "interface"
        ]
        == "perfect_bonding",
        (
            "material config remains "
            "perfect bonding"
        ),
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
        matrix_E == 1000.0,
        "matrix reference modulus remains 1000",
    )
    must(
        particle_E == 10000.0,
        "particle modulus remains 10000",
    )
    must(
        matrix_nu == 0.30,
        "matrix Poisson ratio remains 0.30",
    )
    must(
        particle_nu == 0.25,
        "particle Poisson ratio remains 0.25",
    )
    must(
        particle_E
        / matrix_E
        == 10.0,
        (
            "particle/matrix stiffness ratio "
            "remains 10"
        ),
    )

    must(
        args.load_case == LOAD_CASE,
        (
            "Stage-8 local study is "
            "restricted to X load"
        ),
    )
    must(
        math.isclose(
            float(
                args.macro_amplitude
            ),
            MACRO_AMPLITUDE,
            rel_tol=0.0,
            abs_tol=0.0,
        ),
        (
            "macroscopic strain amplitude "
            "remains exactly 0.01"
        ),
    )
    must(
        args.quadrature_degree
        == PRODUCTION_QUADRATURE_DEGREE,
        (
            "production quadrature degree "
            "remains exactly 8"
        ),
    )

    print()
    print(
        "Executing exactly one authenticated "
        "X-load solve with both local metrics..."
    )

    response = solver.run_mpc_topology_preflight(
        args.mesh,
        mesh_diag,
        width,
        height,
        create_gauge_bc=True,
        create_forms=True,
        create_linear_problem=True,
        solve_problem=True,
        evaluate_response=True,
        load_case=LOAD_CASE,
        macro_amplitude=MACRO_AMPLITUDE,
        matrix_E=matrix_E,
        matrix_nu=matrix_nu,
        particle_E=particle_E,
        particle_nu=particle_nu,
        evaluate_local_response=True,
        physical_voids=physical_voids,
        evaluate_quadrature_local_response=True,
        quadrature_degree=(
            PRODUCTION_QUADRATURE_DEGREE
        ),
    )

    must(
        response[
            "fem_solve_performed"
        ]
        is True,
        (
            "exact case mechanics performed "
            "an FEM solve"
        ),
    )
    must(
        response[
            "response_evaluated"
        ]
        is True,
        "homogenized response was evaluated",
    )
    must(
        response[
            "local_response_evaluated"
        ]
        is True,
        "cell local response was evaluated",
    )
    must(
        response[
            "quadrature_local_response_evaluated"
        ]
        is True,
        (
            "quadrature local response "
            "was evaluated"
        ),
    )
    must(
        response[
            "quadrature_local_degree"
        ]
        == PRODUCTION_QUADRATURE_DEGREE,
        (
            "returned quadrature local degree "
            "is exactly 8"
        ),
    )
    must(
        response[
            "response_positive_component_index"
        ]
        == 0,
        (
            "X-load positive response component "
            "index is exactly zero"
        ),
    )

    stress_voigt = response[
        "response_stress_voigt"
    ]

    must(
        isinstance(
            stress_voigt,
            list,
        )
        and len(
            stress_voigt
        )
        == 3,
        (
            "homogenized stress Voigt vector "
            "has exactly three components"
        ),
    )
    must(
        all(
            math.isfinite(
                float(
                    value
                )
            )
            for value
            in stress_voigt
        ),
        (
            "homogenized stress Voigt "
            "vector is finite"
        ),
    )

    sigma_11 = float(
        stress_voigt[
            0
        ]
    )

    must(
        math.isfinite(
            sigma_11
        )
        and sigma_11 > 0.0,
        (
            "exported gross-RVE Sigma_11 "
            "is finite and positive"
        ),
    )

    cell = response[
        "local_response"
    ]
    quadrature = response[
        "quadrature_local_response"
    ]

    must(
        isinstance(
            cell,
            dict,
        ),
        "cell local response is a dictionary",
    )
    must(
        isinstance(
            quadrature,
            dict,
        ),
        (
            "quadrature local response "
            "is a dictionary"
        ),
    )
    must(
        cell.get(
            "status"
        )
        == "valid",
        "cell local response status is valid",
    )
    must(
        quadrature.get(
            "status"
        )
        == "valid",
        (
            "quadrature local response "
            "status is valid"
        ),
    )
    must(
        cell.get(
            "metric_id"
        )
        == "m8_matrix_vm_annulus_cell_tail10_v1",
        "cell local metric identifier is exact",
    )
    must(
        quadrature.get(
            "metric_id"
        )
        == (
            "m8_matrix_vm_annulus_"
            "quadrature_tail10_v1"
        ),
        (
            "quadrature local metric "
            "identifier is exact"
        ),
    )

    normalization = abs(
        sigma_11
    )

    must(
        math.isclose(
            float(
                cell[
                    "normalization_abs_Sigma_11"
                ]
            ),
            normalization,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        (
            "cell metric normalization equals "
            "abs(response_stress_voigt[0])"
        ),
    )
    must(
        math.isclose(
            float(
                quadrature[
                    "normalization_abs_Sigma_11"
                ]
            ),
            normalization,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        (
            "quadrature metric normalization equals "
            "abs(response_stress_voigt[0])"
        ),
    )

    for metric, label in (
        (cell, "cell"),
        (
            quadrature,
            "quadrature",
        ),
    ):
        k_value = float(
            metric[
                "K_vm_tail10"
            ]
        )
        must(
            math.isfinite(
                k_value
            )
            and k_value >= 0.0,
            (
                f"{label} K_vm_tail10 "
                "is finite and non-negative"
            ),
        )

    must(
        math.isfinite(
            float(
                response[
                    "response_hill_mandel_relative_mismatch"
                ]
            )
        ),
        (
            "Hill-Mandel relative mismatch "
            "is finite"
        ),
    )
    must(
        math.isfinite(
            float(
                response[
                    "response_weak_stationarity_relative"
                ]
            )
        ),
        (
            "weak-stationarity relative "
            "diagnostic is finite"
        ),
    )

    output = {
        "schema":
            CASE_SCHEMA,

        "status":
            "valid",

        "reason":
            None,

        "case": {
            "rve_level":
                "R1",

            "realization":
                int(
                    args.realization
                ),

            "state":
                args.state,

            "mesh_label":
                args.mesh_label,

            "mesh_size":
                float(
                    actual_mesh_size
                ),

            "load_case":
                LOAD_CASE,

            "macro_amplitude":
                float(
                    MACRO_AMPLITUDE
                ),

            "quadrature_degree":
                int(
                    PRODUCTION_QUADRATURE_DEGREE
                ),
        },

        "authorities": {
            **AUTHORITIES,

            "src25_embedded_dependencies":
                dict(
                    solver.AUTHORITIES
                ),
        },

        "inputs": {
            "mesh": {
                "path":
                    str(
                        args.mesh
                    ),

                "sha256":
                    actual_mesh_sha,
            },

            "mesh_diagnostics": {
                "path":
                    str(
                        args.mesh_diagnostics
                    ),

                "sha256":
                    actual_diag_sha,
            },

            "geometry_family": {
                "path":
                    str(
                        args.geometry_family_json
                    ),

                "sha256":
                    actual_family_sha,
            },

            "config": {
                "path":
                    str(
                        args.config
                    ),

                "sha256":
                    sha256_file(
                        args.config
                    ),
            },
        },

        "geometry": {
            "family_identity_sha256":
                str(
                    family[
                        "generated_geometry"
                    ][
                        "family_identity"
                    ][
                        "sha256"
                    ]
                ),

            "state_identity_sha256":
                str(
                    state[
                        "geometry_identity"
                    ][
                        "sha256"
                    ]
                ),

            "particle_identity_sha256":
                str(
                    family[
                        "source_particle_geometry"
                    ][
                        "geometry_identity_sha256"
                    ]
                ),

            "physical_voids":
                physical_voids,
        },

        "material_model": {
            "dimension":
                2,

            "assumption":
                "plane_stress",

            "interface":
                "perfect_bonding",

            "matrix": {
                "youngs_modulus":
                    matrix_E,

                "poissons_ratio":
                    matrix_nu,
            },

            "particle": {
                "youngs_modulus":
                    particle_E,

                "poissons_ratio":
                    particle_nu,

                "stiffness_ratio_to_matrix":
                    particle_E
                    / matrix_E,
            },

            "void": {
                "representation":
                    "true_hole",

                "constitutive_stress_contribution":
                    False,

                "constitutive_energy_contribution":
                    False,
            },
        },

        "macroscopic_response": {
            "Sigma_11":
                sigma_11,

            "stress_voigt":
                stress_voigt,

            "stress_tensor":
                response[
                    "response_stress_tensor"
                ],

            "stiffness_column":
                response[
                    "response_stiffness_column"
                ],

            "stiffness_column_normalized_by_E_matrix":
                response[
                    "response_stiffness_column_normalized_by_E_matrix"
                ],

            "hill_mandel_relative_mismatch":
                response[
                    "response_hill_mandel_relative_mismatch"
                ],

            "weak_stationarity_relative":
                response[
                    "response_weak_stationarity_relative"
                ],
        },

        "local_metrics": {
            "cell":
                cell,

            "quadrature":
                quadrature,
        },

        "solver_diagnostics":
            response,

        "scope_guard": {
            "single_case_mesh_execution":
                True,

            "x_load_only":
                True,

            "one_fem_solve_requested":
                True,

            "cell_local_metric_evaluated":
                True,

            "quadrature_local_metric_evaluated":
                True,

            "quadrature_degree_locked_to_8":
                True,

            "cross_case_comparison_performed":
                False,

            "target_mesh_decision_performed":
                False,

            "machine_learning_performed":
                False,

            "protected_m7_schema_mutated":
                False,

            "protected_pristine_m8_schema_mutated":
                False,
        },
    }

    json_text = (
        json.dumps(
            output,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n"
    )

    must(
        not args.output.exists(),
        (
            "durable output remains absent "
            "immediately before creation"
        ),
    )

    args.output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with args.output.open(
        "x",
        encoding="utf-8",
    ) as handle:
        handle.write(
            json_text
        )

    print()
    print(
        "durable Stage-8 case output =",
        args.output,
    )
    print(
        "durable Stage-8 case output SHA256 =",
        sha256_file(
            args.output
        ),
    )
    print(
        "cell K_vm_tail10 =",
        cell[
            "K_vm_tail10"
        ],
    )
    print(
        "quadrature K_vm_tail10 =",
        quadrature[
            "K_vm_tail10"
        ],
    )
    print(
        "Sigma_11 =",
        sigma_11,
    )

    print(
        "PASS — exactly one case/mesh result was written"
    )
    print(
        "PASS — no cross-case comparison or target-mesh decision occurred"
    )
    print(
        "PASS — no machine learning occurred"
    )

    print()
    print(
        "M8_LOCAL_TARGET_MESH_CASE_OK"
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
