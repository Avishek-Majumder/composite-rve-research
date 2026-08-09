"""Generate reproducible random multi-particle RVE geometry metadata.

This M6 foundation script generates circular particles only.
It does not create void defects, meshes, or FEM solutions.
"""

from __future__ import annotations

import argparse
import json
import math
from dataclasses import asdict, dataclass

import numpy as np
from numpy.random import Generator, PCG64


@dataclass(frozen=True)
class Particle:
    """One circular reinforcing particle."""

    particle_id: int
    center_x: float
    center_y: float
    radius: float
    placement_attempts: int


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate reproducible non-overlapping circular particles "
            "inside a rectangular 2D RVE."
        )
    )

    parser.add_argument("--seed", type=int, required=True)
    parser.add_argument("--particle-count", type=int, required=True)
    parser.add_argument("--radius-min", type=float, required=True)
    parser.add_argument("--radius-max", type=float, required=True)
    parser.add_argument(
        "--min-particle-spacing",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--min-boundary-spacing",
        type=float,
        required=True,
    )
    parser.add_argument(
        "--max-attempts-per-particle",
        type=int,
        default=10000,
    )
    parser.add_argument("--width", type=float, default=1.0)
    parser.add_argument("--height", type=float, default=1.0)

    return parser.parse_args()


def validate_inputs(args: argparse.Namespace) -> None:
    """Validate requested geometry-generation inputs."""

    if args.seed < 0:
        raise ValueError("seed must be a non-negative integer.")

    if args.particle_count <= 0:
        raise ValueError("particle-count must be positive.")

    if (
        not np.isfinite(args.width)
        or not np.isfinite(args.height)
        or args.width <= 0.0
        or args.height <= 0.0
    ):
        raise ValueError("RVE width and height must be finite and positive.")

    if (
        not np.isfinite(args.radius_min)
        or not np.isfinite(args.radius_max)
        or args.radius_min <= 0.0
        or args.radius_max <= 0.0
        or args.radius_min > args.radius_max
    ):
        raise ValueError(
            "Require 0 < radius-min <= radius-max."
        )

    if (
        not np.isfinite(args.min_particle_spacing)
        or args.min_particle_spacing < 0.0
    ):
        raise ValueError(
            "min-particle-spacing must be finite and non-negative."
        )

    if (
        not np.isfinite(args.min_boundary_spacing)
        or args.min_boundary_spacing < 0.0
    ):
        raise ValueError(
            "min-boundary-spacing must be finite and non-negative."
        )

    if args.max_attempts_per_particle <= 0:
        raise ValueError(
            "max-attempts-per-particle must be positive."
        )

    required_half_span = (
        args.radius_max + args.min_boundary_spacing
    )

    if 2.0 * required_half_span >= args.width:
        raise ValueError(
            "radius-max plus boundary spacing leaves no usable "
            "x-position range."
        )

    if 2.0 * required_half_span >= args.height:
        raise ValueError(
            "radius-max plus boundary spacing leaves no usable "
            "y-position range."
        )


def particle_surface_gap(
    candidate_x: float,
    candidate_y: float,
    candidate_radius: float,
    existing: Particle,
) -> float:
    """Return surface-to-surface gap between two circular particles."""

    center_distance = math.hypot(
        candidate_x - existing.center_x,
        candidate_y - existing.center_y,
    )

    return (
        center_distance
        - candidate_radius
        - existing.radius
    )


def minimum_pair_gap(particles: list[Particle]) -> float | None:
    """Return minimum surface gap between all particle pairs."""

    if len(particles) < 2:
        return None

    gaps: list[float] = []

    for i, first in enumerate(particles[:-1]):
        for second in particles[i + 1 :]:
            gaps.append(
                math.hypot(
                    first.center_x - second.center_x,
                    first.center_y - second.center_y,
                )
                - first.radius
                - second.radius
            )

    return min(gaps)


def minimum_boundary_gap(
    particles: list[Particle],
    width: float,
    height: float,
) -> float | None:
    """Return minimum particle-to-RVE-boundary surface gap."""

    if not particles:
        return None

    gaps: list[float] = []

    for particle in particles:
        gaps.extend(
            [
                particle.center_x - particle.radius,
                width - particle.center_x - particle.radius,
                particle.center_y - particle.radius,
                height - particle.center_y - particle.radius,
            ]
        )

    return min(gaps)


