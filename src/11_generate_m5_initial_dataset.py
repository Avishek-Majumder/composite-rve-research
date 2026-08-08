#!/usr/bin/env python3
"""Generate the M5 initial perfect-bonding FEM dataset.

The runner consumes the locked 60-case M4 Latin-hypercube design,
derives one temporary solver configuration per case, invokes the
validated parametric FEM solver, and records one machine-readable
success/failure envelope per case.

No defect model is introduced here.
"""

from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import json
import math
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]

DESIGN_PATH = ROOT / "results/processed/06_m4_lhs_initial_design.csv"
BASE_CONFIG_PATH = ROOT / "configs/03_parametric_rve_base.yaml"
SOLVER_PATH = ROOT / "src/10_parametric_rve_elasticity.py"

RAW_DIR = ROOT / "results/raw/02_m5_initial_dataset"
LOG_DIR = ROOT / "logs/02_m5_initial_dataset"

EXPECTED_HEADER = [
    "case_id",
    "unit_particle_fraction",
    "unit_stiffness_ratio",
    "unit_matrix_poissons_ratio",
    "unit_particle_poissons_ratio",
    "particle_fraction",
    "stiffness_ratio",
    "matrix_poissons_ratio",
    "particle_poissons_ratio",
    "particle_radius",
    "matrix_youngs_modulus",
    "particle_youngs_modulus",
    "center_x",
    "center_y",
    "prescribed_x_displacement",
    "mesh_size",
]

EXPECTED_CASE_IDS = [
    f"M4PB_{index:03d}"
    for index in range(1, 61)
]

REL_TOL = 1.0e-12
ABS_TOL = 1.0e-12

LOCKED_DIMENSION = 2
LOCKED_ASSUMPTION = "plane_stress"
LOCKED_INTERFACE = "perfect_bonding"

LOCKED_WIDTH = 1.0
LOCKED_HEIGHT = 1.0
LOCKED_MATRIX_E = 1000.0
LOCKED_CENTER_X = 0.5
LOCKED_CENTER_Y = 0.5
LOCKED_UX = 0.01
LOCKED_MESH_SIZE = 0.02048


def close(a: float, b: float) -> bool:
    """Return whether two floating-point values match tightly."""
    return math.isclose(
        float(a),
        float(b),
        rel_tol=REL_TOL,
        abs_tol=ABS_TOL,
    )


def finite_float(value: Any, label: str) -> float:
    """Convert a value to finite float or raise a clear error."""
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{label} is not a valid numeric value: {value!r}"
        ) from exc

    if not math.isfinite(result):
        raise ValueError(
            f"{label} must be finite, got {value!r}"
        )

    return result


def load_design() -> list[dict[str, str]]:
    """Load and fully validate the locked M4 design CSV."""
    if not DESIGN_PATH.is_file():
        raise FileNotFoundError(
            f"Locked design is missing: {DESIGN_PATH}"
        )

    with DESIGN_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        header = reader.fieldnames

    if header != EXPECTED_HEADER:
        raise ValueError(
            "Locked design header does not match the expected schema.\n"
            f"Actual:   {header}\n"
            f"Expected: {EXPECTED_HEADER}"
        )

    if len(rows) != 60:
        raise ValueError(
            f"Locked design must contain exactly 60 cases; "
            f"found {len(rows)}."
        )

    case_ids = [row["case_id"] for row in rows]

    if case_ids != EXPECTED_CASE_IDS:
        raise ValueError(
            "Locked design case IDs are not exactly "
            "M4PB_001 through M4PB_060 in order."
        )

    for row in rows:
        validate_design_row(row)

    return rows


