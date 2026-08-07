"""Create and verify the first matrix + circular particle CAD geometry."""

from pathlib import Path
import math

import gmsh
import yaml


def main() -> None:
    """Create two conforming material regions using Gmsh OpenCASCADE."""

    config_path = Path("configs/02_single_particle.yaml")

    with config_path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    width = float(config["geometry"]["width"])
    height = float(config["geometry"]["height"])

    cx = float(config["particle"]["center_x"])
    cy = float(config["particle"]["center_y"])
    radius = float(config["particle"]["radius"])

    expected_particle_area = math.pi * radius**2
    expected_matrix_area = (
        width * height - expected_particle_area
    )

    gmsh.initialize()

    try:
        gmsh.option.setNumber("General.Terminal", 0)

        gmsh.model.add(
            "single_particle_composite_geometry"
        )

        # --------------------------------------------------------------
        # 1. Original CAD surfaces
        # --------------------------------------------------------------
        rectangle = gmsh.model.occ.addRectangle(
            0.0,
            0.0,
            0.0,
            width,
            height,
        )

        disk = gmsh.model.occ.addDisk(
            cx,
            cy,
            0.0,
            radius,
            radius,
        )

        # --------------------------------------------------------------
        # 2. Fragment the overlapping surfaces
        #
        # This creates conforming matrix and particle regions sharing
        # the same internal interface.
        # --------------------------------------------------------------
        gmsh.model.occ.fragment(
            [(2, rectangle)],
            [(2, disk)],
            removeObject=True,
            removeTool=True,
        )

        gmsh.model.occ.synchronize()

        # --------------------------------------------------------------
        # 3. Identify resulting surfaces by their areas
        # --------------------------------------------------------------
        surfaces = gmsh.model.getEntities(dim=2)

        if len(surfaces) != 2:
            raise RuntimeError(
                f"Expected exactly 2 surfaces after fragmentation, "
                f"but found {len(surfaces)}."
            )

        surface_areas = {
            tag: gmsh.model.occ.getMass(2, tag)
            for _, tag in surfaces
        }

        particle_tag = min(
            surface_areas,
            key=lambda tag: abs(
                surface_areas[tag]
                - expected_particle_area
            ),
        )

        matrix_candidates = [
            tag
            for tag in surface_areas
            if tag != particle_tag
        ]

        if len(matrix_candidates) != 1:
            raise RuntimeError(
                "Could not uniquely identify matrix surface."
            )

        matrix_tag = matrix_candidates[0]

        # --------------------------------------------------------------
        # 4. Add named physical material regions
        # --------------------------------------------------------------
        matrix_physical_tag = 1
        particle_physical_tag = 2

        gmsh.model.addPhysicalGroup(
            2,
            [matrix_tag],
            tag=matrix_physical_tag,
            name="matrix",
        )

        gmsh.model.addPhysicalGroup(
            2,
            [particle_tag],
            tag=particle_physical_tag,
            name="particle",
        )

        # --------------------------------------------------------------
        # 5. Verification
        # --------------------------------------------------------------
        matrix_area = surface_areas[matrix_tag]
        particle_area = surface_areas[particle_tag]

        total_area = matrix_area + particle_area

        physical_groups = gmsh.model.getPhysicalGroups()

        print("Number of 2D surfaces:", len(surfaces))
        print("Matrix surface tag:", matrix_tag)
        print("Particle surface tag:", particle_tag)
        print()

        print("Expected matrix area:", expected_matrix_area)
        print("Gmsh matrix area:", matrix_area)
        print()

        print("Expected particle area:", expected_particle_area)
        print("Gmsh particle area:", particle_area)
        print()

        print("Total geometry area:", total_area)
        print()

        print("Physical groups:")

        for dim, tag in physical_groups:
            print(
                f"  name={gmsh.model.getPhysicalName(dim, tag)}, "
                f"dimension={dim}, "
                f"tag={tag}"
            )

        area_tolerance = 1.0e-10

        assert math.isclose(
            matrix_area,
            expected_matrix_area,
            abs_tol=area_tolerance,
            rel_tol=0.0,
        )

        assert math.isclose(
            particle_area,
            expected_particle_area,
            abs_tol=area_tolerance,
            rel_tol=0.0,
        )

        assert math.isclose(
            total_area,
            width * height,
            abs_tol=area_tolerance,
            rel_tol=0.0,
        )

        assert len(physical_groups) == 2

        print()
        print("Single-particle CAD geometry validation passed.")

    finally:
        gmsh.finalize()


if __name__ == "__main__":
    main()
