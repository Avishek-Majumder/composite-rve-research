"""Regression tests for the M7 area-weighted upper-tail statistic.

These tests protect the pure numerical helper underlying the permanent
M7 defect-sensitive candidate:

    m7_matrix_vm_annulus_tail10_v1

The tests intentionally exercise no FEM solve, mesh generation, or
DOLFINx field extraction.
"""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

import numpy as np


REPOSITORY_ROOT = Path(__file__).resolve().parents[1]

M7_SOLVER_PATH = (
    REPOSITORY_ROOT
    / "src"
    / "19_solve_m7_void_elasticity.py"
)


def load_m7_solver_module():
    """Load the numbered M7 solver directly from its source path."""

    module_name = "m7_solver_regression_test_target"

    spec = importlib.util.spec_from_file_location(
        module_name,
        M7_SOLVER_PATH,
    )

    if spec is None or spec.loader is None:
        raise RuntimeError(
            "Could not create an import specification for "
            "the M7 solver."
        )

    module = importlib.util.module_from_spec(
        spec
    )

    sys.modules[module_name] = module

    spec.loader.exec_module(
        module
    )

    return module


M7_SOLVER = load_m7_solver_module()

area_weighted_upper_tail_statistics = (
    M7_SOLVER.area_weighted_upper_tail_statistics
)