def validate_design_row(row: dict[str, str]) -> None:
    """Validate one row against every locked M4 mapping."""
    case_id = row["case_id"]

    values = {
        key: finite_float(row[key], f"{case_id}:{key}")
        for key in EXPECTED_HEADER
        if key != "case_id"
    }

    u_phi = values["unit_particle_fraction"]
    u_ratio = values["unit_stiffness_ratio"]
    u_nu_m = values["unit_matrix_poissons_ratio"]
    u_nu_p = values["unit_particle_poissons_ratio"]

    phi = values["particle_fraction"]
    ratio = values["stiffness_ratio"]
    nu_m = values["matrix_poissons_ratio"]
    nu_p = values["particle_poissons_ratio"]

    radius = values["particle_radius"]
    matrix_E = values["matrix_youngs_modulus"]
    particle_E = values["particle_youngs_modulus"]

    cx = values["center_x"]
    cy = values["center_y"]
    ux = values["prescribed_x_displacement"]
    mesh_size = values["mesh_size"]

    checks = {
        "unit_particle_fraction":
            0.0 <= u_phi <= 1.0,
        "unit_stiffness_ratio":
            0.0 <= u_ratio <= 1.0,
        "unit_matrix_poissons_ratio":
            0.0 <= u_nu_m <= 1.0,
        "unit_particle_poissons_ratio":
            0.0 <= u_nu_p <= 1.0,

        "particle_fraction_bounds":
            0.05 <= phi <= 0.30,
        "stiffness_ratio_bounds":
            2.0 <= ratio <= 20.0,
        "matrix_poissons_ratio_bounds":
            0.20 <= nu_m <= 0.40,
        "particle_poissons_ratio_bounds":
            0.15 <= nu_p <= 0.35,

        "particle_fraction_mapping":
            close(phi, 0.05 + 0.25 * u_phi),
        "stiffness_ratio_mapping":
            close(ratio, 2.0 + 18.0 * u_ratio),
        "matrix_poissons_ratio_mapping":
            close(nu_m, 0.20 + 0.20 * u_nu_m),
        "particle_poissons_ratio_mapping":
            close(nu_p, 0.15 + 0.20 * u_nu_p),

        "particle_radius_mapping":
            close(
                radius,
                math.sqrt(
                    phi * LOCKED_WIDTH * LOCKED_HEIGHT / math.pi
                ),
            ),

        "particle_youngs_modulus_mapping":
            close(particle_E, ratio * matrix_E),

        "matrix_youngs_modulus_fixed":
            close(matrix_E, LOCKED_MATRIX_E),
        "center_x_fixed":
            close(cx, LOCKED_CENTER_X),
        "center_y_fixed":
            close(cy, LOCKED_CENTER_Y),
        "prescribed_x_displacement_fixed":
            close(ux, LOCKED_UX),
        "mesh_size_fixed":
            close(mesh_size, LOCKED_MESH_SIZE),

        "particle_inside_rve": (
            radius > 0.0
            and cx - radius > 0.0
            and cx + radius < LOCKED_WIDTH
            and cy - radius > 0.0
            and cy + radius < LOCKED_HEIGHT
        ),
    }

    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    if failed:
        raise ValueError(
            f"{case_id} violates locked design checks: "
            + ", ".join(failed)
        )


def load_base_config() -> dict[str, Any]:
    """Load and verify the established perfect-bonding base config."""
    if not BASE_CONFIG_PATH.is_file():
        raise FileNotFoundError(
            f"Base configuration is missing: {BASE_CONFIG_PATH}"
        )

    with BASE_CONFIG_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict):
        raise ValueError(
            "Base configuration did not load as a mapping."
        )

    checks = {
        "dimension":
            int(config["model"]["dimension"]) == LOCKED_DIMENSION,
        "assumption":
            str(config["model"]["assumption"]) == LOCKED_ASSUMPTION,
        "interface":
            str(config["model"]["interface"]) == LOCKED_INTERFACE,
        "width":
            close(config["geometry"]["width"], LOCKED_WIDTH),
        "height":
            close(config["geometry"]["height"], LOCKED_HEIGHT),
        "matrix_E":
            close(
                config["matrix"]["youngs_modulus"],
                LOCKED_MATRIX_E,
            ),
        "center_x":
            close(
                config["particle"]["center_x"],
                LOCKED_CENTER_X,
            ),
        "center_y":
            close(
                config["particle"]["center_y"],
                LOCKED_CENTER_Y,
            ),
        "prescribed_ux":
            close(
                config["loading"]["prescribed_x_displacement"],
                LOCKED_UX,
            ),
        "mesh_size":
            close(
                config["mesh"]["global_size"],
                LOCKED_MESH_SIZE,
            ),
    }

    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    if failed:
        raise ValueError(
            "Base configuration violates locked M4/M5 assumptions: "
            + ", ".join(failed)
        )

    return config


