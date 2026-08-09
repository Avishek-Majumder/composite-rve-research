# Composite RVE Research — Project Status

**Last verified milestone checkpoint:** 9 August 2026
**Research route:** Simulation + Machine Learning only
**Laboratory experiments:** None
**Current completed major milestone:** M6 — Multiple/Random-Particle Microstructure Foundation
**Next major milestone:** M7 — Circular Void Defects + Defect-Sensitive Response Definition
**M7 implementation status:** NOT STARTED
**Authoritative post-M5 roadmap:** `docs/Secondary_Planning.docx`

---

## 1. Research Direction

**Working research title**

> An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.

The project combines finite-element simulation, stochastic microstructure generation, surrogate modelling, active learning, uncertainty analysis, and out-of-distribution evaluation.

The original Project 01 planning remains the historical initial scope. The post-M5 **Secondary Planning** record is the authoritative corrected continuation roadmap.

`PROJECT_STATUS.md` is the concise current repository checkpoint and should be updated as milestone execution advances.

---

## 2. Milestone Status

| Milestone | Status        | Summary                                                                                |
| --------- | ------------- | -------------------------------------------------------------------------------------- |
| M0        | 100% COMPLETE | Software and development environment                                                   |
| M1        | 100% COMPLETE | FEM fundamentals and homogeneous validation                                            |
| M2        | 100% COMPLETE | First single-particle composite model                                                  |
| M3        | 100% COMPLETE | Mesh convergence and composite verification                                            |
| M4        | 100% COMPLETE | Parametric RVE and sampling foundation                                                 |
| M5        | 100% COMPLETE | Initial perfect-bonding FEM dataset generation                                         |
| M6        | 100% COMPLETE | Multiple/Random-Particle Microstructure Foundation                                     |
| M7        | NOT STARTED   | Circular Void Defects and Defect-Sensitive Response Definition                         |
| M8        | NOT STARTED   | RVE-Size Study, Homogenization BC/PBC Verification, and Final Target-Mesh Verification |
| M9        | NOT STARTED   | Final Parameter-Space Lock and Stochastic Pilot Dataset                                |
| M10       | NOT STARTED   | Main Quality-Controlled FEM Simulation Database                                        |
| M11       | NOT STARTED   | Baseline Machine-Learning Models and Grouped Validation                                |
| M12       | NOT STARTED   | Active Learning versus Random Sampling                                                 |
| M13       | NOT STARTED   | Uncertainty Calibration, Variability, and OOD Testing                                  |
| M14       | NOT STARTED   | Final Analysis, Ablations, Figures, and Manuscript                                     |

---

## 3. Post-M5 Alignment Decision

The project-plan alignment audit concluded that the work through M5 is scientifically valid and should be retained.

M4 and M5 are interpreted as **inserted parametric, automation, and baseline-data foundation milestones**. They do not replace the random-microstructure, defect, RVE/PBC, stochastic-dataset, active-learning, uncertainty, or OOD stages from the original research plan.

The corrected roadmap therefore continues sequentially through M6-M14.

M6 has now completed the multiple/random-particle foundation required before defect introduction.

The next scientific milestone is:

> **M7 — Circular Void Defects + Defect-Sensitive Response Definition**

M7 must not begin until the M6 closure documentation checkpoint has been validated, committed, pushed to GitHub, repository synchronization has been verified, and the user explicitly confirms the M7 transition.

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

D0-PB remains a deterministic baseline for FEM-pipeline verification, regression testing, surrogate-method development, and later comparison.

It is **not** the final defect-sensitive stochastic research dataset and must not be used to support final claims about void defects, stochastic microstructure variability, uncertainty calibration, OOD behaviour, or active-learning efficiency.

---

## 5. Physics and Terminology Guardrails Through M6

The following assumptions describe the validated mechanics used through the M6 foundation and must not be changed silently:

- Two-dimensional computational representation.
- Small-strain linear elasticity.
- Plane-stress formulation.
- Isotropic matrix material.
- Isotropic reinforcing-particle material.
- Perfect matrix-particle bonding through M6.
- No void defects introduced through M6.
- RVE width = `1.0`.
- RVE height = `1.0`.
- Matrix Young's modulus = `1000.0`.
- Matrix Poisson's ratio = `0.30`.
- Particle Young's modulus = `10000.0`.
- Particle Poisson's ratio = `0.25`.
- Prescribed x displacement = `0.01`.
- M5/M6 validation mesh size = `0.02048`.
- Effective axial modulus and effective Poisson response remain the primary validated global effective-property outputs.
- Local stress extrema remain diagnostic only and are not accepted as fully mesh-converged final ML targets.
- Final homogenization BC/PBC verification remains an M8 task.
- Final stochastic target-mesh verification remains an M8 task.

