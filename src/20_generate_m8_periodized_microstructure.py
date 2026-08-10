"""Generate deterministic M8 periodized circular-particle geometry metadata.

Particle centers live on a rectangular 2D torus. Pair spacing therefore
uses minimum-image distance. Boundary-crossing particles receive periodic
image representations that preserve physical-particle identity.

This source generates geometry metadata only: no voids, mesh, or FEM solve.
It does not change protected M6/M7 geometry semantics.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from dataclasses import asdict, dataclass

import numpy as np
from numpy.random import Generator, PCG64


SCHEMA = "m8_periodized_particle_microstructure_v1"
ARRANGEMENT = "periodized_random_uniform_rejection_v1"
REPRESENTATION_POLICY = "toroidal_wrapped_images_v1"
IDENTITY_METHOD = "sha256_canonical_json_physical_particles_v1"
TOL = 1.0e-12


@dataclass(frozen=True)
class Particle:
    """One physical circular particle on the periodic torus."""

    particle_id: int
    center_x: float
    center_y: float
    radius: float
    placement_attempts: int


def parse_args() -> argparse.Namespace:
    """Parse command-line inputs."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate deterministic M8 periodized "
            "circular-particle geometry metadata."
        )
    )

    parser.add_argument(
        "--seed",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--particle-count",
        type=int,
        required=True,
    )

    parser.add_argument(
        "--radius",
        type=float,
        required=True,
    )

    parser.add_argument(
        "--min-particle-spacing",
        type=float,
        required=True,
    )

    parser.add_argument(
        "--max-attempts-per-particle",
        type=int,
        default=20000,
    )

    parser.add_argument(
        "--width",
        type=float,
        default=1.0,
    )

    parser.add_argument(
        "--height",
        type=float,
        default=1.0,
    )

    return parser.parse_args()


def validate_inputs(
    args: argparse.Namespace,
) -> None:
    """Validate requested periodized geometry state."""

    if args.seed < 0:
        raise ValueError(
            "seed must be non-negative."
        )

    if args.particle_count <= 0:
        raise ValueError(
            "particle-count must be positive."
        )

    if (
        not np.isfinite(args.width)
        or args.width <= 0.0
    ):
        raise ValueError(
            "width must be finite and positive."
        )

    if (
        not np.isfinite(args.height)
        or args.height <= 0.0
    ):
        raise ValueError(
            "height must be finite and positive."
        )

    if (
        not np.isfinite(args.radius)
        or args.radius <= 0.0
    ):
        raise ValueError(
            "radius must be finite and positive."
        )

    if 2.0 * args.radius >= args.width:
        raise ValueError(
            "Require 2*radius < width."
        )

    if 2.0 * args.radius >= args.height:
        raise ValueError(
            "Require 2*radius < height."
        )

    if (
        not np.isfinite(
            args.min_particle_spacing
        )
        or args.min_particle_spacing < 0.0
    ):
        raise ValueError(
            "min-particle-spacing must be "
            "finite and non-negative."
        )

    if args.max_attempts_per_particle <= 0:
        raise ValueError(
            "max-attempts-per-particle must be positive."
        )


def axis_minimum_image_distance(
    first: float,
    second: float,
    length: float,
) -> float:
    """Return minimum-image separation along one periodic axis."""

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
    """Return minimum-image center distance on the torus."""

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
    center_x: float,
    center_y: float,
    radius: float,
    existing: Particle,
    width: float,
    height: float,
) -> float:
    """Return periodic surface gap to an existing particle."""

    return (
        toroidal_center_distance(
            center_x,
            center_y,
            existing.center_x,
            existing.center_y,
            width,
            height,
        )
        - radius
        - existing.radius
    )


def minimum_toroidal_surface_gap(
    particles: list[Particle],
    width: float,
    height: float,
) -> float | None:
    """Return minimum periodic surface gap over all pairs."""

    if len(particles) < 2:
        return None

    gaps = [
        (
            toroidal_center_distance(
                first.center_x,
                first.center_y,
                second.center_x,
                second.center_y,
                width,
                height,
            )
            - first.radius
            - second.radius
        )
        for index, first
        in enumerate(
            particles[:-1]
        )
        for second
        in particles[index + 1 :]
    ]

    return float(
        min(gaps)
    )