def typed_design_row(
    row: dict[str, str],
) -> dict[str, Any]:
    """Return one design row with numeric fields converted to floats."""
    result: dict[str, Any] = {
        "case_id": row["case_id"],
    }

    for key in EXPECTED_HEADER:
        if key == "case_id":
            continue
        result[key] = finite_float(
            row[key],
            f"{row['case_id']}:{key}",
        )

    return result


def design_digest(design: dict[str, Any]) -> str:
    """Return deterministic SHA-256 identity for one typed design row."""
    payload = json.dumps(
        design,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def build_case_config(
    base_config: dict[str, Any],
    design: dict[str, Any],
) -> dict[str, Any]:
    """Derive solver-level YAML inputs from one locked design row."""
    config = copy.deepcopy(base_config)

    case_id = design["case_id"]

    config["model"]["name"] = f"m5_{case_id.lower()}"

    config["model"]["dimension"] = LOCKED_DIMENSION
    config["model"]["assumption"] = LOCKED_ASSUMPTION
    config["model"]["interface"] = LOCKED_INTERFACE

    config["geometry"]["width"] = LOCKED_WIDTH
    config["geometry"]["height"] = LOCKED_HEIGHT

    config["matrix"]["youngs_modulus"] = (
        design["matrix_youngs_modulus"]
    )
    config["matrix"]["poissons_ratio"] = (
        design["matrix_poissons_ratio"]
    )

    config["particle"]["youngs_modulus"] = (
        design["particle_youngs_modulus"]
    )
    config["particle"]["poissons_ratio"] = (
        design["particle_poissons_ratio"]
    )
    config["particle"]["center_x"] = design["center_x"]
    config["particle"]["center_y"] = design["center_y"]
    config["particle"]["radius"] = design["particle_radius"]

    config["loading"]["prescribed_x_displacement"] = (
        design["prescribed_x_displacement"]
    )

    config["mesh"]["global_size"] = design["mesh_size"]

    validate_case_config(config, design)

    return config


def validate_case_config(
    config: dict[str, Any],
    design: dict[str, Any],
) -> None:
    """Verify derived solver inputs before any FEM process starts."""
    checks = {
        "dimension":
            int(config["model"]["dimension"]) == LOCKED_DIMENSION,
        "assumption":
            str(config["model"]["assumption"]) == LOCKED_ASSUMPTION,
        "interface":
            str(config["model"]["interface"]) == LOCKED_INTERFACE,

        "width":
            close(config["geometry"]["width"], LOCKED_WIDTH),
        "height":
            close(config["geometry"]["height"], LOCKED_HEIGHT),

        "matrix_E":
            close(
                config["matrix"]["youngs_modulus"],
                design["matrix_youngs_modulus"],
            ),
        "matrix_nu":
            close(
                config["matrix"]["poissons_ratio"],
                design["matrix_poissons_ratio"],
            ),

        "particle_E":
            close(
                config["particle"]["youngs_modulus"],
                design["particle_youngs_modulus"],
            ),
        "particle_nu":
            close(
                config["particle"]["poissons_ratio"],
                design["particle_poissons_ratio"],
            ),
        "center_x":
            close(
                config["particle"]["center_x"],
                design["center_x"],
            ),
        "center_y":
            close(
                config["particle"]["center_y"],
                design["center_y"],
            ),
        "radius":
            close(
                config["particle"]["radius"],
                design["particle_radius"],
            ),

        "prescribed_ux":
            close(
                config["loading"]["prescribed_x_displacement"],
                design["prescribed_x_displacement"],
            ),

        "mesh_size":
            close(
                config["mesh"]["global_size"],
                design["mesh_size"],
            ),
    }

    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    if failed:
        raise ValueError(
            f"{design['case_id']} derived configuration failed: "
            + ", ".join(failed)
        )


def assert_all_finite(
    value: Any,
    path: str = "root",
) -> None:
    """Recursively reject non-finite numeric values."""
    if isinstance(value, bool) or value is None:
        return

    if isinstance(value, (int, str)):
        return

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(
                f"Non-finite value at {path}: {value!r}"
            )
        return

    if isinstance(value, dict):
        for key, child in value.items():
            assert_all_finite(
                child,
                f"{path}.{key}",
            )
        return

    if isinstance(value, list):
        for index, child in enumerate(value):
            assert_all_finite(
                child,
                f"{path}[{index}]",
            )
        return

    raise TypeError(
        f"Unsupported value type at {path}: "
        f"{type(value).__name__}"
    )


def validate_solver_result(
    result: dict[str, Any],
    design: dict[str, Any],
) -> None:
    """Verify result identity, inputs, responses, and FEM checks."""
    assert_all_finite(result)

    checks = {
        "dimension":
            int(result["model"]["dimension"]) == LOCKED_DIMENSION,
        "assumption":
            result["model"]["assumption"] == LOCKED_ASSUMPTION,
        "interface":
            result["model"]["interface"] == LOCKED_INTERFACE,

        "width":
            close(result["geometry"]["width"], LOCKED_WIDTH),
        "height":
            close(result["geometry"]["height"], LOCKED_HEIGHT),

        "matrix_E":
            close(
                result["matrix"]["youngs_modulus"],
                design["matrix_youngs_modulus"],
            ),
        "matrix_nu":
            close(
                result["matrix"]["poissons_ratio"],
                design["matrix_poissons_ratio"],
            ),

        "particle_E":
            close(
                result["particle"]["youngs_modulus"],
                design["particle_youngs_modulus"],
            ),
        "particle_nu":
            close(
                result["particle"]["poissons_ratio"],
                design["particle_poissons_ratio"],
            ),
        "center_x":
            close(
                result["particle"]["center_x"],
                design["center_x"],
            ),
        "center_y":
            close(
                result["particle"]["center_y"],
                design["center_y"],
            ),
        "radius":
            close(
                result["particle"]["radius"],
                design["particle_radius"],
            ),
        "analytical_fraction":
            close(
                result["particle"]["analytical_fraction"],
                design["particle_fraction"],
            ),

        "prescribed_ux":
            close(
                result["loading"]["prescribed_x_displacement"],
                design["prescribed_x_displacement"],
            ),

        "mesh_size":
            close(
                result["mesh"]["global_size"],
                design["mesh_size"],
            ),

        "effective_modulus_finite":
            math.isfinite(
                float(
                    result["response"]["effective_modulus"]
                )
            ),

        "effective_poissons_ratio_finite":
            math.isfinite(
                float(
                    result["response"][
                        "effective_poissons_ratio"
                    ]
                )
            ),

        "effective_modulus_positive":
            float(
                result["response"]["effective_modulus"]
            ) > 0.0,

        "verification_all_pass":
            bool(result["verification"])
            and all(
                value is True
                for value in result["verification"].values()
            ),
    }

    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    if failed:
        raise ValueError(
            f"{design['case_id']} solver result failed "
            "orchestration validation: "
            + ", ".join(failed)
        )


def write_json_atomic(
    destination: Path,
    record: dict[str, Any],
) -> None:
    """Write JSON through a temporary sibling and atomically replace."""
    destination.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary = destination.with_name(
        destination.name + ".tmp"
    )

    with temporary.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            record,
            file,
            indent=2,
            allow_nan=False,
        )
        file.write("\n")

    os.replace(temporary, destination)