The centered particle at `(0.5, 0.5)` with radius `0.20` remains specifically the D0-PB centered-single-inclusion reference problem. It is not the M6 stochastic geometry assumption.

For this 2D computational model, use **particle area fraction** or **2D particle fraction**, not true three-dimensional particle volume fraction.

---

## 6. M6 Completion Summary

### M6 — Multiple/Random-Particle Microstructure Foundation

M6 established and validated a reproducible multi-particle geometry, meshing, and FEM-response foundation before defect introduction.

### 6.1 Permanent geometry generator

**File**

`src/14_generate_m6_random_microstructure.py`

**SHA-256**

`23b8f90579c7a574f73a461f252ed0e062186b05f8e344c2ec89d3af7454deb9`

**Validated capabilities**

- deterministic regeneration from stored integer random seeds;
- NumPy `PCG64` random-number-generator provenance;
- NumPy-version provenance;
- multiple circular particles;
- variable particle positions;
- variable particle radii;
- requested particle-count control;
- particle-overlap prevention;
- minimum particle-particle surface spacing;
- minimum particle-boundary surface spacing;
- explicit finite placement-attempt limits;
- machine-readable valid/invalid geometry status;
- machine-readable failure reasons;
- reproducible particle-level geometry metadata.

**Permanent arrangement families**

`random_uniform_rejection_v1`

`clustered_bounded_disk_rejection_v1`

The clustered implementation additionally records cluster centers, cluster count, cluster radius, minimum cluster-center distance, particle-cluster assignments, and clustered-placement metadata.

### 6.2 Permanent multi-particle mesher

**File**

`src/15_generate_m6_multi_particle_mesh.py`

**SHA-256**

`a2555d0b699b9ced157c5138bc9088726ca9ad7e52659f4ba2cb291b376842dc`

**Validated capabilities**

- Gmsh OCC construction of the rectangular RVE and circular particles;
- conformal matrix-particle fragmentation;
- matrix physical tag = `1`;
- particle physical tag = `2`;
- CAD particle-area verification;
- CAD particle-center verification;
- matrix-area verification;
- shared matrix-particle interface verification;
- outer-RVE-boundary verification;
- DOLFINx mesh conversion;
- complete material cell-tag transfer;
- analytical-versus-meshed particle-area-fraction diagnostics;
- explicit rejection of invalid geometry metadata.

### 6.3 Permanent multi-particle elasticity solver

**File**

`src/16_solve_m6_multi_particle_elasticity.py`

**SHA-256**

`c2f17962f9aa62cb9648ef797afc30317929410fd34a8e0651f8f2763b08c108`

**Permanent result schema**

`m6_multi_particle_elasticity_v1`

**Validated capabilities**

- consumes valid M6 geometry metadata;
- uses the permanent conformal M6 mesher;
- preserves the validated M5 mechanics;
- material-tagged matrix and particle integration;
- established left-edge x restraint;
- established right-edge prescribed x displacement;
- established bottom-left y restraint;
- PETSc linear solve with explicit convergence checking;
- deterministic repeated FEM response generation in the validated environment;
- global average strain and stress calculation;
- effective axial modulus;
- effective Poisson response;
- material-area and mesh checks;
- invalid geometry rejection before FEM solution;
- source-relative loading of the companion M6 mesher.

Circular void defects are explicitly outside this solver's M6 scope and belong to M7.

---

## 7. M6 Validation Evidence

M6 was not accepted based on a single successful geometry.

The following validation gates were completed:

### STEP 507 — geometry validity and failure handling

- independent particle-spacing recomputation passed;
- independent boundary-spacing recomputation passed;
- particle-area and area-fraction recomputation passed;
- different seeds produced distinct geometries;
- intentionally overdense geometry returned explicit invalid status and exit code `2`.

### STEP 511 — mesh-geometry refinement sanity

For the same six-particle geometry:

- `h = 0.04000`: particle-fraction error `0.0045166289607189575`;
- `h = 0.02048`: particle-fraction error `0.0012691520444568644`;
- `h = 0.01000`: particle-fraction error `0.000304048028974116`.

Particle-area representation error decreased monotonically with mesh refinement while total RVE area remained preserved.

This was an M6 geometry/meshing sanity check, not the final M8 stochastic target-mesh study.

