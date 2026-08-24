"""Mesh one M9 Step-9 defective periodized true-hole geometry state.

The input is an authenticated single-state geometry artifact emitted by src/28.
This source preserves the validated M8 true-hole CAD, physical-tag, periodic
curve-pairing, periodic-mesh, node-correspondence, and area-accounting
mechanisms while adapting only the Step-9 schema/provenance interface and
locked defective multiplicities.

No production pilot identity is created. Merely importing or statically
compiling this source does not initialize Gmsh or generate scientific evidence.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path

import gmsh
import numpy as np

GEOMETRY_SCHEMA = "m9_step9_void_microstructure_v1"
MESH_SCHEMA = "m9_step9_void_mesh_diagnostics_v1"
STEP9_VALIDATION_SEED_NAMESPACE = (
    "composite-rve-m9-step9-transfer-validation-v1"
)
STEP9_ALLOWED_VOID_COUNTS = frozenset({1, 2, 4})
STEP9_PHYSICAL_PARTICLE_COUNT = 16
STEP9_RVE_LENGTH = 1.0
STEP9_MIN_VOID_PARTICLE_SPACING = 0.020
STEP9_MIN_VOID_VOID_SPACING = 0.020
STEP9_MAX_ATTEMPTS_PER_VOID = 20000

AUTHORITIES = {
    "M8_TARGET_MESH_PROTOCOL.md": "0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f",
    "src/18_generate_m7_void_mesh.py": "8455b280f0505910fe66708f3ed4a98f5a9bb097a459ea53ba18e07259f9a258",
    "src/21_generate_m8_periodized_mesh.py": "0713c46add5395bce97d8bdf03e52050310889935921f306d958be076d9cc3cc",
    "src/24_generate_m8_periodized_void_mesh.py": "c5a726bf0a3c0fe51875ba370d725b211722356a8b3eee6ff2fe505fb441a773",
    "src/28_generate_m9_step9_void_microstructure.py": "20c2d56b734518bf6bf18f867652d562778290e146c47be961e3a416645af160",
}

CAD_ABS_TOL = 1.0e-10
BBOX_TOL = 2.0e-6

MATRIX_PHYSICAL_TAG = 1
PARTICLE_PHYSICAL_TAG = 2
VOID_BOUNDARY_PHYSICAL_TAG = 3

LEFT_PHYSICAL_TAG = 11
RIGHT_PHYSICAL_TAG = 12
BOTTOM_PHYSICAL_TAG = 13
TOP_PHYSICAL_TAG = 14

PERIODIC_PAIR_TOL = 1.0e-8
NODE_TOL = 1.0e-10
MESH_AREA_FRACTION_TOL = 5.0e-3



def must(ok: bool, message: str) -> None:
    if not ok:
        print(f"FAIL — DO NOT CONTINUE: {message}")
        raise RuntimeError(message)
    print(f"PASS — {message}")


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description=(
            "Validate or mesh one authenticated M9 Step-9 "
            "single-state defective true-hole geometry."
        )
    )
    p.add_argument(
        "--geometry-json",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--expected-geometry-sha256",
        required=True,
    )
    p.add_argument(
        "--mesh-size",
        type=float,
        required=True,
    )
    p.add_argument(
        "--mesh-out",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--diagnostics-out",
        type=Path,
        required=True,
    )
    p.add_argument(
        "--cad-validate-only",
        action="store_true",
        help=(
            "Build and authenticate the Step-9 periodized true-hole "
            "OpenCASCADE topology, but do not generate a mesh "
            "or write output artifacts."
        ),
    )
    p.add_argument(
        "--generate-mesh",
        action="store_true",
        help=(
            "Apply the validated periodic curve-mesh constraints, generate "
            "the first-order triangular true-hole mesh, authenticate "
            "periodic node correspondence and material coverage, then "
            "write the requested Step-9 mesh and diagnostics."
        ),
    )
    return p.parse_args()



def validate_representation_contract(
    physical: list[dict],
    reps: list[dict],
    id_key: str,
    label: str,
) -> None:
    ids = [
        int(item[id_key])
        for item in physical
    ]

    if ids != list(
        range(
            1,
            len(physical) + 1,
        )
    ):
        raise ValueError(
            f"{label} physical IDs are not contiguous from 1."
        )

    if len(reps) < len(physical):
        raise ValueError(
            f"{label} periodic representation count "
            "is below physical count."
        )

    by_id = {
        int(item[id_key]): item
        for item in physical
    }

    primary = {
        object_id: 0
        for object_id in by_id
    }

    for expected_rep_id, rep in enumerate(
        reps,
        start=1,
    ):
        if (
            int(rep["representation_id"])
            != expected_rep_id
        ):
            raise ValueError(
                f"{label} representation IDs "
                "are not contiguous."
            )

        object_id = int(
            rep[id_key]
        )

        if object_id not in by_id:
            raise ValueError(
                f"{label} representation references "
                "an unknown ID."
            )

        source = by_id[
            object_id
        ]

        ox = float(
            rep["original_center_x"]
        )
        oy = float(
            rep["original_center_y"]
        )
        sx = float(
            rep["shift_x"]
        )
        sy = float(
            rep["shift_y"]
        )
        cx = float(
            rep["center_x"]
        )
        cy = float(
            rep["center_y"]
        )

        if not math.isclose(
            float(rep["radius"]),
            float(source["radius"]),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ):
            raise ValueError(
                f"{label} representation changed radius."
            )

        if not (
            math.isclose(
                ox,
                float(source["center_x"]),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
            and math.isclose(
                oy,
                float(source["center_y"]),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        ):
            raise ValueError(
                f"{label} representation changed "
                "original center."
            )

        if not (
            math.isclose(
                cx,
                ox + sx,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
            and math.isclose(
                cy,
                oy + sy,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
        ):
            raise ValueError(
                f"{label} representation translation "
                "is inconsistent."
            )

        is_primary = bool(
            rep["is_primary"]
        )

        if (
            is_primary
            != (
                sx == 0.0
                and sy == 0.0
            )
        ):
            raise ValueError(
                f"{label} primary flag is inconsistent."
            )

        if is_primary:
            primary[
                object_id
            ] += 1

    if any(
        count != 1
        for count in primary.values()
    ):
        raise ValueError(
            f"{label} lacks exactly one primary "
            "representation per object."
        )

    must(
        True,
        (
            f"{label} periodic representation contract "
            "authenticated"
        ),
    )



def disk_cell_intersection_classification(
    center_x: float,
    center_y: float,
    radius: float,
    width: float,
    height: float,
    tolerance: float = CAD_ABS_TOL,
) -> tuple[str, float]:
    """Classify a periodic disk against the closed RVE rectangle."""

    values = (
        center_x,
        center_y,
        radius,
        width,
        height,
        tolerance,
    )

    if not all(
        math.isfinite(value)
        for value in values
    ):
        raise ValueError(
            "disk/cell intersection inputs must be finite"
        )

    if radius <= 0.0:
        raise ValueError(
            "disk radius must be positive"
        )

    if width <= 0.0 or height <= 0.0:
        raise ValueError(
            "RVE dimensions must be positive"
        )

    if tolerance < 0.0:
        raise ValueError(
            "intersection tolerance must be non-negative"
        )

    nearest_x = min(
        max(center_x, 0.0),
        width,
    )

    nearest_y = min(
        max(center_y, 0.0),
        height,
    )

    distance_to_cell = math.hypot(
        center_x - nearest_x,
        center_y - nearest_y,
    )

    clearance = (
        distance_to_cell
        - radius
    )

    if clearance < -tolerance:
        return (
            "positive_area",
            float(clearance),
        )

    if clearance > tolerance:
        return (
            "disjoint",
            float(clearance),
        )

    return (
        "ambiguous_tangent",
        float(clearance),
    )


def bbox_inside_cell(
    bbox: tuple[float, ...],
    width: float,
    height: float,
) -> bool:
    return (
        bbox[0] >= -BBOX_TOL
        and bbox[1] >= -BBOX_TOL
        and bbox[3] <= width + BBOX_TOL
        and bbox[4] <= height + BBOX_TOL
    )



def curve_center_length(
    curve_tag: int,
) -> tuple[tuple[float, float, float], float]:
    center = (
        gmsh.model.occ.getCenterOfMass(
            1,
            curve_tag,
        )
    )

    length = float(
        gmsh.model.occ.getMass(
            1,
            curve_tag,
        )
    )

    return (
        (
            float(center[0]),
            float(center[1]),
            float(center[2]),
        ),
        length,
    )


def pair_periodic_curves(
    master_tags: list[int],
    slave_tags: list[int],
    dx: float,
    dy: float,
    axis_name: str,
) -> list[tuple[int, int]]:
    """Pair opposite translated CAD pieces as (slave, master)."""

    must(
        len(master_tags) > 0,
        f"{axis_name} master boundary contains CAD segments",
    )

    must(
        len(master_tags) == len(slave_tags),
        f"{axis_name} opposite CAD segment counts match",
    )

    unmatched = {
        int(tag)
        for tag in slave_tags
    }

    pairs: list[
        tuple[int, int]
    ] = []

    for master in sorted(
        int(tag)
        for tag in master_tags
    ):
        (
            master_center,
            master_length,
        ) = curve_center_length(
            master
        )

        target_center = (
            master_center[0] + dx,
            master_center[1] + dy,
            master_center[2],
        )

        matches: list[int] = []

        for slave in sorted(
            unmatched
        ):
            (
                slave_center,
                slave_length,
            ) = curve_center_length(
                slave
            )

            center_error = max(
                abs(
                    slave_center[index]
                    - target_center[index]
                )
                for index
                in range(3)
            )

            length_error = abs(
                slave_length
                - master_length
            )

            if (
                center_error <= PERIODIC_PAIR_TOL
                and length_error <= PERIODIC_PAIR_TOL
            ):
                matches.append(
                    slave
                )

        must(
            len(matches) == 1,
            (
                f"{axis_name} master curve {master} has "
                "exactly one translated center/length match"
            ),
        )

        slave = matches[0]

        unmatched.remove(
            slave
        )

        # Gmsh setPeriodic convention used by protected src/21.
        pairs.append(
            (
                slave,
                master,
            )
        )

    must(
        not unmatched,
        f"{axis_name} all slave CAD segments were paired",
    )

    must(
        len(pairs) == len(master_tags),
        f"{axis_name} every master CAD segment was paired",
    )

    return pairs


def boundary_material_identity(
    curve_tag: int,
    retained_surface_tags: set[int],
    matrix_surface_tags: set[int],
    particle_surface_tags: set[int],
    surface_to_particle_id: dict[int, int],
) -> tuple[str, int | None]:
    upward, _ = (
        gmsh.model.getAdjacencies(
            1,
            curve_tag,
        )
    )

    adjacent = [
        int(tag)
        for tag in upward
        if int(tag)
        in retained_surface_tags
    ]

    must(
        len(adjacent) == 1,
        (
            f"external boundary curve {curve_tag} "
            "has exactly one retained cell-side surface"
        ),
    )

    surface_tag = adjacent[0]

    if (
        surface_tag
        in particle_surface_tags
    ):
        must(
            surface_tag
            in surface_to_particle_id,
            (
                "boundary-adjacent particle surface "
                "has authenticated physical-particle ownership"
            ),
        )

        return (
            "particle",
            int(
                surface_to_particle_id[
                    surface_tag
                ]
            ),
        )

    must(
        surface_tag
        in matrix_surface_tags,
        (
            "external boundary adjacency belongs "
            "to known matrix/particle material"
        ),
    )

    return (
        "matrix",
        None,
    )


def classify_periodic_representations(
    representations: list[dict],
    width: float,
    height: float,
    object_name: str,
) -> tuple[list[dict], list[dict]]:
    positive: list[dict] = []
    disjoint: list[dict] = []

    for rep in representations:
        classification, clearance = (
            disk_cell_intersection_classification(
                center_x=float(rep["center_x"]),
                center_y=float(rep["center_y"]),
                radius=float(rep["radius"]),
                width=width,
                height=height,
            )
        )

        must(
            classification
            != "ambiguous_tangent",
            (
                f"{object_name} representation "
                f"{rep['representation_id']} is not "
                "tangent/near-tangent to the RVE"
            ),
        )

        record = dict(rep)
        record[
            "cell_intersection_classification"
        ] = classification
        record[
            "cell_clearance"
        ] = float(clearance)

        if classification == "positive_area":
            positive.append(record)
        else:
            disjoint.append(record)

    must(
        len(positive) > 0,
        f"{object_name} has positive-area CAD representations",
    )

    must(
        len(positive) + len(disjoint)
        == len(representations),
        (
            f"{object_name} positive-area plus disjoint "
            "representations reproduce input bookkeeping"
        ),
    )

    return positive, disjoint


def build_periodized_true_hole_cad(
    geometry: dict,
    *,
    generate_mesh: bool = False,
    mesh_size: float | None = None,
    mesh_out: Path | None = None,
    diagnostics_out: Path | None = None,
    source_geometry_sha256: str | None = None,
) -> dict:
    """Build/audit Step-9 true-hole CAD and optionally generate its mesh."""

    rve = geometry["rve"]

    width = float(
        rve["width"]
    )
    height = float(
        rve["height"]
    )

    gross_area = (
        width
        * height
    )

    particles = geometry[
        "particles"
    ]

    particle_reps = geometry[
        "particle_periodic_representations"
    ]

    state = geometry[
        "state"
    ]

    voids = state[
        "voids"
    ]

    void_reps = state[
        "periodic_void_representations"
    ]

    expected_particle_area_by_id = {
        int(particle["particle_id"]): (
            math.pi
            * float(particle["radius"]) ** 2
        )
        for particle in particles
    }

    expected_particle_area = sum(
        expected_particle_area_by_id.values()
    )

    expected_void_area = sum(
        math.pi
        * float(void["radius"]) ** 2
        for void in voids
    )

    expected_void_boundary_length = sum(
        2.0
        * math.pi
        * float(void["radius"])
        for void in voids
    )

    expected_matrix_area = (
        gross_area
        - expected_particle_area
        - expected_void_area
    )

    expected_material_area = (
        gross_area
        - expected_void_area
    )

    must(
        expected_matrix_area > 0.0,
        "expected matrix CAD area is positive",
    )

    must(
        math.isclose(
            expected_void_area,
            float(state["void_area"]),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "physical void area agrees with state metadata",
    )

    (
        positive_particle_reps,
        disjoint_particle_reps,
    ) = classify_periodic_representations(
        particle_reps,
        width,
        height,
        "particle",
    )

    (
        positive_void_reps,
        disjoint_void_reps,
    ) = classify_periodic_representations(
        void_reps,
        width,
        height,
        "void",
    )

    print(
        "Positive-area particle representations:",
        len(positive_particle_reps),
    )

    print(
        "Disjoint particle bookkeeping representations:",
        len(disjoint_particle_reps),
    )

    print(
        "Positive-area void representations:",
        len(positive_void_reps),
    )

    print(
        "Disjoint void bookkeeping representations:",
        len(disjoint_void_reps),
    )

    gmsh.initialize()

    try:
        gmsh.option.setNumber(
            "General.Terminal",
            0,
        )

        gmsh.model.add(
            "m9_step9_void_true_hole_cad"
        )

        rectangle_tag = (
            gmsh.model.occ.addRectangle(
                0.0,
                0.0,
                0.0,
                width,
                height,
            )
        )

        # ----------------------------------------------------
        # True holes: subtract only periodic void pieces that
        # have positive-area intersection with the cell.
        # ----------------------------------------------------

        void_disk_dimtags = []

        for rep in positive_void_reps:
            disk_tag = (
                gmsh.model.occ.addDisk(
                    float(rep["center_x"]),
                    float(rep["center_y"]),
                    0.0,
                    float(rep["radius"]),
                    float(rep["radius"]),
                )
            )

            void_disk_dimtags.append(
                (
                    2,
                    int(disk_tag),
                )
            )

        (
            cut_entities,
            _cut_map,
        ) = gmsh.model.occ.cut(
            [
                (
                    2,
                    int(rectangle_tag),
                )
            ],
            void_disk_dimtags,
            removeObject=True,
            removeTool=True,
        )

        material_seed_surfaces = [
            int(tag)
            for dim, tag in cut_entities
            if dim == 2
        ]

        must(
            len(material_seed_surfaces) == 1,
            (
                "periodized void subtraction leaves one "
                "connected material seed surface"
            ),
        )

        # ----------------------------------------------------
        # Conformal particle fragmentation using only
        # positive-area periodic particle representations.
        # ----------------------------------------------------

        particle_disk_dimtags = []

        for rep in positive_particle_reps:
            disk_tag = (
                gmsh.model.occ.addDisk(
                    float(rep["center_x"]),
                    float(rep["center_y"]),
                    0.0,
                    float(rep["radius"]),
                    float(rep["radius"]),
                )
            )

            rep[
                "_cad_disk_tag"
            ] = int(
                disk_tag
            )

            particle_disk_dimtags.append(
                (
                    2,
                    int(disk_tag),
                )
            )

        (
            _fragment_entities,
            fragment_map,
        ) = gmsh.model.occ.fragment(
            [
                (
                    2,
                    material_seed_surfaces[0],
                )
            ],
            particle_disk_dimtags,
            removeObject=True,
            removeTool=True,
        )

        gmsh.model.occ.synchronize()

        must(
            len(fragment_map)
            == 1 + len(positive_particle_reps),
            "particle fragment map has expected object/tool entries",
        )

        inside_surface_tags: set[int] = set()
        outside_surface_dimtags = []

        for dim, tag in gmsh.model.getEntities(
            2
        ):
            if dim != 2:
                continue

            bbox = (
                gmsh.model.getBoundingBox(
                    2,
                    tag,
                )
            )

            if bbox_inside_cell(
                bbox,
                width,
                height,
            ):
                inside_surface_tags.add(
                    int(tag)
                )
            else:
                outside_surface_dimtags.append(
                    (
                        2,
                        int(tag),
                    )
                )

        must(
            bool(inside_surface_tags),
            "fragmentation produced retained cell surfaces",
        )

        if outside_surface_dimtags:
            gmsh.model.occ.remove(
                outside_surface_dimtags,
                recursive=True,
            )

            gmsh.model.occ.synchronize()

        retained_surface_tags = {
            int(tag)
            for dim, tag
            in gmsh.model.getEntities(
                2
            )
            if dim == 2
        }

        must(
            bool(retained_surface_tags),
            "retained CAD surfaces exist after outside trimming",
        )

        particle_surface_tags: set[int] = set()

        surface_to_particle_id: dict[
            int,
            int,
        ] = {}

        for rep, mapping in zip(
            positive_particle_reps,
            fragment_map[1:],
            strict=True,
        ):
            mapped_inside = sorted(
                int(tag)
                for dim, tag in mapping
                if (
                    dim == 2
                    and int(tag)
                    in retained_surface_tags
                )
            )

            must(
                len(mapped_inside) == 1,
                (
                    "each positive-area particle representation "
                    "maps to exactly one retained particle piece "
                    f"(particle {rep['particle_id']}, "
                    f"representation {rep['representation_id']})"
                ),
            )

            surface_tag = (
                mapped_inside[0]
            )

            must(
                surface_tag
                not in surface_to_particle_id,
                "particle CAD piece has unique representation ownership",
            )

            particle_id = int(
                rep["particle_id"]
            )

            surface_to_particle_id[
                surface_tag
            ] = particle_id

            particle_surface_tags.add(
                surface_tag
            )

        matrix_surface_tags = (
            retained_surface_tags
            - particle_surface_tags
        )

        must(
            bool(matrix_surface_tags),
            "matrix CAD surfaces exist",
        )

        must(
            particle_surface_tags.isdisjoint(
                matrix_surface_tags
            ),
            "matrix and particle CAD surface sets are disjoint",
        )

        must(
            particle_surface_tags
            | matrix_surface_tags
            == retained_surface_tags,
            "every retained 2D surface is matrix or particle",
        )

        # ----------------------------------------------------
        # Exact physical area accounting.
        # ----------------------------------------------------

        particle_area_by_id = {
            particle_id: 0.0
            for particle_id
            in expected_particle_area_by_id
        }

        for surface_tag in particle_surface_tags:
            particle_id = (
                surface_to_particle_id[
                    surface_tag
                ]
            )

            particle_area_by_id[
                particle_id
            ] += float(
                gmsh.model.occ.getMass(
                    2,
                    surface_tag,
                )
            )

        maximum_particle_id_area_error = max(
            abs(
                particle_area_by_id[
                    particle_id
                ]
                - expected_particle_area_by_id[
                    particle_id
                ]
            )
            for particle_id
            in particle_area_by_id
        )

        cad_particle_area = sum(
            particle_area_by_id.values()
        )

        cad_matrix_area = sum(
            float(
                gmsh.model.occ.getMass(
                    2,
                    surface_tag,
                )
            )
            for surface_tag
            in matrix_surface_tags
        )

        cad_material_area = (
            cad_particle_area
            + cad_matrix_area
        )

        cad_void_area = (
            gross_area
            - cad_material_area
        )

        print(
            "Expected particle CAD area:",
            expected_particle_area,
        )

        print(
            "Actual particle CAD area  :",
            cad_particle_area,
        )

        print(
            "Expected matrix CAD area  :",
            expected_matrix_area,
        )

        print(
            "Actual matrix CAD area    :",
            cad_matrix_area,
        )

        print(
            "Expected physical void area:",
            expected_void_area,
        )

        print(
            "CAD removed void area      :",
            cad_void_area,
        )

        print(
            "Maximum per-particle wrapped area error:",
            maximum_particle_id_area_error,
        )

        must(
            maximum_particle_id_area_error
            <= CAD_ABS_TOL,
            (
                "each physical particle's wrapped CAD pieces "
                "sum to exactly one physical particle area"
            ),
        )

        must(
            math.isclose(
                cad_particle_area,
                expected_particle_area,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            ),
            "CAD particle area has no periodic double counting",
        )

        must(
            math.isclose(
                cad_matrix_area,
                expected_matrix_area,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            ),
            "CAD matrix area matches analytical matrix area",
        )

        must(
            math.isclose(
                cad_void_area,
                expected_void_area,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            ),
            (
                "true-hole CAD removes exactly one physical "
                "void area with no periodic-image double counting"
            ),
        )

        must(
            math.isclose(
                cad_material_area,
                expected_material_area,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            ),
            "CAD contains no 2D void material surfaces",
        )

        # ----------------------------------------------------
        # Identify external straight pieces versus true-hole
        # circular/arc boundaries using surface adjacency.
        # ----------------------------------------------------

        all_curve_tags = {
            int(tag)
            for dim, tag
            in gmsh.model.getEntities(
                1
            )
            if dim == 1
        }

        def curve_on_side(
            curve_tag: int,
            axis: int,
            value: float,
        ) -> bool:
            bbox = (
                gmsh.model.getBoundingBox(
                    1,
                    curve_tag,
                )
            )

            lo = bbox[
                axis
            ]

            hi = bbox[
                axis + 3
            ]

            return (
                abs(lo - value)
                <= BBOX_TOL
                and abs(hi - value)
                <= BBOX_TOL
            )

        left_curves = {
            tag
            for tag in all_curve_tags
            if curve_on_side(
                tag,
                0,
                0.0,
            )
        }

        right_curves = {
            tag
            for tag in all_curve_tags
            if curve_on_side(
                tag,
                0,
                width,
            )
        }

        bottom_curves = {
            tag
            for tag in all_curve_tags
            if curve_on_side(
                tag,
                1,
                0.0,
            )
        }

        top_curves = {
            tag
            for tag in all_curve_tags
            if curve_on_side(
                tag,
                1,
                height,
            )
        }

        must(
            bool(left_curves)
            and bool(right_curves)
            and bool(bottom_curves)
            and bool(top_curves),
            "all four external CAD sides contain retained segments",
        )

        external_curves = (
            left_curves
            | right_curves
            | bottom_curves
            | top_curves
        )

        # ----------------------------------------------------
        # Periodic CAD-side readiness before mesh.setPeriodic.
        #
        # Boundary-crossing particles and true holes can split
        # external sides into multiple pieces. Opposite sides
        # must nevertheless be one-to-one translated copies.
        # ----------------------------------------------------

        x_pairs = pair_periodic_curves(
            master_tags=sorted(
                left_curves
            ),
            slave_tags=sorted(
                right_curves
            ),
            dx=width,
            dy=0.0,
            axis_name="X",
        )

        y_pairs = pair_periodic_curves(
            master_tags=sorted(
                bottom_curves
            ),
            slave_tags=sorted(
                top_curves
            ),
            dx=0.0,
            dy=height,
            axis_name="Y",
        )

        x_particle_ids: set[int] = set()
        y_particle_ids: set[int] = set()

        for (
            axis_name,
            pairs,
            observed_particle_ids,
        ) in (
            (
                "X",
                x_pairs,
                x_particle_ids,
            ),
            (
                "Y",
                y_pairs,
                y_particle_ids,
            ),
        ):
            for slave, master in pairs:
                master_identity = (
                    boundary_material_identity(
                        master,
                        retained_surface_tags,
                        matrix_surface_tags,
                        particle_surface_tags,
                        surface_to_particle_id,
                    )
                )

                slave_identity = (
                    boundary_material_identity(
                        slave,
                        retained_surface_tags,
                        matrix_surface_tags,
                        particle_surface_tags,
                        surface_to_particle_id,
                    )
                )

                print(
                    f"{axis_name} CAD pair:",
                    "master",
                    master,
                    master_identity,
                    "-> slave",
                    slave,
                    slave_identity,
                )

                must(
                    master_identity
                    == slave_identity,
                    (
                        f"{axis_name} opposite CAD pieces "
                        "have identical material/feature identity"
                    ),
                )

                if (
                    master_identity[0]
                    == "particle"
                ):
                    observed_particle_ids.add(
                        int(
                            master_identity[1]
                        )
                    )

        expected_x_particle_ids = sorted(
            {
                int(rep["particle_id"])
                for rep
                in particle_reps
                if not math.isclose(
                    float(rep["shift_x"]),
                    0.0,
                    rel_tol=0.0,
                    abs_tol=1.0e-14,
                )
            }
        )

        expected_y_particle_ids = sorted(
            {
                int(rep["particle_id"])
                for rep
                in particle_reps
                if not math.isclose(
                    float(rep["shift_y"]),
                    0.0,
                    rel_tol=0.0,
                    abs_tol=1.0e-14,
                )
            }
        )

        must(
            sorted(
                x_particle_ids
            )
            == expected_x_particle_ids,
            (
                "X wrapped particle identities agree with "
                "authenticated periodic representation metadata"
            ),
        )

        must(
            sorted(
                y_particle_ids
            )
            == expected_y_particle_ids,
            (
                "Y wrapped particle identities agree with "
                "authenticated periodic representation metadata"
            ),
        )

        left_boundary_length = sum(
            curve_center_length(
                tag
            )[1]
            for tag
            in left_curves
        )

        right_boundary_length = sum(
            curve_center_length(
                tag
            )[1]
            for tag
            in right_curves
        )

        bottom_boundary_length = sum(
            curve_center_length(
                tag
            )[1]
            for tag
            in bottom_curves
        )

        top_boundary_length = sum(
            curve_center_length(
                tag
            )[1]
            for tag
            in top_curves
        )

        print(
            "External material-side lengths:",
            {
                "left": left_boundary_length,
                "right": right_boundary_length,
                "bottom": bottom_boundary_length,
                "top": top_boundary_length,
            },
        )

        must(
            math.isclose(
                left_boundary_length,
                right_boundary_length,
                rel_tol=0.0,
                abs_tol=PERIODIC_PAIR_TOL,
            ),
            (
                "left/right retained material-side lengths "
                "are periodic matches"
            ),
        )

        must(
            math.isclose(
                bottom_boundary_length,
                top_boundary_length,
                rel_tol=0.0,
                abs_tol=PERIODIC_PAIR_TOL,
            ),
            (
                "bottom/top retained material-side lengths "
                "are periodic matches"
            ),
        )

        void_boundary_curves: set[int] = set()

        for curve_tag in sorted(
            all_curve_tags
            - external_curves
        ):
            upward, _ = (
                gmsh.model.getAdjacencies(
                    1,
                    curve_tag,
                )
            )

            adjacent = {
                int(tag)
                for tag in upward
                if int(tag)
                in retained_surface_tags
            }

            if (
                len(adjacent) == 1
                and next(iter(adjacent))
                in matrix_surface_tags
            ):
                void_boundary_curves.add(
                    curve_tag
                )

        must(
            bool(void_boundary_curves),
            "true-hole CAD contains void-boundary curves",
        )

        cad_void_boundary_length = sum(
            float(
                gmsh.model.occ.getMass(
                    1,
                    curve_tag,
                )
            )
            for curve_tag
            in void_boundary_curves
        )

        print(
            "Expected total physical void-boundary length:",
            expected_void_boundary_length,
        )

        print(
            "Actual total CAD void-boundary length      :",
            cad_void_boundary_length,
        )

        must(
            math.isclose(
                cad_void_boundary_length,
                expected_void_boundary_length,
                rel_tol=0.0,
                abs_tol=CAD_ABS_TOL,
            ),
            (
                "periodized true-hole boundary pieces sum "
                "to the physical void circumferences once"
            ),
        )

        # ----------------------------------------------------
        # CAD physical groups only. No mesh is generated.
        # ----------------------------------------------------

        gmsh.model.addPhysicalGroup(
            2,
            sorted(
                matrix_surface_tags
            ),
            MATRIX_PHYSICAL_TAG,
        )

        gmsh.model.setPhysicalName(
            2,
            MATRIX_PHYSICAL_TAG,
            "matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            sorted(
                particle_surface_tags
            ),
            PARTICLE_PHYSICAL_TAG,
        )

        gmsh.model.setPhysicalName(
            2,
            PARTICLE_PHYSICAL_TAG,
            "particle",
        )

        gmsh.model.addPhysicalGroup(
            1,
            sorted(
                void_boundary_curves
            ),
            VOID_BOUNDARY_PHYSICAL_TAG,
        )

        gmsh.model.setPhysicalName(
            1,
            VOID_BOUNDARY_PHYSICAL_TAG,
            "void_boundary",
        )

        for (
            curves,
            physical_tag,
            physical_name,
        ) in (
            (
                left_curves,
                LEFT_PHYSICAL_TAG,
                "left",
            ),
            (
                right_curves,
                RIGHT_PHYSICAL_TAG,
                "right",
            ),
            (
                bottom_curves,
                BOTTOM_PHYSICAL_TAG,
                "bottom",
            ),
            (
                top_curves,
                TOP_PHYSICAL_TAG,
                "top",
            ),
        ):
            gmsh.model.addPhysicalGroup(
                1,
                sorted(
                    curves
                ),
                physical_tag,
            )

            gmsh.model.setPhysicalName(
                1,
                physical_tag,
                physical_name,
            )

        periodic_mesh_constraints_applied = False
        mesh_generated = False

        mesh_metrics: dict = {}

        if generate_mesh:
            must(
                mesh_size is not None
                and math.isfinite(mesh_size)
                and mesh_size > 0.0,
                "mesh-generation mode received a finite positive mesh size",
            )

            must(
                mesh_out is not None,
                "mesh-generation mode received a mesh output path",
            )

            must(
                diagnostics_out is not None,
                "mesh-generation mode received a diagnostics output path",
            )

            must(
                source_geometry_sha256 is not None,
                "mesh-generation mode received source-geometry provenance",
            )

            must(
                not mesh_out.exists(),
                "mesh output does not already exist",
            )

            must(
                not diagnostics_out.exists(),
                "mesh diagnostics output does not already exist",
            )

            # ------------------------------------------------
            # Gmsh periodic curve constraints.
            # slave = translated copy of master.
            # ------------------------------------------------

            transform_x = [
                1.0, 0.0, 0.0, width,
                0.0, 1.0, 0.0, 0.0,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0,
            ]

            transform_y = [
                1.0, 0.0, 0.0, 0.0,
                0.0, 1.0, 0.0, height,
                0.0, 0.0, 1.0, 0.0,
                0.0, 0.0, 0.0, 1.0,
            ]

            gmsh.model.mesh.setPeriodic(
                1,
                [
                    slave
                    for slave, _
                    in x_pairs
                ],
                [
                    master
                    for _, master
                    in x_pairs
                ],
                transform_x,
            )

            gmsh.model.mesh.setPeriodic(
                1,
                [
                    slave
                    for slave, _
                    in y_pairs
                ],
                [
                    master
                    for _, master
                    in y_pairs
                ],
                transform_y,
            )

            periodic_mesh_constraints_applied = True

            print(
                "PASS — Gmsh X/Y periodic curve-mesh constraints applied"
            )

            # ------------------------------------------------
            # Locked first-order triangular mesh.
            # ------------------------------------------------

            gmsh.option.setNumber(
                "Mesh.CharacteristicLengthMin",
                mesh_size,
            )

            gmsh.option.setNumber(
                "Mesh.CharacteristicLengthMax",
                mesh_size,
            )

            gmsh.option.setNumber(
                "Mesh.ElementOrder",
                1,
            )

            gmsh.option.setNumber(
                "Mesh.RecombineAll",
                0,
            )

            print(
                f"Generating periodized true-hole Gmsh mesh at h={mesh_size} ..."
            )

            gmsh.model.mesh.generate(
                2
            )

            mesh_generated = True

            # ------------------------------------------------
            # Global node-coordinate map and side-node audit.
            # ------------------------------------------------

            (
                node_tags,
                node_coords_flat,
                _parametric,
            ) = gmsh.model.mesh.getNodes()

            node_coords = np.asarray(
                node_coords_flat,
                dtype=float,
            ).reshape(
                (-1, 3)
            )

            must(
                len(node_tags)
                == len(node_coords),
                "global mesh node-tag/coordinate counts match",
            )

            must(
                len(node_tags) > 0,
                "generated mesh contains nodes",
            )

            node_tag_to_coord = {
                int(tag): node_coords[index]
                for index, tag
                in enumerate(
                    node_tags
                )
            }

            left_nodes = node_coords[
                np.abs(
                    node_coords[:, 0]
                )
                <= NODE_TOL
            ]

            right_nodes = node_coords[
                np.abs(
                    node_coords[:, 0]
                    - width
                )
                <= NODE_TOL
            ]

            bottom_nodes = node_coords[
                np.abs(
                    node_coords[:, 1]
                )
                <= NODE_TOL
            ]

            top_nodes = node_coords[
                np.abs(
                    node_coords[:, 1]
                    - height
                )
                <= NODE_TOL
            ]

            print(
                "Boundary mesh-node counts:",
                {
                    "left":
                        len(left_nodes),
                    "right":
                        len(right_nodes),
                    "bottom":
                        len(bottom_nodes),
                    "top":
                        len(top_nodes),
                },
            )

            must(
                len(left_nodes)
                == len(right_nodes)
                and len(left_nodes) > 0,
                "left/right mesh-node counts match",
            )

            must(
                len(bottom_nodes)
                == len(top_nodes)
                and len(bottom_nodes) > 0,
                "bottom/top mesh-node counts match",
            )

            lr_coordinate_error = float(
                np.max(
                    np.abs(
                        np.sort(
                            left_nodes[:, 1]
                        )
                        - np.sort(
                            right_nodes[:, 1]
                        )
                    )
                )
            )

            bt_coordinate_error = float(
                np.max(
                    np.abs(
                        np.sort(
                            bottom_nodes[:, 0]
                        )
                        - np.sort(
                            top_nodes[:, 0]
                        )
                    )
                )
            )

            print(
                "Left/right boundary-node coordinate mismatch:",
                lr_coordinate_error,
            )

            print(
                "Bottom/top boundary-node coordinate mismatch:",
                bt_coordinate_error,
            )

            must(
                lr_coordinate_error
                <= NODE_TOL,
                (
                    "left/right boundary meshes are "
                    "translationally identical"
                ),
            )

            must(
                bt_coordinate_error
                <= NODE_TOL,
                (
                    "bottom/top boundary meshes are "
                    "translationally identical"
                ),
            )

            # ------------------------------------------------
            # Gmsh's actual slave/master node correspondence.
            # ------------------------------------------------

            periodic_node_pair_count = 0
            periodic_transform_error = 0.0
            periodic_master_ok = True

            for (
                pairs,
                translation,
                axis_name,
            ) in (
                (
                    x_pairs,
                    np.array(
                        [
                            width,
                            0.0,
                            0.0,
                        ],
                        dtype=float,
                    ),
                    "X",
                ),
                (
                    y_pairs,
                    np.array(
                        [
                            0.0,
                            height,
                            0.0,
                        ],
                        dtype=float,
                    ),
                    "Y",
                ),
            ):
                for (
                    slave,
                    expected_master,
                ) in pairs:
                    (
                        actual_master,
                        slave_nodes_for_curve,
                        master_nodes_for_curve,
                        _affine,
                    ) = (
                        gmsh.model.mesh.getPeriodicNodes(
                            1,
                            slave,
                            False,
                        )
                    )

                    if (
                        int(actual_master)
                        != int(expected_master)
                    ):
                        periodic_master_ok = False

                    must(
                        len(
                            slave_nodes_for_curve
                        )
                        == len(
                            master_nodes_for_curve
                        ),
                        (
                            f"{axis_name} periodic node-array "
                            f"lengths match for slave curve {slave}"
                        ),
                    )

                    must(
                        len(
                            slave_nodes_for_curve
                        ) > 0,
                        (
                            f"{axis_name} slave curve {slave} "
                            "has periodic node correspondence records"
                        ),
                    )

                    periodic_node_pair_count += (
                        len(
                            slave_nodes_for_curve
                        )
                    )

                    for (
                        slave_node,
                        master_node,
                    ) in zip(
                        slave_nodes_for_curve,
                        master_nodes_for_curve,
                        strict=True,
                    ):
                        slave_xyz = (
                            node_tag_to_coord[
                                int(
                                    slave_node
                                )
                            ]
                        )

                        master_xyz = (
                            node_tag_to_coord[
                                int(
                                    master_node
                                )
                            ]
                        )

                        error = float(
                            np.max(
                                np.abs(
                                    slave_xyz
                                    - (
                                        master_xyz
                                        + translation
                                    )
                                )
                            )
                        )

                        periodic_transform_error = max(
                            periodic_transform_error,
                            error,
                        )

            print(
                "Gmsh periodic node-pair records:",
                periodic_node_pair_count,
            )

            print(
                "Maximum Gmsh periodic transform error:",
                periodic_transform_error,
            )

            must(
                periodic_master_ok,
                (
                    "Gmsh periodic entities report "
                    "the intended master curves"
                ),
            )

            must(
                periodic_node_pair_count > 0,
                (
                    "Gmsh returned periodic node "
                    "correspondence records"
                ),
            )

            must(
                periodic_transform_error
                <= NODE_TOL,
                (
                    "Gmsh periodic node correspondence "
                    "satisfies the translation maps"
                ),
            )

            # ------------------------------------------------
            # Complete matrix/particle element coverage.
            # ------------------------------------------------

            def elements_for_surfaces(
                surface_tags: set[int],
            ) -> set[int]:
                result: set[int] = set()

                for surface_tag in surface_tags:
                    (
                        _types,
                        element_tag_blocks,
                        _nodes,
                    ) = gmsh.model.mesh.getElements(
                        2,
                        surface_tag,
                    )

                    for block in element_tag_blocks:
                        result.update(
                            int(tag)
                            for tag in block
                        )

                return result

            matrix_elements = (
                elements_for_surfaces(
                    matrix_surface_tags
                )
            )

            particle_elements = (
                elements_for_surfaces(
                    particle_surface_tags
                )
            )

            (
                _all_types,
                all_element_tag_blocks,
                _all_nodes,
            ) = gmsh.model.mesh.getElements(
                2
            )

            all_elements: set[int] = set()

            for block in all_element_tag_blocks:
                all_elements.update(
                    int(tag)
                    for tag in block
                )

            must(
                matrix_elements.isdisjoint(
                    particle_elements
                ),
                (
                    "matrix and particle element "
                    "sets are disjoint"
                ),
            )

            must(
                (
                    matrix_elements
                    | particle_elements
                )
                == all_elements,
                (
                    "every 2D element belongs to "
                    "matrix or particle"
                ),
            )

            must(
                len(all_elements) > 0,
                "generated mesh contains 2D elements",
            )

            # ------------------------------------------------
            # First-order triangle / triangulated-area audit.
            # ------------------------------------------------

            def triangulated_area(
                surface_tags: set[int],
            ) -> tuple[float, float]:
                area = 0.0
                minimum_area = math.inf

                for surface_tag in surface_tags:
                    (
                        element_types,
                        _element_tags,
                        node_blocks,
                    ) = gmsh.model.mesh.getElements(
                        2,
                        surface_tag,
                    )

                    for (
                        element_type,
                        node_block,
                    ) in zip(
                        element_types,
                        node_blocks,
                        strict=True,
                    ):
                        (
                            _name,
                            dim,
                            order,
                            num_nodes,
                            _local_coords,
                            _num_primary_nodes,
                        ) = (
                            gmsh.model.mesh.getElementProperties(
                                int(
                                    element_type
                                )
                            )
                        )

                        must(
                            int(dim) == 2,
                            (
                                "material mesh element "
                                "has dimension 2"
                            ),
                        )

                        must(
                            int(order) == 1
                            and int(num_nodes) == 3,
                            (
                                "periodized true-hole mesh "
                                "uses first-order triangles"
                            ),
                        )

                        connectivity = (
                            np.asarray(
                                node_block,
                                dtype=np.int64,
                            ).reshape(
                                (-1, 3)
                            )
                        )

                        for (
                            n0,
                            n1,
                            n2,
                        ) in connectivity:
                            p0 = (
                                node_tag_to_coord[
                                    int(n0)
                                ][:2]
                            )

                            p1 = (
                                node_tag_to_coord[
                                    int(n1)
                                ][:2]
                            )

                            p2 = (
                                node_tag_to_coord[
                                    int(n2)
                                ][:2]
                            )

                            edge1 = (
                                p1 - p0
                            )

                            edge2 = (
                                p2 - p0
                            )

                            # NumPy 2.5-compatible exact 2-D
                            # determinant: do not use np.cross
                            # on 2-component vectors.
                            cross2d = (
                                edge1[0]
                                * edge2[1]
                                - edge1[1]
                                * edge2[0]
                            )

                            tri_area = (
                                0.5
                                * abs(
                                    cross2d
                                )
                            )

                            area += float(
                                tri_area
                            )

                            minimum_area = min(
                                minimum_area,
                                float(
                                    tri_area
                                ),
                            )

                return (
                    area,
                    minimum_area,
                )

            (
                meshed_matrix_area,
                matrix_min_area,
            ) = triangulated_area(
                matrix_surface_tags
            )

            (
                meshed_particle_area,
                particle_min_area,
            ) = triangulated_area(
                particle_surface_tags
            )

            meshed_material_area = (
                meshed_matrix_area
                + meshed_particle_area
            )

            meshed_void_area = (
                gross_area
                - meshed_material_area
            )

            minimum_triangle_area = min(
                matrix_min_area,
                particle_min_area,
            )

            meshed_particle_fraction = (
                meshed_particle_area
                / gross_area
            )

            analytical_particle_fraction = (
                expected_particle_area
                / gross_area
            )

            particle_fraction_error = abs(
                meshed_particle_fraction
                - analytical_particle_fraction
            )

            meshed_void_fraction = (
                meshed_void_area
                / gross_area
            )

            analytical_void_fraction = (
                expected_void_area
                / gross_area
            )

            void_fraction_error = abs(
                meshed_void_fraction
                - analytical_void_fraction
            )

            material_area_error = abs(
                meshed_material_area
                - expected_material_area
            )

            print(
                "2D element count:",
                len(
                    all_elements
                ),
            )

            print(
                "Matrix element count:",
                len(
                    matrix_elements
                ),
            )

            print(
                "Particle element count:",
                len(
                    particle_elements
                ),
            )

            print(
                "Meshed matrix area:",
                meshed_matrix_area,
            )

            print(
                "Meshed particle area:",
                meshed_particle_area,
            )

            print(
                "Meshed material area:",
                meshed_material_area,
            )

            print(
                "Meshed void area:",
                meshed_void_area,
            )

            print(
                "Particle-fraction absolute error:",
                particle_fraction_error,
            )

            print(
                "Void-fraction absolute error:",
                void_fraction_error,
            )

            print(
                "Material-area absolute error:",
                material_area_error,
            )

            print(
                "Minimum triangle area:",
                minimum_triangle_area,
            )

            must(
                minimum_triangle_area > 0.0,
                (
                    "all generated triangles have "
                    "positive area magnitude"
                ),
            )

            must(
                meshed_void_area > 0.0,
                (
                    "triangulated mesh retains a "
                    "positive true-hole area"
                ),
            )

            must(
                particle_fraction_error
                <= MESH_AREA_FRACTION_TOL,
                (
                    "meshed particle fraction is within "
                    "0.005 absolute of analytical gross-RVE fraction"
                ),
            )

            must(
                void_fraction_error
                <= MESH_AREA_FRACTION_TOL,
                (
                    "meshed void fraction is within "
                    "0.005 absolute of analytical gross-RVE fraction"
                ),
            )

            must(
                material_area_error
                <= (
                    MESH_AREA_FRACTION_TOL
                    * gross_area
                ),
                (
                    "meshed material area is within "
                    "0.005 gross-RVE area of CAD authority"
                ),
            )

            # ------------------------------------------------
            # True-hole boundary must itself carry 1-D mesh.
            # ------------------------------------------------

            void_boundary_elements: set[int] = set()

            for curve_tag in void_boundary_curves:
                (
                    _curve_types,
                    curve_element_blocks,
                    _curve_node_blocks,
                ) = gmsh.model.mesh.getElements(
                    1,
                    curve_tag,
                )

                for block in curve_element_blocks:
                    void_boundary_elements.update(
                        int(tag)
                        for tag in block
                    )

            must(
                len(
                    void_boundary_elements
                ) > 0,
                (
                    "true-hole void_boundary physical "
                    "curves contain mesh elements"
                ),
            )

            mesh_metrics = {
                "cell_count":
                    len(all_elements),
                "matrix_cell_count":
                    len(matrix_elements),
                "particle_cell_count":
                    len(particle_elements),
                "void_boundary_element_count":
                    len(
                        void_boundary_elements
                    ),
                "minimum_triangle_area":
                    minimum_triangle_area,
                "global_node_count":
                    len(node_tags),
                "left_node_count":
                    len(left_nodes),
                "right_node_count":
                    len(right_nodes),
                "bottom_node_count":
                    len(bottom_nodes),
                "top_node_count":
                    len(top_nodes),
                "left_right_coordinate_mismatch":
                    lr_coordinate_error,
                "bottom_top_coordinate_mismatch":
                    bt_coordinate_error,
                "periodic_node_pair_record_count":
                    periodic_node_pair_count,
                "periodic_transform_max_error":
                    periodic_transform_error,
                "periodic_master_entities_ok":
                    periodic_master_ok,
                "meshed_matrix_area":
                    meshed_matrix_area,
                "meshed_particle_area":
                    meshed_particle_area,
                "meshed_material_area":
                    meshed_material_area,
                "meshed_void_area":
                    meshed_void_area,
                "analytical_particle_fraction":
                    analytical_particle_fraction,
                "meshed_particle_fraction":
                    meshed_particle_fraction,
                "particle_fraction_absolute_error":
                    particle_fraction_error,
                "analytical_void_fraction":
                    analytical_void_fraction,
                "meshed_void_fraction":
                    meshed_void_fraction,
                "void_fraction_absolute_error":
                    void_fraction_error,
                "material_area_absolute_error":
                    material_area_error,
                "element_policy":
                    "first_order_triangles",
            }

        result = {
            "state": "defective",
            "geometry_identity_sha256": str(
                state["geometry_identity"]["sha256"]
            ),
            "gross_area": gross_area,
            "expected_particle_area":
                expected_particle_area,
            "cad_particle_area":
                cad_particle_area,
            "expected_matrix_area":
                expected_matrix_area,
            "cad_matrix_area":
                cad_matrix_area,
            "expected_void_area":
                expected_void_area,
            "cad_void_area":
                cad_void_area,
            "expected_void_boundary_length":
                expected_void_boundary_length,
            "cad_void_boundary_length":
                cad_void_boundary_length,
            "particle_surface_count":
                len(particle_surface_tags),
            "matrix_surface_count":
                len(matrix_surface_tags),
            "void_boundary_curve_count":
                len(void_boundary_curves),
            "left_curve_count":
                len(left_curves),
            "right_curve_count":
                len(right_curves),
            "bottom_curve_count":
                len(bottom_curves),
            "top_curve_count":
                len(top_curves),
            "x_periodic_curve_pair_count":
                len(x_pairs),
            "y_periodic_curve_pair_count":
                len(y_pairs),
            "x_periodic_particle_ids":
                sorted(x_particle_ids),
            "y_periodic_particle_ids":
                sorted(y_particle_ids),
            "expected_x_periodic_particle_ids":
                expected_x_particle_ids,
            "expected_y_periodic_particle_ids":
                expected_y_particle_ids,
            "left_boundary_material_length":
                left_boundary_length,
            "right_boundary_material_length":
                right_boundary_length,
            "bottom_boundary_material_length":
                bottom_boundary_length,
            "top_boundary_material_length":
                top_boundary_length,
            "periodic_geometric_pairing_ready":
                True,
            "periodic_mesh_constraints_applied":
                periodic_mesh_constraints_applied,
            "positive_particle_representation_count":
                len(positive_particle_reps),
            "disjoint_particle_representation_count":
                len(disjoint_particle_reps),
            "positive_void_representation_count":
                len(positive_void_reps),
            "disjoint_void_representation_count":
                len(disjoint_void_reps),
            "maximum_particle_id_area_error":
                maximum_particle_id_area_error,
            "mesh_generated":
                mesh_generated,
        }

        if generate_mesh:
            result[
                "schema"
            ] = MESH_SCHEMA

            result[
                "status"
            ] = "valid"

            result[
                "source_geometry_sha256"
            ] = source_geometry_sha256

            result[
                "mesh_size"
            ] = float(
                mesh_size
            )

            result[
                "physical_tags"
            ] = {
                "matrix":
                    MATRIX_PHYSICAL_TAG,
                "particle":
                    PARTICLE_PHYSICAL_TAG,
                "void_boundary":
                    VOID_BOUNDARY_PHYSICAL_TAG,
                "left":
                    LEFT_PHYSICAL_TAG,
                "right":
                    RIGHT_PHYSICAL_TAG,
                "bottom":
                    BOTTOM_PHYSICAL_TAG,
                "top":
                    TOP_PHYSICAL_TAG,
            }

            result[
                "mesh"
            ] = mesh_metrics

            result[
                "scope_guard"
            ] = {
                "m9_step9_transfer_validation":
                    True,
                "m9_stochastic_pilot_production":
                    False,
                "production_design_id_created":
                    False,
                "production_realization_id_created":
                    False,
                "production_pilot_sampling_rng_consumed":
                    False,
                "source_geometry_regenerated":
                    False,
                "mesh_generated":
                    True,
                "mpc_constructed":
                    False,
                "fem_solve_performed":
                    False,
                "tensor_reconstructed":
                    False,
                "machine_learning_performed":
                    False,
                "protected_pristine_m8_schema_mutated":
                    False,
            }

            mesh_out.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            diagnostics_out.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            gmsh.write(
                str(
                    mesh_out
                )
            )

            must(
                mesh_out.is_file(),
                "Gmsh mesh artifact was written",
            )

            result[
                "artifacts"
            ] = {
                "mesh":
                    str(mesh_out),
                "diagnostics":
                    str(
                        diagnostics_out
                    ),
            }

            diagnostics_out.write_text(
                json.dumps(
                    result,
                    indent=2,
                    sort_keys=True,
                    allow_nan=False,
                )
                + "\n",
                encoding="utf-8",
            )

            must(
                diagnostics_out.is_file(),
                "mesh diagnostics JSON was written",
            )

        return result

    finally:
        gmsh.finalize()


def main() -> int:
    args = parse_args()

    must(
        math.isfinite(args.mesh_size)
        and args.mesh_size > 0.0,
        "future mesh size is finite and positive",
    )

    must(
        not args.mesh_out.exists(),
        "future mesh output does not already exist",
    )

    must(
        not args.diagnostics_out.exists(),
        "future diagnostics output does not already exist",
    )

    repo = Path(__file__).resolve().parents[1]

    for relative, expected in AUTHORITIES.items():
        path = repo / relative
        must(
            path.is_file(),
            f"authority exists: {relative}",
        )
        actual = sha256_file(path)
        print(f"{relative} SHA256 = {actual}")
        must(
            actual == expected,
            f"authority SHA authenticated: {relative}",
        )

    path = args.geometry_json
    must(
        path.is_file(),
        "Step-9 defective geometry JSON exists",
    )

    expected_geometry_sha = (
        args.expected_geometry_sha256.strip().lower()
    )
    must(
        len(expected_geometry_sha) == 64
        and all(
            character in "0123456789abcdef"
            for character in expected_geometry_sha
        ),
        "expected Step-9 geometry SHA256 is canonical",
    )

    geometry_sha = sha256_file(path)
    print(f"Step-9 geometry SHA256 = {geometry_sha}")
    must(
        geometry_sha == expected_geometry_sha,
        "Step-9 geometry SHA256 authenticated",
    )

    geometry = json.loads(
        path.read_text(encoding="utf-8")
    )

    must(
        geometry.get("schema") == GEOMETRY_SCHEMA,
        "Step-9 defective geometry schema authenticated",
    )
    must(
        geometry.get("status") == "valid"
        and geometry.get("failure_reason") is None,
        "Step-9 defective geometry status is valid",
    )
    must(
        all(
            value is True
            for value in geometry["checks"].values()
        ),
        "top-level Step-9 geometry checks all PASS",
    )

    scope = geometry["scope_guard"]
    must(
        scope["m9_step9_transfer_validation"] is True,
        "input belongs to Step-9 transfer validation",
    )
    must(
        scope["m9_stochastic_pilot_production"] is False,
        "input is not stochastic-pilot production evidence",
    )
    must(
        scope["production_design_id_created"] is False,
        "input created no production design ID",
    )
    must(
        scope["production_realization_id_created"] is False,
        "input created no production realization ID",
    )
    must(
        scope["production_pilot_sampling_rng_consumed"] is False,
        "input consumed no production pilot sampling RNG",
    )
    must(
        scope["source_particle_geometry_regenerated"] is False,
        "particle geometry was reused without regeneration",
    )
    must(
        scope["protected_pristine_m8_schema_mutated"] is False,
        "protected pristine M8 schema remains unmutated",
    )
    for key, label in (
        ("mesh_generated", "input geometry predates meshing"),
        ("mpc_constructed", "input geometry predates MPC"),
        ("fem_solve_performed", "input geometry predates FEM"),
        ("tensor_reconstructed", "input geometry predates tensor reconstruction"),
        ("machine_learning_performed", "input geometry predates ML"),
    ):
        must(scope[key] is False, label)

    rng = geometry["rng"]
    must(
        rng["bit_generator"] == "PCG64",
        "Step-9 geometry records PCG64",
    )
    must(
        rng["rng_namespace"]
        == STEP9_VALIDATION_SEED_NAMESPACE,
        "Step-9 validation-seed namespace authenticated",
    )
    must(
        rng["void_seed_status"] == "applicable",
        "defective geometry has an applicable void seed",
    )

    rve = geometry["rve"]
    width = float(rve["width"])
    height = float(rve["height"])
    must(
        math.isclose(
            width, STEP9_RVE_LENGTH,
            rel_tol=0.0, abs_tol=1.0e-12,
        )
        and math.isclose(
            height, STEP9_RVE_LENGTH,
            rel_tol=0.0, abs_tol=1.0e-12,
        ),
        "Step-9 RVE side length is locked to 1.0",
    )
    must(
        math.isclose(
            float(rve["area"]),
            width * height,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "Step-9 RVE area is consistent",
    )

    particles = geometry["particles"]
    must(
        len(particles) == STEP9_PHYSICAL_PARTICLE_COUNT,
        "Step-9 geometry contains 16 physical particles",
    )
    validate_representation_contract(
        particles,
        geometry["particle_periodic_representations"],
        "particle_id",
        "particle",
    )

    state = geometry["state"]
    must(
        state["state"] == "defective",
        "single Step-9 defect state is self-consistent",
    )
    must(
        all(
            value is True
            for value in state["checks"].values()
        ),
        "single Step-9 defect-state checks all PASS",
    )

    voids = state["voids"]
    void_count = len(voids)
    must(
        void_count in STEP9_ALLOWED_VOID_COUNTS,
        "physical void count belongs to locked Step-9 set {1,2,4}",
    )
    must(
        int(state["void_count"]) == void_count,
        "state void count matches physical void records",
    )

    requested = geometry["requested_void_geometry"]
    must(
        requested["state"] == "defective",
        "requested geometry is the single defective state",
    )
    must(
        int(requested["void_count"]) == void_count,
        "requested void count matches state",
    )
    must(
        math.isclose(
            float(requested["void_radius"]),
            float(state["void_radius"]),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "requested void radius matches state radius",
    )
    must(
        math.isclose(
            float(requested["minimum_toroidal_void_particle_surface_gap"]),
            STEP9_MIN_VOID_PARTICLE_SPACING,
            rel_tol=0.0,
            abs_tol=0.0,
        ),
        "locked Step-9 void-particle clearance authenticated",
    )
    must(
        math.isclose(
            float(requested["minimum_toroidal_void_void_surface_gap"]),
            STEP9_MIN_VOID_VOID_SPACING,
            rel_tol=0.0,
            abs_tol=0.0,
        ),
        "locked Step-9 void-void clearance authenticated",
    )
    must(
        int(requested["max_attempts_per_void"])
        == STEP9_MAX_ATTEMPTS_PER_VOID,
        "locked Step-9 void placement budget authenticated",
    )
    must(
        requested["external_boundary_clearance_imposed"] is False,
        "external-boundary clearance remains disabled",
    )

    generated = geometry["generated_geometry"]
    must(
        int(generated["particle_count"])
        == STEP9_PHYSICAL_PARTICLE_COUNT,
        "generated particle count remains 16",
    )
    must(
        int(generated["void_count"]) == void_count,
        "generated void count matches state",
    )

    state_radius = float(state["void_radius"])
    must(
        all(
            math.isclose(
                float(void["radius"]),
                state_radius,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
            for void in voids
        ),
        "all physical void records use the single locked state radius",
    )

    validate_representation_contract(
        voids,
        state["periodic_void_representations"],
        "void_id",
        "void",
    )

    physical_void_area = sum(
        math.pi * float(void["radius"]) ** 2
        for void in voids
    )
    must(
        math.isclose(
            physical_void_area,
            float(state["void_area"]),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "physical void area is counted once",
    )
    must(
        math.isclose(
            float(generated["void_area"]),
            float(state["void_area"]),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "generated and state void areas agree",
    )
    must(
        state["analytical_area_counting"]
        == "physical_voids_once_no_periodic_image_double_counting",
        "periodic-image analytical area double counting is forbidden",
    )

    print()
    print(f"Step-9 geometry SHA256 = {geometry_sha}")
    print(
        "particle identity = "
        + str(
            geometry["source_particle_geometry"]
            ["geometry_identity_sha256"]
        )
    )
    print(
        "defective geometry identity = "
        + str(state["geometry_identity"]["sha256"])
    )
    print(f"reserved mesh schema = {MESH_SCHEMA}")
    print(
        "PASS — Step-9 mesh input contract authenticated; "
        "no CAD, mesh, MPC, FEM, tensor or ML evidence was "
        "generated by the input-contract checks"
    )
    print("M9_STEP9_VOID_MESH_INPUT_CONTRACT_OK")

    must(
        not (
            args.cad_validate_only
            and args.generate_mesh
        ),
        "--cad-validate-only and --generate-mesh cannot be requested together",
    )

    if args.cad_validate_only:
        cad_diagnostics = build_periodized_true_hole_cad(
            geometry,
        )
        print(
            "CAD diagnostics = "
            + json.dumps(
                cad_diagnostics,
                sort_keys=True,
            )
        )
        print("PASS — CAD validation generated no mesh")
        print("M9_STEP9_VOID_TRUE_HOLE_CAD_OK")

    if args.generate_mesh:
        mesh_diagnostics = build_periodized_true_hole_cad(
            geometry,
            generate_mesh=True,
            mesh_size=float(args.mesh_size),
            mesh_out=args.mesh_out,
            diagnostics_out=args.diagnostics_out,
            source_geometry_sha256=geometry_sha,
        )
        print()
        print(
            "MESH diagnostics = "
            + json.dumps(
                mesh_diagnostics,
                sort_keys=True,
            )
        )
        print(
            "PASS — Step-9 periodized true-hole periodic mesh "
            "generation and internal validation"
        )
        print("M9_STEP9_VOID_TRUE_HOLE_PERIODIC_MESH_OK")

    return 0



if __name__ == "__main__":
    raise SystemExit(
        main()
    )
