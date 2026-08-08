# Composite RVE Research — Project Status

**Last planning checkpoint:** 9 August 2026
**Research route:** Simulation + Machine Learning only
**Laboratory experiments:** None
**Current major milestone:** M6 not started
**Authoritative post-M5 roadmap:** `docs/Secondary_Planning.docx`

---

## 1. Research Direction

**Working research title**

> An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.

The project combines finite-element simulation, stochastic microstructure generation, surrogate modelling, active learning, uncertainty analysis, and out-of-distribution evaluation.

The original Project 01 planning remains the historical initial scope. The post-M5 **Secondary Planning** record is the authoritative corrected continuation roadmap.

---

## 2. Milestone Status

| Milestone | Status | Summary |
|---|---|---|
| M0 | 100% COMPLETE | Software and development environment |
| M1 | 100% COMPLETE | FEM fundamentals and homogeneous validation |
| M2 | 100% COMPLETE | First single-particle composite model |
| M3 | 100% COMPLETE | Mesh convergence and composite verification |
| M4 | 100% COMPLETE | Parametric RVE and sampling foundation |
| M5 | 100% COMPLETE | Initial perfect-bonding FEM dataset generation |
| M6 | NOT STARTED | Multiple/Random-Particle Microstructure Foundation |
| M7 | NOT STARTED | Circular Void Defects and Defect-Sensitive Response Definition |
| M8 | NOT STARTED | RVE-Size Study, Homogenization BC/PBC Verification, and Final Target-Mesh Verification |
| M9 | NOT STARTED | Final Parameter-Space Lock and Stochastic Pilot Dataset |
| M10 | NOT STARTED | Main Quality-Controlled FEM Simulation Database |
| M11 | NOT STARTED | Baseline Machine-Learning Models and Grouped Validation |
| M12 | NOT STARTED | Active Learning versus Random Sampling |
| M13 | NOT STARTED | Uncertainty Calibration, Variability, and OOD Testing |
| M14 | NOT STARTED | Final Analysis, Ablations, Figures, and Manuscript |

---

## 3. Post-M5 Alignment Decision

The project-plan alignment audit concluded that the work through M5 is scientifically valid and should be retained.

M4 and M5 are interpreted as **inserted parametric, automation, and baseline-data foundation milestones**. They do not replace the random-microstructure, defect, RVE/PBC, stochastic-dataset, active-learning, uncertainty, or OOD stages from the original research plan.

The project must **not proceed directly from M5 into final research ML**.

The next scientific milestone is:

> **M6 — Multiple/Random-Particle Microstructure Foundation**

M6 begins only after the Secondary Planning / project-status documentation checkpoint has been validated, committed, pushed to GitHub, and explicitly approved by the user.

---

## 4. M5 Baseline Dataset — D0-PB

The validated M5 aggregate is retained under the conceptual name:

> **D0-PB — Perfect-Bonding Centered-Single-Inclusion Baseline Dataset**

**File**

`results/processed/07_m5_initial_fem_dataset.csv`

**Validated state**

- 60 FEM cases.
- 60/60 successful.
- 0 failed FEM cases.
- 45 aggregate columns.
- All FEM verification flags passed.
- Deterministic byte-for-byte regeneration verified.
- Exact case order: `M4PB_001` through `M4PB_060`.

**Aggregate SHA-256**

`e48e9eb731b6e13eb15b33ab643722a9d72e8bdb933bf24d9c1c3847776c17d1`

**Effective axial modulus range**

`1051.948603727062` to `1589.3874813628656`

**Effective Poisson response range**

`0.21573865543142967` to `0.3863453188926385`

D0-PB is a deterministic baseline for FEM-pipeline verification, regression testing, surrogate-method development, and later comparison.

It is **not** the final defect-sensitive stochastic research dataset and must not be used to support final claims about void defects, random arrangements, microstructure variability, uncertainty calibration, OOD behaviour, or active-learning efficiency.

---

## 5. Locked Baseline Physics Through M5

The following assumptions describe the validated baseline and must not be changed silently:

- Two-dimensional computational model.
- Small-strain linear elasticity.
- Plane-stress formulation.
- Isotropic matrix material.
- Isotropic reinforcing-particle material.
- Perfect matrix-particle bonding through M5.
- No defects introduced through M5.
- RVE width = `1.0`.
- RVE height = `1.0`.
- D0-PB particle center = `(0.5, 0.5)`.
- Matrix Young's modulus = `1000.0`.
- Prescribed x displacement = `0.01`.
- D0-PB production mesh size = `0.02048`.
- Effective axial modulus and effective Poisson response remain primary global effective-property outputs.
- Local stress extrema remain diagnostic only and are not accepted as fully mesh-converged final ML targets.

For the 2D model, use **particle area fraction** or **2D particle fraction** rather than implying a measured three-dimensional particle volume fraction.

---

## 6. Scientific Work Restored to the Roadmap

Before the final research ML stage, the project still requires:

