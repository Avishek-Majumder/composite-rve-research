# M9 — Final Parameter-Space and Stochastic-Pilot Design Record

**Project:** Composite-RVE Research

**Working title:** *An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.*

**Research route:** Simulation + Machine Learning only; no laboratory experiments.

**Milestone:** M9 — Final Parameter-Space Lock and Stochastic Pilot Dataset

**Record initiated:** 19 August 2026

**Current M9 state:** IN PROGRESS

**Closed M9 design gates at this checkpoint:** Steps 1, 2, 3A, and 3B

**Next scientific gate:** Step 4 — Final Parameter-Range Lock

**Stochastic M9 pilot:** NOT AUTHORIZED

**M10 production database:** NOT AUTHORIZED

**Machine-learning training:** NOT AUTHORIZED

---

## 1. Purpose and document authority

This document is the permanent design and decision record for M9.

It was created only after:

1. permanent M0-M8 scientific closure;
2. M8 compatibility-environment reproducibility freeze;
3. the post-M8 independent audit;
4. the M0-M8 evidence manifest;
5. authenticated read-only transition into M9.

The historical roadmap in:

`docs/Secondary_Planning.docx`

remains preserved and must not be silently rewritten as though later
project-specific decisions had always existed.

This M9 document records the decisions actually made during M9.

`PROJECT_STATUS.md` remains the concise repository-wide current-status
authority and must be updated separately after this M9 record is audited.

---

## 2. Non-reopen rule inherited from M0-M8

M0-M8 are permanently closed under their authenticated authorities.

They must not be reopened merely for reassurance.

A completed M0-M8 decision may be reopened only if genuinely new evidence
establishes a real:

- scientific contradiction;
- invalidated result;
- provenance break;
- reproducibility defect.

A brittle checker, parser, literal-count test, string matcher, AST assumption,
or other harness failure by itself is not sufficient justification for
changing authenticated science.

Checker/harness defects must be distinguished from scientific/source defects
before corrective action.

---

## 3. M9 Step 1 — Read-only handoff authentication

### Status

**PASS / CLOSED**

The M9 transition began by authenticating the final repository state without
modifying source, documentation, environment, or scientific results.

Authenticated authority:

- repository:
  `/home/avishek/projects/composite-rve-research`
- branch:
  `main`
- HEAD:
  `6a26811750d00e71e56206dcf19e07915cfbf20d`
- `origin/main`:
  `6a26811750d00e71e56206dcf19e07915cfbf20d`
- public GitHub `main`:
  `6a26811750d00e71e56206dcf19e07915cfbf20d`
- HEAD tree:
  `683306e7452e318ff3ad2f32b02168ea38826961`
- HEAD parent:
  `d26baa0099d027c7862a5d19d614577a0e18dfed`
- divergence:
  `0 / 0`
- repository/index/worktree:
  clean
- tracked-file count:
  `74`
- Git-history count:
  `80`

Final M0-M8 evidence manifest:

- file:
  `M0_M8_EVIDENCE_MANIFEST.md`
- SHA-256:
  `9d25bbb887caa67ff97628b401f6a12114fe9dc4b767f3e408cda50293e49276`
- Git blob:
  `1b5d8b86ef4c1d4f9101e6e189be738daabd1d09`

No corrective M0-M8 commit, rerun, or repository repair was required.

---

## 4. M9 Step 2 — Current literature and novelty refresh

### Status

**PASS / CLOSED WITH NOVELTY REFINEMENT**

The current-literature refresh established that the publication must not claim
novelty merely from combining:

> RVE + PBC + FEM + ML + active learning

because recent literature already contains closely overlapping combinations of
those ingredients.

The project must also not claim novelty merely because:

- voids or defects occur in an RVE-to-ML workflow;
- particle- or reinforcement-based composites are studied using ML;
- FEM-generated composite data are used to train a surrogate.

### 4.1 Important close literature

A relevant example is:

H. Al-Hadidi, I. H. Abuzayed, C. Zhang, and J. L. Curiel-Sosa,
“Micromechanical modelling and machine learning approaches for predicting
effective properties of composite materials,”
*Composite Structures*, 375, 119767, 2026.

DOI:

`10.1016/j.compstruct.2025.119767`

Another relevant example is:

M. Karimian and S. A. Hosseini Kordkheili,
“Application of deep residual networks to predict the effective properties
of fiber-reinforced composites with voids,”
*Advances in Mechanical Engineering*, 17(1), 2025.

