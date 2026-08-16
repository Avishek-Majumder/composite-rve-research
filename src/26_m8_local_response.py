"""Pure numerical kernels for the M8 Stage-7 cell local response.

The module consumes pre-evaluated matrix-cell midpoint coordinates,
von-Mises values, physical cell areas, physical void records, and the
gross macroscopic X-load stress. It performs no mechanics solve and no
file input/output.
"""

from __future__ import annotations

import math

import numpy as np


M8_CELL_METRIC_ID = "m8_matrix_vm_annulus_cell_tail10_v1"
M8_LOCAL_TAIL_FRACTION = 0.10

def area_weighted_upper_tail_statistics(values, areas, tail_fraction: float) -> dict:
    """Return exact physical-area-weighted upper-tail statistics."""
    stress_values = np.asarray(values, dtype=np.float64)
    cell_areas = np.asarray(areas, dtype=np.float64)
    if stress_values.ndim != 1:
        raise ValueError('values must be one-dimensional.')
    if cell_areas.ndim != 1:
        raise ValueError('areas must be one-dimensional.')
    if stress_values.size == 0:
        raise ValueError('At least one value is required.')
    if stress_values.size != cell_areas.size:
        raise ValueError('values and areas must have identical lengths.')
    if not np.all(np.isfinite(stress_values)):
        raise ValueError('All values must be finite.')
    if not np.all(np.isfinite(cell_areas)):
        raise ValueError('All areas must be finite.')
    if not np.all(cell_areas > 0.0):
        raise ValueError('All cell areas must be strictly positive.')
    tail_fraction = float(tail_fraction)
    if not math.isfinite(tail_fraction) or tail_fraction <= 0.0 or tail_fraction > 1.0:
        raise ValueError('tail_fraction must satisfy 0 < tail_fraction <= 1.')
    total_area = float(np.sum(cell_areas, dtype=np.float64))
    if not math.isfinite(total_area) or total_area <= 0.0:
        raise ValueError('Total physical area must be finite and positive.')
    target_tail_area = tail_fraction * total_area
    order = np.argsort(-stress_values, kind='stable')
    accumulated_area = 0.0
    weighted_sum = 0.0
    contributing_cell_count = 0
    fractional_cutoff_used = False
    area_tolerance = 64.0 * np.finfo(np.float64).eps * total_area
    for index in order:
        remaining_area = target_tail_area - accumulated_area
        if remaining_area <= area_tolerance:
            break
        available_area = float(cell_areas[index])
        included_area = min(available_area, remaining_area)
        if included_area <= 0.0:
            continue
        weighted_sum += float(stress_values[index]) * included_area
        accumulated_area += included_area
        contributing_cell_count += 1
        if included_area < available_area - area_tolerance:
            fractional_cutoff_used = True
    if not math.isclose(accumulated_area, target_tail_area, rel_tol=0.0, abs_tol=area_tolerance):
        raise RuntimeError('Upper-tail area accumulation did not reach the requested physical area.')
    tail_mean = weighted_sum / target_tail_area
    area_weighted_mean = float(np.sum(stress_values * cell_areas, dtype=np.float64) / total_area)
    raw_max = float(stress_values[order[0]])
    outputs = (tail_mean, raw_max, area_weighted_mean, weighted_sum, accumulated_area)
    if not all((math.isfinite(float(value)) for value in outputs)):
        raise RuntimeError('Upper-tail calculation produced a non-finite output.')
    return {'tail_fraction': float(tail_fraction), 'total_area': float(total_area), 'target_tail_area': float(target_tail_area), 'effective_tail_area': float(accumulated_area), 'tail_mean': float(tail_mean), 'raw_max': float(raw_max), 'area_weighted_mean': float(area_weighted_mean), 'contributing_cell_count': int(contributing_cell_count), 'fractional_cutoff_used': bool(fractional_cutoff_used)}