def write_log(
    log_path: Path,
    *,
    case_id: str,
    command: list[str],
    returncode: int,
    stdout: str,
    stderr: str,
) -> None:
    """Write the captured FEM process log."""
    log_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with log_path.open(
        "w",
        encoding="utf-8",
    ) as file:
        file.write(
            f"case_id: {case_id}\n"
        )
        file.write(
            "solver: src/10_parametric_rve_elasticity.py\n"
        )
        file.write(
            "mode: --no-plots\n"
        )
        file.write(
            f"returncode: {returncode}\n"
        )
        file.write(
            "command:\n"
        )
        file.write(
            " ".join(command) + "\n"
        )

        file.write("\n========== STDOUT ==========\n")
        file.write(stdout)
        if stdout and not stdout.endswith("\n"):
            file.write("\n")

        file.write("\n========== STDERR ==========\n")
        file.write(stderr)
        if stderr and not stderr.endswith("\n"):
            file.write("\n")


def existing_record_state(
    output_path: Path,
    design: dict[str, Any],
) -> str | None:
    """Validate an existing record and return success/failed/None."""
    if not output_path.is_file():
        return None

    try:
        with output_path.open(
            "r",
            encoding="utf-8",
        ) as file:
            record = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise RuntimeError(
            f"Existing record is unreadable: {output_path}"
        ) from exc

    if record.get("case_id") != design["case_id"]:
        raise RuntimeError(
            f"Existing result identity mismatch: {output_path}"
        )

    expected_digest = design_digest(design)

    if record.get("design_sha256") != expected_digest:
        raise RuntimeError(
            f"Existing result design digest mismatch: {output_path}"
        )

    status = record.get("status")

    if status not in {"success", "failed"}:
        raise RuntimeError(
            f"Existing result has invalid status: {output_path}"
        )

    if status == "success":
        solver_result = record.get("solver_result")

        if not isinstance(solver_result, dict):
            raise RuntimeError(
                f"Existing success record lacks solver_result: "
                f"{output_path}"
            )

        validate_solver_result(
            solver_result,
            design,
        )

    return str(status)