DOI:

`10.1177/16878132251315871`

These references establish important overlap in RVE/FEM/ML and
void-containing composite-surrogate research.

They do not invalidate this project.

They narrow the defensible contribution.

### 4.2 Intended defensible novelty boundary

The intended differentiation is the integrated, rigorously controlled
workflow combining:

- stochastic defect-sensitive micromechanics;
- explicit circular true matrix holes/voids;
- global homogenized elastic responses;
- a separately validated local defect-sensitive stress-tail response;
- RVE representativity before production-database generation;
- authenticated production-mesh verification;
- authenticated local-response verification;
- targeted transfer-validation across difficult/extreme final-domain cases;
- deterministic design IDs, realization IDs, seeds, and provenance;
- non-overwrite of stochastic realization evidence;
- grouped/leakage-safe later ML validation;
- explicit separation of microstructure-realization variability from
  surrogate/model uncertainty;
- uncertainty and OOD evaluation;
- matched-FEM-budget active-learning versus random-sampling comparison.

This is the intended integrated contribution.

The individual ingredients are not claimed to be first-ever contributions.

No “first-ever” claim is authorized unless a later sufficiently exhaustive
literature review supports that wording.

### 4.3 Literature-supported versus project-specific decisions

Literature can support broad decisions such as the relevance of:

- stochastic microstructure;
- particle/reinforcement fraction;
- void content and morphology;
- RVE/PBC homogenization;
- FEM-generated surrogate data;
- uncertainty-aware sampling.

Literature does not automatically authorize this project's exact:

- `Ep/Em` range;
- Poisson-ratio ranges;
- particle-area-fraction range;
- void-area-fraction range;
- void-count set;
- void-radius values;
- spacing constraints;
- severity bounds;
- seed allocation;
- pilot size;
- rejection thresholds;
- transfer-validation cases.

Those remain project-specific M9 decisions.

---

## 5. Permanent M8 scientific authority entering M9

M9 inherits the following M8 authorities without reopening them:

- accepted representative RVE:
  `R1`
- R1 side length:
  `1.0`
- gross area:
  `1.0`
- physical particle count:
  `16`
- accepted production target mesh:
  `h = 0.02048`
- numerical fine-reference mesh:
  `h = 0.010`
- production quadrature degree:
  `8`
- selected M8 local metric:
  `m8_matrix_vm_annulus_quadrature_tail10_v1`
- protected M7 metric:
  `m7_matrix_vm_annulus_tail10_v1`

`h = 0.010` is a numerical fine reference.

It is not claimed to be exact continuum truth.

The publication scope remains restricted to a class of:

- two-dimensional systems;
- isotropic materials;
- small-strain linear elasticity;
- plane stress;
- perfectly bonded particle-reinforced composites;
- circular particles;
- circular true matrix voids where applicable.

The project does not claim that the framework “works for all materials.”

There is no experimental validation.

---

## 6. M9 Step 3A — Final model-output definitions

### Status

**PASS / CONCEPTUALLY LOCKED**

No numerical parameter ranges are implied by this output lock.

### 6.1 Canonical global FEM response

For every successful production realization, retain the complete actually
recovered normalized in-plane homogenized stiffness response:

`Cbar / E_matrix`

Store:

- `C11_over_Em`
- `C12_over_Em`
- `C16_over_Em`
- `C21_over_Em`
- `C22_over_Em`
- `C26_over_Em`
- `C61_over_Em`
- `C62_over_Em`
- `C66_over_Em`

Do not silently:

- force isotropy;
- force orthotropy;
- force `C16` to zero;
- force `C26` to zero;
- average `C12` with `C21`;
- average `C16` with `C61`;
- average `C26` with `C62`.

The recovered matrix is retained as the canonical FEM result.

Numerical reciprocity/symmetry discrepancies remain available as QC signals.

### 6.2 Derived global engineering responses

Also retain:

- `Ex_over_Em`
- `Ey_over_Em`
- `Gxy_over_Em`
- `nu_xy`
- `nu_yx`

These are derived engineering responses.

They do not replace the canonical recovered homogenized matrix.

### 6.3 Canonical local defect-sensitive response

The primary local response is the authenticated M8 metric:

`m8_matrix_vm_annulus_quadrature_tail10_v1`

under X periodic loading.

The primary normalized local scalar is:

`K_vm_tail10_X`

using the authenticated normalization by:

