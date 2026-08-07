"""Analyze effective-modulus convergence for the single-particle model."""

from pathlib import Path
import csv

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt


def main() -> None:
    """Create the effective-modulus mesh-convergence plot."""

    input_path = Path(
        "results/processed/01_mesh_convergence_summary.csv"
    )

    output_path = Path(
        "figures/05_effective_modulus_convergence.png"
    )

    if not input_path.exists():
        raise FileNotFoundError(
            f"Processed convergence file not found: {input_path}"
        )

    with input_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:
        rows = list(csv.DictReader(file))

    expected_mesh_sizes = [
        0.05,
        0.04,
        0.032,
        0.0256,
        0.02048,
        0.016384,
    ]

    actual_mesh_sizes = [
        float(row["mesh_size"])
        for row in rows
    ]

    if actual_mesh_sizes != expected_mesh_sizes:
        raise RuntimeError(
            "Unexpected mesh-size sequence: "
            + str(actual_mesh_sizes)
        )

    cell_counts = [
        int(row["total_cell_count"])
        for row in rows
    ]

    effective_moduli = [
        float(row["effective_axial_modulus"])
        for row in rows
    ]

    particle_fraction_errors = [
        float(row["particle_fraction_error"])
        for row in rows
    ]

    refined_cell_counts = cell_counts[1:]

    matrix_min_changes = [
        float(
            row[
                "matrix_sigma_xx_min_successive_difference_pct"
            ]
        )
        for row in rows[1:]
    ]

    matrix_max_changes = [
        float(
            row[
                "matrix_sigma_xx_max_successive_difference_pct"
            ]
        )
        for row in rows[1:]
    ]

    particle_min_changes = [
        float(
            row[
                "particle_sigma_xx_min_successive_difference_pct"
            ]
        )
        for row in rows[1:]
    ]

    particle_max_changes = [
        float(
            row[
                "particle_sigma_xx_max_successive_difference_pct"
            ]
        )
        for row in rows[1:]
    ]

    fig, ax = plt.subplots(
        figsize=(7.0, 4.8),
        constrained_layout=True,
    )

    ax.plot(
        cell_counts,
        effective_moduli,
        marker="o",
    )

    ax.set_xlabel("Total cell count")
    ax.set_ylabel("Effective axial modulus")
    ax.set_title(
        "Effective Axial Modulus Mesh Convergence"
    )

    ax.grid(True)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fig.savefig(
        output_path,
        dpi=300,
    )

    plt.close(fig)

    particle_output_path = Path(
        "figures/06_particle_fraction_error_convergence.png"
    )

    particle_fig, particle_ax = plt.subplots(
        figsize=(7.0, 4.8),
        constrained_layout=True,
    )

    particle_ax.plot(
        cell_counts,
        particle_fraction_errors,
        marker="o",
    )

    particle_ax.set_xlabel("Total cell count")
    particle_ax.set_ylabel("Particle-fraction absolute error")
    particle_ax.set_title(
        "Particle Geometry Representation Convergence"
    )

    particle_ax.grid(True)

    particle_fig.savefig(
        particle_output_path,
        dpi=300,
    )

    plt.close(particle_fig)

    stress_output_path = Path(
        "figures/07_local_stress_convergence.png"
    )

    stress_fig, stress_ax = plt.subplots(
        figsize=(7.0, 4.8),
        constrained_layout=True,
    )

    stress_ax.plot(
        refined_cell_counts,
        matrix_min_changes,
        marker="o",
        label="Matrix sigma_xx min",
    )

    stress_ax.plot(
        refined_cell_counts,
        matrix_max_changes,
        marker="o",
        label="Matrix sigma_xx max",
    )

    stress_ax.plot(
        refined_cell_counts,
        particle_min_changes,
        marker="o",
        label="Particle sigma_xx min",
    )

    stress_ax.plot(
        refined_cell_counts,
        particle_max_changes,
        marker="o",
        label="Particle sigma_xx max",
    )

    stress_ax.set_xlabel("Total cell count")
    stress_ax.set_ylabel("Successive difference (%)")
    stress_ax.set_title(
        "Local Stress Extrema Mesh Sensitivity"
    )

    stress_ax.set_yscale("log")
    stress_ax.grid(True)
    stress_ax.legend()

    stress_fig.savefig(
        stress_output_path,
        dpi=300,
    )

    plt.close(stress_fig)

    print("Mesh-convergence analysis input: PASSED")
    print("Run count:", len(rows))
    print("Cell counts:", cell_counts)
    print("Effective moduli:", effective_moduli)
    print("Particle-fraction errors:", particle_fraction_errors)
    print("Created:", output_path)
    print("Created:", particle_output_path)
    print("Created:", stress_output_path)


if __name__ == "__main__":
    main()