### STEP 518 — limited geometry and mesh robustness sweep

- 12/12 geometries valid;
- 12/12 deterministic geometry regenerations passed;
- 12/12 DOLFINx meshes valid;
- 12/12 complete cell-tagging checks passed;
- 12/12 interface-count checks passed;
- random and clustered arrangements both covered;
- particle counts ranged from `4` to `14`;
- maximum particle-fraction mesh error was `0.002773712611909722`.

This was validation only and was not retained as a production dataset.

### STEP 521 — exact M5-to-M6 physics regression

The M6 meshing/solver route reproduced the centered M5 reference exactly for the validated comparison quantities:

- identical cell count;
- identical meshed particle fraction;
- identical global average strains;
- identical global average stresses;
- identical effective axial modulus;
- identical effective Poisson response;
- identical displacement ranges;
- positive PETSc convergence reason.

The centered reference effective modulus was:

`1184.4588076691466`

The centered reference effective Poisson response was:

`0.3014325439907935`

### STEP 522 — random and clustered multi-particle FEM preflight

A ten-particle random case and a ten-particle clustered case both:

- regenerated deterministically;
- meshed successfully;
- solved successfully;
- produced deterministic repeated FEM result records;
- preserved complete cell tagging;
- preserved the imposed global axial strain;
- produced finite positive effective-property outputs.

These cases were validation examples only; their response difference must not be interpreted as an isolated clustering effect because their particle area fractions were different.

### STEP 526 — post-commit FEM robustness gate

Six varied post-commit FEM cases passed:

- 3 random cases;
- 3 clustered cases;
- particle counts from `4` to `14`;
- 6/6 deterministic geometry regenerations;
- 6/6 deterministic FEM regenerations;
- 6/6 positive PETSc convergence reasons;
- 6/6 global response checks;
- invalid random geometry rejected;
- invalid clustered geometry rejected.

Observed validation-response ranges across these six cases were:

**Effective axial modulus**

`1052.3683246286728` to `1094.1993240871789`

**Effective Poisson response**

`0.29890259191278173` to `0.30088870151020575`

**Maximum absolute average transverse stress**

`1.8461989749474177e-13`

**Maximum particle-fraction mesh error**

`0.002773712611909722`

These six cases are robustness evidence only and are not the final research simulation database.

---

## 8. M6 Git Checkpoints

### Random microstructure generator

Commit:

`19f25d7954cd82e7ee3c6e6f99fc5aebce27e6f1`

Subject:

`Add reproducible M6 random microstructure generator`

### Multi-particle mesher

Commit:

`8fff8946e9762902f2fa86c232c4d7d8070b0c20`

Subject:

`Add validated M6 multi-particle mesher`

### Clustered microstructure generation

Commit:

`3904dcd617ab66caa3501166ff2a4ca7304af509`

Subject:

`Add clustered M6 microstructure generation`

### Multi-particle elasticity solver

Commit:

`8527aff55dec30d479c289be6d46567fb598b392`

Subject:

`Add validated M6 multi-particle elasticity solver`

Commit `8527aff55dec30d479c289be6d46567fb598b392` is the validated M6 implementation checkpoint immediately before this closure-status update.

The future documentation-closure commit hash is intentionally not hard-coded in this file before that commit exists.

---

## 9. M6 Scope Boundary

M6 completes the **multiple/random-particle foundation**, not the full research problem.

M6 did **not** introduce:

- circular void defects;
- defect-sensitive stress-concentration targets;
- periodic boundary conditions;
- a final homogenization BC/PBC selection;
- an RVE-size/statistical-representativity study;
- final stochastic target-mesh verification;
- final parameter-space locking;
- the stochastic pilot dataset;
- the production FEM database;
- machine-learning model training;
- active-learning experiments;
- uncertainty calibration;
- OOD experiments.

Those requirements remain assigned to later milestones in `docs/Secondary_Planning.docx`.

---

## 10. Remaining Scientific Roadmap Before Final ML Claims

The project still requires:

1. Circular void defects as the Version-1 defect model.
2. A robust defect-sensitive stress-concentration response.
3. RVE-size/statistical-representativity verification.
4. Final homogenization boundary-condition / PBC verification.
5. Final stochastic target-mesh verification.
6. Final stochastic parameter-space locking.
7. Geometry, mesh, solver, runtime, failure, and provenance recording.
8. A quality-controlled stochastic pilot dataset.
9. A quality-controlled main FEM simulation database.
10. Grouped/leakage-safe ML validation.
11. Active learning versus random sampling at equal FEM budgets.
12. Quantitative uncertainty calibration.
13. Separation of microstructure variability from model uncertainty.
14. Deliberate out-of-distribution testing.
15. Final ablations, figures, reproducibility evidence, and manuscript analysis.

