from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import gmsh
import numpy as np


GEOMETRY_SCHEMA = (
    "m8_periodized_particle_microstructure_v1"
)

MESH_SCHEMA = (
    "m8_periodized_particle_mesh_diagnostics_v1"
)

# Permanent M8 validation construction.
# The radius is fixed by the protected M8 design;
# it is NOT an M9 production parameter-space lock.
M8_VALIDATION_PARTICLE_RADIUS = 0.05

RVE_SIDE_BY_LEVEL = {
    "R1": 1.0,
    "R2": 1.5,
    "R3": 2.0,
    "R4": 2.5,
    "R5": 3.0,
}

RVE_PARTICLE_COUNT_BY_LEVEL = {
    "R1": 16,
    "R2": 36,
    "R3": 64,
    "R4": 100,
    "R5": 144,
}

CAD_TOL = 1.0e-10
BBOX_TOL = 2.0e-6
PAIR_TOL = 1.0e-8
NODE_TOL = 1.0e-10

# This reproduces the validated STEP 622A mesh-fraction
# acceptance gate. It is a meshing-validity tolerance,
# not the final M8 target-mesh decision.
MESH_FRACTION_TOL = 0.005

MATRIX_TAG = 1
PARTICLE_TAG = 2
LEFT_TAG = 11
RIGHT_TAG = 12
BOTTOM_TAG = 13
TOP_TAG = 14

# Runtime state loaded only inside main().
# The preserved validated meshing helpers use these names.
L = math.nan
R = math.nan
H = math.nan
SEED = -1
GEOMETRY_SHA = ""
RVE_AREA = math.nan

EXPECTED_PARTICLE_COUNT = 0
EXPECTED_REPRESENTATION_COUNT = 0
EXPECTED_TRANSLATED_IMAGE_COUNT = 0
EXPECTED_CROSSING_IDS = []

EXPECTED_X_PERIODIC_PARTICLE_IDS = []
EXPECTED_Y_PERIODIC_PARTICLE_IDS = []

EXPECTED_PARTICLE_AREA = math.nan
EXPECTED_PARTICLE_FRACTION = math.nan

OUT_MSH = None
OUT_JSON = None

PARTICLES = []


def parse_args() -> argparse.Namespace:
    """Parse permanent M8 periodized-mesher inputs."""

    parser = argparse.ArgumentParser(
        description=(
            "Generate and validate a periodic Gmsh mesh "
            "from an M8 periodized-particle geometry JSON."
        )
    )

    parser.add_argument(
        "--geometry-json",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--rve-level",
        choices=tuple(
            RVE_SIDE_BY_LEVEL
        ),
        required=True,
    )

    parser.add_argument(
        "--mesh-size",
        type=float,
        required=True,
    )

    parser.add_argument(
        "--mesh-out",
        type=Path,
        required=True,
    )

    parser.add_argument(
        "--diagnostics-out",
        type=Path,
        required=True,
    )

    return parser.parse_args()


def load_geometry_record(
    path: Path,
) -> dict:
    """Load one permanent src/20 geometry record."""

    if not path.is_file():
        raise FileNotFoundError(
            f"geometry JSON does not exist: {path}"
        )

    record = json.loads(
        path.read_text(
            encoding="utf-8"
        )
    )

    if not isinstance(
        record,
        dict,
    ):
        raise ValueError(
            "geometry JSON root must be an object."
        )

    return record

def must(condition: bool, message: str) -> None:
    if condition:
        print(f"PASS — {message}")
        return

    print(f"FAIL — DO NOT CONTINUE: {message}")
    raise RuntimeError(message)


def bbox_inside_cell(
    bbox: tuple[float, ...],
) -> bool:
    return (
        bbox[0] >= -BBOX_TOL
        and bbox[1] >= -BBOX_TOL
        and bbox[3] <= L + BBOX_TOL
        and bbox[4] <= L + BBOX_TOL
    )



