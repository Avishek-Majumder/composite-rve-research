# Composite RVE Research — Project Status

**Last verified milestone checkpoint:** 19 August 2026
**Research route:** Simulation + Machine Learning only
**Laboratory experiments:** None
**Current completed major milestone:** M8 — RVE-Size Study, Homogenization BC/PBC Verification, and Final Target-Mesh Verification
**Current active major milestone:** M9 — Final Parameter-Space Lock and Stochastic Pilot Dataset
**M8 implementation status:** 100% COMPLETE
**M9 implementation status:** IN PROGRESS — Steps 1-3B complete; Step 4 next
**M9 design authority:** `docs/M9_PARAMETER_SPACE_AND_PILOT_DESIGN.md`
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
| M7        | 100% COMPLETE | Circular Void Defects and Defect-Sensitive Response Definition                         |
| M8        | 100% COMPLETE | RVE-Size Study, Homogenization BC/PBC Verification, and Final Target-Mesh Verification |
| M9        | IN PROGRESS   | Final Parameter-Space Lock and Stochastic Pilot Dataset — Steps 1-3B complete          |
| M10       | NOT STARTED   | Main Quality-Controlled FEM Simulation Database                                        |
| M11       | NOT STARTED   | Baseline Machine-Learning Models and Grouped Validation                                |
| M12       | NOT STARTED   | Active Learning versus Random Sampling                                                 |
| M13       | NOT STARTED   | Uncertainty Calibration, Variability, and OOD Testing                                  |
| M14       | NOT STARTED   | Final Analysis, Ablations, Figures, and Manuscript                                     |

---

## 3. Post-M5 Alignment Decision

The project-plan alignment audit concluded that the work through M5
is scientifically valid and should be retained.

M4 and M5 remain interpreted as inserted parametric, automation, and
baseline-data foundation milestones. They do not replace the later
random-microstructure, defect, RVE/PBC, stochastic-dataset,
active-learning, uncertainty, or OOD stages from the original
research plan.

The corrected roadmap therefore continues sequentially through
M6-M14.

M6 completed the multiple/random-particle microstructure foundation.
M7 completed the circular true-hole defect and defect-sensitive
response foundation.

M8 is now scientifically COMPLETE under its permanent protocols and
authenticated checkpoints. M8 closed the RVE-size/statistical-
representativity study, the periodized homogenization/PBC
verification programme, and the final target-mesh/local-response
verification.

The accepted representative RVE is R1, the accepted production
target mesh is `h = 0.02048`, and `h = 0.010` is retained as the
numerical fine-reference mesh.

The selected M8 local metric is
`m8_matrix_vm_annulus_quadrature_tail10_v1` at production
quadrature degree `8`.

The current scientific milestone is:

> **M9 — Final Parameter-Space Lock and Stochastic Pilot Dataset**

M9 is now IN PROGRESS after successful read-only authentication of the
final Pre-M9 repository authority.

The permanent current M9 design record is:

`docs/M9_PARAMETER_SPACE_AND_PILOT_DESIGN.md`

M9 Steps 1-3B are closed at their current scope:

- Step 1: repository handoff authentication PASS;
- Step 2: literature/novelty refresh PASS with a refined novelty boundary;
- Step 3A: final model-output architecture conceptually locked;
- Step 3B: final model-input architecture conceptually locked.

Exact numerical parameter ranges remain unlocked and belong to M9 Step 4.

No stochastic M9 pilot, M10 production database generation, or
machine-learning training is authorized at this checkpoint.

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

## 5. Physics and Terminology Guardrails Through M8

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
- M8 homogenization BC/PBC verification is COMPLETE under the permanent M8 authorities.
- M8 accepted production target mesh = `0.02048`; `h = 0.010` is retained only as the numerical fine-reference mesh.
- Selected M8 local metric = `m8_matrix_vm_annulus_quadrature_tail10_v1` with production quadrature degree `8`.

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

## 10. Remaining Scientific Roadmap After M8

M8 completes the locked RVE-size/statistical-representativity,
periodized homogenization/PBC verification, and final target-mesh/
local-response verification programme, but it does not complete the
full research programme.

The project still requires:

1. Final parameter-space locking and stochastic pilot design.
2. Continued geometry, mesh, solver, runtime, failure, and provenance recording.
3. A quality-controlled stochastic pilot dataset.
4. A quality-controlled main FEM simulation database.
5. Grouped/leakage-safe ML validation.
6. Active learning versus random sampling at equal FEM budgets.
7. Quantitative uncertainty calibration.
8. Separation of microstructure variability from model uncertainty.
9. Deliberate out-of-distribution testing.
10. Final ablations, figures, reproducibility evidence, and manuscript analysis.