`abs_Sigma11_X`

and production quadrature degree:

`8`

The metric retains its authenticated M8 semantics, including:

- matrix material only;
- physical annulus around true voids;
- radius-scaled annulus definition;
- overlapping annulus contributions counted once;
- physical quadrature-point evaluation;
- physical-area quadrature weighting;
- upper 10% by physical area;
- gross-RVE macroscopic X-stress normalization.

### 6.4 Supporting local quantities

Retain sufficient supporting quantities to audit/reconstruct the normalized
local response, including:

- `sigma_vm_tail10_X`
- `abs_Sigma11_X`
- `K_vm_tail10_X`
- local metric identifier;
- quadrature degree;
- metric-definition/provenance identifier.

These supporting values are not automatically separate ML objectives.

### 6.5 No invented Y/XY local authority

M8 authenticated the selected local response under X loading.

M9 therefore does not silently invent:

- `K_vm_tail10_Y`
- `K_vm_tail10_XY`

and represent them as though they had already been validated by M8.

Any future extension would require an explicit new scientific definition and
validation decision.

### 6.6 Full-field scope

Full-field stress prediction is not part of the primary tabular ML target.

Full FEM fields may remain durable scientific evidence where appropriate.

The project is not being expanded into a full-field image/CNN/GNN surrogate
study during this M9 lock.

### 6.7 Pristine-case semantics

A pristine realization containing no true void has valid global responses.

For a pristine case:

`K_vm_tail10_X`

is undefined.

It must never be encoded as zero merely to populate a rectangular dataset.

Zero would falsely imply that a valid defect annulus exists and has exactly
zero normalized stress-tail response.

---

## 7. M9 Step 3B — Final model-input definitions

### Status

**PASS / CONCEPTUALLY LOCKED**

No numerical ranges for these variables are locked yet.

### 7.1 Core physical design vector

The principal in-domain physical design vector is:

`X = [Ep_over_Em, nu_matrix, nu_particle, particle_area_fraction_requested, void_area_fraction_requested, void_count]`

The six core baseline physical inputs are:

1. `Ep_over_Em`
2. `nu_matrix`
3. `nu_particle`
4. `particle_area_fraction_requested`
5. `void_area_fraction_requested`
6. `void_count`

### 7.2 Normalized material input

`Ep_over_Em`

represents particle-to-matrix stiffness contrast.

The arbitrary absolute reference value of `E_matrix` is not used as an
ordinary ML predictor in the normalized framework.

Permitted material anchors and exact material-property ranges remain subject
to M9 Steps 4 and 5.

### 7.3 Requested particle area fraction

For this 2D model, use:

`particle_area_fraction_requested`

or equivalent terminology such as 2D particle fraction.

Do not silently call this a measured 3D particle volume fraction.

### 7.4 Requested void area fraction

The primary void-content design variable is:

`void_area_fraction_requested`

representing true matrix holes in the 2D gross RVE.

### 7.5 Void count

`void_count`

is retained separately because total defect fraction alone does not uniquely
specify defect multiplicity or characteristic individual void size.

For equal-radius circular voids, void fraction and count together determine
the nominal radius.

---

## 8. Fixed principal in-domain quantities

For the principal M9/M10 in-domain study, the following remain fixed and are
not ordinary baseline ML predictors:

- RVE side length:
  `L = 1`
- gross area:
  `1`
- physical particle count:
  `16`
- 2D representation;
- plane stress;
- small-strain linear elasticity;
- isotropic matrix;
- isotropic particle phase;
- circular particles;
- perfectly bonded matrix-particle interfaces;
- production target mesh:
  `h = 0.02048`
- production quadrature degree:
  `8`

A constant column is not promoted into an ordinary model feature merely
because it exists in metadata.

---

## 9. Derived particle geometry

The principal in-domain particle population is monodisperse within a
realization.

With:

`N_p = 16`

and:

`L = 1`

particle radius is derived from the requested particle area fraction:

`r_p = sqrt(phi_p_requested / (16*pi))`

before geometry-feasibility checks.

Therefore:

`particle_radius_over_L`

is a derived geometry quantity, not an independently sampled seventh physical
input.

Particle count, radius, and particle fraction must not all be independently
sampled when two determine the third.

---

## 10. Derived void geometry

For equal-radius circular true voids with:

`void_count > 0`

the nominal void radius is derived from:

`r_v = sqrt(phi_v_requested / (void_count*pi))`

