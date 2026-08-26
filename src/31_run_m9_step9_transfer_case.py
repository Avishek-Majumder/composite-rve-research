#!/usr/bin/env python3
"""Run one locked M9 Step-9 transfer-validation case.

Contract-only invocation authenticates the selected case and protected source
authorities without importing project source modules, creating files, or
executing scientific work.

Scientific orchestration is available only behind --execute and remains
externally authorization-gated by the project workflow.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import subprocess
import sys
from decimal import Decimal
from pathlib import Path
from types import ModuleType
from typing import Any

REPO = Path(__file__).resolve().parents[1]

CASE_NAMESPACE = "composite-rve-m9-step9-transfer-case-v1"
SEED_NAMESPACE = "composite-rve-m9-step9-transfer-validation-v1"

STEP9_RAW_ROOT = REPO / "results/raw/06_m9_step9_transfer_validation"
PRODUCTION_RAW_ROOT = REPO / "results/raw/05_m9_stochastic_pilot"

BASE_PYTHON = Path("/home/avishek/miniforge3/envs/composite-sim/bin/python")
MPC_PYTHON = Path(
    "/home/avishek/miniforge3/envs/composite-sim-m8-mpc-compat/bin/python"
)

SRC20 = REPO / "src/20_generate_m8_periodized_microstructure.py"
SRC21 = REPO / "src/21_generate_m8_periodized_mesh.py"
SRC22 = REPO / "src/22_solve_m8_periodized_pbc.py"
SRC28 = REPO / "src/28_generate_m9_step9_void_microstructure.py"
SRC29 = REPO / "src/29_generate_m9_step9_void_mesh.py"
SRC30 = REPO / "src/30_solve_m9_step9_void_pbc.py"

SOURCE_SHA256 = {
    SRC20: "63dc1bcd24324589f069013fc5f730477ece944b9c79626d8e7f94f7b3b30187",
    SRC21: "0713c46add5395bce97d8bdf03e52050310889935921f306d958be076d9cc3cc",
    SRC22: "90079e56df7f2a74cac3b301e81cbaa0ea520ebcd1987f1ac7f81f4a6ee12e5b",
    SRC28: "20c2d56b734518bf6bf18f867652d562778290e146c47be961e3a416645af160",
    SRC29: "15fce610f15b7e54eb81142b459788e83dab1079d56d8253bd6b942d9ea57a30",
    SRC30: "734d4d2c0df18690d6ea9a81f7f128e5503fa997ce461cfcc6823c6f05df2332",
}

PARTICLE_COUNT = 16
RVE_SIDE = 1.0
MIN_PARTICLE_SPACING = 0.020
MAX_PARTICLE_ATTEMPTS = 20000
MATRIX_E = 1000.0
MACRO_AMPLITUDE = 0.01
CANDIDATE_H = 0.02048
FINE_H = 0.010
LOADS = ("X", "Y", "XY")

CASE_MANIFEST_SCHEMA = "m9_step9_transfer_case_manifest_v1"
EXECUTION_EVENT_SCHEMA = "m9_step9_transfer_execution_event_v1"
COMPARISON_SCHEMA = "m9_step9_transfer_comparison_v1"
CASE_SUMMARY_SCHEMA = "m9_step9_transfer_case_summary_v1"

LOCAL_METRIC_ID = "m8_matrix_vm_annulus_quadrature_tail10_v1"
LOCAL_QUADRATURE_DEGREE = 8

CASES: dict[str, dict[str, Any]] = {
    "M9TV-01": {
        "Ep_over_Em": "2",
        "nu_matrix": "0.25",
        "nu_particle": "0.15",
        "particle_fraction": "0.08",
        "void_fraction": "0",
        "void_count": 0,
        "particle_radius": 0.03989422804014327,
        "void_radius": None,
        "case_sha256": "b8f037b23f40b4e3b4f11351bba7eb1e56a74916c4830adeb6bfa540f36e8b68",
        "particle_seed_sha256": "6bca81dddde0cb530392c754f5f19fd77374eedb2e433665d41e71441bd0e9f5",
        "particle_seed": 143278873523340767025418018152741183447,
        "void_seed_sha256": None,
        "void_seed": None,
    },
    "M9TV-02": {
        "Ep_over_Em": "30",
        "nu_matrix": "0.40",
        "nu_particle": "0.30",
        "particle_fraction": "0.20",
        "void_fraction": "0",
        "void_count": 0,
        "particle_radius": 0.063078313050504,
        "void_radius": None,
        "case_sha256": "8a731f01d50c9da105d49f54d84199597f95d95256bffe674bfad5da1d4fa874",
        "particle_seed_sha256": "7776a8956d6d4f53e05ac1fb137e00051e468c73dff2e319e1038138b535b040",
        "particle_seed": 158794241811387740240800122303890194437,
        "void_seed_sha256": None,
        "void_seed": None,
    },
    "M9TV-03": {
        "Ep_over_Em": "2",
        "nu_matrix": "0.40",
        "nu_particle": "0.15",
        "particle_fraction": "0.08",
        "void_fraction": "0.0075",
        "void_count": 4,
        "particle_radius": 0.03989422804014327,
        "void_radius": 0.024430125595145995,
        "case_sha256": "5178ad415ef8baf3a89cf2073f0e9a84a971d32abedd68fdc6dfd0e2bd3245ee",
        "particle_seed_sha256": "f90aff5ad09e1096878a2a6340b6e743c3cc50d629364d7c132fdc601644836b",
        "particle_seed": 331034873128576928746062640963927861059,
        "void_seed_sha256": "c7f37127fa59f259bdf96f66b69658a64ad0f67c8d465f471283a26272b2356d",
        "void_seed": 265780394377485763838077729012744345766,
    },
    "M9TV-04": {
        "Ep_over_Em": "30",
        "nu_matrix": "0.25",
        "nu_particle": "0.30",
        "particle_fraction": "0.20",
        "void_fraction": "0.03",
        "void_count": 1,
        "particle_radius": 0.063078313050504,
        "void_radius": 0.09772050238058398,
        "case_sha256": "5fb722b3668181d67657e2928da81c637c31448d89fc932da04a4f09e5cd6ca8",
        "particle_seed_sha256": "7e216bc0fee989d1b52257e368d12fffc48a76fcfd3f0fd9c1d5343fdd345e13",
        "particle_seed": 167656258773757365808330988195306090495,
        "void_seed_sha256": "3675e7e9657c66be1e64bcbfdfafef0d685a6ce8e1b09e7c7d80aed9b0654a53",
        "void_seed": 72390514233022719310843015955024441101,
    },
    "M9TV-05": {
        "Ep_over_Em": "30",
        "nu_matrix": "0.40",
        "nu_particle": "0.15",
        "particle_fraction": "0.20",
        "void_fraction": "0.03",
        "void_count": 4,
        "particle_radius": 0.063078313050504,
        "void_radius": 0.04886025119029199,
        "case_sha256": "75ac68b1516dd0ceedccefddc33b10fec7f8d4d9544c9d0aef144dd1d752fbe6",
        "particle_seed_sha256": "05b166bdeb87a19488ab3de5c1b5f92e6ce3d6f03d41f8c452016359346d6ccd",
        "particle_seed": 7567260375680476855745945029095848238,
        "void_seed_sha256": "769c19859b70a6b333f816406b9ca112a611490f82cb2215290f3688b0a545af",
        "void_seed": 157659419458243575234270926394187620626,
    },
    "M9TV-06": {
        "Ep_over_Em": "2",
        "nu_matrix": "0.25",
        "nu_particle": "0.30",
        "particle_fraction": "0.08",
        "void_fraction": "0.03",
        "void_count": 2,
        "particle_radius": 0.03989422804014327,
        "void_radius": 0.06909882989426709,
        "case_sha256": "7474d99669663326914df9baba5f24e01be8a7cbe0c513be1e34e5a91a84c98e",
        "particle_seed_sha256": "60b46ba2ed89400ec8753e308709eb7d4dcadcc5c351e48acb525e6abfa9c3c2",
        "particle_seed": 128542684156191983480558845568121170813,
        "void_seed_sha256": "1c774abbe49176bca349dcc2f5d746c588d5e19f4e8bc534b5df39fb37da5fd3",
        "void_seed": 37837782992858786522254068446842537669,
    },
}


def must(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def canonical_decimal(value: Any) -> str:
    d = Decimal(str(value))
    must(d.is_finite(), f"non-finite canonical decimal: {value!r}")
    if d == 0:
        return "0"
    text = format(d, "f")
    return text.rstrip("0").rstrip(".") if "." in text else text


def canonical_case_material(case: dict[str, Any]) -> str:
    return (
        f"{CASE_NAMESPACE}"
        f"|Ep_over_Em={canonical_decimal(case['Ep_over_Em'])}"
        f"|nu_matrix={canonical_decimal(case['nu_matrix'])}"
        f"|nu_particle={canonical_decimal(case['nu_particle'])}"
        f"|particle_area_fraction_requested={canonical_decimal(case['particle_fraction'])}"
        f"|void_area_fraction_requested={canonical_decimal(case['void_fraction'])}"
        f"|void_count={int(case['void_count'])}"
    )


def derive_seed(case_sha256: str, stream: str) -> tuple[str, str, int]:
    material = (
        f"{SEED_NAMESPACE}"
        f"|transfer_case_sha256={case_sha256}"
        f"|stream={stream}"
    )
    digest = hashlib.sha256(material.encode("utf-8")).digest()
    return material, digest.hex(), int.from_bytes(digest[:16], "big", signed=False)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Authenticate or execute one locked M9 Step-9 transfer-validation case."
    )
    parser.add_argument("case_id", choices=tuple(CASES))
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the locked Step-9 scientific orchestration. Omit for contract-only authentication.",
    )
    return parser.parse_args()


def authenticate_case(case_id: str) -> dict[str, Any]:
    case = dict(CASES[case_id])
    material = canonical_case_material(case)
    case_sha = hashlib.sha256(material.encode("utf-8")).hexdigest()
    must(case_sha == case["case_sha256"], f"{case_id}: transfer-case SHA mismatch")

    pmat, psha, pseed = derive_seed(case_sha, "particle")
    must(psha == case["particle_seed_sha256"], f"{case_id}: particle seed SHA mismatch")
    must(pseed == int(case["particle_seed"]), f"{case_id}: particle seed mismatch")

    if int(case["void_count"]) == 0:
        must(case["void_seed"] is None, f"{case_id}: pristine case has void seed")
        must(case["void_seed_sha256"] is None, f"{case_id}: pristine case has void seed SHA")
        vmat = vsha = vseed = None
    else:
        vmat, vsha, vseed = derive_seed(case_sha, "void")
        must(vsha == case["void_seed_sha256"], f"{case_id}: void seed SHA mismatch")
        must(vseed == int(case["void_seed"]), f"{case_id}: void seed mismatch")

    particle_radius = math.sqrt(float(case["particle_fraction"]) / (PARTICLE_COUNT * math.pi))
    must(
        math.isclose(particle_radius, float(case["particle_radius"]), rel_tol=0.0, abs_tol=1e-15),
        f"{case_id}: particle radius mismatch",
    )

    if int(case["void_count"]) == 0:
        must(case["void_radius"] is None, f"{case_id}: pristine case has void radius")
    else:
        void_radius = math.sqrt(
            float(case["void_fraction"]) / (int(case["void_count"]) * math.pi)
        )
        must(
            math.isclose(void_radius, float(case["void_radius"]), rel_tol=0.0, abs_tol=1e-15),
            f"{case_id}: void radius mismatch",
        )

    case["canonical_physical_case_material"] = material
    case["particle_seed_material"] = pmat
    case["void_seed_material"] = vmat
    return case


def authenticate_sources() -> dict[str, str]:
    found: dict[str, str] = {}
    for path, expected in SOURCE_SHA256.items():
        must(path.is_file(), f"missing protected source: {path}")
        actual = sha256_file(path)
        must(actual == expected, f"protected source SHA mismatch: {path}")
        found[str(path.relative_to(REPO))] = actual
    must(BASE_PYTHON.is_file(), f"base interpreter missing: {BASE_PYTHON}")
    must(MPC_PYTHON.is_file(), f"MPC interpreter missing: {MPC_PYTHON}")
    return found


def contract_record(case_id: str) -> dict[str, Any]:
    case = authenticate_case(case_id)
    source_hashes = authenticate_sources()
    return {
        "schema": CASE_MANIFEST_SCHEMA,
        "status": "contract_authenticated",
        "case_id": case_id,
        "physical_case": {
            "Ep_over_Em": float(case["Ep_over_Em"]),
            "nu_matrix": float(case["nu_matrix"]),
            "nu_particle": float(case["nu_particle"]),
            "particle_area_fraction_requested": float(case["particle_fraction"]),
            "void_area_fraction_requested": float(case["void_fraction"]),
            "void_count": int(case["void_count"]),
            "particle_radius": float(case["particle_radius"]),
            "void_radius": case["void_radius"],
        },
        "identity": {
            "namespace": CASE_NAMESPACE,
            "canonical_physical_case_material": case["canonical_physical_case_material"],
            "transfer_case_sha256": case["case_sha256"],
            "human_case_label_enters_hash": False,
            "mesh_size_enters_hash": False,
        },
        "validation_rng": {
            "namespace": SEED_NAMESPACE,
            "bit_generator": "PCG64",
            "particle_seed_material": case["particle_seed_material"],
            "particle_seed_sha256": case["particle_seed_sha256"],
            "particle_seed": int(case["particle_seed"]),
            "void_seed_status": "not_applicable" if int(case["void_count"]) == 0 else "applicable",
            "void_seed_material": case["void_seed_material"],
            "void_seed_sha256": case["void_seed_sha256"],
            "void_seed": case["void_seed"],
        },
        "mesh_pair": {
            "candidate_h": CANDIDATE_H,
            "fine_h": FINE_H,
            "same_geometry_required": True,
            "geometry_regeneration_forbidden": True,
        },
        "loads": list(LOADS),
        "invocation_topology": {
            "src20": "A_IN_PROCESS_AUTHENTICATED_FUNCTION_REUSE",
            "src21": "C_ISOLATED_BASE_ENV_RUNTIME_ADAPTER",
            "src22": "B_MPC_ENV_CLI_CHILD",
            "src28": "B_BASE_ENV_CLI_CHILD",
            "src29": "B_BASE_ENV_CLI_CHILD",
            "src30": "B_MPC_ENV_CLI_CHILD",
        },
        "source_sha256": {
            **source_hashes,
            "src/31_run_m9_step9_transfer_case.py": sha256_file(Path(__file__).resolve()),
        },
        "transfer_comparison": {
            "numerical_threshold_locked": False,
            "m8_threshold_inheritance_forbidden": True,
            "relative_difference_omitted": True,
            "signed_delta_definition": "candidate_minus_fine",
        },
        "scope_guard": {
            "m9_step9_transfer_validation": True,
            "m9_stochastic_pilot_production": False,
            "production_lhs_generation": False,
            "production_design_id": False,
            "production_realization_id": False,
            "production_attempt_id": False,
            "production_rng_consumption": False,
            "m10_execution": False,
            "machine_learning": False,
        },
    }


def json_text(value: Any) -> str:
    return json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n"


def write_text_exclusive(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    must(isinstance(value, dict), f"expected JSON object: {path}")
    return value


def dynamic_load(path: Path, name: str) -> ModuleType:
    spec = importlib.util.spec_from_file_location(name, path)
    must(spec is not None and spec.loader is not None, f"cannot load module spec: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def generate_particle_geometry(case: dict[str, Any], output: Path) -> str:
    module = dynamic_load(SRC20, "_m9_step9_src20")
    ns = argparse.Namespace(
        seed=int(case["particle_seed"]),
        particle_count=PARTICLE_COUNT,
        radius=float(case["particle_radius"]),
        min_particle_spacing=MIN_PARTICLE_SPACING,
        max_attempts_per_particle=MAX_PARTICLE_ATTEMPTS,
        width=RVE_SIDE,
        height=RVE_SIDE,
    )
    module.validate_inputs(ns)
    particles, status, failure_reason, total_attempts = module.generate_particles(ns)
    metadata = module.build_metadata(
        ns, particles, status, failure_reason, total_attempts
    )
    must(metadata["status"] == "valid", f"particle generation failed: {metadata['failure_reason']}")
    write_text_exclusive(output, json_text(metadata))
    return sha256_file(output)


def write_material_config(case: dict[str, Any], path: Path) -> str:
    particle_E = float(case["Ep_over_Em"]) * MATRIX_E
    text = (
        "model:\n"
        "  dimension: 2\n"
        "  assumption: plane_stress\n"
        "  interface: perfect_bonding\n"
        "matrix:\n"
        f"  youngs_modulus: {MATRIX_E:.1f}\n"
        f"  poissons_ratio: {float(case['nu_matrix']):.17g}\n"
        "particle:\n"
        f"  youngs_modulus: {particle_E:.17g}\n"
        f"  poissons_ratio: {float(case['nu_particle']):.17g}\n"
    )
    write_text_exclusive(path, text)
    return sha256_file(path)


def run_child(
    stage: str,
    command: list[str],
    cwd: Path,
    log_dir: Path,
    env: dict[str, str] | None = None,
) -> None:
    stdout_path = log_dir / f"{stage}.stdout.txt"
    stderr_path = log_dir / f"{stage}.stderr.txt"
    with stdout_path.open("x", encoding="utf-8", newline="\n") as out, \
         stderr_path.open("x", encoding="utf-8", newline="\n") as err:
        completed = subprocess.run(
            command,
            cwd=str(cwd),
            env=env,
            text=True,
            stdout=out,
            stderr=err,
            check=False,
        )
    must(completed.returncode == 0, f"child stage failed: {stage}; returncode={completed.returncode}")


def run_src21_adapter(
    geometry_json: Path,
    mesh_size: float,
    mesh_out: Path,
    diagnostics_out: Path,
    particle_radius: float,
    log_dir: Path,
    stage: str,
) -> None:
    adapter = r"""