The M5, M6, M7, and M8 validation/verification cases must not be
silently promoted into the final stochastic research dataset.

The protected M7 local-response identifier
`m7_matrix_vm_annulus_tail10_v1` remains unchanged as historical M7
authority.

M8 selected the distinct quadrature-based local metric
`m8_matrix_vm_annulus_quadrature_tail10_v1` for the locked M8
framework because it preserved the intended physical annulus/tail
semantics while showing lower authenticated mesh dependence.

That M8 selection did not by itself establish the final machine-
learning target or a production stochastic dataset. M9 Step 3A has
now adopted the authenticated X-load quadrature-tail metric as the
primary local defect-sensitive response `K_vm_tail10_X`, while the
production stochastic dataset remains ungenerated and unauthorized.

---

## 11. M7 Completion Summary

### M7 — Circular Void Defects + Defect-Sensitive Response Definition

M7 is scientifically complete and has passed the corrected final
closure-readiness audit.

M7 extends the validated M6 multi-particle foundation without
modifying the protected M6 implementation in place.

### 11.1 Permanent M7 design record

**File**

`docs/M7_V1_VOID_DESIGN.md`

**SHA-256**

`6bae86aa2302d2173ca235cc320af59dc326c4924143138ccadabdb6b014d814`

The design record defines:

- true circular matrix-phase geometric voids;
- strictly positive configured void-particle, void-void, and
  void-boundary spacing;
- independent void RNG provenance;
- gross-RVE area accounting;
- true-hole conformal meshing requirements;
- the permanent global-response identifier
  `m7_gross_rve_axial_v1`;
- the Version-1 defect-sensitive candidate
  `m7_matrix_vm_annulus_tail10_v1`;
- raw local stress maxima as diagnostic only;
- explicit M7/M8 scope ownership.

### 11.2 Permanent M7 void generator

**File**

`src/17_generate_m7_void_microstructure.py`

**SHA-256**

`3e24d3025f335a10ebbe3238807b4fc56d9b901296ea7fd4e52f994a1c6b587d`

**Schema**

`m7_void_microstructure_v1`

Validated capabilities include:

- deterministic circular-void generation from an independent integer
  void seed;
- preservation of the source M6 particle realization;
- matrix-phase void placement;
- requested void count and radius-range control;
- void-particle, void-void, and void-boundary spacing enforcement;
- zero-void regression support;
- explicit invalid-placement status and failure reason;
- geometry, area, gap, seed, NumPy, and source-file provenance.

### 11.3 Permanent M7 true-hole mesher

**File**

`src/18_generate_m7_void_mesh.py`

**SHA-256**

`8455b280f0505910fe66708f3ed4a98f5a9bb097a459ea53ba18e07259f9a258`

**Schema**

`m7_void_mesh_diagnostics_v1`

Validated capabilities include:

- OpenCASCADE true-hole circular void topology;
- matrix physical cell tag = `1`;
- particle physical cell tag = `2`;
- physical facet group `void_boundary`;
- CAD area and topology verification;
- DOLFINx cell-tag and void-boundary facet-tag transfer;
- explicit matrix, particle, void, and solid fraction checks;
- void-boundary length verification;
- valid zero-void behavior.

### 11.4 Permanent M7 elasticity and response solver

**File**

`src/19_solve_m7_void_elasticity.py`

**SHA-256**

`d9325a845be85ee4ca2e0bcfe73e699070e2a8a579d3e11b7e30beb3729118cf`

**Result schema**

`m7_void_elasticity_v2`

**Global-response identifier**

`m7_gross_rve_axial_v1`

**Local-response identifier**

`m7_matrix_vm_annulus_tail10_v1`

The solver preserves the validated small-strain, plane-stress,
isotropic matrix/particle, perfect matrix-particle bonding mechanics
while treating the void as a true geometric hole.

The M7 macroscopic axial stress is normalized by the gross RVE
reference area.

The local response uses matrix-cell von Mises stress in the
radius-scaled void-annulus union and an area-weighted upper 10% tail
mean normalized by the absolute gross-RVE macro axial stress.

Raw maximum local stress remains diagnostic only.

### 11.5 Key M7 validation evidence

M7 validation included:

- deterministic geometry regeneration;
- different-void-seed behavior;
- zero-void regression behavior;
- impossible-geometry failure handling;
- exact zero-void mechanics regression to the protected M6 solver;
- true-hole CAD topology verification;
- DOLFINx material/facet tag transfer;
- controlled void-severity comparisons at common radius scales
  `0.50`, `0.75`, `1.00`, and `1.10`;
- strictly decreasing apparent axial modulus across that controlled
  severity sequence;
- real solved-field evaluation of
  `m7_matrix_vm_annulus_tail10_v1`;
- response-specific comparison over `h = 0.038`,
  `h = 0.02048`, and `h = 0.010`;
- extreme-severity reference/fine checks;
- random-particle and clustered-particle end-to-end coverage.

For the fixed scale-1.00 validation geometry, the relative difference
in `K_vm_tail10` between `h = 0.02048` and the finest tested
`h = 0.010` mesh was:

`0.004930485547127743`

Across the additional tested extreme-severity reference/fine cases,
the largest observed `K_vm_tail10` relative difference was:

`0.035741662489806474`

No post-hoc pass/fail tolerance or Grid Convergence Index claim was
introduced from those limited validation cases.

The raw maximum von Mises stress showed materially larger mesh
sensitivity and remains diagnostic only.

### 11.6 Clustered-particle coverage

A validation-only clustered M6 geometry was augmented with M7 voids,
meshed, and solved end-to-end.

The final clustered M7 FEM validation produced:

- 8 particles;
- 2 circular voids;
- mesh size `0.02048`;
- apparent axial modulus `1061.5887895016347`;
- `K_vm_tail10 = 1.8343415779766636`;
- all permanent FEM verification checks passed.

This confirms implementation coverage of both M6 particle-arrangement
branches.

It does not establish a causal random-versus-clustered response
difference.

### 11.7 M7 Git implementation/evidence checkpoints

Permanent M7 checkpoints include:

- `77819bb2d93b1288b90c2f1acda5b2f90f12167a`
  — `Document M7 Version-1 void design`;
- `793831d2b59f2c5a95d414fdb03534ea0203deac`
  — `Add validated M7 void microstructure generator`;
- `6e21f74d80c4a8b98aa9eda8b96cb8e707435e89`
  — `Add validated M7 void-capable mesher`;
- `cea566960e7e4f1520ed6bd8215e57bb3cf7ca13`
  — `Add M7 gross-RVE elasticity response`;
- `dd2665912a6796d6dcb920d0dbbcc8e5aa0f4750`
  — `Lock M7 local stress validation metric`;
- `d2fbe187363dc4a6cfb228294fcd0e1f81fbdb3c`
  — `Add M7 defect-sensitive local response`;
- `598c112e067ca9d905bad9e8fd52078f16154d7a`
  — `Record M7 local response validation evidence`;
- `cd838537c49fa3cb0c819bc7a44302efb2db9195`
  — `Record clustered M7 validation coverage`;
- `564b5130040c88963116d5a498e27bf25a705029`
  — `Record M7 global response identifier`.

Commit `564b5130040c88963116d5a498e27bf25a705029`
is the final validated M7 implementation/evidence checkpoint
immediately before this closure-status update.

The future M7 documentation-closure commit hash is intentionally not
hard-coded before that commit exists.

### 11.8 M7/M8 boundary

M7 does not perform:

- final RVE-size/statistical-representativity verification;
- final homogenization BC/PBC selection;
- final production stochastic target-mesh verification;
- final parameter-space lock;
- stochastic pilot dataset generation;
- production FEM database generation;
- machine-learning training.

Those responsibilities remain in later milestones, beginning with M8.

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

The Secondary Planning document remains unchanged through M8 closure because it is the authoritative roadmap and historical planning record.

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

## 16. M8 Completion Summary

### M8 — RVE-Size Study, Homogenization BC/PBC Verification, and Final Target-Mesh Verification

M8 scientific execution and decision-making are COMPLETE.

**Permanent RVE representativity checkpoint**

`M8_RVE_REPRESENTATIVITY_CHECKPOINT.md`

**SHA-256**

`0f129f26c63dbf173572189d6c28ef43cf310920f2f5d1c5e1775ab8649fe420`

Authenticated RVE decision:

- accepted representative level: `R1`;
- accepted side length: `1.0`;
- accepted gross area: `1.0`;
- physical particle count: `16`;
- all R1-R5 statistical levels resolved under the locked protocol;
- R1 is the smallest eligible tested level satisfying every locked
  comparison against the larger resolved levels.