def generate_particles(
    args: argparse.Namespace,
) -> tuple[list[Particle], str, str | None, int]:
    """Generate particles using deterministic rejection sampling."""

    rng = Generator(PCG64(args.seed))

    particles: list[Particle] = []
    total_attempts = 0
    tolerance = 1.0e-12

    for particle_index in range(1, args.particle_count + 1):
        radius = float(
            rng.uniform(args.radius_min, args.radius_max)
        )

        x_low = radius + args.min_boundary_spacing
        x_high = (
            args.width
            - radius
            - args.min_boundary_spacing
        )

        y_low = radius + args.min_boundary_spacing
        y_high = (
            args.height
            - radius
            - args.min_boundary_spacing
        )

        placed = False

        for attempt in range(
            1,
            args.max_attempts_per_particle + 1,
        ):
            total_attempts += 1

            center_x = float(rng.uniform(x_low, x_high))
            center_y = float(rng.uniform(y_low, y_high))

            spacing_valid = all(
                particle_surface_gap(
                    center_x,
                    center_y,
                    radius,
                    existing,
                )
                + tolerance
                >= args.min_particle_spacing
                for existing in particles
            )

            if not spacing_valid:
                continue

            particles.append(
                Particle(
                    particle_id=particle_index,
                    center_x=center_x,
                    center_y=center_y,
                    radius=radius,
                    placement_attempts=attempt,
                )
            )

            placed = True
            break

        if not placed:
            reason = (
                "placement_failed_for_particle_"
                f"{particle_index}_after_"
                f"{args.max_attempts_per_particle}_attempts"
            )

            return (
                particles,
                "invalid",
                reason,
                total_attempts,
            )

    return particles, "valid", None, total_attempts


def build_metadata(
    args: argparse.Namespace,
    particles: list[Particle],
    status: str,
    failure_reason: str | None,
    total_attempts: int,
) -> dict:
    """Build reproducible machine-readable geometry metadata."""

    total_particle_area = sum(
        math.pi * particle.radius**2
        for particle in particles
    )

    rve_area = args.width * args.height

    pair_gap = minimum_pair_gap(particles)

    boundary_gap = minimum_boundary_gap(
        particles,
        args.width,
        args.height,
    )

    tolerance = 1.0e-12

    pair_spacing_ok = (
        pair_gap is None
        or pair_gap + tolerance
        >= args.min_particle_spacing
    )

    boundary_spacing_ok = (
        boundary_gap is None
        or boundary_gap + tolerance
        >= args.min_boundary_spacing
    )

    return {
        "schema": "m6_random_microstructure_v1",
        "status": status,
        "failure_reason": failure_reason,
        "arrangement": "random_uniform_rejection_v1",
        "rng": {
            "bit_generator": "PCG64",
            "seed": args.seed,
            "numpy_version": np.__version__,
        },
        "rve": {
            "width": args.width,
            "height": args.height,
            "area": rve_area,
        },
        "requested_geometry": {
            "particle_count": args.particle_count,
            "radius_min": args.radius_min,
            "radius_max": args.radius_max,
        },
        "constraints": {
            "min_particle_spacing": (
                args.min_particle_spacing
            ),
            "min_boundary_spacing": (
                args.min_boundary_spacing
            ),
            "max_attempts_per_particle": (
                args.max_attempts_per_particle
            ),
        },
        "generated_geometry": {
            "particle_count": len(particles),
            "particle_area": total_particle_area,
            "particle_area_fraction": (
                total_particle_area / rve_area
            ),
            "minimum_particle_surface_gap": pair_gap,
            "minimum_boundary_surface_gap": boundary_gap,
            "total_placement_attempts": total_attempts,
        },
        "checks": {
            "requested_particle_count_reached": (
                len(particles) == args.particle_count
            ),
            "particle_spacing_satisfied": pair_spacing_ok,
            "boundary_spacing_satisfied": (
                boundary_spacing_ok
            ),
        },
        "particles": [
            asdict(particle)
            for particle in particles
        ],
    }


def main() -> int:
    """Generate and print one geometry metadata record."""

    args = parse_args()
    validate_inputs(args)

    (
        particles,
        status,
        failure_reason,
        total_attempts,
    ) = generate_particles(args)

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
        )
    )

    return 0 if status == "valid" else 2


if __name__ == "__main__":
    raise SystemExit(main())