before geometry-feasibility checks.

Therefore:

`void_radius_over_L`

is a derived geometry quantity rather than an independently sampled core
input when requested void fraction and void count already determine it.

The final admissible void-count set and final void-fraction interval remain
open for M9 Step 4.

---

## 11. Stochastic-realization semantics

Random seeds are provenance.

They are not physics.

Retain, at minimum:

- physical design-point ID;
- realization ID;
- particle RNG seed;
- void RNG seed;
- geometry identity/hash;
- geometry-generator/version provenance.

Do not use raw seed integers as ordinary ML predictors.

Multiple stochastic realizations may share one physical input vector.

For a fixed design state `X_i`, realizations:

`R_i1, R_i2, R_i3, ...`

sample response variability conditional on that same physical state.

Conceptually, the repeated realizations sample:

`Y | X_i`

rather than defining unrelated material/design conditions.

This repeated-realization structure is required later to help distinguish:

- microstructure-realization variability;
- surrogate/model uncertainty.

Related realizations must remain grouped during later leakage-safe
train/validation/test procedures.

---

## 12. Geometry coordinates and baseline ML scope

Store physical geometry information such as:

- particle centers;
- particle radii;
- void centers;
- void radii;
- periodic/wrapped identities;
- geometry hashes.

However, raw coordinates are not ordinary baseline tabular ML predictors.

Using the complete coordinates, images, voxelizations, graphs, or equivalent
realization-specific encodings would change the research question into a
geometry-to-property learning problem.

That is outside the principal baseline-surrogate scope.

---

## 13. Requested-versus-realized fractions

Requested and realized quantities must remain distinct.

For particles retain, where available:

- `particle_area_fraction_requested`;
- analytical/constructed particle fraction;
- meshed particle fraction;
- discrepancy/QC fields.

For voids retain, where available:

- `void_area_fraction_requested`;
- analytical/constructed void fraction;
- meshed void fraction;
- discrepancy/QC fields.

The requested physical fraction remains the baseline design input.

Realized and meshed values are primarily QC/provenance quantities.

A meshing artifact must not silently redefine the requested physical design
point.

---

## 14. Principal in-domain arrangement family

The principal M9/M10 in-domain particle ensemble is the periodized
random/uniform arrangement family.

Existing clustered-generation capability remains valid historical
implementation capability.

Clustered arrangements are not automatically mixed into the principal
in-domain training distribution.

They are reserved as a strong candidate for later deliberate
distribution-shift/OOD evaluation unless a later explicit M9 decision changes
their role.

This is a project-specific scope decision.

It is not presented as a universal literature requirement.

---

## 15. Principal particle-size policy

The principal in-domain M9/M10 study uses monodisperse particles at each
physical design state.

Existing variable-particle-radius implementation capability remains valid.

It is not automatically promoted into an additional primary M9 training
dimension.

Particle-size dispersion remains available as a possible later sensitivity or
OOD direction.

---

## 16. Geometry constraints versus physical predictors

Quantities such as:

- minimum particle-particle clearance;
- minimum particle-void clearance;
- minimum void-void clearance;
- periodic/boundary clearance rules;
- finite placement-attempt limits;
- minimum realized gap;
- geometry-generation attempt count

are geometry feasibility or QC quantities unless explicitly promoted into
scientific design variables.

Their exact numerical values and invalid-case rules remain open until M9
Step 6.

---

## 17. Data-role hierarchy

### 17.1 Baseline physical ML inputs

- `Ep_over_Em`
- `nu_matrix`
- `nu_particle`
- `particle_area_fraction_requested`
- `void_area_fraction_requested`
- `void_count`

### 17.2 Canonical global FEM output

Complete recovered normalized in-plane homogenized stiffness response:

- `C11_over_Em`
- `C12_over_Em`
- `C16_over_Em`
- `C21_over_Em`
- `C22_over_Em`
- `C26_over_Em`
- `C61_over_Em`
- `C62_over_Em`
- `C66_over_Em`

### 17.3 Derived global responses

- `Ex_over_Em`
- `Ey_over_Em`
- `Gxy_over_Em`
- `nu_xy`
- `nu_yx`

### 17.4 Primary local response

For valid defective cases:

- `K_vm_tail10_X`

### 17.5 Local supporting quantities

- `sigma_vm_tail10_X`
- `abs_Sigma11_X`
- metric-definition/provenance fields.

