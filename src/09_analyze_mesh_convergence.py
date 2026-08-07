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

    print("Mesh-convergence analysis input: PASSED")
    print("Run count:", len(rows))
    print("Cell counts:", cell_counts)
    print("Effective moduli:", effective_moduli)
    print("Particle-fraction errors:", particle_fraction_errors)
    print("Created:", output_path)
    print("Created:", particle_output_path)


if __name__ == "__main__":
    main()