import hashlib
import importlib.util
import math
import sys
from pathlib import Path

src = Path(sys.argv[1])
expected_sha = sys.argv[2]
radius = float(sys.argv[3])
geometry = Path(sys.argv[4])
mesh_size = sys.argv[5]
mesh_out = Path(sys.argv[6])
diag_out = Path(sys.argv[7])

actual = hashlib.sha256(src.read_bytes()).hexdigest()
if actual != expected_sha:
    raise RuntimeError("protected src/21 SHA mismatch")

spec = importlib.util.spec_from_file_location("_m9_step9_src21_adapter", src)
if spec is None or spec.loader is None:
    raise RuntimeError("cannot load protected src/21")
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

native = float(module.M8_VALIDATION_PARTICLE_RADIUS)
if not math.isclose(native, 0.05, rel_tol=0.0, abs_tol=0.0):
    raise RuntimeError("unexpected native src/21 M8 validation radius")

module.M8_VALIDATION_PARTICLE_RADIUS = radius
sys.argv = [
    str(src),
    "--geometry-json", str(geometry),
    "--rve-level", "R1",
    "--mesh-size", str(mesh_size),
    "--mesh-out", str(mesh_out),
    "--diagnostics-out", str(diag_out),
]
module.main()
"""
    run_child(
        stage,
        [
            str(BASE_PYTHON),
            "-c",
            adapter,
            str(SRC21),
            SOURCE_SHA256[SRC21],
            repr(float(particle_radius)),
            str(geometry_json),
            repr(float(mesh_size)),
            str(mesh_out),
            str(diagnostics_out),
        ],
        REPO,
        log_dir,
    )


def run_src28(case: dict[str, Any], particle_json: Path, particle_sha: str, output: Path, log_dir: Path) -> str:
    must(int(case["void_count"]) > 0, "src/28 requested for pristine case")
    run_child(
        "void_geometry",
        [
            str(BASE_PYTHON),
            str(SRC28),
            "--source-particle-geometry-json", str(particle_json),
            "--expected-source-sha256", particle_sha,
            "--expected-particle-seed", str(case["particle_seed"]),
            "--void-seed", str(case["void_seed"]),
            "--void-count", str(case["void_count"]),
            "--void-radius", repr(float(case["void_radius"])),
            "--output-json", str(output),
        ],
        REPO,
        log_dir,
    )
    return sha256_file(output)


def run_pristine_mesh(
    case: dict[str, Any],
    geometry_json: Path,
    mesh_size: float,
    mesh_out: Path,
    diagnostics_out: Path,
    log_dir: Path,
    mesh_label: str,
) -> tuple[str, str]:
    run_src21_adapter(
        geometry_json,
        mesh_size,
        mesh_out,
        diagnostics_out,
        float(case["particle_radius"]),
        log_dir,
        f"{mesh_label}.src21_mesh",
    )
    return sha256_file(mesh_out), sha256_file(diagnostics_out)


def run_defective_mesh(
    geometry_json: Path,
    geometry_sha: str,
    mesh_size: float,
    mesh_out: Path,
    diagnostics_out: Path,
    log_dir: Path,
    mesh_label: str,
) -> tuple[str, str]:
    run_child(
        f"{mesh_label}.src29_mesh",
        [
            str(BASE_PYTHON),
            str(SRC29),
            "--geometry-json", str(geometry_json),
            "--expected-geometry-sha256", geometry_sha,
            "--mesh-size", repr(float(mesh_size)),
            "--mesh-out", str(mesh_out),
            "--diagnostics-out", str(diagnostics_out),
            "--generate-mesh",
        ],
        REPO,
        log_dir,
    )
    return sha256_file(mesh_out), sha256_file(diagnostics_out)


def run_pristine_load(
    mesh: Path,
    mesh_diag: Path,
    config: Path,
    load: str,
    output: Path,
    log_dir: Path,
    mesh_label: str,
) -> None:
    run_child(
        f"{mesh_label}.src22_{load}",
        [
            str(MPC_PYTHON),
            str(SRC22),
            "--mesh", str(mesh),
            "--mesh-diagnostics", str(mesh_diag),
            "--config", str(config),
            "--load-case", load,
            "--macro-amplitude", repr(MACRO_AMPLITUDE),
            "--output", str(output),
        ],
        REPO,
        log_dir,
    )


def run_defective_load(
    mesh: Path,
    mesh_sha: str,
    mesh_diag: Path,
    mesh_diag_sha: str,
    geometry: Path,
    geometry_sha: str,
    config: Path,
    load: str,
    output: Path,
    log_dir: Path,
    mesh_label: str,
) -> None:
    run_child(
        f"{mesh_label}.src30_{load}",
        [
            str(MPC_PYTHON),
            str(SRC30),
            "--mesh", str(mesh),
            "--expected-mesh-sha256", mesh_sha,
            "--mesh-diagnostics", str(mesh_diag),
            "--expected-mesh-diagnostics-sha256", mesh_diag_sha,
            "--geometry-json", str(geometry),
            "--expected-geometry-sha256", geometry_sha,
            "--config", str(config),
            "--load-case", load,
            "--macro-amplitude", repr(MACRO_AMPLITUDE),
            "--output", str(output),
        ],
        REPO,
        log_dir,
    )


def normalized_column(record: dict[str, Any], defective: bool, expected_load: str) -> list[float]:
    expected_schema = (
        "m9_step9_void_pbc_load_validation_v1"
        if defective
        else "m8_periodized_particle_pbc_load_validation_v1"
    )
    expected_status = "validated" if defective else "valid"
    must(record.get("schema") == expected_schema, "load record schema is not expected")
    must(record.get("status") == expected_status, "load record status is not expected")
    case_block = record.get("case")
    must(isinstance(case_block, dict), "load record missing case block")
    must(case_block.get("load_case") == expected_load, "load-case authority mismatch")

    response = record.get("response")
    must(isinstance(response, dict), "load record missing response block")

    if defective:
        column = response.get("response_stiffness_column_normalized_by_E_matrix")
        must(isinstance(column, list) and len(column) == 3, "defective normalized column malformed")
        return [float(value) for value in column]

    raw = response.get("stiffness_column")
    must(isinstance(raw, list) and len(raw) == 3, "pristine raw stiffness column malformed")
    model = record.get("model")
    must(isinstance(model, dict), "pristine model block missing")
    matrix = model.get("matrix")
    must(isinstance(matrix, dict), "pristine matrix block missing")
    matrix_E = float(matrix["youngs_modulus"])
    must(math.isfinite(matrix_E) and matrix_E > 0.0, "pristine matrix modulus invalid")
    reconstructed = [float(value) / matrix_E for value in raw]
    legacy = response.get("x_stiffness_column_normalized")
    must(isinstance(legacy, list) and len(legacy) == 3, "legacy pristine normalized field malformed")
    for a, b in zip(reconstructed, legacy):
        must(math.isclose(a, float(b), rel_tol=1e-12, abs_tol=1e-12), "pristine legacy normalized cross-check failed")
    return reconstructed


def reconstruct_cbar(load_records: dict[str, dict[str, Any]], defective: bool) -> list[list[float]]:
    columns = {
        load: normalized_column(load_records[load], defective, load)
        for load in LOADS
    }
    return [
        [columns["X"][0], columns["Y"][0], columns["XY"][0]],
        [columns["X"][1], columns["Y"][1], columns["XY"][1]],
        [columns["X"][2], columns["Y"][2], columns["XY"][2]],
    ]


def defective_local_k(record: dict[str, Any]) -> float:
    local = record.get("local_response")
    must(isinstance(local, dict), "defective record missing local_response")
    must(local.get("applicable") is True, "defective X local response not applicable")
    must(local.get("load_case_authority") == "X", "defective local load authority mismatch")
    must(int(local.get("quadrature_degree")) == LOCAL_QUADRATURE_DEGREE, "defective local quadrature degree mismatch")
    metric = local.get("metric")
    must(isinstance(metric, dict), "defective local metric missing")
    must(metric.get("metric_id") == LOCAL_METRIC_ID, "defective local metric id mismatch")
    value = float(metric["K_vm_tail10"])
    must(math.isfinite(value) and value >= 0.0, "defective local K invalid")
    return value


def matrix_component_record(candidate: list[list[float]], fine: list[list[float]]) -> dict[str, Any]:
    labels = (
        ("C11_over_Em", 0, 0), ("C12_over_Em", 0, 1), ("C16_over_Em", 0, 2),
        ("C21_over_Em", 1, 0), ("C22_over_Em", 1, 1), ("C26_over_Em", 1, 2),
        ("C61_over_Em", 2, 0), ("C62_over_Em", 2, 1), ("C66_over_Em", 2, 2),
    )
    result: dict[str, Any] = {}
    for label, i, j in labels:
        c = float(candidate[i][j])
        f = float(fine[i][j])
        result[label] = {
            "candidate": c,
            "fine": f,
            "signed_delta": c - f,
            "abs_delta": abs(c - f),
        }
    return result


def execute(case_id: str) -> int:
    must(
        Path(sys.executable).resolve() == BASE_PYTHON.resolve(),
        "Step-9 orchestrator execution must use the locked base interpreter",
    )
    must(not PRODUCTION_RAW_ROOT.exists(), "production stochastic-pilot raw root must remain absent")
    must(not STEP9_RAW_ROOT.exists() or STEP9_RAW_ROOT.is_dir(), "Step-9 raw root path is not a directory")

    case = authenticate_case(case_id)
    source_hashes = authenticate_sources()

    STEP9_RAW_ROOT.mkdir(parents=True, exist_ok=True)
    case_root = STEP9_RAW_ROOT / case_id
    case_root.mkdir(parents=False, exist_ok=False)

    log_dir = case_root / "logs"
    log_dir.mkdir(exist_ok=False)

    manifest = contract_record(case_id)
    manifest["status"] = "execution_started"
    manifest["case_root"] = str(case_root.relative_to(REPO))
    write_text_exclusive(case_root / "case_manifest.json", json_text(manifest))

    journal = case_root / "execution_journal.jsonl"
    write_text_exclusive(
        journal,
        json.dumps(
            {
                "schema": EXECUTION_EVENT_SCHEMA,
                "event_index": 1,
                "event": "case_root_created",
                "case_id": case_id,
            },
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
    )

    config_path = case_root / "material_config.yaml"
    config_sha = write_material_config(case, config_path)

    particle_json = case_root / "particle_geometry.json"
    particle_sha = generate_particle_geometry(case, particle_json)

    defective = int(case["void_count"]) > 0
    if defective:
        geometry_json = case_root / "defective_geometry.json"
        geometry_sha = run_src28(case, particle_json, particle_sha, geometry_json, log_dir)
    else:
        geometry_json = particle_json
        geometry_sha = particle_sha

    mesh_results: dict[str, Any] = {}
    for mesh_label, h in (("candidate", CANDIDATE_H), ("fine", FINE_H)):
        mesh_dir = case_root / mesh_label
        mesh_dir.mkdir(exist_ok=False)
        mesh_path = mesh_dir / "mesh.msh"
        mesh_diag = mesh_dir / "mesh_diagnostics.json"

        if defective:
            mesh_sha, mesh_diag_sha = run_defective_mesh(
                geometry_json, geometry_sha, h, mesh_path, mesh_diag, log_dir, mesh_label
            )
        else:
            mesh_sha, mesh_diag_sha = run_pristine_mesh(
                case, geometry_json, h, mesh_path, mesh_diag, log_dir, mesh_label
            )

        loads: dict[str, dict[str, Any]] = {}
        for load in LOADS:
            output = mesh_dir / f"{load}.json"
            if defective:
                run_defective_load(
                    mesh_path, mesh_sha, mesh_diag, mesh_diag_sha,
                    geometry_json, geometry_sha, config_path,
                    load, output, log_dir, mesh_label,
                )
            else:
                run_pristine_load(
                    mesh_path, mesh_diag, config_path,
                    load, output, log_dir, mesh_label,
                )
            loads[load] = load_json(output)

        cbar = reconstruct_cbar(loads, defective)
        local_k = defective_local_k(loads["X"]) if defective else None
        mesh_results[mesh_label] = {
            "h": h,
            "mesh_sha256": mesh_sha,
            "mesh_diagnostics_sha256": mesh_diag_sha,
            "Cbar_over_E_matrix": cbar,
            "K_vm_tail10_X": local_k,
        }

    candidate = mesh_results["candidate"]
    fine = mesh_results["fine"]
    comparison: dict[str, Any] = {
        "schema": COMPARISON_SCHEMA,
        "status": "recorded_without_numerical_threshold",
        "case_id": case_id,
        "transfer_case_sha256": case["case_sha256"],
        "candidate_h": CANDIDATE_H,
        "fine_h": FINE_H,
        "numerical_threshold_locked": False,
        "m8_threshold_inheritance_forbidden": True,
        "relative_difference_omitted": True,
        "global_components": matrix_component_record(
            candidate["Cbar_over_E_matrix"],
            fine["Cbar_over_E_matrix"],
        ),
        "defective_local": None,
    }

    if defective:
        ck = float(candidate["K_vm_tail10_X"])
        fk = float(fine["K_vm_tail10_X"])
        comparison["defective_local"] = {
            "metric_id": LOCAL_METRIC_ID,
            "load_case": "X",
            "quadrature_degree": LOCAL_QUADRATURE_DEGREE,
            "candidate": ck,
            "fine": fk,
            "signed_delta": ck - fk,
            "abs_delta": abs(ck - fk),
        }

    comparison_path = case_root / "comparison.json"
    write_text_exclusive(comparison_path, json_text(comparison))

    summary = {
        "schema": CASE_SUMMARY_SCHEMA,
        "status": "completed",
        "case_id": case_id,
        "transfer_case_sha256": case["case_sha256"],
        "material_config_sha256": config_sha,
        "particle_geometry_sha256": particle_sha,
        "defective_geometry_sha256": geometry_sha if defective else None,
        "candidate": candidate,
        "fine": fine,
        "comparison_sha256": sha256_file(comparison_path),
        "hard_gate_outcomes": "all_invoked_child_processes_returned_zero_and_records_authenticated",
        "transfer_comparison_status": "recorded_without_numerical_threshold",
        "scope_guard": manifest["scope_guard"],
        "source_sha256": source_hashes,
    }
    write_text_exclusive(case_root / "case_summary.json", json_text(summary))

    print(json_text(summary), end="")
    return 0


def main() -> int:
    args = parse_args()
    record = contract_record(args.case_id)

    if not args.execute:
        print(json_text(record), end="")
        print("PASS — Step-9 transfer-case contract authenticated; no files or scientific evidence created.")
        return 0

    return execute(args.case_id)


if __name__ == "__main__":
    raise SystemExit(main())