def generate_particles(
    args: argparse.Namespace,
) -> tuple[
    list[Particle],
    str,
    str | None,
    int,
]:
    """Generate deterministic physical particles on the torus."""

    rng = Generator(
        PCG64(
            args.seed
        )
    )

    particles: list[Particle] = []
    total_attempts = 0

    for particle_id in range(
        1,
        args.particle_count + 1,
    ):
        for attempt in range(
            1,
            args.max_attempts_per_particle + 1,
        ):
            total_attempts += 1

            center_x = float(
                rng.uniform(
                    0.0,
                    args.width,
                )
            )

            center_y = float(
                rng.uniform(
                    0.0,
                    args.height,
                )
            )

            spacing_ok = all(
                toroidal_surface_gap(
                    center_x,
                    center_y,
                    args.radius,
                    existing,
                    args.width,
                    args.height,
                )
                + TOL
                >= args.min_particle_spacing
                for existing
                in particles
            )

            if not spacing_ok:
                continue

            particles.append(
                Particle(
                    particle_id=particle_id,
                    center_x=center_x,
                    center_y=center_y,
                    radius=float(
                        args.radius
                    ),
                    placement_attempts=attempt,
                )
            )

            break

        else:
            failure_reason = (
                "periodized_particle_"
                f"{particle_id}_"
                "placement_failed_after_"
                f"{args.max_attempts_per_particle}_"
                "attempts"
            )

            return (
                particles,
                "invalid",
                failure_reason,
                total_attempts,
            )

    return (
        particles,
        "valid",
        None,
        total_attempts,
    )


def periodic_shifts(
    particle: Particle,
    width: float,
    height: float,
) -> list[
    tuple[
        float,
        float,
    ]
]:
    """Return the primary and required wrapped-image shifts."""

    x_shifts = [
        0.0
    ]

    y_shifts = [
        0.0
    ]

    if (
        particle.center_x
        - particle.radius
        < 0.0
    ):
        x_shifts.append(
            width
        )

    if (
        particle.center_x
        + particle.radius
        > width
    ):
        x_shifts.append(
            -width
        )

    if (
        particle.center_y
        - particle.radius
        < 0.0
    ):
        y_shifts.append(
            height
        )

    if (
        particle.center_y
        + particle.radius
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
        for shift_x
        in x_shifts
        for shift_y
        in y_shifts
    ]


def build_representations(
    particles: list[Particle],
    width: float,
    height: float,
    seed: int,
) -> tuple[
    list[dict],
    list[int],
]:
    """Create primary and translated disk representations."""

    records: list[dict] = []
    crossing_ids: list[int] = []

    for particle in particles:

        shifts = periodic_shifts(
            particle,
            width,
            height,
        )

        if len(shifts) > 1:
            crossing_ids.append(
                particle.particle_id
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
                    "particle_id": (
                        particle.particle_id
                    ),
                    "radius": (
                        particle.radius
                    ),
                    "original_center_x": (
                        particle.center_x
                    ),
                    "original_center_y": (
                        particle.center_y
                    ),
                    "shift_x": float(
                        shift_x
                    ),
                    "shift_y": float(
                        shift_y
                    ),
                    "center_x": float(
                        particle.center_x
                        + shift_x
                    ),
                    "center_y": float(
                        particle.center_y
                        + shift_y
                    ),
                    "is_primary": (
                        shift_x == 0.0
                        and shift_y == 0.0
                    ),
                    "source_seed": seed,
                }
            )

    return (
        records,
        crossing_ids,
    )