1. Reproducible multiple/random-particle microstructure generation.
2. Stored random seeds and repeated realizations.
3. Particle overlap prevention and minimum-spacing rules.
4. Particle-size variability.
5. Random and clustered particle arrangements.
6. Circular void defects as the Version-1 defect model.
7. A robust defect-sensitive stress-concentration response.
8. RVE-size/statistical-representativity verification.
9. Final homogenization boundary-condition / PBC verification.
10. Final production-mesh verification for stochastic defect simulations.
11. Final stochastic parameter-space locking.
12. Geometry, mesh, solver, runtime, failure, and provenance recording.
13. A quality-controlled main FEM simulation database.
14. Grouped/leakage-safe ML validation.
15. Active learning versus random sampling at equal FEM budgets.
16. Quantitative uncertainty calibration.
17. Separation of microstructure variability from model uncertainty.
18. Deliberate out-of-distribution testing.
19. Final ablations, figures, reproducibility evidence, and manuscript analysis.

---

## 7. M6 Goal

### M6 — Multiple/Random-Particle Microstructure Foundation

The objective of M6 is to build and verify a reproducible multi-particle geometry foundation before introducing defects.

M6 is expected to establish:

- deterministic regeneration from stored random seeds;
- multiple circular particles;
- particle-position variability;
- particle-size variability;
- overlap prevention;
- minimum particle-particle spacing;
- minimum particle-boundary spacing where required;
- random arrangements;
- clustered arrangements;
- geometry-validity checks;
- explicit handling of invalid geometry;
- meshing robustness checks;
- reproducible geometry metadata.

M6 does **not** introduce circular void defects. Defects belong to M7.

M6 does **not** begin final research machine learning.

---

## 8. ML and Active-Learning Guardrails

- D0-PB is not the final ML research dataset.
- Final surrogate claims wait until stochastic microstructures and defects are implemented and validated.
- Related microstructure realizations must not leak across training and validation groups.
- Begin with conventional tabular surrogate baselines.
- Neural networks require later evidence that their added complexity is justified.
- Active learning must be compared against random acquisition using equal FEM simulation budgets.
- Uncertainty must be quantitatively evaluated and calibrated.
- OOD testing must be explicit rather than inferred from ordinary random train/test splits.

---

## 9. Secondary Planning Documentation

**Formal planning document**

`docs/Secondary_Planning.docx`

**Validated DOCX SHA-256**

`b3373047b4413786f121c4d8818de647c439e00231e5d4fb46c5d60d6f58e46a`

**Reproducible generator**

`src/13_generate_secondary_planning.py`

**Validated generator SHA-256**

`90e3902807fde5bc353564e879c0aeb73c3f817f5711264f231ae8e4db385edf`

The DOCX passed:

- Word-package integrity validation;
- reopening with `python-docx`;
- content checks;
- heading checks;
- saved table-row pagination checks;
- independent numbering checks;
- PDF rendering;
- eight-page visual inspection.

Temporary PDF/PNG rendering artifacts are QA-only and are not project deliverables.

---

## 10. Stable Git Checkpoints

**M5 closure commit**

`5914bf50108c042019303ece09552768faeeb977`

Subject:

`Add validated M5 initial FEM dataset`

**Documentation-dependency commit**

`05c5fc7e9d7315c6aaa48af78c9290319f1a0b6b`

Subject:

`Add document generation dependency`

The current repository history after this status file is committed should be treated as the source of truth for the latest `HEAD`; this status document intentionally does not hard-code a future documentation-commit hash.

---

## 11. Working Rules

Research work follows these rules:

1. Work on one concrete step at a time.
2. Wait for the complete terminal output after every step.
3. Verify the result before continuing.
4. Fix failures before moving forward.
5. Do not silently modify established physics.
6. Announce every major milestone transition.
7. Summarize what has been completed before a new milestone.
8. State the next milestone's objective and progress state.
9. Obtain explicit user confirmation before starting a new major milestone.
10. Inspect exact Git changes before staging.
11. Stage only intended paths.
12. Run staged safety checks.
13. Commit one meaningful validated work unit at a time.
14. Push validated commits to `origin/main`.
15. Verify local `HEAD`, `origin/main`, and remote `main` synchronize.
16. Finish each repository checkpoint with a clean worktree.

---

## 12. Immediate Next Gate

Current scientific state:

- **M0-M5:** COMPLETE.
- **Post-M5 alignment audit:** COMPLETE.
- **Secondary Planning:** APPROVED and validated.
- **Random microstructures:** NOT YET IMPLEMENTED.
- **Circular void defects:** NOT YET IMPLEMENTED.
- **Final defect-sensitive stochastic dataset:** NOT YET GENERATED.
- **Final research ML:** NOT READY TO START.
- **M6:** NOT STARTED.

Before M6 starts:

1. Validate this `PROJECT_STATUS.md`.
2. Validate the final documentation file set.
3. Stage only the intended documentation files.
4. Commit them.
5. Push to GitHub.
6. Verify repository synchronization and cleanliness.
7. Obtain explicit user confirmation to enter M6.

Only after that gate is passed should the project begin:

> **M6 — Multiple/Random-Particle Microstructure Foundation**
