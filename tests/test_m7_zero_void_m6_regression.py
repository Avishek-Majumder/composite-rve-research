"""Permanent M6→M7 zero-void FEM integration regression.

This test protects the validated M7 no-void limit against invasive M8
homogenization, boundary-condition, geometry, or solver changes.

Transient geometry and solver results are generated only inside a
TemporaryDirectory and are not stored in the repository.
"""

from __future__ import annotations

import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

CONFIG = (
    REPOSITORY_ROOT
    / "configs"
    / "03_parametric_rve_base.yaml"
)

M6_GENERATOR = (
    REPOSITORY_ROOT
    / "src"
    / "14_generate_m6_random_microstructure.py"
)

M6_SOLVER = (
    REPOSITORY_ROOT
    / "src"
    / "16_solve_m6_multi_particle_elasticity.py"
)

M7_GENERATOR = (
    REPOSITORY_ROOT
    / "src"
    / "17_generate_m7_void_microstructure.py"
)

M7_SOLVER = (
    REPOSITORY_ROOT
    / "src"
    / "19_solve_m7_void_elasticity.py"
)


class TestM7ZeroVoidM6Regression(
    unittest.TestCase
):
    """Protect exact M6→M7 mechanics in the zero-void limit."""

    SUBPROCESS_TIMEOUT_SECONDS = 180

    EPSILON_ATOL = 1.0e-12
    STRESS_ATOL = 1.0e-10
    MODULUS_ATOL = 1.0e-8
    POISSON_ATOL = 1.0e-10

    def run_command(
        self,
        command: list[str],
    ) -> subprocess.CompletedProcess[str]:
        """Run one regression subprocess with captured diagnostics."""

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

        self.assertEqual(
            completed.returncode,
            0,
            msg=(
                "Regression subprocess failed.\n"
                f"Command: {' '.join(command)}\n"
                f"Return code: {completed.returncode}\n"
                f"STDOUT:\n{completed.stdout}\n"
                f"STDERR:\n{completed.stderr}"
            ),
        )

        return completed

    def load_json(
        self,
        path: Path,
    ) -> dict:
        """Read one generated regression JSON object."""

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

    def assert_regression_close(
        self,
        left,
        right,
        *,
        atol: float,
        label: str,
    ) -> None:
        """Compare two validated response quantities."""

        left_value = float(
            left
        )

        right_value = float(
            right
        )

        self.assertTrue(
            math.isclose(
                left_value,
                right_value,
                rel_tol=0.0,
                abs_tol=atol,
            ),
            msg=(
                f"{label} regression mismatch: "
                f"{left_value!r} vs {right_value!r}; "
                f"atol={atol!r}"
            ),
        )

    def test_zero_void_m7_reproduces_m6_mechanics(
        self,
    ) -> None:
        """Require M7 zero-void mechanics to reproduce protected M6."""

        temporary_path = None

        with tempfile.TemporaryDirectory(
            prefix="m7_zero_void_m6_regression_"
        ) as temporary_directory:

            temporary_path = Path(
                temporary_directory
            )

            m6_geometry_file = (
                temporary_path
                / "m6_geometry.json"
            )

            m6_result_file = (
                temporary_path
                / "m6_result.json"
            )

            m7_geometry_file = (
                temporary_path
                / "m7_zero_void_geometry.json"
            )

            m7_result_file = (
                temporary_path
                / "m7_zero_void_result.json"
            )

            # ----------------------------------------------------
            # Deterministic protected M6 realization.
            # ----------------------------------------------------

            completed = self.run_command(
                [
                    sys.executable,
                    str(
                        M6_GENERATOR
                    ),
                    "--arrangement",
                    "random",
                    "--seed",
                    "2026083001",
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
                ]
            )

            m6_geometry_file.write_text(
                completed.stdout,
                encoding="utf-8",
            )

            m6_geometry = self.load_json(
                m6_geometry_file
            )

            self.assertEqual(
                m6_geometry.get(
                    "schema"
                ),
                "m6_random_microstructure_v1",
            )

            self.assertEqual(
                m6_geometry.get(
                    "status"
                ),
                "valid",
            )

            self.assertEqual(
                m6_geometry.get(
                    "arrangement"
                ),
                "random_uniform_rejection_v1",
            )

            self.assertEqual(
                m6_geometry.get(
                    "rng",
                    {},
                ).get(
                    "seed"
                ),
                2026083001,
            )

            self.assertEqual(
                len(
                    m6_geometry.get(
                        "particles",
                        [],
                    )
                ),
                4,
            )

            self.assertTrue(
                all(
                    value is True
                    for value in m6_geometry.get(
                        "checks",
                        {},
                    ).values()
                )
            )

            # ----------------------------------------------------
            # Protected M6 mechanics.
            # ----------------------------------------------------

            self.run_command(
                [
                    sys.executable,
                    str(
                        M6_SOLVER
                    ),
                    "--config",
                    str(
                        CONFIG
                    ),
                    "--geometry-json",
                    str(
                        m6_geometry_file
                    ),
                    "--mesh-size",
                    "0.02048",
                    "--results-file",
                    str(
                        m6_result_file
                    ),
                ]
            )

            m6_result = self.load_json(
                m6_result_file
            )

            self.assertEqual(
                m6_result.get(
                    "schema"
                ),
                "m6_multi_particle_elasticity_v1",
            )

            # M6 v1 intentionally has no top-level status field.
            self.assertNotIn(
                "status",
                m6_result,
            )

            self.assertGreater(
                int(
                    m6_result[
                        "solver"
                    ][
                        "convergence_reason"
                    ]
                ),
                0,
            )

            self.assertTrue(
                all(
                    value is True
                    for value in m6_result[
                        "verification"
                    ].values()
                )
            )

            # ----------------------------------------------------
            # Wrap the identical M6 realization with zero M7 voids.
            # ----------------------------------------------------

            self.run_command(
                [
                    sys.executable,
                    str(
                        M7_GENERATOR
                    ),
                    "--source-geometry-json",
                    str(
                        m6_geometry_file
                    ),
                    "--output-json",
                    str(
                        m7_geometry_file
                    ),
                    "--void-seed",
                    "2026083002",
                    "--void-count",
                    "0",
                    "--void-radius-min",
                    "0.020",
                    "--void-radius-max",
                    "0.030",
                    "--min-void-particle-spacing",
                    "0.010",
                    "--min-void-void-spacing",
                    "0.010",
                    "--min-void-boundary-spacing",
                    "0.010",
                    "--max-placement-attempts",
                    "10000",
                ]
            )

            m7_geometry = self.load_json(
                m7_geometry_file
            )

            self.assertEqual(
                m7_geometry.get(
                    "schema"
                ),
                "m7_void_microstructure_v1",
            )

            self.assertEqual(
                m7_geometry.get(
                    "status"
                ),
                "valid",
            )

            self.assertEqual(
                m7_geometry[
                    "source_m6_geometry"
                ][
                    "particle_seed"
                ],
                2026083001,
            )

            self.assertEqual(
                m7_geometry[
                    "rng"
                ][
                    "void_seed"
                ],
                2026083002,
            )

            generated = (
                m7_geometry[
                    "generated_geometry"
                ]
            )

            self.assertEqual(
                generated[
                    "void_count"
                ],
                0,
            )

            self.assertEqual(
                float(
                    generated[
                        "void_area"
                    ]
                ),
                0.0,
            )

            self.assertEqual(
                float(
                    generated[
                        "void_area_fraction"
                    ]
                ),
                0.0,
            )

            self.assertEqual(
                generated[
                    "total_placement_attempts"
                ],
                0,
            )

            self.assertEqual(
                m7_geometry[
                    "voids"
                ],
                [],
            )

            self.assertTrue(
                all(
                    value is True
                    for value in m7_geometry[
                        "checks"
                    ].values()
                )
            )

            # ----------------------------------------------------
            # M7 zero-void mechanics.
            # ----------------------------------------------------

            self.run_command(
                [
                    sys.executable,
                    str(
                        M7_SOLVER
                    ),
                    "--config",
                    str(
                        CONFIG
                    ),
                    "--geometry-json",
                    str(
                        m7_geometry_file
                    ),
                    "--mesh-size",
                    "0.02048",
                    "--results-file",
                    str(
                        m7_result_file
                    ),
                ]
            )

            m7_result = self.load_json(
                m7_result_file
            )

            self.assertEqual(
                m7_result.get(
                    "schema"
                ),
                "m7_void_elasticity_v2",
            )

            self.assertEqual(
                m7_result.get(
                    "response_definition"
                ),
                "m7_gross_rve_axial_v1",
            )

            self.assertEqual(
                m7_result.get(
                    "local_response_definition"
                ),
                "m7_matrix_vm_annulus_tail10_v1",
            )

            self.assertEqual(
                m7_result.get(
                    "status"
                ),
                "valid",
            )

            self.assertTrue(
                m7_result[
                    "solver"
                ][
                    "converged"
                ]
            )

            self.assertGreater(
                int(
                    m7_result[
                        "solver"
                    ][
                        "convergence_reason"
                    ]
                ),
                0,
            )

            self.assertEqual(
                m7_result[
                    "geometry"
                ][
                    "void_count"
                ],
                0,
            )

            self.assertEqual(
                float(
                    m7_result[
                        "geometry"
                    ][
                        "void_area_fraction"
                    ]
                ),
                0.0,
            )

            self.assertTrue(
                m7_result[
                    "mesh"
                ][
                    "checks_passed"
                ]
            )

            self.assertEqual(
                m7_result[
                    "mesh"
                ][
                    "void_boundary_facet_count"
                ],
                0,
            )

            verification = (
                m7_result[
                    "verification"
                ]
            )

            self.assertTrue(
                all(
                    value is True
                    for value in verification.values()
                )
            )

            required_zero_void_checks = (
                "local_response_not_applicable",
                "local_response_zero_void_payload",
                "zero_void_solid_area_equals_gross",
                "zero_void_macro_sigma_equals_solid_average",
                "zero_void_macro_strain_equals_solid_average",
                "zero_void_apparent_modulus_equals_solid_diagnostic",
            )

            for key in required_zero_void_checks:
                with self.subTest(
                    verification_key=key
                ):
                    self.assertIs(
                        verification.get(
                            key
                        ),
                        True,
                    )

            # ----------------------------------------------------
            # Zero-void local response is not physically applicable.
            # ----------------------------------------------------

            local_response = (
                m7_result[
                    "local_response"
                ]
            )

            self.assertEqual(
                local_response.get(
                    "metric_id"
                ),
                "m7_matrix_vm_annulus_tail10_v1",
            )

            self.assertEqual(
                local_response.get(
                    "status"
                ),
                "not_applicable",
            )

            self.assertEqual(
                local_response.get(
                    "reason"
                ),
                "zero_void_geometry",
            )

            self.assertEqual(
                local_response.get(
                    "neighborhood_matrix_cell_count"
                ),
                0,
            )

            self.assertEqual(
                local_response.get(
                    "upper_tail_contributing_cell_count"
                ),
                0,
            )

            nullable_fields = (
                "neighborhood_matrix_area",
                "upper_tail_effective_area",
                "raw_max_sigma_vm",
                "area_weighted_neighborhood_mean_sigma_vm",
                "sigma_vm_tail10",
                "normalization_abs_macro_sigma_xx",
                "K_vm_tail10",
            )

            for field in nullable_fields:
                with self.subTest(
                    local_field=field
                ):
                    self.assertIsNone(
                        local_response.get(
                            field
                        )
                    )

            # ----------------------------------------------------
            # Exact protected M6→M7 mechanics regression.
            # ----------------------------------------------------

            m6_response = (
                m6_result[
                    "response"
                ]
            )

            m7_response = (
                m7_result[
                    "response"
                ]
            )

            comparisons = (
                (
                    "epsilon_xx_solid",
                    m6_response[
                        "average_epsilon_xx"
                    ],
                    m7_response[
                        "solid_domain_average_epsilon_xx"
                    ],
                    self.EPSILON_ATOL,
                ),
                (
                    "epsilon_yy_solid",
                    m6_response[
                        "average_epsilon_yy"
                    ],
                    m7_response[
                        "solid_domain_average_epsilon_yy"
                    ],
                    self.EPSILON_ATOL,
                ),
                (
                    "sigma_xx_solid",
                    m6_response[
                        "average_sigma_xx"
                    ],
                    m7_response[
                        "solid_domain_average_sigma_xx"
                    ],
                    self.STRESS_ATOL,
                ),
                (
                    "sigma_yy_solid",
                    m6_response[
                        "average_sigma_yy"
                    ],
                    m7_response[
                        "solid_domain_average_sigma_yy"
                    ],
                    self.STRESS_ATOL,
                ),
                (
                    "modulus_solid",
                    m6_response[
                        "effective_modulus"
                    ],
                    m7_response[
                        "solid_domain_modulus_diagnostic"
                    ],
                    self.MODULUS_ATOL,
                ),
                (
                    "poisson_solid",
                    m6_response[
                        "effective_poissons_ratio"
                    ],
                    m7_response[
                        "solid_domain_poisson_diagnostic"
                    ],
                    self.POISSON_ATOL,
                ),
                (
                    "epsilon_xx_macro",
                    m6_response[
                        "average_epsilon_xx"
                    ],
                    m7_response[
                        "macro_epsilon_xx"
                    ],
                    self.EPSILON_ATOL,
                ),
                (
                    "sigma_xx_macro",
                    m6_response[
                        "average_sigma_xx"
                    ],
                    m7_response[
                        "macro_sigma_xx"
                    ],
                    self.STRESS_ATOL,
                ),
                (
                    "modulus_macro",
                    m6_response[
                        "effective_modulus"
                    ],
                    m7_response[
                        "apparent_axial_modulus"
                    ],
                    self.MODULUS_ATOL,
                ),
            )

            for (
                label,
                m6_value,
                m7_value,
                tolerance,
            ) in comparisons:

                with self.subTest(
                    response_comparison=label
                ):
                    self.assert_regression_close(
                        m6_value,
                        m7_value,
                        atol=tolerance,
                        label=label,
                    )

        self.assertIsNotNone(
            temporary_path
        )

        self.assertFalse(
            temporary_path.exists(),
            msg=(
                "Temporary regression directory "
                "was not cleaned."
            ),
        )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
