"""Regression tests for M8 periodic corner-image classification."""

from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path


REPOSITORY_ROOT = (
    Path(__file__).resolve().parents[1]
)

MESHER_PATH = (
    REPOSITORY_ROOT
    / "src"
    / "21_generate_m8_periodized_mesh.py"
)


def load_mesher_module():
    module_name = (
        "m8_periodic_corner_regression_target"
    )

    spec = importlib.util.spec_from_file_location(
        module_name,
        MESHER_PATH,
    )

    if (
        spec is None
        or spec.loader is None
    ):
        raise RuntimeError(
            "Could not load permanent M8 mesher."
        )

    module = (
        importlib.util.module_from_spec(
            spec
        )
    )

    sys.modules[
        module_name
    ] = module

    spec.loader.exec_module(
        module
    )

    return module


MESHER = load_mesher_module()

classify = (
    MESHER.disk_cell_intersection_classification
)


class TestM8PeriodicCornerRepresentation(
    unittest.TestCase
):
    def classify_particle7(
        self,
        *,
        center_x: float,
        center_y: float,
    ):
        return classify(
            center_x=center_x,
            center_y=center_y,
            radius=0.05,
            cell_side=2.5,
            tolerance=1.0e-10,
        )

    def test_primary_is_positive_area(
        self,
    ) -> None:
        category, clearance = (
            self.classify_particle7(
                center_x=2.451744100900038,
                center_y=0.041285930361791845,
            )
        )

        self.assertEqual(
            category,
            "positive_area",
        )

        self.assertLess(
            clearance,
            -1.0e-10,
        )

    def test_top_wrapped_image_is_positive_area(
        self,
    ) -> None:
        category, clearance = (
            self.classify_particle7(
                center_x=2.451744100900038,
                center_y=2.541285930361792,
            )
        )

        self.assertEqual(
            category,
            "positive_area",
        )

        self.assertLess(
            clearance,
            -1.0e-10,
        )

    def test_left_wrapped_image_is_positive_area(
        self,
    ) -> None:
        category, clearance = (
            self.classify_particle7(
                center_x=-0.048255899099962196,
                center_y=0.041285930361791845,
            )
        )

        self.assertEqual(
            category,
            "positive_area",
        )

        self.assertLess(
            clearance,
            -1.0e-10,
        )

    def test_diagonal_image_is_disjoint(
        self,
    ) -> None:
        category, clearance = (
            self.classify_particle7(
                center_x=-0.048255899099962196,
                center_y=2.541285930361792,
            )
        )

        self.assertEqual(
            category,
            "disjoint",
        )

        self.assertAlmostEqual(
            clearance,
            0.013507163720201346,
            places=14,
        )

    def test_exact_corner_tangent_is_ambiguous(
        self,
    ) -> None:
        category, clearance = classify(
            center_x=-0.03,
            center_y=2.54,
            radius=0.05,
            cell_side=2.5,
            tolerance=1.0e-10,
        )

        self.assertEqual(
            category,
            "ambiguous_tangent",
        )

        self.assertLessEqual(
            abs(clearance),
            1.0e-10,
        )

    def test_nonfinite_input_rejected(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError
        ):
            classify(
                center_x=float("nan"),
                center_y=0.0,
                radius=0.05,
                cell_side=2.5,
            )

    def test_zero_radius_rejected(
        self,
    ) -> None:
        with self.assertRaises(
            ValueError
        ):
            classify(
                center_x=0.5,
                center_y=0.5,
                radius=0.0,
                cell_side=2.5,
            )


if __name__ == "__main__":
    unittest.main(
        verbosity=2
    )
