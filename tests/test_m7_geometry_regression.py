"""Regression protection for deterministic M7 void geometry behavior.

This module protects three pre-M8 contracts:

1. identical M6 source geometry, M7 parameters, and void seed produce
   byte-identical M7 geometry metadata;
2. the independent M7 void seed changes the void realization without
   changing the protected source-particle realization;
3. a syntactically valid but geometrically impossible void request is
   returned as controlled invalid metadata rather than a partial geometry.

No FEM solve is performed by these tests.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

M6_GENERATOR = (
    REPOSITORY_ROOT
    / "src"
    / "14_generate_m6_random_microstructure.py"
)

M7_GENERATOR = (
    REPOSITORY_ROOT
    / "src"
    / "17_generate_m7_void_microstructure.py"
)


class TestM7GeometryRegression(
    unittest.TestCase
):
    SUBPROCESS_TIMEOUT_SECONDS = 60

    M6_PARTICLE_SEED = 2026083001

    M7_VOID_SEED_A = 2026083002
    M7_VOID_SEED_B = 2026083003

    INVALID_VOID_SEED = 2026083999

    def run_command(
        self,
        command: list[str],
        *,
        allowed_return_codes: tuple[int, ...],
    ) -> subprocess.CompletedProcess[str]:

        completed = subprocess.run(
            command,
            cwd=REPOSITORY_ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=self.SUBPROCESS_TIMEOUT_SECONDS,
            env={
                **os.environ,
                "PYTHONDONTWRITEBYTECODE": "1",
            },
        )

        self.assertIn(
            completed.returncode,
            allowed_return_codes,
            msg=(
                "Unexpected regression subprocess return code.\n"
                f"Command: {' '.join(command)}\n"
                f"Return code: {completed.returncode}\n"
                f"Allowed: {allowed_return_codes}\n"
                f"STDOUT:\n{completed.stdout}\n"
                f"STDERR:\n{completed.stderr}"
            ),
        )

        return completed

    def load_json(
        self,
        path: Path,
    ) -> dict:

        self.assertTrue(
            path.is_file(),
            msg=f"Expected JSON file missing: {path}",
        )

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        self.assertIsInstance(
            data,
            dict,
        )

        return data

    def create_m6_source(
        self,
        temporary_path: Path,
    ) -> tuple[Path, dict]:

        geometry_file = (
            temporary_path
            / "m6_source_geometry.json"
        )

        completed = self.run_command(
            [
                sys.executable,
                str(
                    M6_GENERATOR
                ),
                "--arrangement",
                "random",
                "--seed",
                str(
                    self.M6_PARTICLE_SEED
                ),
                "--particle-count",
                "4",
                "--radius-min",
                "0.050",
                "--radius-max",
                "0.050",
                "--min-particle-spacing",
                "0.020",
                "--min-boundary-spacing",
                "0.020",
                "--max-attempts-per-particle",
                "10000",
                "--width",
                "1.0",
                "--height",
                "1.0",
            ],
            allowed_return_codes=(0,),
        )

        geometry_file.write_text(
            completed.stdout,
            encoding="utf-8",
        )

        data = self.load_json(
            geometry_file
        )

        self.assertEqual(
            data.get(
                "schema"
            ),
            "m6_random_microstructure_v1",
        )

        self.assertEqual(
            data.get(
                "status"
            ),
            "valid",
        )

        self.assertEqual(
            data.get(
                "rng",
                {},
            ).get(
                "seed"
            ),
            self.M6_PARTICLE_SEED,
        )

        self.assertEqual(
            len(
                data.get(
                    "particles",
                    [],
                )
            ),
            4,
        )

        self.assertTrue(
            all(
                value is True
                for value in data.get(
                    "checks",
                    {},
                ).values()
            )
        )

        return geometry_file, data

    def create_valid_m7(
        self,
        *,
        source_file: Path,
        output_file: Path,
        void_seed: int,
    ) -> dict:

        self.run_command(
            [
                sys.executable,
                str(
                    M7_GENERATOR
                ),
                "--source-geometry-json",
                str(
                    source_file
                ),
                "--output-json",
                str(
                    output_file
                ),
                "--void-seed",
                str(
                    void_seed
                ),
                "--void-count",
                "1",
                "--void-radius-min",
                "0.025",
                "--void-radius-max",
                "0.025",
                "--min-void-particle-spacing",
                "0.010",
                "--min-void-void-spacing",
                "0.010",
                "--min-void-boundary-spacing",
                "0.010",
                "--max-placement-attempts",
                "10000",
            ],
            allowed_return_codes=(0,),
        )

        data = self.load_json(
            output_file
        )

        self.assertEqual(
            data.get(
                "schema"
            ),
            "m7_void_microstructure_v1",
        )

        self.assertEqual(
            data.get(
                "status"
            ),
            "valid",
        )

        self.assertEqual(
            data.get(
                "rng",
                {},
            ).get(
                "void_seed"
            ),
            void_seed,
        )

        generated = (
            data.get(
                "generated_geometry",
                {}
            )
        )

        self.assertEqual(
            generated.get(
                "void_count"
            ),
            1,
        )

        self.assertEqual(
            len(
                data.get(
                    "voids",
                    [],
                )
            ),
            1,
        )

        self.assertTrue(
            all(
                value is True
                for value in data.get(
                    "checks",
                    {},
                ).values()
            )
        )

        return data

    def test_identical_void_seed_is_byte_deterministic(
        self,
    ) -> None:

        with tempfile.TemporaryDirectory(
            prefix="m7_geometry_determinism_"
        ) as temporary_directory:

            temporary_path = Path(
                temporary_directory
            )

            source_file, _ = (
                self.create_m6_source(
                    temporary_path
                )
            )

            first_file = (
                temporary_path
                / "m7_same_seed_a.json"
            )

            second_file = (
                temporary_path
                / "m7_same_seed_b.json"
            )

            first = self.create_valid_m7(
                source_file=source_file,
                output_file=first_file,
                void_seed=self.M7_VOID_SEED_A,
            )

            second = self.create_valid_m7(
                source_file=source_file,
                output_file=second_file,
                void_seed=self.M7_VOID_SEED_A,
            )

            self.assertEqual(
                first_file.read_bytes(),
                second_file.read_bytes(),
            )

            self.assertEqual(
                first,
                second,
            )

            self.assertEqual(
                first[
                    "voids"
                ],
                second[
                    "voids"
                ],
            )

    def test_void_seed_is_independent_of_particle_realization(
        self,
    ) -> None:

        with tempfile.TemporaryDirectory(
            prefix="m7_void_seed_regression_"
        ) as temporary_directory:

            temporary_path = Path(
                temporary_directory
            )

            source_file, _ = (
                self.create_m6_source(
                    temporary_path
                )
            )

            first_file = (
                temporary_path
                / "m7_seed_a.json"
            )

            second_file = (
                temporary_path
                / "m7_seed_b.json"
            )

            first = self.create_valid_m7(
                source_file=source_file,
                output_file=first_file,
                void_seed=self.M7_VOID_SEED_A,
            )

            second = self.create_valid_m7(
                source_file=source_file,
                output_file=second_file,
                void_seed=self.M7_VOID_SEED_B,
            )

            self.assertEqual(
                first[
                    "source_m6_geometry"
                ][
                    "sha256"
                ],
                second[
                    "source_m6_geometry"
                ][
                    "sha256"
                ],
            )

            self.assertEqual(
                first[
                    "source_m6_geometry"
                ][
                    "particle_seed"
                ],
                self.M6_PARTICLE_SEED,
            )

            self.assertEqual(
                second[
                    "source_m6_geometry"
                ][
                    "particle_seed"
                ],
                self.M6_PARTICLE_SEED,
            )

            self.assertEqual(
                first[
                    "particles"
                ],
                second[
                    "particles"
                ],
            )

            self.assertNotEqual(
                first[
                    "rng"
                ][
                    "void_seed"
                ],
                second[
                    "rng"
                ][
                    "void_seed"
                ],
            )

            self.assertNotEqual(
                first[
                    "voids"
                ],
                second[
                    "voids"
                ],
            )

    def test_impossible_void_region_returns_controlled_invalid_metadata(
        self,
    ) -> None:

        with tempfile.TemporaryDirectory(
            prefix="m7_invalid_geometry_regression_"
        ) as temporary_directory:

            temporary_path = Path(
                temporary_directory
            )

            source_file, _ = (
                self.create_m6_source(
                    temporary_path
                )
            )

            invalid_file = (
                temporary_path
                / "m7_invalid_geometry.json"
            )

            completed = self.run_command(
                [
                    sys.executable,
                    str(
                        M7_GENERATOR
                    ),
                    "--source-geometry-json",
                    str(
                        source_file
                    ),
                    "--output-json",
                    str(
                        invalid_file
                    ),
                    "--void-seed",
                    str(
                        self.INVALID_VOID_SEED
                    ),
                    "--void-count",
                    "1",
                    "--void-radius-min",
                    "0.49",
                    "--void-radius-max",
                    "0.49",
                    "--min-void-particle-spacing",
                    "0.001",
                    "--min-void-void-spacing",
                    "0.001",
                    "--min-void-boundary-spacing",
                    "0.020",
                    "--max-placement-attempts",
                    "10000",
                ],
                allowed_return_codes=(2,),
            )

            self.assertEqual(
                completed.returncode,
                2,
            )

            invalid = self.load_json(
                invalid_file
            )

            self.assertEqual(
                invalid.get(
                    "schema"
                ),
                "m7_void_microstructure_v1",
            )

            self.assertEqual(
                invalid.get(
                    "status"
                ),
                "invalid",
            )

            self.assertEqual(
                invalid.get(
                    "failure_reason"
                ),
                (
                    "void_radius_and_boundary_spacing_"
                    "leave_no_usable_sampling_region"
                ),
            )

            generated = (
                invalid.get(
                    "generated_geometry",
                    {}
                )
            )

            self.assertEqual(
                generated.get(
                    "void_count"
                ),
                0,
            )

            self.assertEqual(
                float(
                    generated.get(
                        "void_area"
                    )
                ),
                0.0,
            )

            self.assertEqual(
                float(
                    generated.get(
                        "void_area_fraction"
                    )
                ),
                0.0,
            )

            self.assertEqual(
                generated.get(
                    "total_placement_attempts"
                ),
                0,
            )

            self.assertEqual(
                invalid.get(
                    "voids"
                ),
                [],
            )

            self.assertIs(
                invalid.get(
                    "checks",
                    {},
                ).get(
                    "requested_void_count_reached"
                ),
                False,
            )

            other_checks = {
                key: value
                for key, value
                in invalid.get(
                    "checks",
                    {},
                ).items()
                if key
                != "requested_void_count_reached"
            }

            self.assertTrue(
                all(
                    value is True
                    for value in other_checks.values()
                )
            )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