M8 also completed the required periodized PBC/homogenization
verification before the final target-mesh decision.

**Permanent final target-mesh checkpoint**

`M8_TARGET_MESH_CHECKPOINT.md`

**SHA-256**

`2cc4b55f15a5da2f9d6922de8032ad14b736e8768329ed90f22f4f08d9e1f5a8`

Authenticated final target-mesh/local-response decision:

- production target mesh: `h = 0.02048`;
- numerical fine reference: `h = 0.010`;
- selected M8 local metric:
  `m8_matrix_vm_annulus_quadrature_tail10_v1`;
- production quadrature degree: `8`;
- six pristine R1 global target-mesh comparisons: PASS;
- 24/24 durable Stage-8 FEM/PBC results authenticated;
- 12/12 selected-metric two-mesh defect cases represented;
- baseline cases: `6/6`;
- high-severity cases: `6/6`;
- selected-metric median `delta_K`: `0.48368166407152385%`;
- selected-metric maximum `delta_K`: `1.1265826061942061%`;
- median `<=3%` local acceptance criterion: PASS;
- no individual case `>5%`: PASS;
- no realization or severity was removed or response-selected;
- protected M7 metric identifier remains unchanged.

`h = 0.010` is a numerical comparison reference and is not claimed
to be an exact continuum solution.

The M8 conclusions apply only to the locked established computational
model class and do not claim universal applicability to arbitrary
materials, constitutive laws, geometries, dimensions, or physics.

M8 did not create the final stochastic research dataset and did not
perform machine learning.

---

## 17. Current M9 Gate

Current scientific state:

- **M0-M8:** scientific milestone work COMPLETE / CLOSED.
- **Pre-M9 prerequisites:** COMPLETE / CLOSED.
- **M9 Step 1:** read-only repository handoff authentication PASS / CLOSED.
- **M9 Step 2:** current literature/novelty refresh PASS / CLOSED with refined novelty boundary.
- **M9 Step 3A:** final model-output architecture PASS / conceptually locked.
- **M9 Step 3B:** final model-input architecture PASS / conceptually locked.
- **M9 Step 4:** NOT STARTED.
- **Final numerical M9 parameter ranges:** NOT YET LOCKED.
- **Stochastic M9 pilot:** NOT AUTHORIZED.
- **M10 production FEM database:** NOT AUTHORIZED.
- **Machine-learning training:** NOT AUTHORIZED.

Permanent M9 design authority:

`docs/M9_PARAMETER_SPACE_AND_PILOT_DESIGN.md`

The immediate next scientific gate is:

> **M9 Step 4 — Final Parameter-Range Lock**

The currently locked baseline physical input vector is:

`X = [Ep_over_Em, nu_matrix, nu_particle, particle_area_fraction_requested, void_area_fraction_requested, void_count]`

The currently locked response architecture retains:

- the complete recovered normalized in-plane homogenized stiffness response;
- `Ex_over_Em`;
- `Ey_over_Em`;
- `Gxy_over_Em`;
- `nu_xy`;
- `nu_yx`;
- authenticated X-load local response `K_vm_tail10_X` for valid defective cases.

No isotropy or orthotropy projection is authorized.

`C16` and `C26` must not be silently forced to zero.

For pristine cases, `K_vm_tail10_X` is undefined rather than zero.

Before parameter ranges are frozen, each numerical bound must be scientifically
justified for the restricted normalized 2D isotropic, small-strain,
linear-elastic, plane-stress particle/true-void model class.

Previously discussed planning ranges are not automatically authorized.

After Step 4, M9 must still complete:

1. material/normalization lock;
2. geometry/defect/feasibility lock;
3. stochastic reproducibility policy;
4. pilot-design and QC lock;
5. targeted transfer-validation across deliberately difficult/extreme
   production conditions;
6. formal pilot authorization.

The stochastic M9 pilot may begin only after all preceding M9 gates pass.

Machine-learning training remains unauthorized throughout M9 and remains
unauthorized until the M10 quality-controlled FEM database and its
QC/provenance gates are formally closed.

The public Git repository must not be represented as a complete historical
backup of Git-ignored raw scientific evidence.

Git-ignored scientific outputs, solver logs, meshes, figures, and other
generated evidence remain governed by the existing provenance and
non-overwrite policies.

No stochastic realization may be overwritten or cherry-picked because its
response appears more desirable.