The current M6 validation cases must not be silently promoted into the final stochastic research dataset.

---

## 11. M7 Goal

### M7 — Circular Void Defects + Defect-Sensitive Response Definition

M7 is the next planned scientific milestone.

Its purpose is to introduce and validate the Version-1 circular void-defect representation on top of the verified M6 multi-particle foundation.

M7 must include explicit scientific decisions and validation for the defect representation rather than silently altering the M6 geometry or physics assumptions.

M7 also must define and mesh-check a robust defect-sensitive stress-concentration response before that response can become a primary downstream ML target.

Raw local stress extrema remain diagnostic only unless later validation establishes an appropriate robust target.

M7 has **not started**.

---

## 12. ML and Active-Learning Guardrails

- D0-PB is not the final ML research dataset.
- M6 validation cases are not the final ML research dataset.
- Final surrogate claims wait until stochastic microstructures, defects, and the remaining verification milestones are completed.
- Related microstructure realizations must not leak across training and validation groups.
- Begin later ML work with conventional tabular surrogate baselines.
- Neural networks require evidence that their added complexity is justified.
- Active learning must be compared against random acquisition using equal FEM simulation budgets.
- Uncertainty must be quantitatively evaluated and calibrated.
- OOD testing must be explicit rather than inferred from ordinary random train/test splits.

---

## 13. Secondary Planning Documentation

**Formal planning document**

`docs/Secondary_Planning.docx`

**Validated DOCX SHA-256**

`b3373047b4413786f121c4d8818de647c439e00231e5d4fb46c5d60d6f58e46a`

**Reproducible generator**

`src/13_generate_secondary_planning.py`

**Validated generator SHA-256**

`90e3902807fde5bc353564e879c0aeb73c3f817f5711264f231ae8e4db385edf`

The Secondary Planning document remains unchanged at M6 closure because it is the authoritative roadmap and historical planning record.

Its statement that M6 had not started refers explicitly to the project state **at the time of that planning revision**. Current execution state is maintained in `PROJECT_STATUS.md`.

---

## 14. Earlier Stable Checkpoints

### M5 closure commit

`5914bf50108c042019303ece09552768faeeb977`

Subject:

`Add validated M5 initial FEM dataset`

### Documentation dependency commit

`05c5fc7e9d7315c6aaa48af78c9290319f1a0b6b`

Subject:

`Add document generation dependency`

### Post-M5 planning checkpoint

`300a9495783f9579c37dde72886a18ba47050f5a`

Subject:

`Add secondary planning and project status`

---

## 15. Working Rules

Research work follows these rules:

1. Work on one concrete step at a time.
2. Wait for the complete terminal output after every step.
3. Verify the result before continuing.
4. Fix failures before moving forward.
5. Do not silently modify established physics.
6. Announce every major milestone transition.
7. Summarize what has been completed before a new milestone.
8. State the next milestone objective and progress state.
9. Obtain explicit user confirmation before starting a new major milestone.
10. Inspect exact Git changes before staging.
11. Stage only intended paths.
12. Run staged safety checks.
13. Commit one meaningful validated work unit at a time.
14. Push validated commits to `origin/main`.
15. Verify local `HEAD`, `origin/main`, and direct remote `main` synchronize.
16. Finish each repository checkpoint with a clean worktree.

---

## 16. Immediate Next Gate

Current scientific state:

- **M0-M5:** 100% COMPLETE.
- **Post-M5 alignment audit:** COMPLETE.
- **Secondary Planning:** APPROVED and validated.
- **M6 implementation:** COMPLETE and validated.
- **M6 source-of-truth closure update:** prepared by this status revision.
- **Circular void defects:** NOT YET INTRODUCED.
- **M7 implementation:** NOT STARTED.
- **Final stochastic research dataset:** NOT YET GENERATED.
- **Final research ML:** NOT READY TO START.

The next repository gate is to validate this M6 closure-status update, stage only `PROJECT_STATUS.md`, commit it, push it to `origin/main`, verify local/remote synchronization, and finish with a clean working tree.

Only after that closure checkpoint is complete should M6 be formally closed in the guided workflow.

The next major milestone must then require explicit user confirmation before beginning:

> **M7 — Circular Void Defects + Defect-Sensitive Response Definition**

No M7 implementation should occur before that confirmation.
