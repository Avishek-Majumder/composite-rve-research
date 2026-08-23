"""Generate one M9 Step-9 defective periodized-void geometry state.

The authenticated pristine particle artifact is reused read-only.
Circular true-hole centers are sampled on the rectangular periodic torus
using the locked Step-9 validation void seed, exact requested void radius,
locked toroidal clearances, and finite placement budget.

This source creates Step-9 transfer-validation geometry metadata only.
It does not generate a mesh, construct an MPC, solve FEM, reconstruct a
tensor, create production pilot identities, or perform machine learning.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np
from numpy.random import Generator, PCG64


SCHEMA = "m9_step9_void_microstructure_v1"
SOURCE_SCHEMA = "m8_periodized_particle_microstructure_v1"
VOID_ARRANGEMENT = "periodized_uniform_rejection_single_state_v1"
REPRESENTATION_POLICY = "toroidal_wrapped_void_images_v1"
STATE_IDENTITY_METHOD = (
    "sha256_canonical_json_particle_identity_physical_voids_v1"
)

STEP9_VALIDATION_SEED_NAMESPACE = (
    "composite-rve-m9-step9-transfer-validation-v1"
)
STEP9_ALLOWED_VOID_COUNTS = frozenset(
    {
        1,
        2,
        4,
    }
)
STEP9_MIN_VOID_PARTICLE_SPACING = 0.020
STEP9_MIN_VOID_VOID_SPACING = 0.020
STEP9_MAX_ATTEMPTS_PER_VOID = 20000
STEP9_PHYSICAL_PARTICLE_COUNT = 16
STEP9_RVE_LENGTH = 1.0

TOL = 1.0e-12


@dataclass(frozen=True)
class Particle:
    particle_id: int
    center_x: float
    center_y: float
    radius: float


@dataclass(frozen=True)
class VoidCenter:
    void_id: int
    center_x: float
    center_y: float
    placement_attempts: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate one M9 Step-9 defective "
            "periodized-void geometry state "
            "from an authenticated pristine "
            "particle artifact."
        )
    )

    parser.add_argument(
        "--source-particle-geometry-json",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--expected-source-sha256",
        required=True,
    )

    parser.add_argument(
        "--expected-particle-seed",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--void-seed",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--void-count",
        type=int,
        choices=sorted(
            STEP9_ALLOWED_VOID_COUNTS
        ),
        required=True,
    )

    parser.add_argument(
        "--void-radius",
        type=float,
        required=True,
    )

    parser.add_argument(
        "--output-json",
        type=Path,
        required=True,
    )

    return parser.parse_args()

def sha256_file(path: Path) -> str:
    return hashlib.sha256(
        path.read_bytes()
    ).hexdigest()


def validate_sha256_text(
    value: str,
) -> str:
    normalized = value.strip().lower()

    if len(normalized) != 64:
        raise ValueError(
            "expected-source-sha256 must contain "
            "64 hex characters."
        )

    try:
        int(
            normalized,
            16,
        )

    except ValueError as exc:
        raise ValueError(
            "expected-source-sha256 must contain "
            "only hexadecimal characters."
        ) from exc

    return normalized


def validate_numeric_inputs(
    args: argparse.Namespace,
) -> None:
    if args.expected_particle_seed < 0:
        raise ValueError(
            "expected-particle-seed must be "
            "non-negative."
        )

    if args.void_seed < 0:
        raise ValueError(
            "void-seed must be non-negative."
        )

    if (
        args.void_count
        not in STEP9_ALLOWED_VOID_COUNTS
    ):
        raise ValueError(
            "void-count must be one of "
            "{1, 2, 4}."
        )

    if (
        not np.isfinite(
            args.void_radius
        )
        or args.void_radius <= 0.0
    ):
        raise ValueError(
            "void-radius must be finite "
            "and positive."
        )

    validate_sha256_text(
        args.expected_source_sha256
    )

def axis_minimum_image_distance(
    first: float,
    second: float,
    length: float,
) -> float:
    direct = abs(
        first - second
    )

    return min(
        direct,
        length - direct,
    )


def toroidal_center_distance(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    width: float,
    height: float,
) -> float:
    dx = axis_minimum_image_distance(
        x1,
        x2,
        width,
    )

    dy = axis_minimum_image_distance(
        y1,
        y2,
        height,
    )

    return math.hypot(
        dx,
        dy,
    )


def toroidal_surface_gap(
    x1: float,
    y1: float,
    r1: float,
    x2: float,
    y2: float,
    r2: float,
    width: float,
    height: float,
) -> float:
    return (
        toroidal_center_distance(
            x1,
            y1,
            x2,
            y2,
            width,
            height,
        )
        - r1
        - r2
    )


def canonical_source_particle_identity(
    source: dict,
) -> str:
    payload = {
        "width": float(
            source["rve"]["width"]
        ),
        "height": float(
            source["rve"]["height"]
        ),
        "particles": [
            {
                "particle_id": int(
                    particle["particle_id"]
                ),
                "center_x": float(
                    particle["center_x"]
                ),
                "center_y": float(
                    particle["center_y"]
                ),
                "radius": float(
                    particle["radius"]
                ),
            }
            for particle in source[
                "particles"
            ]
        ],
    }

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        allow_nan=False,
    ).encode(
        "utf-8"
    )

    return hashlib.sha256(
        canonical
    ).hexdigest()


def load_source_particle_geometry(
    path: Path,
    expected_sha256: str,
) -> tuple[
    dict,
    list[Particle],
    str,
]:
    if not path.is_file():
        raise FileNotFoundError(
            f"Missing source particle geometry: {path}"
        )

    expected = validate_sha256_text(
        expected_sha256
    )

    actual = sha256_file(
        path
    )

    if actual != expected:
        raise ValueError(
            "Source particle geometry SHA mismatch: "
            f"expected {expected}, got {actual}."
        )

    source = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if (
        source.get("schema")
        != SOURCE_SCHEMA
    ):
        raise ValueError(
            "Source schema must be "
            f"{SOURCE_SCHEMA}; got "
            f"{source.get('schema')}."
        )

    if (
        source.get("status") != "valid"
        or source.get("failure_reason")
        is not None
    ):
        raise ValueError(
            "Source particle geometry is not "
            "a valid pristine artifact."
        )

    scope = source.get(
        "scope_guard",
        {},
    )

    if (
        scope.get(
            "voids_generated"
        )
        is not False
    ):
        raise ValueError(
            "Source artifact is not pristine "
            "particle-only geometry."
        )

    if (
        scope.get(
            "fem_solve_performed"
        )
        is not False
    ):
        raise ValueError(
            "Source artifact unexpectedly "
            "records a FEM solve."
        )

    width = float(
        source["rve"]["width"]
    )

    height = float(
        source["rve"]["height"]
    )

    area = float(
        source["rve"]["area"]
    )

    if not (
        math.isfinite(width)
        and width > 0.0
        and math.isfinite(height)
        and height > 0.0
    ):
        raise ValueError(
            "Source RVE dimensions must be "
            "finite and positive."
        )

    if not math.isclose(
        area,
        width * height,
        rel_tol=0.0,
        abs_tol=TOL,
    ):
        raise ValueError(
            "Source RVE area is inconsistent "
            "with width*height."
        )

    raw_particles = source.get(
        "particles"
    )

    if (
        not isinstance(
            raw_particles,
            list,
        )
        or not raw_particles
    ):
        raise ValueError(
            "Source particle list is absent or empty."
        )

    ids = [
        int(
            particle[
                "particle_id"
            ]
        )
        for particle in raw_particles
    ]

    if ids != list(
        range(
            1,
            len(raw_particles) + 1,
        )
    ):
        raise ValueError(
            "Source particle IDs are not "
            "contiguous from 1."
        )

    particles: list[
        Particle
    ] = []

    for item in raw_particles:
        particle = Particle(
            particle_id=int(
                item["particle_id"]
            ),
            center_x=float(
                item["center_x"]
            ),
            center_y=float(
                item["center_y"]
            ),
            radius=float(
                item["radius"]
            ),
        )

        if not (
            0.0
            <= particle.center_x
            < width
            and 0.0
            <= particle.center_y
            < height
        ):
            raise ValueError(
                "Particle "
                f"{particle.particle_id} "
                "center lies outside primary cell."
            )

        if (
            not math.isfinite(
                particle.radius
            )
            or particle.radius <= 0.0
        ):
            raise ValueError(
                "Particle "
                f"{particle.particle_id} "
                "radius is not positive."
            )

        particles.append(
            particle
        )

    stored_identity = str(
        source[
            "geometry_identity"
        ][
            "sha256"
        ]
    )

    if (
        canonical_source_particle_identity(
            source
        )
        != stored_identity
    ):
        raise ValueError(
            "Source physical-particle identity "
            "failed reproduction."
        )

    primary_counts = {
        particle.particle_id: 0
        for particle in particles
    }

    for record in source.get(
        "periodic_representations",
        [],
    ):
        particle_id = int(
            record[
                "particle_id"
            ]
        )

        if (
            particle_id
            not in primary_counts
        ):
            raise ValueError(
                "Periodic representation references "
                "unknown particle."
            )

        if bool(
            record[
                "is_primary"
            ]
        ):
            primary_counts[
                particle_id
            ] += 1

    if any(
        count != 1
        for count in primary_counts.values()
    ):
        raise ValueError(
            "Source lacks exactly one primary "
            "representation per particle."
        )

    return (
        source,
        particles,
        actual,
    )


def validate_source_dependent_inputs(
    args: argparse.Namespace,
    source: dict,
) -> None:
    width = float(
        source["rve"]["width"]
    )

    height = float(
        source["rve"]["height"]
    )

    if not math.isclose(
        width,
        STEP9_RVE_LENGTH,
        rel_tol=0.0,
        abs_tol=0.0,
    ):
        raise ValueError(
            "Step-9 requires RVE width = 1."
        )

    if not math.isclose(
        height,
        STEP9_RVE_LENGTH,
        rel_tol=0.0,
        abs_tol=0.0,
    ):
        raise ValueError(
            "Step-9 requires RVE height = 1."
        )

    particles = source.get(
        "particles"
    )

    if (
        not isinstance(
            particles,
            list,
        )
        or len(
            particles
        )
        != STEP9_PHYSICAL_PARTICLE_COUNT
    ):
        raise ValueError(
            "Step-9 requires exactly "
            "16 physical particles."
        )

    source_rng = source.get(
        "rng",
        {},
    )

    if (
        source_rng.get(
            "bit_generator"
        )
        != "PCG64"
    ):
        raise ValueError(
            "Source particle geometry must "
            "record PCG64."
        )

    try:
        source_particle_seed = int(
            source_rng[
                "seed"
            ]
        )
    except (
        KeyError,
        TypeError,
        ValueError,
    ) as exc:
        raise ValueError(
            "Source particle geometry lacks "
            "a valid particle seed."
        ) from exc

    if (
        source_particle_seed
        != args.expected_particle_seed
    ):
        raise ValueError(
            "Source particle seed does not "
            "match expected Step-9 "
            "validation particle seed."
        )

    if (
        2.0
        * args.void_radius
        >= width
    ):
        raise ValueError(
            "Require 2*void-radius < "
            "RVE width."
        )

    if (
        2.0
        * args.void_radius
        >= height
    ):
        raise ValueError(
            "Require 2*void-radius < "
            "RVE height."
        )

def generate_void_centers(
    args: argparse.Namespace,
    particles: list[Particle],
    width: float,
    height: float,
) -> tuple[
    list[VoidCenter],
    str,
    str | None,
    int,
]:
    rng = Generator(
        PCG64(
            args.void_seed
        )
    )

    centers: list[
        VoidCenter
    ] = []

    total_attempts = 0

    for void_id in range(
        1,
        args.void_count + 1,
    ):
        for attempt in range(
            1,
            STEP9_MAX_ATTEMPTS_PER_VOID + 1,
        ):
            total_attempts += 1

            center_x = float(
                rng.uniform(
                    0.0,
                    width,
                )
            )

            center_y = float(
                rng.uniform(
                    0.0,
                    height,
                )
            )

            particle_ok = all(
                toroidal_surface_gap(
                    center_x,
                    center_y,
                    args.void_radius,
                    particle.center_x,
                    particle.center_y,
                    particle.radius,
                    width,
                    height,
                )
                + TOL
                >= STEP9_MIN_VOID_PARTICLE_SPACING
                for particle
                in particles
            )

            if not particle_ok:
                continue

            void_ok = all(
                toroidal_surface_gap(
                    center_x,
                    center_y,
                    args.void_radius,
                    existing.center_x,
                    existing.center_y,
                    args.void_radius,
                    width,
                    height,
                )
                + TOL
                >= STEP9_MIN_VOID_VOID_SPACING
                for existing
                in centers
            )

            if not void_ok:
                continue

            centers.append(
                VoidCenter(
                    void_id=void_id,
                    center_x=center_x,
                    center_y=center_y,
                    placement_attempts=attempt,
                )
            )

            break

        else:
            return (
                centers,
                "invalid",
                (
                    "periodized_void_"
                    f"{void_id}_"
                    "placement_failed_after_"
                    f"{STEP9_MAX_ATTEMPTS_PER_VOID}_"
                    "attempts"
                ),
                total_attempts,
            )

    return (
        centers,
        "valid",
        None,
        total_attempts,
    )

def minimum_void_particle_gap(
    centers: list[VoidCenter],
    radius: float,
    particles: list[Particle],
    width: float,
    height: float,
) -> float | None:
    if (
        not centers
        or not particles
    ):
        return None

    return float(
        min(
            toroidal_surface_gap(
                center.center_x,
                center.center_y,
                radius,
                particle.center_x,
                particle.center_y,
                particle.radius,
                width,
                height,
            )
            for center in centers
            for particle in particles
        )
    )


def minimum_void_void_gap(
    centers: list[VoidCenter],
    radius: float,
    width: float,
    height: float,
) -> float | None:
    if len(
        centers
    ) < 2:
        return None

    return float(
        min(
            toroidal_surface_gap(
                first.center_x,
                first.center_y,
                radius,
                second.center_x,
                second.center_y,
                radius,
                width,
                height,
            )
            for index, first
            in enumerate(
                centers[:-1]
            )
            for second
            in centers[
                index + 1 :
            ]
        )
    )


def periodic_shifts(
    center_x: float,
    center_y: float,
    radius: float,
    width: float,
    height: float,
) -> list[
    tuple[
        float,
        float,
    ]
]:
    x_shifts = [
        0.0
    ]

    y_shifts = [
        0.0
    ]

    if (
        center_x - radius
        < 0.0
    ):
        x_shifts.append(
            width
        )

    if (
        center_x + radius
        > width
    ):
        x_shifts.append(
            -width
        )

    if (
        center_y - radius
        < 0.0
    ):
        y_shifts.append(
            height
        )

    if (
        center_y + radius
        > height
    ):
        y_shifts.append(
            -height
        )

    return [
        (
            shift_x,
            shift_y,
        )
        for shift_x in x_shifts
        for shift_y in y_shifts
    ]


def build_void_representations(
    centers: list[VoidCenter],
    radius: float,
    width: float,
    height: float,
    void_seed: int,
) -> tuple[
    list[dict],
    list[int],
]:
    records: list[
        dict
    ] = []

    crossing_ids: list[
        int
    ] = []

    for center in centers:
        shifts = periodic_shifts(
            center.center_x,
            center.center_y,
            radius,
            width,
            height,
        )

        if len(
            shifts
        ) > 1:
            crossing_ids.append(
                center.void_id
            )

        for (
            shift_x,
            shift_y,
        ) in shifts:
            records.append(
                {
                    "representation_id": (
                        len(records) + 1
                    ),
                    "void_id": (
                        center.void_id
                    ),
                    "radius": float(
                        radius
                    ),
                    "original_center_x": (
                        center.center_x
                    ),
                    "original_center_y": (
                        center.center_y
                    ),
                    "shift_x": float(
                        shift_x
                    ),
                    "shift_y": float(
                        shift_y
                    ),
                    "center_x": float(
                        center.center_x
                        + shift_x
                    ),
                    "center_y": float(
                        center.center_y
                        + shift_y
                    ),
                    "is_primary": (
                        shift_x == 0.0
                        and shift_y == 0.0
                    ),
                    "source_void_seed": int(
                        void_seed
                    ),
                }
            )

    return (
        records,
        crossing_ids,
    )


def state_identity_sha256(
    source_particle_identity: str,
    width: float,
    height: float,
    centers: list[VoidCenter],
    radius: float,
) -> str:
    payload = {
        "source_particle_geometry_identity_sha256": (
            source_particle_identity
        ),
        "width": float(
            width
        ),
        "height": float(
            height
        ),
        "voids": [
            {
                "void_id": (
                    center.void_id
                ),
                "center_x": (
                    center.center_x
                ),
                "center_y": (
                    center.center_y
                ),
                "radius": float(
                    radius
                ),
            }
            for center in centers
        ],
    }

    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(
            ",",
            ":",
        ),
        allow_nan=False,
    ).encode(
        "utf-8"
    )

    return hashlib.sha256(
        canonical
    ).hexdigest()




def build_state(
    radius: float,
    centers: list[VoidCenter],
    particles: list[Particle],
    width: float,
    height: float,
    particle_area: float,
    args: argparse.Namespace,
    source_particle_identity: str,
) -> dict:
    (
        representations,
        crossing_ids,
    ) = build_void_representations(
        centers,
        radius,
        width,
        height,
        args.void_seed,
    )

    primary_count = sum(
        bool(
            record[
                "is_primary"
            ]
        )
        for record
        in representations
    )

    min_void_particle = (
        minimum_void_particle_gap(
            centers,
            radius,
            particles,
            width,
            height,
        )
    )

    min_void_void = (
        minimum_void_void_gap(
            centers,
            radius,
            width,
            height,
        )
    )

    gross_area = (
        width * height
    )

    void_area = (
        len(
            centers
        )
        * math.pi
        * radius**2
    )

    matrix_area = (
        gross_area
        - particle_area
        - void_area
    )

    solid_area = (
        matrix_area
        + particle_area
    )

    checks = {
        "requested_void_count_reached": (
            len(
                centers
            )
            == args.void_count
        ),
        "void_count_is_step9_locked": (
            args.void_count
            in STEP9_ALLOWED_VOID_COUNTS
        ),
        "toroidal_void_particle_spacing_satisfied": (
            min_void_particle
            is None
            or (
                min_void_particle
                + TOL
                >= STEP9_MIN_VOID_PARTICLE_SPACING
            )
        ),
        "toroidal_void_void_spacing_satisfied": (
            min_void_void
            is None
            or (
                min_void_void
                + TOL
                >= STEP9_MIN_VOID_VOID_SPACING
            )
        ),
        "one_primary_representation_per_physical_void": (
            primary_count
            == len(
                centers
            )
        ),
        "periodic_representation_count_not_below_physical_count": (
            len(
                representations
            )
            >= len(
                centers
            )
        ),
        "positive_matrix_area": (
            matrix_area > 0.0
        ),
        "solid_area_consistent": (
            math.isclose(
                solid_area,
                gross_area
                - void_area,
                rel_tol=0.0,
                abs_tol=TOL,
            )
        ),
        "external_boundary_clearance_not_imposed": (
            True
        ),
    }

    return {
        "state": "defective",
        "void_radius": float(
            radius
        ),
        "void_count": len(
            centers
        ),
        "void_area": float(
            void_area
        ),
        "void_area_fraction": float(
            void_area
            / gross_area
        ),
        "matrix_area": float(
            matrix_area
        ),
        "solid_area": float(
            solid_area
        ),
        "gross_rve_area": float(
            gross_area
        ),
        "minimum_toroidal_void_particle_surface_gap": (
            min_void_particle
        ),
        "minimum_toroidal_void_void_surface_gap": (
            min_void_void
        ),
        "boundary_crossing_void_ids": (
            crossing_ids
        ),
        "boundary_crossing_void_count": (
            len(
                crossing_ids
            )
        ),
        "periodic_representation_count": (
            len(
                representations
            )
        ),
        "translated_periodic_image_count": (
            len(
                representations
            )
            - primary_count
        ),
        "analytical_area_counting": (
            "physical_voids_once_"
            "no_periodic_image_double_counting"
        ),
        "geometry_identity": {
            "method": (
                STATE_IDENTITY_METHOD
            ),
            "sha256": (
                state_identity_sha256(
                    source_particle_identity,
                    width,
                    height,
                    centers,
                    radius,
                )
            ),
        },
        "checks": checks,
        "voids": [
            {
                "void_id": (
                    center.void_id
                ),
                "center_x": (
                    center.center_x
                ),
                "center_y": (
                    center.center_y
                ),
                "radius": float(
                    radius
                ),
                "placement_attempts": (
                    center.placement_attempts
                ),
            }
            for center
            in centers
        ],
        "periodic_void_representations": (
            representations
        ),
    }

def build_metadata(
    args: argparse.Namespace,
    source_path: Path,
    source: dict,
    particles: list[Particle],
    source_sha256: str,
    centers: list[VoidCenter],
    placement_status: str,
    failure_reason: str | None,
    total_attempts: int,
) -> dict:
    width = float(
        source["rve"]["width"]
    )

    height = float(
        source["rve"]["height"]
    )

    gross_area = (
        width * height
    )

    source_identity = str(
        source[
            "geometry_identity"
        ][
            "sha256"
        ]
    )

    source_rng = source.get(
        "rng",
        {},
    )

    source_particle_seed = int(
        source_rng[
            "seed"
        ]
    )

    particle_area = float(
        sum(
            math.pi
            * particle.radius**2
            for particle
            in particles
        )
    )

    state = build_state(
        args.void_radius,
        centers,
        particles,
        width,
        height,
        particle_area,
        args,
        source_identity,
    )

    source_particle_area = float(
        source[
            "generated_geometry"
        ][
            "particle_area"
        ]
    )

    checks = {
        "source_particle_geometry_valid": (
            source.get(
                "status"
            )
            == "valid"
        ),
        "source_particle_geometry_sha256_authenticated": (
            source_sha256
            == validate_sha256_text(
                args.expected_source_sha256
            )
        ),
        "source_particle_identity_reproduced": (
            canonical_source_particle_identity(
                source
            )
            == source_identity
        ),
        "source_particle_area_preserved": (
            math.isclose(
                particle_area,
                source_particle_area,
                rel_tol=0.0,
                abs_tol=TOL,
            )
        ),
        "source_particle_seed_authenticated": (
            source_particle_seed
            == args.expected_particle_seed
        ),
        "source_particle_count_is_step9_locked": (
            len(
                particles
            )
            == STEP9_PHYSICAL_PARTICLE_COUNT
        ),
        "rve_width_is_step9_locked": (
            math.isclose(
                width,
                STEP9_RVE_LENGTH,
                rel_tol=0.0,
                abs_tol=0.0,
            )
        ),
        "rve_height_is_step9_locked": (
            math.isclose(
                height,
                STEP9_RVE_LENGTH,
                rel_tol=0.0,
                abs_tol=0.0,
            )
        ),
        "requested_void_count_reached": (
            len(
                centers
            )
            == args.void_count
        ),
        "defective_state_checks_pass": (
            all(
                state[
                    "checks"
                ].values()
            )
        ),
        "particle_geometry_reused_without_regeneration": (
            True
        ),
    }

    status = (
        placement_status
    )

    final_failure_reason = (
        failure_reason
    )

    if (
        status
        == "valid"
        and not all(
            checks.values()
        )
    ):
        status = "invalid"

        failed = [
            key
            for key, value
            in checks.items()
            if not value
        ]

        final_failure_reason = (
            "post_generation_checks_failed:"
            + ",".join(
                failed
            )
        )

    requested_void_area_fraction = (
        args.void_count
        * math.pi
        * args.void_radius**2
        / gross_area
    )

    return {
        "schema": SCHEMA,
        "status": status,
        "failure_reason": (
            final_failure_reason
        ),
        "particle_arrangement": (
            source.get(
                "arrangement"
            )
        ),
        "void_arrangement": (
            VOID_ARRANGEMENT
        ),
        "void_representation_policy": (
            REPRESENTATION_POLICY
        ),
        "source_particle_geometry": {
            "path": str(
                source_path
            ),
            "sha256": (
                source_sha256
            ),
            "schema": (
                source[
                    "schema"
                ]
            ),
            "status": (
                source[
                    "status"
                ]
            ),
            "particle_seed": (
                source_particle_seed
            ),
            "geometry_identity_sha256": (
                source_identity
            ),
            "reuse_policy": (
                "immutable_authenticated_"
                "existing_artifact"
            ),
        },
        "rng": {
            "bit_generator": (
                "PCG64"
            ),
            "rng_namespace": (
                STEP9_VALIDATION_SEED_NAMESPACE
            ),
            "particle_seed": int(
                args.expected_particle_seed
            ),
            "void_seed_status": (
                "applicable"
            ),
            "void_seed": int(
                args.void_seed
            ),
            "numpy_version": (
                np.__version__
            ),
            "seed_semantics": (
                "step9_transfer_validation_"
                "deterministic_sampling_"
                "and_provenance"
            ),
        },
        "rve": copy.deepcopy(
            source[
                "rve"
            ]
        ),
        "requested_void_geometry": {
            "state": (
                "defective"
            ),
            "void_count": int(
                args.void_count
            ),
            "void_radius": float(
                args.void_radius
            ),
            "void_area_fraction_requested_derived_from_radius": float(
                requested_void_area_fraction
            ),
            "minimum_toroidal_void_particle_surface_gap": (
                STEP9_MIN_VOID_PARTICLE_SPACING
            ),
            "minimum_toroidal_void_void_surface_gap": (
                STEP9_MIN_VOID_VOID_SPACING
            ),
            "external_boundary_clearance_imposed": (
                False
            ),
            "max_attempts_per_void": (
                STEP9_MAX_ATTEMPTS_PER_VOID
            ),
            "placement_topology": (
                "rectangular_periodic_torus"
            ),
            "state_policy": (
                "single_defective_physical_state"
            ),
        },
        "generated_geometry": {
            "particle_count": (
                len(
                    particles
                )
            ),
            "particle_area": (
                particle_area
            ),
            "particle_area_fraction": (
                particle_area
                / gross_area
            ),
            "void_count": (
                len(
                    centers
                )
            ),
            "void_area": (
                state[
                    "void_area"
                ]
            ),
            "void_area_fraction": (
                state[
                    "void_area_fraction"
                ]
            ),
            "total_void_placement_attempts": int(
                total_attempts
            ),
            "geometry_identity": (
                copy.deepcopy(
                    state[
                        "geometry_identity"
                    ]
                )
            ),
        },
        "checks": checks,
        "particles": copy.deepcopy(
            source[
                "particles"
            ]
        ),
        "particle_periodic_representations": (
            copy.deepcopy(
                source[
                    "periodic_representations"
                ]
            )
        ),
        "void_centers": [
            asdict(
                center
            )
            for center
            in centers
        ],
        "state": state,
        "scope_guard": {
            "m9_step9_transfer_validation": (
                True
            ),
            "m9_stochastic_pilot_production": (
                False
            ),
            "production_design_id_created": (
                False
            ),
            "production_realization_id_created": (
                False
            ),
            "production_pilot_sampling_rng_consumed": (
                False
            ),
            "source_particle_geometry_regenerated": (
                False
            ),
            "protected_pristine_m8_schema_mutated": (
                False
            ),
            "mesh_generated": (
                False
            ),
            "mpc_constructed": (
                False
            ),
            "fem_solve_performed": (
                False
            ),
            "tensor_reconstructed": (
                False
            ),
            "machine_learning_performed": (
                False
            ),
        },
    }

def write_metadata(
    output_path: Path,
    metadata: dict,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    payload = (
        json.dumps(
            metadata,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n"
    )

    with output_path.open(
        "x",
        encoding="utf-8",
        newline="\n",
    ) as handle:
        handle.write(
            payload
        )

def main() -> int:
    args = parse_args()

    validate_numeric_inputs(
        args
    )

    if args.output_json.exists():
        raise FileExistsError(
            "Refusing to overwrite existing output: "
            f"{args.output_json}"
        )

    if (
        args.output_json.resolve()
        == args.source_particle_geometry_json.resolve()
    ):
        raise ValueError(
            "Output JSON must not overwrite "
            "source particle geometry."
        )

    (
        source,
        particles,
        source_sha256,
    ) = load_source_particle_geometry(
        args.source_particle_geometry_json,
        args.expected_source_sha256,
    )

    validate_source_dependent_inputs(
        args,
        source,
    )

    width = float(
        source["rve"]["width"]
    )

    height = float(
        source["rve"]["height"]
    )

    (
        centers,
        placement_status,
        failure_reason,
        total_attempts,
    ) = generate_void_centers(
        args,
        particles,
        width,
        height,
    )

    metadata = build_metadata(
        args,
        args.source_particle_geometry_json,
        source,
        particles,
        source_sha256,
        centers,
        placement_status,
        failure_reason,
        total_attempts,
    )

    write_metadata(
        args.output_json,
        metadata,
    )

    print(
        json.dumps(
            metadata,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
    )

    return (
        0
        if metadata[
            "status"
        ]
        == "valid"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