def make_failure_record(
    *,
    design: dict[str, Any],
    failure_type: str,
    message: str,
    returncode: int | None,
    log_path: Path,
) -> dict[str, Any]:
    """Build one explicit machine-readable failed-case envelope."""
    return {
        "case_id": design["case_id"],
        "status": "failed",
        "design_sha256": design_digest(design),
        "design": design,
        "solver": {
            "script": "src/10_parametric_rve_elasticity.py",
            "base_config":
                "configs/03_parametric_rve_base.yaml",
            "mode": "--no-plots",
        },
        "failure": {
            "type": failure_type,
            "message": message,
            "returncode": returncode,
            "log_path": str(
                log_path.relative_to(ROOT)
            ),
        },
    }


def run_case(
    *,
    row: dict[str, str],
    base_config: dict[str, Any],
    retry_failures: bool,
    dry_run: bool,
) -> str:
    """Run or safely skip one case."""
    design = typed_design_row(row)
    case_id = design["case_id"]

    output_path = RAW_DIR / f"{case_id}.json"
    log_path = LOG_DIR / f"{case_id}.log"

    existing = existing_record_state(
        output_path,
        design,
    )

    if existing == "success":
        print(f"{case_id}: SKIP existing validated success")
        return "skipped_success"

    if existing == "failed" and not retry_failures:
        print(
            f"{case_id}: SKIP existing failure "
            "(use --retry-failures to retry)"
        )
        return "skipped_failure"

    case_config = build_case_config(
        base_config,
        design,
    )

    if dry_run:
        if existing == "failed":
            action = "would retry previous failure"
        else:
            action = "would run"

        print(f"{case_id}: DRY RUN {action}")
        return "dry_run"

    RAW_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )
    LOG_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with tempfile.TemporaryDirectory(
        prefix=f"{case_id}_",
    ) as temporary_directory:
        temporary_root = Path(temporary_directory)

        config_path = temporary_root / "case.yaml"
        solver_result_path = temporary_root / "solver_result.json"

        with config_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            yaml.safe_dump(
                case_config,
                file,
                sort_keys=False,
            )

        command = [
            sys.executable,
            str(SOLVER_PATH),
            "--config",
            str(config_path),
            "--results-file",
            str(solver_result_path),
            "--no-plots",
        ]

        process = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

        write_log(
            log_path,
            case_id=case_id,
            command=command,
            returncode=process.returncode,
            stdout=process.stdout,
            stderr=process.stderr,
        )

        if process.returncode != 0:
            failure = make_failure_record(
                design=design,
                failure_type="solver_nonzero_exit",
                message=(
                    "Validated FEM solver returned a non-zero "
                    f"exit code: {process.returncode}"
                ),
                returncode=process.returncode,
                log_path=log_path,
            )

            write_json_atomic(
                output_path,
                failure,
            )

            print(
                f"{case_id}: FAILED "
                f"(solver return code {process.returncode})"
            )
            return "failed"

        if not solver_result_path.is_file():
            failure = make_failure_record(
                design=design,
                failure_type="missing_solver_result",
                message=(
                    "Solver exited successfully but did not create "
                    "the requested JSON result."
                ),
                returncode=process.returncode,
                log_path=log_path,
            )

            write_json_atomic(
                output_path,
                failure,
            )

            print(
                f"{case_id}: FAILED "
                "(missing solver result JSON)"
            )
            return "failed"

        try:
            with solver_result_path.open(
                "r",
                encoding="utf-8",
            ) as file:
                solver_result = json.load(file)

            if not isinstance(solver_result, dict):
                raise ValueError(
                    "Solver result JSON is not an object."
                )

            validate_solver_result(
                solver_result,
                design,
            )

        except (
            OSError,
            json.JSONDecodeError,
            KeyError,
            TypeError,
            ValueError,
        ) as exc:
            failure = make_failure_record(
                design=design,
                failure_type="result_validation_failed",
                message=str(exc),
                returncode=process.returncode,
                log_path=log_path,
            )

            write_json_atomic(
                output_path,
                failure,
            )

            print(
                f"{case_id}: FAILED "
                "(result validation failed)"
            )
            return "failed"

        record = {
            "case_id": case_id,
            "status": "success",
            "design_sha256": design_digest(design),
            "design": design,
            "solver": {
                "script":
                    "src/10_parametric_rve_elasticity.py",
                "base_config":
                    "configs/03_parametric_rve_base.yaml",
                "mode": "--no-plots",
                "returncode": process.returncode,
                "log_path": str(
                    log_path.relative_to(ROOT)
                ),
            },
            "solver_result": solver_result,
        }

        assert_all_finite(record)

        write_json_atomic(
            output_path,
            record,
        )

    print(f"{case_id}: SUCCESS")
    return "success"