def axis_minimum_image_distance(first: float, second: float, length: float) -> float:
    direct = abs(first - second)
    return min(direct, length - direct)


def toroidal_center_distance(x1: float, y1: float, x2: float, y2: float, width: float, height: float) -> float:
    dx = axis_minimum_image_distance(x1, x2, width)
    dy = axis_minimum_image_distance(y1, y2, height)
    return math.hypot(dx, dy)


def _validated_physical_voids(
    physical_voids: list[dict],
    width: float,
    height: float,
) -> list[tuple[int, float, float, float]]:
    """Validate and canonicalize physical void records."""
    if not isinstance(
        physical_voids,
        list,
    ):
        raise ValueError(
            "physical_voids must be a list."
        )

    width = float(
        width
    )
    height = float(
        height
    )

    if (
        not math.isfinite(
            width
        )
        or width <= 0.0
        or not math.isfinite(
            height
        )
        or height <= 0.0
    ):
        raise ValueError(
            "Periodic cell dimensions must be finite and positive."
        )

    image_record_fields = {
        "representation_id",
        "original_center_x",
        "original_center_y",
        "shift_x",
        "shift_y",
        "is_primary",
    }

    canonical = []
    seen_ids = set()

    for record in physical_voids:
        if not isinstance(
            record,
            dict,
        ):
            raise ValueError(
                "Each physical void record must be a dictionary."
            )

        if (
            image_record_fields
            & set(
                record
            )
        ):
            raise ValueError(
                "physical_voids must contain physical records, "
                "not periodic image records."
            )

        required = {
            "void_id",
            "center_x",
            "center_y",
            "radius",
        }

        if not required.issubset(
            record
        ):
            raise ValueError(
                "Each physical void record must contain "
                "void_id, center_x, center_y and radius."
            )

        void_id = int(
            record[
                "void_id"
            ]
        )
        center_x = float(
            record[
                "center_x"
            ]
        )
        center_y = float(
            record[
                "center_y"
            ]
        )
        radius = float(
            record[
                "radius"
            ]
        )

        if void_id <= 0:
            raise ValueError(
                "Physical void IDs must be positive."
            )

        if void_id in seen_ids:
            raise ValueError(
                "Physical void IDs must be unique."
            )

        seen_ids.add(
            void_id
        )

        if (
            not math.isfinite(
                center_x
            )
            or not math.isfinite(
                center_y
            )
            or not math.isfinite(
                radius
            )
            or radius <= 0.0
        ):
            raise ValueError(
                "Void centers/radii must be finite and radius positive."
            )

        tolerance_x = (
            64.0
            * np.finfo(
                np.float64
            ).eps
            * max(
                1.0,
                abs(
                    width
                ),
            )
        )

        tolerance_y = (
            64.0
            * np.finfo(
                np.float64
            ).eps
            * max(
                1.0,
                abs(
                    height
                ),
            )
        )

        if (
            center_x < -tolerance_x
            or center_x > width + tolerance_x
            or center_y < -tolerance_y
            or center_y > height + tolerance_y
        ):
            raise ValueError(
                "Physical void centers must lie inside the periodic cell."
            )

        center_x = min(
            max(
                center_x,
                0.0,
            ),
            width,
        )

        center_y = min(
            max(
                center_y,
                0.0,
            ),
            height,
        )

        canonical.append(
            (
                void_id,
                center_x,
                center_y,
                radius,
            )
        )

    return canonical


