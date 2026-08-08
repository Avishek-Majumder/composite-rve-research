#!/usr/bin/env python3
"""Aggregate validated M5 per-case FEM results into one flat CSV dataset."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]

DESIGN_PATH = (
    ROOT
    / "results/processed/06_m4_lhs_initial_design.csv"
)

RAW_DIR = (
    ROOT
    / "results/raw/02_m5_initial_dataset"
)

DEFAULT_OUTPUT = (
    ROOT
    / "results/processed/07_m5_initial_fem_dataset.csv"
)


DESIGN_HEADER = [
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


VERIFICATION_FIELDS = [
    "solver_converged",
    "positive_material_areas",
    "total_area",
    "particle_fraction",
    "average_epsilon_xx",
    "finite_response",
    "positive_effective_modulus",
]


OUTPUT_FIELDS = [
    "case_id",
    "status",
    "design_sha256",

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

    "model_dimension",
    "model_assumption",
    "model_interface",

    "rve_width",
    "rve_height",

    "analytical_particle_fraction",
    "meshed_particle_fraction",
    "particle_fraction_error",

    "cell_count",

    "average_epsilon_xx",
    "average_epsilon_yy",
    "average_sigma_xx",
    "average_sigma_yy",

    "effective_modulus",
    "effective_poissons_ratio",

    "matrix_sigma_xx_min",
    "matrix_sigma_xx_max",
    "particle_sigma_xx_min",
    "particle_sigma_xx_max",

    "solver_convergence_reason",

    "verification_solver_converged",
    "verification_positive_material_areas",
    "verification_total_area",
    "verification_particle_fraction",
    "verification_average_epsilon_xx",
    "verification_finite_response",
    "verification_positive_effective_modulus",
]


REL_TOL = 1.0e-12
ABS_TOL = 1.0e-12


def close(a: Any, b: Any) -> bool:
    """Compare two numeric values using tight deterministic tolerances."""
    return math.isclose(
        float(a),
        float(b),
        rel_tol=REL_TOL,
        abs_tol=ABS_TOL,
    )


def finite_float(
    value: Any,
    label: str,
) -> float:
    """Convert a value to a finite float."""
    try:
        result = float(value)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"{label} is not numeric: {value!r}"
        ) from exc

    if not math.isfinite(result):
        raise ValueError(
            f"{label} is not finite: {value!r}"
        )

    return result


def reject_nonstandard_constant(value: str) -> None:
    """Reject JSON NaN and Infinity constants."""
    raise ValueError(
        f"Non-standard JSON numeric constant: {value}"
    )


def assert_all_finite(
    value: Any,
    path: str = "root",
) -> None:
    """Recursively ensure all floating-point values are finite."""
    if value is None or isinstance(value, bool):
        return

    if isinstance(value, int):
        return

    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(
                f"Non-finite numeric value at {path}: {value!r}"
            )
        return

    if isinstance(value, str):
        return

    if isinstance(value, list):
        for index, child in enumerate(value):
            assert_all_finite(
                child,
                f"{path}[{index}]",
            )
        return

    if isinstance(value, dict):
        for key, child in value.items():
            assert_all_finite(
                child,
                f"{path}.{key}",
            )
        return

    raise TypeError(
        f"Unsupported value type at {path}: "
        f"{type(value).__name__}"
    )


def typed_design_row(
    row: dict[str, str],
) -> dict[str, Any]:
    """Convert one locked design row to deterministic typed values."""
    case_id = row["case_id"]

    result: dict[str, Any] = {
        "case_id": case_id,
    }

    for key in DESIGN_HEADER:
        if key == "case_id":
            continue

        result[key] = finite_float(
            row[key],
            f"{case_id}:{key}",
        )

    return result


def design_digest(
    design: dict[str, Any],
) -> str:
    """Reproduce the runner's per-case SHA-256 design identity."""
    payload = json.dumps(
        design,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")

    return hashlib.sha256(payload).hexdigest()


def load_design() -> list[dict[str, Any]]:
    """Load and validate the complete locked M4 Latin-hypercube design."""
    if not DESIGN_PATH.is_file():
        raise FileNotFoundError(
            f"Locked design missing: {DESIGN_PATH}"
        )

    with DESIGN_PATH.open(
        "r",
        newline="",
        encoding="utf-8",
    ) as file:
        reader = csv.DictReader(file)

        raw_rows = list(reader)
        header = reader.fieldnames

    if header != DESIGN_HEADER:
        raise ValueError(
            "Locked design header mismatch.\n"
            f"Actual:   {header}\n"
            f"Expected: {DESIGN_HEADER}"
        )

    if len(raw_rows) != 60:
        raise ValueError(
            "Locked design must contain exactly 60 rows; "
            f"found {len(raw_rows)}."
        )

    rows = [
        typed_design_row(row)
        for row in raw_rows
    ]

    case_ids = [
        row["case_id"]
        for row in rows
    ]

    if case_ids != EXPECTED_CASE_IDS:
        raise ValueError(
            "Locked design case IDs are not exactly "
            "M4PB_001 through M4PB_060 in order."
        )

    return rows


def validate_embedded_design(
    embedded: Any,
    design: dict[str, Any],
) -> None:
    """Verify the JSON envelope contains the exact corresponding design."""
    case_id = design["case_id"]

    if not isinstance(embedded, dict):
        raise ValueError(
            f"{case_id}: embedded design is not an object."
        )

    if embedded.get("case_id") != case_id:
        raise ValueError(
            f"{case_id}: embedded case ID mismatch."
        )

    for key, expected in design.items():
        if key == "case_id":
            continue

        if key not in embedded:
            raise ValueError(
                f"{case_id}: embedded design missing {key}."
            )

        if not close(
            embedded[key],
            expected,
        ):
            raise ValueError(
                f"{case_id}: embedded design mismatch for {key}."
            )


def load_case_record(
    design: dict[str, Any],
) -> dict[str, Any]:
    """Load and deeply validate one successful raw M5 result record."""
    case_id = design["case_id"]

    path = RAW_DIR / f"{case_id}.json"

    if not path.is_file():
        raise FileNotFoundError(
            f"{case_id}: missing raw JSON: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        record = json.load(
            file,
            parse_constant=reject_nonstandard_constant,
        )

    if not isinstance(record, dict):
        raise ValueError(
            f"{case_id}: raw JSON top level is not an object."
        )

    assert_all_finite(record)

    if record.get("case_id") != case_id:
        raise ValueError(
            f"{case_id}: result-envelope case ID mismatch."
        )

    if record.get("status") != "success":
        raise ValueError(
            f"{case_id}: result status is not success."
        )

    expected_digest = design_digest(design)

    if record.get("design_sha256") != expected_digest:
        raise ValueError(
            f"{case_id}: design SHA-256 mismatch."
        )

    validate_embedded_design(
        record.get("design"),
        design,
    )

    solver_result = record.get("solver_result")

    if not isinstance(solver_result, dict):
        raise ValueError(
            f"{case_id}: solver_result is missing or invalid."
        )

    model = solver_result["model"]
    geometry = solver_result["geometry"]
    matrix = solver_result["matrix"]
    particle = solver_result["particle"]
    loading = solver_result["loading"]
    mesh = solver_result["mesh"]
    response = solver_result["response"]
    solver = solver_result["solver"]
    verification = solver_result["verification"]

    checks = {
        "dimension":
            int(model["dimension"]) == 2,

        "assumption":
            model["assumption"] == "plane_stress",

        "interface":
            model["interface"] == "perfect_bonding",

        "rve_width":
            close(
                geometry["width"],
                1.0,
            ),

        "rve_height":
            close(
                geometry["height"],
                1.0,
            ),

        "matrix_youngs_modulus":
            close(
                matrix["youngs_modulus"],
                design["matrix_youngs_modulus"],
            ),

        "matrix_poissons_ratio":
            close(
                matrix["poissons_ratio"],
                design["matrix_poissons_ratio"],
            ),

        "particle_youngs_modulus":
            close(
                particle["youngs_modulus"],
                design["particle_youngs_modulus"],
            ),

        "particle_poissons_ratio":
            close(
                particle["poissons_ratio"],
                design["particle_poissons_ratio"],
            ),

        "center_x":
            close(
                particle["center_x"],
                design["center_x"],
            ),

        "center_y":
            close(
                particle["center_y"],
                design["center_y"],
            ),

        "particle_radius":
            close(
                particle["radius"],
                design["particle_radius"],
            ),

        "analytical_particle_fraction":
            close(
                particle["analytical_fraction"],
                design["particle_fraction"],
            ),

        "prescribed_x_displacement":
            close(
                loading["prescribed_x_displacement"],
                design["prescribed_x_displacement"],
            ),

        "mesh_size":
            close(
                mesh["global_size"],
                design["mesh_size"],
            ),

        "cell_count_positive":
            int(mesh["cell_count"]) > 0,

        "solver_converged":
            int(solver["convergence_reason"]) > 0,

        "verification_schema":
            list(verification.keys())
            == VERIFICATION_FIELDS,

        "verification_all_true":
            all(
                value is True
                for value in verification.values()
            ),
    }

    for key in [
        "average_epsilon_xx",
        "average_epsilon_yy",
        "average_sigma_xx",
        "average_sigma_yy",
        "effective_modulus",
        "effective_poissons_ratio",
        "matrix_sigma_xx_min",
        "matrix_sigma_xx_max",
        "particle_sigma_xx_min",
        "particle_sigma_xx_max",
    ]:
        value = finite_float(
            response[key],
            f"{case_id}:response.{key}",
        )

        checks[f"{key}_finite"] = math.isfinite(value)

    checks["effective_modulus_positive"] = (
        float(response["effective_modulus"]) > 0.0
    )

    checks["average_epsilon_xx_expected"] = (
        math.isclose(
            float(response["average_epsilon_xx"]),
            0.01,
            rel_tol=0.0,
            abs_tol=1.0e-8,
        )
    )

    fraction_error = finite_float(
        particle["fraction_error"],
        f"{case_id}:particle.fraction_error",
    )

    checks["particle_fraction_error"] = (
        fraction_error <= 0.005
    )

    failed = [
        name
        for name, passed in checks.items()
        if not passed
    ]

    if failed:
        raise ValueError(
            f"{case_id}: raw result failed aggregation checks: "
            + ", ".join(failed)
        )

    return record


def make_aggregate_row(
    design: dict[str, Any],
    record: dict[str, Any],
) -> dict[str, Any]:
    """Flatten one validated successful record into one dataset row."""
    result = record["solver_result"]

    model = result["model"]
    geometry = result["geometry"]
    particle = result["particle"]
    mesh = result["mesh"]
    response = result["response"]
    solver = result["solver"]
    verification = result["verification"]

    row = {
        "case_id":
            design["case_id"],

        "status":
            record["status"],

        "design_sha256":
            record["design_sha256"],

        "unit_particle_fraction":
            design["unit_particle_fraction"],

        "unit_stiffness_ratio":
            design["unit_stiffness_ratio"],

        "unit_matrix_poissons_ratio":
            design["unit_matrix_poissons_ratio"],

        "unit_particle_poissons_ratio":
            design["unit_particle_poissons_ratio"],

        "particle_fraction":
            design["particle_fraction"],

        "stiffness_ratio":
            design["stiffness_ratio"],

        "matrix_poissons_ratio":
            design["matrix_poissons_ratio"],

        "particle_poissons_ratio":
            design["particle_poissons_ratio"],

        "particle_radius":
            design["particle_radius"],

        "matrix_youngs_modulus":
            design["matrix_youngs_modulus"],

        "particle_youngs_modulus":
            design["particle_youngs_modulus"],

        "center_x":
            design["center_x"],

        "center_y":
            design["center_y"],

        "prescribed_x_displacement":
            design["prescribed_x_displacement"],

        "mesh_size":
            design["mesh_size"],

        "model_dimension":
            int(model["dimension"]),

        "model_assumption":
            model["assumption"],

        "model_interface":
            model["interface"],

        "rve_width":
            float(geometry["width"]),

        "rve_height":
            float(geometry["height"]),

        "analytical_particle_fraction":
            float(particle["analytical_fraction"]),

        "meshed_particle_fraction":
            float(particle["meshed_fraction"]),

        "particle_fraction_error":
            float(particle["fraction_error"]),

        "cell_count":
            int(mesh["cell_count"]),

        "average_epsilon_xx":
            float(response["average_epsilon_xx"]),

        "average_epsilon_yy":
            float(response["average_epsilon_yy"]),

        "average_sigma_xx":
            float(response["average_sigma_xx"]),

        "average_sigma_yy":
            float(response["average_sigma_yy"]),

        "effective_modulus":
            float(response["effective_modulus"]),

        "effective_poissons_ratio":
            float(response["effective_poissons_ratio"]),

        "matrix_sigma_xx_min":
            float(response["matrix_sigma_xx_min"]),

        "matrix_sigma_xx_max":
            float(response["matrix_sigma_xx_max"]),

        "particle_sigma_xx_min":
            float(response["particle_sigma_xx_min"]),

        "particle_sigma_xx_max":
            float(response["particle_sigma_xx_max"]),

        "solver_convergence_reason":
            int(solver["convergence_reason"]),

        "verification_solver_converged":
            verification["solver_converged"],

        "verification_positive_material_areas":
            verification["positive_material_areas"],

        "verification_total_area":
            verification["total_area"],

        "verification_particle_fraction":
            verification["particle_fraction"],

        "verification_average_epsilon_xx":
            verification["average_epsilon_xx"],

        "verification_finite_response":
            verification["finite_response"],

        "verification_positive_effective_modulus":
            verification["positive_effective_modulus"],
    }

    if list(row.keys()) != OUTPUT_FIELDS:
        raise RuntimeError(
            f"{design['case_id']}: aggregate column order mismatch."
        )

    return row


def validate_aggregate_rows(
    rows: list[dict[str, Any]],
) -> None:
    """Validate the complete in-memory aggregate before writing."""
    if len(rows) != 60:
        raise ValueError(
            f"Aggregate must contain exactly 60 rows; found {len(rows)}."
        )

    case_ids = [
        row["case_id"]
        for row in rows
    ]

    if case_ids != EXPECTED_CASE_IDS:
        raise ValueError(
            "Aggregate case IDs are not exactly "
            "M4PB_001 through M4PB_060."
        )

    for row in rows:
        case_id = row["case_id"]

        if row["status"] != "success":
            raise ValueError(
                f"{case_id}: aggregate status is not success."
            )

        digest = row["design_sha256"]

        if (
            not isinstance(digest, str)
            or len(digest) != 64
            or any(
                char not in "0123456789abcdef"
                for char in digest
            )
        ):
            raise ValueError(
                f"{case_id}: invalid design SHA-256."
            )

        if row["model_dimension"] != 2:
            raise ValueError(
                f"{case_id}: model dimension changed."
            )

        if row["model_assumption"] != "plane_stress":
            raise ValueError(
                f"{case_id}: model assumption changed."
            )

        if row["model_interface"] != "perfect_bonding":
            raise ValueError(
                f"{case_id}: interface assumption changed."
            )

        if int(row["cell_count"]) <= 0:
            raise ValueError(
                f"{case_id}: non-positive cell count."
            )

        if int(row["solver_convergence_reason"]) <= 0:
            raise ValueError(
                f"{case_id}: solver did not converge."
            )

        if float(row["effective_modulus"]) <= 0.0:
            raise ValueError(
                f"{case_id}: non-positive effective modulus."
            )

        for key, value in row.items():
            if key in {
                "case_id",
                "status",
                "design_sha256",
                "model_assumption",
                "model_interface",
            }:
                continue

            if isinstance(value, bool):
                continue

            if isinstance(value, (int, float)):
                if not math.isfinite(float(value)):
                    raise ValueError(
                        f"{case_id}:{key} is non-finite."
                    )

        for field in OUTPUT_FIELDS:
            if field.startswith("verification_"):
                if row[field] is not True:
                    raise ValueError(
                        f"{case_id}:{field} is not True."
                    )


def build_aggregate() -> list[dict[str, Any]]:
    """Build the complete validated 60-row in-memory aggregate."""
    designs = load_design()

    rows = []

    for design in designs:
        record = load_case_record(design)

        rows.append(
            make_aggregate_row(
                design,
                record,
            )
        )

    validate_aggregate_rows(rows)

    return rows


def write_csv_atomic(
    output_path: Path,
    rows: list[dict[str, Any]],
) -> None:
    """Write aggregate CSV atomically using LF line endings."""
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    temporary_path = output_path.with_name(
        output_path.name + ".tmp"
    )

    with temporary_path.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:
        writer = csv.DictWriter(
            file,
            fieldnames=OUTPUT_FIELDS,
            extrasaction="raise",
            lineterminator="\n",
        )

        writer.writeheader()
        writer.writerows(rows)

    os.replace(
        temporary_path,
        output_path,
    )


def parse_args() -> argparse.Namespace:
    """Parse aggregation command-line arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Aggregate the validated 60-case M5 "
            "perfect-bonding FEM dataset."
        )
    )

    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=(
            "Output CSV path. Defaults to "
            "results/processed/07_m5_initial_fem_dataset.csv."
        ),
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Perform the complete 60-case aggregation validation "
            "without writing the CSV."
        ),
    )

    return parser.parse_args()


def main() -> int:
    """Aggregate and optionally write the validated M5 dataset."""
    args = parse_args()

    rows = build_aggregate()

    effective_moduli = [
        float(row["effective_modulus"])
        for row in rows
    ]

    effective_poissons = [
        float(row["effective_poissons_ratio"])
        for row in rows
    ]

    cell_counts = [
        int(row["cell_count"])
        for row in rows
    ]

    fraction_errors = [
        float(row["particle_fraction_error"])
        for row in rows
    ]

    print("M5 Initial FEM Dataset Aggregator")
    print(
        "Design:",
        DESIGN_PATH.relative_to(ROOT),
    )
    print(
        "Raw results:",
        RAW_DIR.relative_to(ROOT),
    )
    print("Validated rows:", len(rows))
    print("Columns:", len(OUTPUT_FIELDS))

    print()
    print("Effective modulus range:")
    print(
        min(effective_moduli),
        "to",
        max(effective_moduli),
    )

    print("Effective Poisson response range:")
    print(
        min(effective_poissons),
        "to",
        max(effective_poissons),
    )

    print("Cell-count range:")
    print(
        min(cell_counts),
        "to",
        max(cell_counts),
    )

    print("Maximum particle-fraction error:")
    print(
        max(fraction_errors)
    )

    if args.dry_run:
        print()
        print(
            "DRY RUN: validation passed; "
            "no aggregate CSV was written."
        )
        return 0

    output_path = args.output

    if not output_path.is_absolute():
        output_path = ROOT / output_path

    write_csv_atomic(
        output_path,
        rows,
    )

    print()
    print(
        "Aggregate CSV:",
        output_path.relative_to(ROOT)
        if output_path.is_relative_to(ROOT)
        else output_path,
    )

    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except KeyboardInterrupt:
        print(
            "\nInterrupted by user.",
            file=__import__("sys").stderr,
        )
        raise SystemExit(130)
    except Exception as exc:
        print(
            f"FATAL: {type(exc).__name__}: {exc}",
            file=__import__("sys").stderr,
        )
        raise SystemExit(2)