def geometry_sha256(
    particles: list[Particle],
    width: float,
    height: float,
) -> str:
    """Hash canonical physical geometry without RNG metadata."""

    payload = {
        "width": float(
            width
        ),
        "height": float(
            height
        ),
        "particles": [
            {
                "particle_id": (
                    particle.particle_id
                ),
                "center_x": (
                    particle.center_x
                ),
                "center_y": (
                    particle.center_y
                ),
                "radius": (
                    particle.radius
                ),
            }
            for particle
            in particles
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


def build_metadata(
    args: argparse.Namespace,
    particles: list[Particle],
    status: str,
    failure_reason: str | None,
    total_attempts: int,
) -> dict:
    """Build one machine-readable M8 geometry record."""

    (
        representations,
        crossing_ids,
    ) = build_representations(
        particles,
        args.width,
        args.height,
        args.seed,
    )

    minimum_gap = (
        minimum_toroidal_surface_gap(
            particles,
            args.width,
            args.height,
        )
    )

    rve_area = (
        args.width
        * args.height
    )

    particle_area = sum(
        math.pi
        * particle.radius**2
        for particle
        in particles
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

    return {
        "schema": SCHEMA,
        "status": status,
        "failure_reason": (
            failure_reason
        ),
        "arrangement": (
            ARRANGEMENT
        ),
        "representation_policy": (
            REPRESENTATION_POLICY
        ),
        "rng": {
            "bit_generator": (
                "PCG64"
            ),
            "seed": (
                args.seed
            ),
            "numpy_version": (
                np.__version__
            ),
            "seed_semantics": (
                "provenance_and_grouping_only"
            ),
        },
        "rve": {
            "width": (
                args.width
            ),
            "height": (
                args.height
            ),
            "area": (
                rve_area
            ),
        },
        "requested_geometry": {
            "particle_count": (
                args.particle_count
            ),
            "particle_radius": (
                args.radius
            ),
        },
        "constraints": {
            "minimum_toroidal_particle_surface_gap": (
                args.min_particle_spacing
            ),
            "max_attempts_per_particle": (
                args.max_attempts_per_particle
            ),
            "placement_domain": (
                "particle_centers_uniform_"
                "on_rectangular_torus"
            ),
        },
        "generated_geometry": {
            "particle_count": (
                len(particles)
            ),
            "particle_area": (
                particle_area
            ),
            "particle_area_fraction": (
                particle_area
                / rve_area
            ),
            "minimum_actual_toroidal_surface_gap": (
                minimum_gap
            ),
            "total_placement_attempts": (
                total_attempts
            ),
            "boundary_crossing_particle_ids": (
                crossing_ids
            ),
            "boundary_crossing_particle_count": (
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
                "physical_particles_once_"
                "no_periodic_image_double_counting"
            ),
        },
        "geometry_identity": {
            "method": (
                IDENTITY_METHOD
            ),
            "sha256": (
                geometry_sha256(
                    particles,
                    args.width,
                    args.height,
                )
            ),
        },
        "checks": {
            "requested_particle_count_reached": (
                len(particles)
                == args.particle_count
            ),
            "toroidal_particle_spacing_satisfied": (
                minimum_gap is None
                or minimum_gap
                + TOL
                >= args.min_particle_spacing
            ),
            "one_primary_representation_per_physical_particle": (
                primary_count
                == len(particles)
            ),
            "periodic_representation_count_not_below_physical_count": (
                len(representations)
                >= len(particles)
            ),
        },
        "particles": [
            asdict(
                particle
            )
            for particle
            in particles
        ],
        "periodic_representations": (
            representations
        ),
        "scope_guard": {
            "m8_validation_construction": (
                True
            ),
            "m9_production_parameterization": (
                False
            ),
            "mesh_generated": (
                False
            ),
            "voids_generated": (
                False
            ),
            "fem_solve_performed": (
                False
            ),
            "protected_m6_m7_schema_mutated": (
                False
            ),
        },
    }


def main() -> int:
    """Generate and print one periodized geometry JSON record."""

    args = parse_args()

    validate_inputs(
        args
    )

    (
        particles,
        status,
        failure_reason,
        total_attempts,
    ) = generate_particles(
        args
    )

    metadata = build_metadata(
        args,
        particles,
        status,
        failure_reason,
        total_attempts,
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
        if status == "valid"
        else 2
    )


if __name__ == "__main__":
    raise SystemExit(
        main()
    )