def matrix_cell_annulus_union_mask(
    matrix_cell_midpoints,
    physical_voids: list[dict],
    width: float,
    height: float,
):
    """Return the union mask for the locked M8 physical annuli."""
    points = np.asarray(
        matrix_cell_midpoints,
        dtype=np.float64,
    )

    if (
        points.ndim != 2
        or points.shape[1] != 2
    ):
        raise ValueError(
            "matrix_cell_midpoints must have shape (N, 2)."
        )

    if not np.all(
        np.isfinite(
            points
        )
    ):
        raise ValueError(
            "All matrix-cell midpoint coordinates must be finite."
        )

    width = float(
        width
    )
    height = float(
        height
    )

    canonical_voids = (
        _validated_physical_voids(
            physical_voids,
            width,
            height,
        )
    )

    tolerance_x = (
        64.0
        * np.finfo(
            np.float64
        ).eps
        * max(
            1.0,
            abs(
                width
            ),
        )
    )

    tolerance_y = (
        64.0
        * np.finfo(
            np.float64
        ).eps
        * max(
            1.0,
            abs(
                height
            ),
        )
    )

    if (
        np.any(
            points[
                :,
                0
            ]
            < -tolerance_x
        )
        or np.any(
            points[
                :,
                0
            ]
            > width + tolerance_x
        )
        or np.any(
            points[
                :,
                1
            ]
            < -tolerance_y
        )
        or np.any(
            points[
                :,
                1
            ]
            > height + tolerance_y
        )
    ):
        raise ValueError(
            "Matrix-cell midpoints must lie inside the periodic cell."
        )

    points = points.copy()

    points[
        :,
        0
    ] = np.clip(
        points[
            :,
            0
        ],
        0.0,
        width,
    )

    points[
        :,
        1
    ] = np.clip(
        points[
            :,
            1
        ],
        0.0,
        height,
    )

    mask = np.zeros(
        points.shape[0],
        dtype=bool,
    )

    for (
        _void_id,
        center_x,
        center_y,
        radius,
    ) in canonical_voids:
        direct_x = np.abs(
            points[
                :,
                0
            ]
            - center_x
        )

        direct_y = np.abs(
            points[
                :,
                1
            ]
            - center_y
        )

        dx = np.minimum(
            direct_x,
            width - direct_x,
        )

        dy = np.minimum(
            direct_y,
            height - direct_y,
        )

        distances = np.sqrt(
            dx * dx
            + dy * dy
        )

        mask |= (
            (distances > radius)
            & (
                distances
                <= 2.0 * radius
            )
        )

    return mask