class TestAreaWeightedUpperTailStatistics(
    unittest.TestCase
):
    """Protect the permanent M7 upper-tail numerical behavior."""

    FLOAT_ATOL = 1.0e-12

    EXPECTED_KEYS = {
        "tail_fraction",
        "total_area",
        "target_tail_area",
        "effective_tail_area",
        "tail_mean",
        "raw_max",
        "area_weighted_mean",
        "contributing_cell_count",
        "fractional_cutoff_used",
    }

    def assert_float_equal(
        self,
        actual: float,
        expected: float,
    ) -> None:
        np.testing.assert_allclose(
            actual,
            expected,
            rtol=0.0,
            atol=self.FLOAT_ATOL,
            equal_nan=False,
        )

    def assert_result_contract(
        self,
        result: dict,
        *,
        tail_fraction: float,
        total_area: float,
        target_tail_area: float,
        effective_tail_area: float,
        tail_mean: float,
        raw_max: float,
        area_weighted_mean: float,
        contributing_cell_count: int,
        fractional_cutoff_used: bool,
    ) -> None:

        self.assertEqual(
            set(result),
            self.EXPECTED_KEYS,
        )

        float_expectations = {
            "tail_fraction": tail_fraction,
            "total_area": total_area,
            "target_tail_area": target_tail_area,
            "effective_tail_area": effective_tail_area,
            "tail_mean": tail_mean,
            "raw_max": raw_max,
            "area_weighted_mean": area_weighted_mean,
        }

        for key, expected in float_expectations.items():
            with self.subTest(
                field=key
            ):
                self.assert_float_equal(
                    result[key],
                    expected,
                )

        self.assertEqual(
            result[
                "contributing_cell_count"
            ],
            contributing_cell_count,
        )

        self.assertIs(
            result[
                "fractional_cutoff_used"
            ],
            fractional_cutoff_used,
        )

    def test_single_exact_top_cell(self) -> None:

        result = (
            area_weighted_upper_tail_statistics(
                values=np.array(
                    [10.0, 8.0, 1.0]
                ),
                areas=np.array(
                    [1.0, 1.0, 8.0]
                ),
                tail_fraction=0.10,
            )
        )

        self.assert_result_contract(
            result,
            tail_fraction=0.10,
            total_area=10.0,
            target_tail_area=1.0,
            effective_tail_area=1.0,
            tail_mean=10.0,
            raw_max=10.0,
            area_weighted_mean=2.6,
            contributing_cell_count=1,
            fractional_cutoff_used=False,
        )

    def test_two_exact_top_cells(self) -> None:

        result = (
            area_weighted_upper_tail_statistics(
                values=np.array(
                    [10.0, 8.0, 1.0]
                ),
                areas=np.array(
                    [0.5, 0.5, 9.0]
                ),
                tail_fraction=0.10,
            )
        )

        self.assert_result_contract(
            result,
            tail_fraction=0.10,
            total_area=10.0,
            target_tail_area=1.0,
            effective_tail_area=1.0,
            tail_mean=9.0,
            raw_max=10.0,
            area_weighted_mean=1.8,
            contributing_cell_count=2,
            fractional_cutoff_used=False,
        )

    def test_fractional_cutoff_cell(self) -> None:

        result = (
            area_weighted_upper_tail_statistics(
                values=np.array(
                    [10.0, 1.0]
                ),
                areas=np.array(
                    [0.6, 9.4]
                ),
                tail_fraction=0.10,
            )
        )

        self.assert_result_contract(
            result,
            tail_fraction=0.10,
            total_area=10.0,
            target_tail_area=1.0,
            effective_tail_area=1.0,
            tail_mean=6.4,
            raw_max=10.0,
            area_weighted_mean=1.54,
            contributing_cell_count=2,
            fractional_cutoff_used=True,
        )

    def test_unsorted_values_are_ranked_by_stress(self) -> None:

        result = (
            area_weighted_upper_tail_statistics(
                values=np.array(
                    [2.0, 10.0, 6.0, 4.0]
                ),
                areas=np.array(
                    [2.0, 2.0, 2.0, 4.0]
                ),
                tail_fraction=0.20,
            )
        )

        self.assert_result_contract(
            result,
            tail_fraction=0.20,
            total_area=10.0,
            target_tail_area=2.0,
            effective_tail_area=2.0,
            tail_mean=10.0,
            raw_max=10.0,
            area_weighted_mean=5.2,
            contributing_cell_count=1,
            fractional_cutoff_used=False,
        )

    def test_full_tail_equals_area_weighted_mean(self) -> None:

        result = (
            area_weighted_upper_tail_statistics(
                values=np.array(
                    [2.0, 10.0, 6.0, 4.0]
                ),
                areas=np.array(
                    [2.0, 2.0, 2.0, 4.0]
                ),
                tail_fraction=1.0,
            )
        )

        self.assert_result_contract(
            result,
            tail_fraction=1.0,
            total_area=10.0,
            target_tail_area=10.0,
            effective_tail_area=10.0,
            tail_mean=5.2,
            raw_max=10.0,
            area_weighted_mean=5.2,
            contributing_cell_count=4,
            fractional_cutoff_used=False,
        )

    def test_empty_input_is_rejected(self) -> None:

        with self.assertRaises(
            ValueError
        ):
            area_weighted_upper_tail_statistics(
                values=[],
                areas=[],
                tail_fraction=0.10,
            )

    def test_inputs_must_be_one_dimensional(self) -> None:

        cases = [
            (
                [[1.0, 2.0]],
                [1.0, 1.0],
            ),
            (
                [1.0, 2.0],
                [[1.0, 1.0]],
            ),
        ]

        for values, areas in cases:
            with self.subTest(
                values=values,
                areas=areas,
            ):
                with self.assertRaises(
                    ValueError
                ):
                    area_weighted_upper_tail_statistics(
                        values=values,
                        areas=areas,
                        tail_fraction=0.10,
                    )

    def test_length_mismatch_is_rejected(self) -> None:

        with self.assertRaises(
            ValueError
        ):
            area_weighted_upper_tail_statistics(
                values=[1.0, 2.0],
                areas=[1.0],
                tail_fraction=0.10,
            )

    def test_nonfinite_values_are_rejected(self) -> None:

        invalid_values = [
            float("nan"),
            float("inf"),
            float("-inf"),
        ]

        for invalid_value in invalid_values:
            with self.subTest(
                invalid_value=invalid_value
            ):
                with self.assertRaises(
                    ValueError
                ):
                    area_weighted_upper_tail_statistics(
                        values=[
                            1.0,
                            invalid_value,
                        ],
                        areas=[
                            1.0,
                            1.0,
                        ],
                        tail_fraction=0.10,
                    )

    def test_invalid_areas_are_rejected(self) -> None:

        invalid_areas = [
            float("nan"),
            float("inf"),
            0.0,
            -1.0,
        ]

        for invalid_area in invalid_areas:
            with self.subTest(
                invalid_area=invalid_area
            ):
                with self.assertRaises(
                    ValueError
                ):
                    area_weighted_upper_tail_statistics(
                        values=[
                            1.0,
                            2.0,
                        ],
                        areas=[
                            1.0,
                            invalid_area,
                        ],
                        tail_fraction=0.10,
                    )

    def test_invalid_tail_fractions_are_rejected(self) -> None:

        invalid_tail_fractions = [
            0.0,
            -0.10,
            1.10,
            float("inf"),
            float("nan"),
        ]

        for tail_fraction in invalid_tail_fractions:
            with self.subTest(
                tail_fraction=tail_fraction
            ):
                with self.assertRaises(
                    ValueError
                ):
                    area_weighted_upper_tail_statistics(
                        values=[
                            1.0,
                            2.0,
                        ],
                        areas=[
                            1.0,
                            1.0,
                        ],
                        tail_fraction=tail_fraction,
                    )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