def disk_cell_intersection_classification(
    center_x: float,
    center_y: float,
    radius: float,
    cell_side: float,
    tolerance: float = CAD_TOL,
) -> tuple[str, float]:
    """Classify a periodic disk relative to the closed square cell."""

    values = (
        center_x,
        center_y,
        radius,
        cell_side,
        tolerance,
    )

    if not all(
        math.isfinite(value)
        for value in values
    ):
        raise ValueError(
            "disk/cell intersection inputs must be finite."
        )

    if radius <= 0.0:
        raise ValueError(
            "disk radius must be positive."
        )

    if cell_side <= 0.0:
        raise ValueError(
            "cell side must be positive."
        )

    if tolerance < 0.0:
        raise ValueError(
            "intersection tolerance must be non-negative."
        )

    nearest_x = min(
        max(
            center_x,
            0.0,
        ),
        cell_side,
    )

    nearest_y = min(
        max(
            center_y,
            0.0,
        ),
        cell_side,
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


def curve_center_length(tag: int):
    center = gmsh.model.occ.getCenterOfMass(
        1,
        tag,
    )
    length = gmsh.model.occ.getMass(
        1,
        tag,
    )
    return np.asarray(center), float(length)


def side_curves(axis: int, value: float) -> list[int]:
    found = []

    for dim, tag in gmsh.model.getEntities(1):
        if dim != 1:
            continue

        bb = gmsh.model.getBoundingBox(
            1,
            tag,
        )

        lo = bb[axis]
        hi = bb[axis + 3]

        if (
            abs(lo - value) <= BBOX_TOL
            and abs(hi - value) <= BBOX_TOL
        ):
            found.append(int(tag))

    return sorted(found)


def pair_curves(
    master_tags: list[int],
    slave_tags: list[int],
    dx: float,
    dy: float,
) -> list[tuple[int, int]]:
    unmatched = set(slave_tags)
    pairs: list[tuple[int, int]] = []

    for master in master_tags:
        master_center, master_length = (
            curve_center_length(master)
        )

        target_center = (
            master_center
            + np.array(
                [dx, dy, 0.0],
                dtype=float,
            )
        )

        matches = []

        for slave in sorted(unmatched):
            slave_center, slave_length = (
                curve_center_length(slave)
            )

            center_error = float(
                np.max(
                    np.abs(
                        slave_center
                        - target_center
                    )
                )
            )

            length_error = abs(
                slave_length
                - master_length
            )

            if (
                center_error <= PAIR_TOL
                and length_error <= PAIR_TOL
            ):
                matches.append(slave)

        must(
            len(matches) == 1,
            (
                f"unique periodic geometric match for "
                f"master curve {master}"
            ),
        )

        slave = matches[0]
        unmatched.remove(slave)

        # Stored as (slave, master), matching Gmsh API.
        pairs.append((slave, master))

    must(
        not unmatched,
        "all slave boundary curves were paired",
    )

    return pairs


def main() -> None:
    global L
    global R
    global H
    global SEED
    global GEOMETRY_SHA
    global RVE_AREA

    global EXPECTED_PARTICLE_COUNT
    global EXPECTED_REPRESENTATION_COUNT
    global EXPECTED_TRANSLATED_IMAGE_COUNT
    global EXPECTED_CROSSING_IDS

    global EXPECTED_X_PERIODIC_PARTICLE_IDS
    global EXPECTED_Y_PERIODIC_PARTICLE_IDS

    global EXPECTED_PARTICLE_AREA
    global EXPECTED_PARTICLE_FRACTION

    global OUT_MSH
    global OUT_JSON
    global PARTICLES

    args = parse_args()

    must(
        np.isfinite(
            args.mesh_size
        )
        and args.mesh_size > 0.0,
        "mesh size is finite and positive",
    )

    geometry = load_geometry_record(
        args.geometry_json
    )

    must(
        geometry.get("schema")
        == GEOMETRY_SCHEMA,
        "input uses permanent M8 periodized geometry schema",
    )

    must(
        geometry.get("status")
        == "valid",
        "input periodized geometry status is valid",
    )

    scope_guard = geometry.get(
        "scope_guard",
        {},
    )

    must(
        scope_guard.get(
            "mesh_generated"
        )
        is False,
        "src/20 geometry record predates meshing",
    )

    must(
        scope_guard.get(
            "voids_generated"
        )
        is False,
        "pristine particle-only M8 geometry supplied",
    )

    must(
        scope_guard.get(
            "fem_solve_performed"
        )
        is False,
        "geometry record contains no FEM solve",
    )

    rve = geometry["rve"]

    width = float(
        rve["width"]
    )

    height = float(
        rve["height"]
    )

    expected_side = float(
        RVE_SIDE_BY_LEVEL[
            args.rve_level
        ]
    )

    must(
        math.isclose(
            width,
            expected_side,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "geometry width matches selected M8 RVE level",
    )

    must(
        math.isclose(
            height,
            expected_side,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "geometry height matches selected M8 RVE level",
    )

    must(
        math.isclose(
            width,
            height,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "permanent M8 mesher receives a square RVE",
    )

    requested = geometry[
        "requested_geometry"
    ]

    physical_records = geometry[
        "particles"
    ]

    representations = [
        dict(record)
        for record in geometry[
            "periodic_representations"
        ]
    ]

    generated = geometry[
        "generated_geometry"
    ]

    EXPECTED_PARTICLE_COUNT = int(
        requested[
            "particle_count"
        ]
    )

    expected_design_count = int(
        RVE_PARTICLE_COUNT_BY_LEVEL[
            args.rve_level
        ]
    )

    must(
        EXPECTED_PARTICLE_COUNT
        == expected_design_count,
        "particle count matches controlled M8 RVE-size design",
    )

    requested_radius = float(
        requested[
            "particle_radius"
        ]
    )

    must(
        math.isclose(
            requested_radius,
            M8_VALIDATION_PARTICLE_RADIUS,
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "particle radius matches controlled M8 validation design",
    )

    must(
        len(physical_records)
        == EXPECTED_PARTICLE_COUNT,
        "physical-particle record count matches request",
    )

    L = width
    R = requested_radius
    H = float(
        args.mesh_size
    )

    SEED = int(
        geometry[
            "rng"
        ][
            "seed"
        ]
    )

    GEOMETRY_SHA = str(
        geometry[
            "geometry_identity"
        ][
            "sha256"
        ]
    )

    RVE_AREA = (
        width
        * height
    )

    OUT_MSH = args.mesh_out
    OUT_JSON = args.diagnostics_out

    must(
        OUT_MSH.resolve()
        != args.geometry_json.resolve(),
        "mesh output does not overwrite geometry input",
    )

    must(
        OUT_JSON.resolve()
        != args.geometry_json.resolve(),
        "diagnostics output does not overwrite geometry input",
    )

    must(
        OUT_MSH.resolve()
        != OUT_JSON.resolve(),
        "mesh and diagnostics outputs are distinct",
    )

    PARTICLES = [
        (
            int(
                record[
                    "particle_id"
                ]
            ),
            float(
                record[
                    "center_x"
                ]
            ),
            float(
                record[
                    "center_y"
                ]
            ),
        )
        for record
        in physical_records
    ]

    ids = [
        particle_id
        for particle_id, _, _
        in PARTICLES
    ]

    must(
        ids
        == list(
            range(
                1,
                EXPECTED_PARTICLE_COUNT
                + 1,
            )
        ),
        "physical particle IDs are sequential and complete",
    )

    for record in physical_records:
        must(
            math.isclose(
                float(
                    record[
                        "radius"
                    ]
                ),
                R,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),
            "physical particle radius matches M8 monodisperse radius",
        )

    input_crossing_ids = sorted(
        int(value)
        for value in generated[
            "boundary_crossing_particle_ids"
        ]
    )

    computed_crossing_ids = sorted(
        particle_id
        for particle_id, x, y
        in PARTICLES
        if (
            x - R < 0.0
            or x + R > L
            or y - R < 0.0
            or y + R > L
        )
    )

    must(
        computed_crossing_ids
        == input_crossing_ids,
        "boundary-crossing IDs reproduce permanent geometry metadata",
    )

    EXPECTED_CROSSING_IDS = (
        input_crossing_ids
    )

    EXPECTED_REPRESENTATION_COUNT = int(
        generated[
            "periodic_representation_count"
        ]
    )

    EXPECTED_TRANSLATED_IMAGE_COUNT = int(
        generated[
            "translated_periodic_image_count"
        ]
    )

    must(
        len(representations)
        == EXPECTED_REPRESENTATION_COUNT,
        "periodic representation count matches geometry metadata",
    )

    primary_representations = [
        rep
        for rep in representations
        if bool(
            rep[
                "is_primary"
            ]
        )
    ]

    translated_representations = [
        rep
        for rep in representations
        if not bool(
            rep[
                "is_primary"
            ]
        )
    ]

    must(
        len(primary_representations)
        == EXPECTED_PARTICLE_COUNT,
        "one primary periodic representation exists per particle",
    )

    must(
        len(translated_representations)
        == EXPECTED_TRANSLATED_IMAGE_COUNT,
        "translated periodic-image count matches geometry metadata",
    )

    translated_feature_ids = sorted(
        {
            int(
                rep[
                    "particle_id"
                ]
            )
            for rep
            in translated_representations
        }
    )

    must(
        translated_feature_ids
        == EXPECTED_CROSSING_IDS,
        "translated images preserve all crossing-feature identities",
    )

    particle_by_id = {
        int(
            record[
                "particle_id"
            ]
        ): record
        for record
        in physical_records
    }

    for rep in representations:
        particle_id = int(
            rep[
                "particle_id"
            ]
        )

        must(
            particle_id
            in particle_by_id,
            "periodic representation references a known particle ID",
        )

        particle = particle_by_id[
            particle_id
        ]

        must(
            math.isclose(
                float(
                    rep[
                        "radius"
                    ]
                ),
                R,
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),
            "periodic representation preserves particle radius",
        )

        must(
            math.isclose(
                float(
                    rep[
                        "original_center_x"
                    ]
                ),
                float(
                    particle[
                        "center_x"
                    ]
                ),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
            and math.isclose(
                float(
                    rep[
                        "original_center_y"
                    ]
                ),
                float(
                    particle[
                        "center_y"
                    ]
                ),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),
            "periodic representation preserves original center",
        )

        must(
            math.isclose(
                float(
                    rep[
                        "center_x"
                    ]
                ),
                (
                    float(
                        rep[
                            "original_center_x"
                        ]
                    )
                    + float(
                        rep[
                            "shift_x"
                        ]
                    )
                ),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            )
            and math.isclose(
                float(
                    rep[
                        "center_y"
                    ]
                ),
                (
                    float(
                        rep[
                            "original_center_y"
                        ]
                    )
                    + float(
                        rep[
                            "shift_y"
                        ]
                    )
                ),
                rel_tol=0.0,
                abs_tol=1.0e-12,
            ),
            "periodic representation center equals original plus translation",
        )

        must(
            int(
                rep[
                    "source_seed"
                ]
            )
            == SEED,
            "periodic representation preserves source seed",
        )

    EXPECTED_X_PERIODIC_PARTICLE_IDS = sorted(
        {
            int(
                rep[
                    "particle_id"
                ]
            )
            for rep
            in translated_representations
            if not math.isclose(
                float(
                    rep[
                        "shift_x"
                    ]
                ),
                0.0,
                rel_tol=0.0,
                abs_tol=1.0e-14,
            )
        }
    )

    EXPECTED_Y_PERIODIC_PARTICLE_IDS = sorted(
        {
            int(
                rep[
                    "particle_id"
                ]
            )
            for rep
            in translated_representations
            if not math.isclose(
                float(
                    rep[
                        "shift_y"
                    ]
                ),
                0.0,
                rel_tol=0.0,
                abs_tol=1.0e-14,
            )
        }
    )

    EXPECTED_PARTICLE_AREA = sum(
        math.pi
        * float(
            record[
                "radius"
            ]
        )**2
        for record
        in physical_records
    )

    EXPECTED_PARTICLE_FRACTION = (
        EXPECTED_PARTICLE_AREA
        / RVE_AREA
    )

    must(
        math.isclose(
            EXPECTED_PARTICLE_AREA,
            float(
                generated[
                    "particle_area"
                ]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "analytical particle area reproduces geometry metadata",
    )

    must(
        math.isclose(
            EXPECTED_PARTICLE_FRACTION,
            float(
                generated[
                    "particle_area_fraction"
                ]
            ),
            rel_tol=0.0,
            abs_tol=1.0e-12,
        ),
        "analytical particle fraction reproduces geometry metadata",
    )

    print(
        "RVE level:",
        args.rve_level,
    )

    print(
        "RVE side:",
        L,
    )

    print(
        "Physical particles:",
        EXPECTED_PARTICLE_COUNT,
    )

    print(
        "Periodic disk representations:",
        len(
            representations
        ),
    )

    print(
        "Translated periodic images:",
        len(
            translated_representations
        ),
    )

    print(
        "Boundary-crossing particle IDs:",
        EXPECTED_CROSSING_IDS,
    )

    representation_intersection_expected = {}
    nonintersecting_bookkeeping_representations = []

    for rep in representations:
        representation_id = int(
            rep[
                "representation_id"
            ]
        )

        (
            intersection_class,
            clearance,
        ) = disk_cell_intersection_classification(
            center_x=float(
                rep[
                    "center_x"
                ]
            ),
            center_y=float(
                rep[
                    "center_y"
                ]
            ),
            radius=float(
                rep[
                    "radius"
                ]
            ),
            cell_side=L,
            tolerance=CAD_TOL,
        )

        must(
            intersection_class
            != "ambiguous_tangent",
            (
                "periodic representation is not "
                "tangent/near-tangent to the RVE "
                f"(particle {rep['particle_id']}, "
                f"shift=({rep['shift_x']},"
                f"{rep['shift_y']}), "
                f"clearance={clearance})"
            ),
        )

        representation_intersection_expected[
            representation_id
        ] = (
            intersection_class
            == "positive_area"
        )

        if intersection_class == "disjoint":
            nonintersecting_bookkeeping_representations.append(
                {
                    "representation_id":
                        representation_id,
                    "particle_id":
                        int(
                            rep[
                                "particle_id"
                            ]
                        ),
                    "shift_x":
                        float(
                            rep[
                                "shift_x"
                            ]
                        ),
                    "shift_y":
                        float(
                            rep[
                                "shift_y"
                            ]
                        ),
                    "clearance":
                        float(
                            clearance
                        ),
                }
            )

    expected_mesh_representation_count = sum(
        1
        for expected
        in representation_intersection_expected.values()
        if expected
    )

    must(
        expected_mesh_representation_count
        >= EXPECTED_PARTICLE_COUNT,
        (
            "positive-area periodic representation count "
            "is not below physical particle count"
        ),
    )

    must(
        (
            expected_mesh_representation_count
            + len(
                nonintersecting_bookkeeping_representations
            )
        )
        == EXPECTED_REPRESENTATION_COUNT,
        (
            "positive-area plus disjoint bookkeeping "
            "representations reproduce geometry metadata"
        ),
    )

    print(
        "Positive-area periodic representations:",
        expected_mesh_representation_count,
    )

    print(
        "Disjoint bookkeeping representations:",
        len(
            nonintersecting_bookkeeping_representations
        ),
    )

    if nonintersecting_bookkeeping_representations:
        print(
            "Disjoint bookkeeping representation records:",
            nonintersecting_bookkeeping_representations,
        )

    gmsh.initialize()

    diagnostics = {}

    try:
        gmsh.option.setNumber(
            "General.Terminal",
            0,
        )

        gmsh.model.add(
            "m8_periodized_particle_mesh"
        )

        rectangle = (
            gmsh.model.occ.addRectangle(
                0.0,
                0.0,
                0.0,
                L,
                L,
            )
        )

        disk_dimtags = []

        for rep in representations:
            disk_tag = gmsh.model.occ.addDisk(
                rep["center_x"],
                rep["center_y"],
                0.0,
                R,
                R,
            )

            rep["disk_tag"] = int(
                disk_tag
            )

            disk_dimtags.append(
                (2, disk_tag)
            )

        _, fragment_map = (
            gmsh.model.occ.fragment(
                [(2, rectangle)],
                disk_dimtags,
                removeObject=True,
                removeTool=True,
            )
        )

        gmsh.model.occ.synchronize()

        must(
            len(fragment_map)
            == 1 + len(representations),
            "Gmsh fragment map has expected object/tool entries",
        )

        # Determine which fragmented surfaces are physically
        # inside the computational cell.
        inside_surface_tags = []
        outside_surface_dimtags = []

        for dim, tag in gmsh.model.getEntities(2):
            bb = gmsh.model.getBoundingBox(
                2,
                tag,
            )

            if bbox_inside_cell(bb):
                inside_surface_tags.append(
                    int(tag)
                )
            else:
                outside_surface_dimtags.append(
                    (2, int(tag))
                )

        must(
            len(inside_surface_tags) > 0,
            "fragmentation produced surfaces inside ""the computational cell",
        )

        # Delete protruding pieces outside the unit cell.
        # The periodic translated pieces INSIDE the cell remain.
        if outside_surface_dimtags:
            gmsh.model.occ.remove(
                outside_surface_dimtags,
                recursive=True,
            )
            gmsh.model.occ.synchronize()

        retained_surface_tags = {
            int(tag)
            for dim, tag
            in gmsh.model.getEntities(2)
            if dim == 2
        }

        must(
            retained_surface_tags,
            "retained computational-cell surfaces exist",
        )

        particle_surface_tags = set()
        surface_to_particle_id = {}

        for rep, mapping in zip(
            representations,
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

            representation_id = int(
                rep[
                    "representation_id"
                ]
            )

            expected_to_intersect = (
                representation_intersection_expected[
                    representation_id
                ]
            )

            if expected_to_intersect:
                must(
                    len(mapped_inside) == 1,
                    (
                        "each positive-area periodic disk "
                        "representation maps to exactly one "
                        "retained particle piece "
                        f"(particle {rep['particle_id']}, "
                        f"shift=({rep['shift_x']},"
                        f"{rep['shift_y']}))"
                    ),
                )
            else:
                must(
                    len(mapped_inside) == 0,
                    (
                        "each analytically disjoint periodic "
                        "bookkeeping representation maps to "
                        "no retained particle piece "
                        f"(particle {rep['particle_id']}, "
                        f"shift=({rep['shift_x']},"
                        f"{rep['shift_y']}))"
                    ),
                )

                continue

            surface_tag = mapped_inside[0]

            must(
                (
                    surface_tag
                    not in surface_to_particle_id
                ),
                (
                    "particle surface piece has unique "
                    "periodic representation ownership"
                ),
            )

            surface_to_particle_id[
                surface_tag
            ] = int(
                rep[
                    "particle_id"
                ]
            )

            particle_surface_tags.add(
                surface_tag
            )

        matrix_surface_tags = (
            retained_surface_tags
            - particle_surface_tags
        )

        print(
            "Retained surface count:",
            len(retained_surface_tags),
        )
        print(
            "Particle surface-piece count:",
            len(particle_surface_tags),
        )
        print(
            "Matrix surface count:",
            len(matrix_surface_tags),
        )

        must(
            len(particle_surface_tags)
            == expected_mesh_representation_count,
            (
                "all positive-area periodic particle "
                "surface pieces retained"
            ),
        )

        must(
            len(matrix_surface_tags) >= 1,
            "matrix surface exists",
        )

        # ----------------------------------------------------
        # Exact CAD area accounting and feature-ID accounting.
        # ----------------------------------------------------

        area_by_particle = {
            particle_id: 0.0
            for particle_id, _, _
            in PARTICLES
        }

        for surface_tag in particle_surface_tags:
            area = gmsh.model.occ.getMass(
                2,
                surface_tag,
            )

            particle_id = (
                surface_to_particle_id[
                    surface_tag
                ]
            )

            area_by_particle[
                particle_id
            ] += float(area)

        single_particle_area = (
            math.pi * R**2
        )

        max_particle_id_area_error = max(
            abs(
                area_by_particle[particle_id]
                - single_particle_area
            )
            for particle_id
            in area_by_particle
        )

        cad_particle_area = sum(
            area_by_particle.values()
        )

        cad_matrix_area = sum(
            float(
                gmsh.model.occ.getMass(
                    2,
                    tag,
                )
            )
            for tag in matrix_surface_tags
        )

        cad_total_area = (
            cad_particle_area
            + cad_matrix_area
        )

        print(
            "Expected particle CAD area:",
            EXPECTED_PARTICLE_AREA,
        )
        print(
            "Actual particle CAD area  :",
            cad_particle_area,
        )
        print(
            "Actual matrix CAD area    :",
            cad_matrix_area,
        )
        print(
            "Actual total CAD area     :",
            cad_total_area,
        )
        print(
            "Maximum per-ID wrapped area error:",
            max_particle_id_area_error,
        )

        must(
            max_particle_id_area_error
            <= CAD_TOL,
            (
                "each physical particle's wrapped pieces "
                "sum to exactly one particle area"
            ),
        )

        must(
            math.isclose(
                cad_particle_area,
                EXPECTED_PARTICLE_AREA,
                rel_tol=0.0,
                abs_tol=CAD_TOL,
            ),
            "CAD particle area has no periodic double counting",
        )

        must(
            math.isclose(
                cad_total_area,
                RVE_AREA,
                rel_tol=0.0,
                abs_tol=CAD_TOL,
            ),
            "CAD matrix + particle area equals gross RVE area",
        )

        # ----------------------------------------------------
        # Discover split external boundaries.
        # ----------------------------------------------------

        left = side_curves(
            axis=0,
            value=0.0,
        )
        right = side_curves(
            axis=0,
            value=L,
        )
        bottom = side_curves(
            axis=1,
            value=0.0,
        )
        top = side_curves(
            axis=1,
            value=L,
        )

        print("Left boundary curves  :", left)
        print("Right boundary curves :", right)
        print("Bottom boundary curves:", bottom)
        print("Top boundary curves   :", top)

        must(
            len(left) > 0
            and len(right) > 0,
            "left/right external boundaries contain segments",
        )

        must(
            len(left)
            == len(right),
            "left/right geometric segment counts match",
        )

        must(
            len(bottom) > 0
            and len(top) > 0,
            "bottom/top external boundaries contain segments",
        )

        must(
            len(bottom)
            == len(top),
            "bottom/top geometric segment counts match",
        )

        x_pairs = pair_curves(
            master_tags=left,
            slave_tags=right,
            dx=L,
            dy=0.0,
        )

        y_pairs = pair_curves(
            master_tags=bottom,
            slave_tags=top,
            dx=0.0,
            dy=L,
        )

        must(
            len(x_pairs) == len(left),
            "all left/right geometric boundary segments paired",
        )

        must(
            len(y_pairs) == len(bottom),
            "all bottom/top geometric boundary segments paired",
        )

        def boundary_identity(
            curve_tag: int,
        ):
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
                    "external boundary curve "
                    f"{curve_tag} has exactly one "
                    "cell-side adjacent surface"
                ),
            )

            surface_tag = adjacent[0]

            if (
                surface_tag
                in particle_surface_tags
            ):
                return (
                    "particle",
                    surface_to_particle_id[
                        surface_tag
                    ],
                )

            must(
                surface_tag
                in matrix_surface_tags,
                (
                    "external boundary adjacency belongs "
                    "to known material"
                ),
            )

            return ("matrix", None)

        x_particle_ids = set()
        y_particle_ids = set()

        for slave, master in x_pairs:
            master_identity = (
                boundary_identity(master)
            )
            slave_identity = (
                boundary_identity(slave)
            )

            print(
                "X pair:",
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
                    "left/right material occupancy and "
                    "feature identity match"
                ),
            )

            if (
                master_identity[0]
                == "particle"
            ):
                x_particle_ids.add(
                    int(master_identity[1])
                )

        for slave, master in y_pairs:
            master_identity = (
                boundary_identity(master)
            )
            slave_identity = (
                boundary_identity(slave)
            )

            print(
                "Y pair:",
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
                    "bottom/top material occupancy and "
                    "feature identity match"
                ),
            )

            if (
                master_identity[0]
                == "particle"
            ):
                y_particle_ids.add(
                    int(master_identity[1])
                )

        must(
            sorted(
                x_particle_ids
            )
            == EXPECTED_X_PERIODIC_PARTICLE_IDS,
            (
                "left/right wrapped particle identities "
                "match permanent periodized geometry metadata"
            ),
        )

        must(
            sorted(
                y_particle_ids
            )
            == EXPECTED_Y_PERIODIC_PARTICLE_IDS,
            (
                "bottom/top wrapped particle identities "
                "match permanent periodized geometry metadata"
            ),
        )

        # ----------------------------------------------------
        # Physical groups.
        # ----------------------------------------------------

        gmsh.model.addPhysicalGroup(
            2,
            sorted(matrix_surface_tags),
            MATRIX_TAG,
        )
        gmsh.model.setPhysicalName(
            2,
            MATRIX_TAG,
            "matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            sorted(particle_surface_tags),
            PARTICLE_TAG,
        )
        gmsh.model.setPhysicalName(
            2,
            PARTICLE_TAG,
            "particle",
        )

        for curves, physical_tag, name in [
            (left, LEFT_TAG, "left"),
            (right, RIGHT_TAG, "right"),
            (bottom, BOTTOM_TAG, "bottom"),
            (top, TOP_TAG, "top"),
        ]:
            gmsh.model.addPhysicalGroup(
                1,
                curves,
                physical_tag,
            )
            gmsh.model.setPhysicalName(
                1,
                physical_tag,
                name,
            )

        # ----------------------------------------------------
        # Gmsh periodic mesh constraints:
        # slave = translated copy of master.
        # ----------------------------------------------------

        transform_x = [
            1.0, 0.0, 0.0, L,
            0.0, 1.0, 0.0, 0.0,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]

        transform_y = [
            1.0, 0.0, 0.0, 0.0,
            0.0, 1.0, 0.0, L,
            0.0, 0.0, 1.0, 0.0,
            0.0, 0.0, 0.0, 1.0,
        ]

        gmsh.model.mesh.setPeriodic(
            1,
            [slave for slave, _ in x_pairs],
            [master for _, master in x_pairs],
            transform_x,
        )

        gmsh.model.mesh.setPeriodic(
            1,
            [slave for slave, _ in y_pairs],
            [master for _, master in y_pairs],
            transform_y,
        )

        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMin",
            H,
        )
        gmsh.option.setNumber(
            "Mesh.CharacteristicLengthMax",
            H,
        )
        gmsh.option.setNumber(
            "Mesh.ElementOrder",
            1,
        )
        gmsh.option.setNumber(
            "Mesh.RecombineAll",
            0,
        )

        print()
        print(
            f"Generating periodic Gmsh mesh at h={H} ..."
        )

        gmsh.model.mesh.generate(2)

        # ----------------------------------------------------
        # Global node-coordinate verification.
        # ----------------------------------------------------

        node_tags, node_coords_flat, _ = (
            gmsh.model.mesh.getNodes()
        )

        node_coords = np.asarray(
            node_coords_flat,
            dtype=float,
        ).reshape((-1, 3))

        node_tag_to_coord = {
            int(tag): node_coords[i]
            for i, tag
            in enumerate(node_tags)
        }

        left_nodes = node_coords[
            np.abs(node_coords[:, 0]) <= NODE_TOL
        ]
        right_nodes = node_coords[
            np.abs(node_coords[:, 0] - L) <= NODE_TOL
        ]
        bottom_nodes = node_coords[
            np.abs(node_coords[:, 1]) <= NODE_TOL
        ]
        top_nodes = node_coords[
            np.abs(node_coords[:, 1] - L) <= NODE_TOL
        ]

        print(
            "Boundary mesh-node counts:",
            {
                "left": len(left_nodes),
                "right": len(right_nodes),
                "bottom": len(bottom_nodes),
                "top": len(top_nodes),
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
                    np.sort(left_nodes[:, 1])
                    - np.sort(right_nodes[:, 1])
                )
            )
        )

        bt_coordinate_error = float(
            np.max(
                np.abs(
                    np.sort(bottom_nodes[:, 0])
                    - np.sort(top_nodes[:, 0])
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
            "left/right boundary meshes are translationally identical",
        )

        must(
            bt_coordinate_error
            <= NODE_TOL,
            "bottom/top boundary meshes are translationally identical",
        )

        # ----------------------------------------------------
        # Verify Gmsh's actual periodic master/slave
        # correspondence records.
        # ----------------------------------------------------

        periodic_node_pair_count = 0
        periodic_transform_error = 0.0
        periodic_master_ok = True

        for (
            pairs,
            translation,
            axis_name,
        ) in [
            (
                x_pairs,
                np.array([L, 0.0, 0.0]),
                "X",
            ),
            (
                y_pairs,
                np.array([0.0, L, 0.0]),
                "Y",
            ),
        ]:
            for slave, expected_master in pairs:
                (
                    actual_master,
                    slave_nodes,
                    master_nodes,
                    _,
                ) = gmsh.model.mesh.getPeriodicNodes(
                    1,
                    slave,
                    False,
                )

                if (
                    int(actual_master)
                    != int(expected_master)
                ):
                    periodic_master_ok = False

                must(
                    len(slave_nodes)
                    == len(master_nodes),
                    (
                        f"{axis_name} periodic node-array "
                        f"lengths match for curve {slave}"
                    ),
                )

                periodic_node_pair_count += (
                    len(slave_nodes)
                )

                for slave_node, master_node in zip(
                    slave_nodes,
                    master_nodes,
                    strict=True,
                ):
                    slave_xyz = (
                        node_tag_to_coord[
                            int(slave_node)
                        ]
                    )
                    master_xyz = (
                        node_tag_to_coord[
                            int(master_node)
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
            "Gmsh periodic entities report intended master curves",
        )

        must(
            periodic_node_pair_count > 0,
            "Gmsh returned periodic node correspondence records",
        )

        must(
            periodic_transform_error
            <= NODE_TOL,
            "Gmsh periodic node correspondence satisfies translation map",
        )

        # ----------------------------------------------------
        # Element coverage + actual triangulated areas.
        # ----------------------------------------------------

        def elements_for_surfaces(
            surface_tags,
        ) -> set[int]:
            result = set()

            for surface_tag in surface_tags:
                (
                    _element_types,
                    element_tag_blocks,
                    _node_tag_blocks,
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
            _all_element_types,
            all_element_tag_blocks,
            _all_node_tag_blocks,
        ) = gmsh.model.mesh.getElements(2)

        all_elements = set()

        for block in all_element_tag_blocks:
            all_elements.update(
                int(tag)
                for tag in block
            )

        must(
            matrix_elements.isdisjoint(
                particle_elements
            ),
            "matrix and particle element sets are disjoint",
        )

        must(
            (
                matrix_elements
                | particle_elements
            )
            == all_elements,
            "every 2D mesh element belongs to matrix or particle",
        )

        must(
            len(all_elements) > 0,
            "2D mesh contains elements",
        )

        def triangulated_area(
            surface_tags,
        ):
            area = 0.0
            minimum_area = math.inf

            for surface_tag in surface_tags:
                (
                    element_types,
                    _element_tag_blocks,
                    node_tag_blocks,
                ) = gmsh.model.mesh.getElements(
                    2,
                    surface_tag,
                )

                for element_type, node_block in zip(
                    element_types,
                    node_tag_blocks,
                    strict=True,
                ):
                    (
                        _name,
                        dim,
                        order,
                        num_nodes,
                        _local_coords,
                        _num_primary_nodes,
                    ) = gmsh.model.mesh.getElementProperties(
                        int(element_type)
                    )

                    must(
                        int(dim) == 2,
                        "material element has dimension 2",
                    )

                    must(
                        int(order) == 1
                        and int(num_nodes) == 3,
                        (
                            "M8 mesh uses "
                            "first-order triangles"
                        ),
                    )

                    connectivity = np.asarray(
                        node_block,
                        dtype=np.int64,
                    ).reshape((-1, 3))

                    for n0, n1, n2 in connectivity:
                        p0 = node_tag_to_coord[
                            int(n0)
                        ][:2]
                        p1 = node_tag_to_coord[
                            int(n1)
                        ][:2]
                        p2 = node_tag_to_coord[
                            int(n2)
                        ][:2]

                        edge1 = p1 - p0
                        edge2 = p2 - p0

                        # NumPy 2.5 removed np.cross support
                        # for 2-component vectors.  For a
                        # planar triangle, use the exact
                        # scalar 2-D determinant instead.
                        cross2d = (
                            edge1[0] * edge2[1]
                            - edge1[1] * edge2[0]
                        )

                        tri_area = 0.5 * abs(
                            cross2d
                        )

                        area += float(tri_area)
                        minimum_area = min(
                            minimum_area,
                            float(tri_area),
                        )

            return area, minimum_area

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

        meshed_total_area = (
            meshed_matrix_area
            + meshed_particle_area
        )

        meshed_particle_fraction = (
            meshed_particle_area
            / meshed_total_area
        )

        particle_fraction_error = abs(
            meshed_particle_fraction
            - EXPECTED_PARTICLE_FRACTION
        )

        minimum_triangle_area = min(
            matrix_min_area,
            particle_min_area,
        )

        print(
            "2D element count:",
            len(all_elements),
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
            "Meshed total area:",
            meshed_total_area,
        )
        print(
            "Analytical particle fraction:",
            EXPECTED_PARTICLE_FRACTION,
        )
        print(
            "Meshed particle fraction:",
            meshed_particle_fraction,
        )
        print(
            "Particle-fraction absolute error:",
            particle_fraction_error,
        )
        print(
            "Minimum triangle area:",
            minimum_triangle_area,
        )

        must(
            math.isclose(
                meshed_total_area,
                RVE_AREA,
                rel_tol=0.0,
                abs_tol=1.0e-10,
            ),
            "triangulated total area equals gross RVE area",
        )

        must(
            particle_fraction_error
            <= MESH_FRACTION_TOL,
            (
                "meshed particle fraction is within "
                "0.005 absolute of analytical fraction"
            ),
        )

        must(
            minimum_triangle_area > 0.0,
            "all generated triangles have positive area magnitude",
        )

        gmsh.write(
            str(OUT_MSH)
        )

        diagnostics = {
            "schema": MESH_SCHEMA,
            "status": "valid",
            "source_geometry": {
                "path": str(
                    args.geometry_json
                ),
                "schema": (
                    geometry[
                        "schema"
                    ]
                ),
                "geometry_sha256": (
                    GEOMETRY_SHA
                ),
                "seed": SEED,
            },
            "provenance": {
                "rve_level": (
                    args.rve_level
                ),
                "width": L,
                "height": L,
                "gross_area": (
                    RVE_AREA
                ),
                "particle_radius": R,
                "particle_count": (
                    EXPECTED_PARTICLE_COUNT
                ),
                "mesh_size": H,
                "purpose": (
                    "permanent M8 periodized "
                    "particle-mesh generation"
                ),
            },
            "physical_tags": {
                "matrix": (
                    MATRIX_TAG
                ),
                "particle": (
                    PARTICLE_TAG
                ),
                "left": (
                    LEFT_TAG
                ),
                "right": (
                    RIGHT_TAG
                ),
                "bottom": (
                    BOTTOM_TAG
                ),
                "top": (
                    TOP_TAG
                ),
            },
            "periodic_geometry": {
                "representation_count": (
                    len(
                        representations
                    )
                ),
                "translated_image_count": (
                    len(
                        translated_representations
                    )
                ),
                "boundary_crossing_ids": (
                    EXPECTED_CROSSING_IDS
                ),
                "x_periodic_particle_ids": (
                    sorted(
                        x_particle_ids
                    )
                ),
                "y_periodic_particle_ids": (
                    sorted(
                        y_particle_ids
                    )
                ),
                "mesh_intersecting_representation_count": (
                    expected_mesh_representation_count
                ),
                "nonintersecting_bookkeeping_representation_count": (
                    len(
                        nonintersecting_bookkeeping_representations
                    )
                ),
                "nonintersecting_bookkeeping_representations": (
                    nonintersecting_bookkeeping_representations
                ),
                "particle_surface_piece_count": (
                    len(
                        particle_surface_tags
                    )
                ),
                "matrix_surface_count": (
                    len(
                        matrix_surface_tags
                    )
                ),
            },
            "cad_area": {
                "expected_particle_area": (
                    EXPECTED_PARTICLE_AREA
                ),
                "particle_area": (
                    cad_particle_area
                ),
                "matrix_area": (
                    cad_matrix_area
                ),
                "total_area": (
                    cad_total_area
                ),
                "max_per_particle_wrapped_area_error": (
                    max_particle_id_area_error
                ),
            },
            "boundary_geometry": {
                "left_curve_count": (
                    len(left)
                ),
                "right_curve_count": (
                    len(right)
                ),
                "bottom_curve_count": (
                    len(bottom)
                ),
                "top_curve_count": (
                    len(top)
                ),
                "x_pair_count": (
                    len(x_pairs)
                ),
                "y_pair_count": (
                    len(y_pairs)
                ),
            },
            "mesh": {
                "cell_count": (
                    len(
                        all_elements
                    )
                ),
                "matrix_cell_count": (
                    len(
                        matrix_elements
                    )
                ),
                "particle_cell_count": (
                    len(
                        particle_elements
                    )
                ),
                "minimum_triangle_area": (
                    minimum_triangle_area
                ),
                "left_node_count": (
                    len(
                        left_nodes
                    )
                ),
                "right_node_count": (
                    len(
                        right_nodes
                    )
                ),
                "bottom_node_count": (
                    len(
                        bottom_nodes
                    )
                ),
                "top_node_count": (
                    len(
                        top_nodes
                    )
                ),
                "left_right_coordinate_mismatch": (
                    lr_coordinate_error
                ),
                "bottom_top_coordinate_mismatch": (
                    bt_coordinate_error
                ),
                "periodic_node_pair_record_count": (
                    periodic_node_pair_count
                ),
                "periodic_transform_max_error": (
                    periodic_transform_error
                ),
                "element_policy": (
                    "first_order_triangles"
                ),
            },
            "meshed_area": {
                "matrix_area": (
                    meshed_matrix_area
                ),
                "particle_area": (
                    meshed_particle_area
                ),
                "total_area": (
                    meshed_total_area
                ),
                "analytical_particle_fraction": (
                    EXPECTED_PARTICLE_FRACTION
                ),
                "meshed_particle_fraction": (
                    meshed_particle_fraction
                ),
                "particle_fraction_absolute_error": (
                    particle_fraction_error
                ),
            },
            "artifacts": {
                "mesh": str(
                    OUT_MSH
                ),
                "diagnostics": str(
                    OUT_JSON
                ),
            },
            "scope_guard": {
                "fem_solve_performed": False,
                "voids_generated": False,
                "protected_m6_m7_schema_mutated": False,
                "m9_production_parameterization": False,
            },
        }

        OUT_JSON.write_text(
            json.dumps(
                diagnostics,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
            + "\n",
            encoding="utf-8",
        )

        print()
        print(
            json.dumps(
                diagnostics,
                indent=2,
                sort_keys=True,
                allow_nan=False,
            )
        )

        print()
        print(
            "PASS — permanent M8 periodized "
            "Gmsh mesh validation"
        )

    finally:
        gmsh.finalize()


if __name__ == "__main__":
    main()