def evaluate_m8_matrix_vm_annulus_cell_tail10(
    matrix_cell_midpoints,
    sigma_vm_values,
    cell_areas,
    physical_voids: list[dict],
    width: float,
    height: float,
    macro_sigma_11: float,
) -> dict:
    """Evaluate the locked M8 cell-based local-response candidate."""
    points = np.asarray(
        matrix_cell_midpoints,
        dtype=np.float64,
    )

    sigma_vm = np.asarray(
        sigma_vm_values,
        dtype=np.float64,
    )

    areas = np.asarray(
        cell_areas,
        dtype=np.float64,
    )

    if (
        points.ndim != 2
        or points.shape[1] != 2
    ):
        raise ValueError(
            "matrix_cell_midpoints must have shape (N, 2)."
        )

    if sigma_vm.ndim != 1:
        raise ValueError(
            "sigma_vm_values must be one-dimensional."
        )

    if areas.ndim != 1:
        raise ValueError(
            "cell_areas must be one-dimensional."
        )

    if (
        points.shape[0] != sigma_vm.size
        or sigma_vm.size != areas.size
    ):
        raise ValueError(
            "Midpoint, stress and area arrays must have identical lengths."
        )

    if not np.all(
        np.isfinite(
            sigma_vm
        )
    ):
        raise ValueError(
            "All von-Mises values must be finite."
        )

    if not np.all(
        sigma_vm >= 0.0
    ):
        raise ValueError(
            "Von-Mises values must be non-negative."
        )

    if (
        not np.all(
            np.isfinite(
                areas
            )
        )
        or not np.all(
            areas > 0.0
        )
    ):
        raise ValueError(
            "All physical cell areas must be finite and positive."
        )

    canonical_voids = (
        _validated_physical_voids(
            physical_voids,
            width,
            height,
        )
    )

    if len(
        canonical_voids
    ) == 0:
        return {
            "metric_id": M8_CELL_METRIC_ID,
            "status": "not_applicable",
            "reason": "zero_void_geometry",
            "tail_fraction": float(
                M8_LOCAL_TAIL_FRACTION
            ),
            "physical_void_count": 0,
            "neighborhood_matrix_cell_count": 0,
            "neighborhood_matrix_area": None,
            "upper_tail_effective_area": None,
            "upper_tail_contributing_cell_count": 0,
            "fractional_cutoff_used": None,
            "raw_max_sigma_vm": None,
            "area_weighted_neighborhood_mean_sigma_vm": None,
            "sigma_vm_tail10": None,
            "normalization_abs_Sigma_11": None,
            "K_vm_tail10": None,
        }

    macro_sigma_11 = float(
        macro_sigma_11
    )

    if (
        not math.isfinite(
            macro_sigma_11
        )
        or abs(
            macro_sigma_11
        ) <= 0.0
    ):
        raise ValueError(
            "Positive-void local metric requires finite, non-zero Sigma_11."
        )

    mask = matrix_cell_annulus_union_mask(
        matrix_cell_midpoints=points,
        physical_voids=physical_voids,
        width=width,
        height=height,
    )

    neighborhood_count = int(
        np.count_nonzero(
            mask
        )
    )

    if neighborhood_count <= 0:
        raise RuntimeError(
            "Positive-void geometry produced no eligible "
            "matrix cells in the locked annulus neighborhood."
        )

    statistics = (
        area_weighted_upper_tail_statistics(
            values=sigma_vm[
                mask
            ],
            areas=areas[
                mask
            ],
            tail_fraction=M8_LOCAL_TAIL_FRACTION,
        )
    )

    normalization = abs(
        macro_sigma_11
    )

    K_vm_tail10 = (
        statistics[
            "tail_mean"
        ]
        / normalization
    )

    if (
        not math.isfinite(
            K_vm_tail10
        )
        or K_vm_tail10 < 0.0
    ):
        raise RuntimeError(
            "Normalized local response is invalid."
        )

    tolerance = (
        1.0e-12
        * max(
            1.0,
            abs(
                statistics[
                    "raw_max"
                ]
            ),
        )
    )

    if not (
        statistics[
            "raw_max"
        ]
        + tolerance
        >= statistics[
            "tail_mean"
        ]
        and statistics[
            "tail_mean"
        ]
        + tolerance
        >= statistics[
            "area_weighted_mean"
        ]
    ):
        raise RuntimeError(
            "Local-response ordering sanity failed."
        )

    return {
        "metric_id": M8_CELL_METRIC_ID,
        "status": "valid",
        "reason": None,
        "tail_fraction": float(
            M8_LOCAL_TAIL_FRACTION
        ),
        "physical_void_count": int(
            len(
                canonical_voids
            )
        ),
        "neighborhood_matrix_cell_count": int(
            neighborhood_count
        ),
        "neighborhood_matrix_area": float(
            statistics[
                "total_area"
            ]
        ),
        "upper_tail_effective_area": float(
            statistics[
                "effective_tail_area"
            ]
        ),
        "upper_tail_contributing_cell_count": int(
            statistics[
                "contributing_cell_count"
            ]
        ),
        "fractional_cutoff_used": bool(
            statistics[
                "fractional_cutoff_used"
            ]
        ),
        "raw_max_sigma_vm": float(
            statistics[
                "raw_max"
            ]
        ),
        "area_weighted_neighborhood_mean_sigma_vm": float(
            statistics[
                "area_weighted_mean"
            ]
        ),
        "sigma_vm_tail10": float(
            statistics[
                "tail_mean"
            ]
        ),
        "normalization_abs_Sigma_11": float(
            normalization
        ),
        "K_vm_tail10": float(
            K_vm_tail10
        ),
    }