def parse_args() -> argparse.Namespace:
    """Parse M5 runner command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Generate the locked 60-case M5 initial "
            "perfect-bonding FEM dataset."
        )
    )

    parser.add_argument(
        "--case-id",
        choices=EXPECTED_CASE_IDS,
        default=None,
        help=(
            "Run or inspect only one case. "
            "Default: process all 60 locked cases."
        ),
    )

    parser.add_argument(
        "--retry-failures",
        action="store_true",
        help=(
            "Retry existing records whose status is failed. "
            "Validated successful records are still skipped."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Validate design/configuration and report intended "
            "actions without running FEM or creating outputs."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Entry point for M5 initial FEM dataset generation."""
    args = parse_args()

    if not SOLVER_PATH.is_file():
        raise FileNotFoundError(
            f"Validated solver is missing: {SOLVER_PATH}"
        )

    rows = load_design()
    base_config = load_base_config()

    if args.case_id is not None:
        rows = [
            row
            for row in rows
            if row["case_id"] == args.case_id
        ]

        if len(rows) != 1:
            raise RuntimeError(
                f"Could not uniquely select {args.case_id}."
            )

    counters = {
        "success": 0,
        "failed": 0,
        "skipped_success": 0,
        "skipped_failure": 0,
        "dry_run": 0,
    }

    print("M5 Initial FEM Dataset Runner")
    print(f"Design: {DESIGN_PATH.relative_to(ROOT)}")
    print(f"Cases selected: {len(rows)}")
    print(
        "Mode:",
        "DRY RUN" if args.dry_run else "FEM EXECUTION",
    )
    print()

    for row in rows:
        state = run_case(
            row=row,
            base_config=base_config,
            retry_failures=args.retry_failures,
            dry_run=args.dry_run,
        )
        counters[state] += 1

    print()
    print("========== M5 RUN SUMMARY ==========")
    print(f"Selected:        {len(rows)}")
    print(f"Success:         {counters['success']}")
    print(f"Failed:          {counters['failed']}")
    print(
        f"Skipped success: {counters['skipped_success']}"
    )
    print(
        f"Skipped failure: {counters['skipped_failure']}"
    )
    print(f"Dry run:         {counters['dry_run']}")

    unresolved_failures = (
        counters["failed"]
        + counters["skipped_failure"]
    )

    if unresolved_failures:
        return 1

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print(
            "\nInterrupted by user. Existing completed "
            "per-case records are preserved.",
            file=sys.stderr,
        )
        raise SystemExit(130)
    except Exception as exc:
        print(
            f"FATAL: {type(exc).__name__}: {exc}",
            file=sys.stderr,
        )
        raise SystemExit(2)