### 17.6 Geometry/provenance

Examples include:

- design-point ID;
- realization ID;
- particle seed;
- void seed;
- particle coordinates;
- void coordinates;
- derived radii;
- geometry hash;
- generator/version provenance.

### 17.7 QC/numerical metadata

Examples include:

- requested-versus-realized fraction discrepancies;
- clearance/gap diagnostics;
- geometry-generation status;
- rejection reason;
- solver convergence;
- mesh identifier;
- mesh size;
- quadrature degree;
- runtime/provenance fields.

---

## 18. Current non-authorizations

The following are not yet scientifically locked or authorized:

- exact `Ep_over_Em` interval;
- exact `nu_matrix` interval;
- exact `nu_particle` interval;
- exact particle-area-fraction interval;
- exact void-area-fraction interval;
- exact allowed void-count set;
- final geometry-spacing rules;
- final geometry rejection rules;
- deterministic case-ID specification;
- final random-seed allocation policy;
- exact repeated-realization count;
- pilot sampling strategy;
- pilot sample size;
- pilot raw-output schema;
- final pilot QC gates;
- transfer-validation case set;
- stochastic pilot execution;
- M10 production FEM generation;
- ML training.

Previously discussed planning ranges are not automatically authorized.

---

## 19. Remaining exact M9 sequence

M9 must continue in this order.

### Step 4 — Final parameter-range lock

Scientifically justify and freeze numerical ranges for the core design
variables.

### Step 5 — Material and normalization lock

Preserve the normalized framework and define permitted material anchors
without expanding claims beyond the restricted model class.

### Step 6 — Geometry, defect, and feasibility lock

Define final:

- admissible geometry;
- particle/void spacing;
- periodic rules;
- invalid-state definitions;
- rejection/failure states;
- feasibility criteria.

### Step 7 — Stochastic reproducibility policy

Lock:

- deterministic design-point IDs;
- deterministic realization IDs;
- seed derivation/allocation;
- repeated-realization policy;
- non-overwrite behavior;
- provenance requirements.

### Step 8 — Pilot design and QC lock

Define:

- sampling strategy;
- pilot size;
- success/failure classifications;
- raw-output schema;
- metadata;
- QC gates;
- stop conditions.

### Step 9 — Targeted transfer-validation

Deliberately test difficult/extreme final-domain conditions.

M8 production-mesh/local-response verification must not simply be assumed to
transfer over the complete future M9 domain.

### Step 10 — Pilot authorization

Only after Steps 4-9 pass may the stochastic M9 pilot begin.

Run the pilot under the established authenticated one-step-at-a-time protocol.

---

## 20. Machine-learning authorization boundary

M9 is not an ML-training milestone.

Machine-learning training remains unauthorized throughout M9.

The intended later roadmap is:

- M9:
  final parameter-space lock + stochastic pilot
- M10:
  main quality-controlled FEM database
- M11:
  baseline ML + grouped validation
- M12:
  active learning versus random sampling
- M13:
  uncertainty, variability, and OOD evaluation
- M14:
  final analysis, ablations, figures, reproducibility, and manuscript

ML training remains unauthorized until M10 and its FEM database
QC/provenance gates are formally closed.

---

## 21. Current checkpoint

At creation of this document:

- M0-M8:
  `100% COMPLETE / CLOSED`
- Pre-M9 prerequisite package:
  `100% COMPLETE`
- M9 Step 1:
  `PASS / CLOSED`
- M9 Step 2:
  `PASS / CLOSED`
- M9 Step 3A:
  `PASS / CONCEPTUALLY LOCKED`
- M9 Step 3B:
  `PASS / CONCEPTUALLY LOCKED`
- M9 Step 4:
  `NOT STARTED`
- approximate M9 milestone progress:
  `18%`

The percentage is an approximate milestone-progress indicator, not a
mathematically exact project-completion measure.

---

## 22. Documentation and provenance policy

This M9 record is intended to be Git-tracked.

Scientific raw output, solver logs, generated meshes, figures, and other
large/generated evidence remain governed by the existing Git-ignore and
provenance policies.

Hashes authenticate evidence but do not constitute backups.

The public GitHub repository must not be described as a complete historical
backup of Git-ignored raw scientific evidence.

External conversation-history documents must not be silently represented as
Git-tracked evidence unless they are actually added under an explicit
repository decision.

No stochastic realization may be overwritten or cherry-picked because its
response appears more desirable.
