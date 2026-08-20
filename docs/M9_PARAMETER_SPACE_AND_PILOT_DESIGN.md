# M9 — Final Parameter-Space and Stochastic-Pilot Design Record

**Project:** Composite-RVE Research

**Working title:** *An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.*

**Research route:** Simulation + Machine Learning only; no laboratory experiments.

**Milestone:** M9 — Final Parameter-Space Lock and Stochastic Pilot Dataset

**Record initiated:** 19 August 2026

**Current M9 state:** IN PROGRESS

**Closed M9 design gates at this checkpoint:** Steps 1, 2, 3A, 3B, 4, 5, 6, and 7

**Next scientific gate:** Step 8 — Pilot Design and QC Lock

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

The numerical material-property domains are locked under M9 Step 4.
M9 Step 5 now locks the material-scale, normalization, and reference-anchor
policy recorded in Section 19.

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

The admissible pristine/defective void-fraction and void-count domain is
now locked under M9 Step 4 and recorded in Section 18.

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

## 18. M9 Step 4 — Final parameter-range lock

### Status

**PASS / CONCEPTUALLY LOCKED**

M9 Step 4 is complete at the scientific-design level.

All six core physical input domains are now numerically defined.

The ranges below are project-specific, literature-informed computational-domain
choices for the restricted normalized two-dimensional isotropic,
small-strain, linear-elastic, plane-stress particle/true-void framework.

They are not universal material limits.

### 18.1 Step 4A — Material-property ranges

The stiffness-contrast input is locked to:

`Ep_over_Em in [2, 30]`

The matrix Poisson-ratio input is locked to:

`nu_matrix in [0.25, 0.40]`

The particle Poisson-ratio input is locked to:

`nu_particle in [0.15, 0.30]`

The protected reference material state remains inside the locked domain:

- `Ep_over_Em = 10`
- `nu_matrix = 0.30`
- `nu_particle = 0.25`

The `Ep_over_Em` interval intentionally covers modest-to-strong stiff-particle
contrast while avoiding an unnecessary expansion into very-high-contrast
regimes before targeted transfer validation.

The Poisson-ratio intervals are conservative project-specific model-domain
choices. They are not claims that real constituent materials cannot exist
outside these ranges.

M9 transfer validation must deliberately include difficult material-edge and
corner conditions rather than assuming the M8 reference-material numerical
verification transfers automatically.

### 18.2 Step 4B — Particle area-fraction range

The requested particle content is locked to:

`particle_area_fraction_requested in [0.08, 0.20]`

This variable is a two-dimensional particle **area fraction**.

It must not be silently described as a measured three-dimensional particle
volume fraction.

For the fixed principal R1 configuration:

- `L = 1`
- `N_p = 16`

and monodisperse particles,

`r_p = sqrt(phi_p_requested / (16*pi))`.

The locked area-fraction bounds therefore correspond approximately to:

- at `phi_p = 0.08`:
  `r_p = 0.0398942`
- at `phi_p = 0.20`:
  `r_p = 0.0630783`

At production:

`h = 0.02048`

the corresponding particle diameters are approximately:

- `3.90*h` at the lower particle-fraction boundary;
- `6.16*h` at the upper particle-fraction boundary.

The protected M8 reference particle state:

- `r_p = 0.05`
- `phi_p approximately 0.1256637`

lies inside the locked M9 interval.

The 8% lower bound is intentionally more conservative than lower particle
fractions used in some published composite studies because this project fixes
16 physical particles in R1 and must preserve a numerically credible
particle-size regime at the accepted production mesh.

This does not by itself prove that M8 representativity or mesh verification
transfers to either 8% or 20%.

Those boundaries remain mandatory targeted transfer-validation conditions.

### 18.3 Step 4B — Void fraction and void-count domain

The void domain is piecewise rather than a naive rectangular Cartesian
product.

#### Pristine state

The only admissible pristine state is:

`void_area_fraction_requested = 0`

with:

`void_count = 0`

#### Defective states

For defective cases:

`void_area_fraction_requested in [0.0075, 0.03]`

and:

`void_count in {1, 2, 4}`

Therefore:

- positive void fraction with `void_count = 0` is invalid;
- `void_count > 0` with zero requested void fraction is invalid.

For equal-radius circular true holes,

`r_v = sqrt(phi_v_requested / (void_count*pi))`.

Representative boundary values are approximately:

- `phi_v = 0.0075`, `N_v = 1`:
  `r_v = 0.0488603`
- `phi_v = 0.0075`, `N_v = 2`:
  `r_v = 0.0345494`
- `phi_v = 0.0075`, `N_v = 4`:
  `r_v = 0.0244301`
- `phi_v = 0.03`, `N_v = 1`:
  `r_v = 0.0977205`
- `phi_v = 0.03`, `N_v = 2`:
  `r_v = 0.0690988`
- `phi_v = 0.03`, `N_v = 4`:
  `r_v = 0.0488603`

At the smallest locked void:

`phi_v = 0.0075`, `N_v = 4`

the hole diameter is approximately:

`2.39*h`

at production `h = 0.02048`.

This is intentionally close to the authenticated M8 baseline true-hole
diameter:

`2*r_v = 0.05`

which is approximately:

`2.44*h`.

The lower defective void-fraction bound also contains the authenticated M8
void states:

- baseline:
  `4*pi*(0.025)^2 approximately 0.00785398`
- high severity:
  `4*pi*(0.0275)^2 approximately 0.00950332`

The upper 3% defective bound is intentionally conservative relative to
published void/porosity parameter studies and avoids automatically expanding
the principal M9 domain to more severe porosity before transfer validation.

`void_count` remains a separate physical design input because total void
fraction alone does not uniquely define defect multiplicity or characteristic
individual void size.

### 18.4 Final six-input numerical domain

The locked principal M9 physical domain is:

- `Ep_over_Em in [2, 30]`
- `nu_matrix in [0.25, 0.40]`
- `nu_particle in [0.15, 0.30]`
- `particle_area_fraction_requested in [0.08, 0.20]`
- pristine void state:
  `(void_area_fraction_requested, void_count) = (0, 0)`
- defective void states:
  `void_area_fraction_requested in [0.0075, 0.03]`
  with
  `void_count in {1, 2, 4}`

The continuous-domain sampling density is not defined by this range lock.

### 18.5 Literature traceability for the Step-4 ranges

The Step-4 bounds are project-specific computational-domain choices.

The literature below provides context for plausibility and nearby published
parameter regimes. It does **not** directly authorize the exact M9 bounds,
because the cited studies differ from this project in dimensionality,
microstructure type, constitutive setting, or research objective.

1. Y. Liu, F. P. van der Meer, and L. J. Sluys,
   “A dispersive homogenization model for composites and its RVE existence,”
   *Computational Mechanics*, 65, 79–98, 2020.

   DOI:

   `10.1007/s00466-019-01753-9`

   Relevant contextual observations include material-contrast factors:

   `c in {2, 4, 9, 16, 30}`

   and a reported constituent example with approximately:

   - `E_inclusion = 74 GPa`
   - `E_matrix = 3.76 GPa`
   - `nu_inclusion = 0.20`
   - `nu_matrix = 0.30`

   This source supports the plausibility of the selected contrast and
   Poisson-ratio neighborhood only. Its dynamic homogenization, fiber,
   and plane-strain context is not treated as equivalent to the present
   2D plane-stress particle-RVE framework.

2. S. Zhu, S. Wu, Y. Fu, and S. Guo,
   “Prediction of particle-reinforced composite material properties based on
   an improved Halpin–Tsai model,”
   *AIP Advances*, 14, 045339, 2024.

   DOI:

   `10.1063/5.0206774`

   The study considers SiC particle volume fractions:

   `5%, 10%, 15%, 20%`

   and porosity values spanning:

   `0% to 5%`.

   This source provides particle-content and porosity context only.
   Its three-dimensional volume fractions must not be silently equated with
   this project's two-dimensional requested particle/void area fractions.

3. M. Karimian and S. A. Hosseini Kordkheili,
   “Application of deep residual networks to predict the effective properties
   of fiber-reinforced composites with voids,”
   *Advances in Mechanical Engineering*, 17(1), 2025.

   DOI:

   `10.1177/16878132251315871`

   The study uses random RVEs with periodic boundary conditions and FEM,
   with void volume fractions in the range:

   `0.00 to 0.03`.

   This provides direct literature context for choosing a conservative
   defective upper bound of 3%, but its fiber-composite volume-fraction
   domain is not treated as identical to this project's 2D particle-RVE
   area-fraction domain.

Accordingly, the final M9 Step-4 limits remain literature-informed but
project-specific. No cited literature range is copied mechanically into the
production domain.

### 18.6 Still open after Step 4

Step 4 does not lock:

- particle-particle clearance;
- particle-void clearance;
- void-void clearance;
- periodic/boundary-clearance rules;
- geometry rejection/failure rules;
- deterministic case-ID specification;
- seed derivation/allocation;
- repeated-realization count;
- pilot sampling density/design;
- pilot sample size;
- pilot raw-output schema;
- final pilot QC gates;
- final transfer-validation case set.

Those responsibilities remain assigned to later M9 gates.

The stochastic M9 pilot remains unauthorized.

M10 production FEM generation remains unauthorized.

Machine-learning training remains unauthorized.

---

## 19. M9 Step 5 — Material and normalization lock

### Status

**PASS / CONCEPTUALLY LOCKED**

M9 Step 5 fixes how constituent elastic properties, geometry scale, and
mechanical responses are normalized and interpreted throughout the principal
M9/M10 computational database.

This step does not expand the constitutive model beyond the already locked
two-dimensional isotropic, small-strain, linear-elastic, plane-stress scope.

### 19.1 Fixed internal matrix-modulus scale

The internal solver reference modulus remains:

`E_matrix = 1000`

This is a computational reference scale.

It is:

- not an ordinary ML predictor;
- not independently sampled;
- not a claim that the matrix represents a specific named real material.

The physical stiffness design variable remains:

`Ep_over_Em`

and therefore:

`E_particle = Ep_over_Em * E_matrix`.

With the Step-4 locked contrast domain:

`Ep_over_Em in [2, 30]`

the corresponding internal solver particle modulus spans:

`E_particle in [2000, 30000]`.

Those internal dimensional-looking values are numerical realizations of the
dimensionless modulus contrast. The scientific input remains `Ep_over_Em`.

### 19.2 Common modulus-scale invariance

For the fixed geometry, fixed Poisson ratios, small-strain linear-elastic
constitutive law, and prescribed macroscopic-strain periodic cell problem,
consider multiplying both constituent stiffness tensors by the same positive
constant `alpha`.

Equivalently:

`E_matrix -> alpha * E_matrix`

and:

`E_particle -> alpha * E_particle`

while all Poisson ratios and geometry remain unchanged.

Because the linear cell problem uses the same common stiffness scale in the
equilibrium operator and imposed-macrostrain contribution, the periodic
displacement/fluctuation solution is unchanged by that common positive scale.

Local stresses, macroscopic stresses, and dimensional homogenized stiffness
then scale by `alpha`.

Therefore the principal normalized responses remain invariant to this common
modulus scale:

- `Cbar / E_matrix`
- `Ex_over_Em`
- `Ey_over_Em`
- `Gxy_over_Em`
- `nu_xy`
- `nu_yx`
- `K_vm_tail10_X`

where:

`K_vm_tail10_X = sigma_vm_tail10_X / abs_Sigma11_X`.

The numerator and denominator of `K_vm_tail10_X` scale by the same common
modulus factor.

This scale-invariance statement applies to the currently locked linear,
prescribed-strain/PBC framework. It must not be generalized automatically to
nonlinear constitutive laws, different loading control, damage, plasticity,
contact, or other physics outside the publication scope.

### 19.3 Numerical-scale policy

The project deliberately retains one stable internal modulus scale rather than
sampling arbitrary common absolute Young-modulus magnitudes.

This avoids introducing a scientifically redundant feature into the design
space and avoids unnecessary variation in numerical coefficient/residual
magnitude and in the behavior of absolute solver tolerances or finite-precision
scaling.

A common positive scalar multiple of the assembled linear stiffness operator
does not change its matrix condition number in exact arithmetic:

`kappa(alpha*A) = kappa(A)` for `alpha > 0`.

Therefore no conditioning improvement is claimed from choosing
`E_matrix = 1000`; the purpose of the fixed scale is normalization consistency
and numerical reproducibility.

The normalized material physics is represented by the modulus contrast and
the two independent Poisson ratios.

### 19.4 Poisson-ratio policy

The material inputs:

- `nu_matrix`
- `nu_particle`

remain separate dimensionless physical inputs.

They are not replaced by:

- a Poisson-ratio ratio;
- a common Poisson ratio;
- an isotropic projection of the effective response.

Their Step-4 ranges remain:

- `nu_matrix in [0.25, 0.40]`
- `nu_particle in [0.15, 0.30]`.

### 19.5 Canonical global normalization

The canonical global FEM output remains the complete actually recovered:

`Cbar / E_matrix`.

Retain all nine normalized in-plane components:

- `C11_over_Em`
- `C12_over_Em`
- `C16_over_Em`
- `C21_over_Em`
- `C22_over_Em`
- `C26_over_Em`
- `C61_over_Em`
- `C62_over_Em`
- `C66_over_Em`

Derived global engineering responses remain:

- `Ex_over_Em`
- `Ey_over_Em`
- `Gxy_over_Em`
- `nu_xy`
- `nu_yx`.

Because `nu_xy` and `nu_yx` are already dimensionless, no further modulus
normalization is applied to them.

No isotropy or orthotropy projection is introduced.

`C16` and `C26` must not be silently forced to zero.

### 19.6 Canonical local normalization

The selected local defect-sensitive metric remains:

`m8_matrix_vm_annulus_quadrature_tail10_v1`

under X periodic loading.

The primary normalized local response remains:

`K_vm_tail10_X`

with:

`K_vm_tail10_X = sigma_vm_tail10_X / abs_Sigma11_X`.

Supporting quantities may retain the internal solver stress units for
provenance:

- `sigma_vm_tail10_X`
- `abs_Sigma11_X`.

The primary ML-facing local response remains the normalized dimensionless
ratio.

No Y/XY local metric is created by this Step-5 lock.

### 19.7 Length normalization

The principal RVE side length remains:

`L = 1`.

Coordinates, radii, clearances, and other geometric lengths are interpreted
relative to this RVE side length.

No additional absolute physical length scale is introduced into the principal
M9/M10 database.

This preserves the existing normalized geometric framework.

### 19.8 Permanent reference computational anchor

The permanent reference state remains:

- `E_matrix = 1000`
- `E_particle = 10000`
- `nu_matrix = 0.30`
- `nu_particle = 0.25`

equivalently:

- `Ep_over_Em = 10`
- `nu_matrix = 0.30`
- `nu_particle = 0.25`.

Its roles are limited to:

- continuity with authenticated M0-M8 work;
- regression/reference checks;
- interpretation of historical authenticated results;
- an interior reference point within the final M9 domain.

It is a **computational reference anchor**.

It must not be silently labeled as:

- epoxy/SiC;
- aluminum/ceramic;
- glass/polymer;
- or any other named real material system.

### 19.9 Named-material-anchor policy

No additional named real-material system is introduced as a separate
production anchor in the principal M9/M10 database.

A later publication may include a clearly labeled illustrative dimensional
mapping if useful.

Such a mapping must be described as illustrative only and must not be treated
as:

- experimental validation;
- a separate FEM training domain;
- evidence that the framework was validated for that named material;
- authorization to expand beyond the locked isotropic linear-elastic scope.

There remains no experimental validation.

The project does not claim that the framework works for all materials.

### 19.10 Formulation traceability

The Step-5 scaling argument follows directly from the linear periodic
homogenization formulation in which:

- microscopic stress satisfies a linear elasticity law;
- macroscopic stress is obtained by cell averaging;
- homogenized stiffness linearly maps imposed macroscopic strain to
  macroscopic stress.

An implementation-level reference formulation is:

“Periodic homogenization of linear elasticity,”
Computational Mechanics Numerical Tours with FEniCSx.

Reference page:

`https://bleyerj.github.io/comet-fenicsx/tours/homogenization/periodic_elasticity/periodic_elasticity.html`

This reference supports the linear periodic-homogenization formulation.
The common-modulus-scale invariance used here is the project-specific
algebraic consequence of applying a common positive stiffness scale to that
linear prescribed-strain cell problem.

### 19.11 Step-5 non-authorizations

Step 5 does not authorize:

- changing the constitutive model;
- introducing nonlinear material behavior;
- introducing named real-material production anchors;
- stochastic pilot execution;
- M10 production FEM generation;
- machine-learning training.

Exact geometry clearance, feasibility, and rejection rules remain assigned to
M9 Step 6.

### 19.12 Step-5 closure transition

M9 Step 5 remains closed at its authenticated scientific-design scope.

Its material-scale, normalization, and computational-reference authorities
remain unchanged and are inherited by Step 6.

---

## 20. M9 Step 6 — Geometry, defect, and feasibility lock

### Status

**PASS / CONCEPTUALLY LOCKED**

M9 Step 6 locks the principal production geometry, periodic topology,
pair-clearance policy, finite placement controls, deterministic invalid-case
behavior, and stage-aware case/failure taxonomy.

No stochastic M9 pilot is authorized by this lock.

### 20.1 Principal periodic topology

The principal M9/M10 geometry remains a two-dimensional periodic square cell:

`Omega = [0, L) x [0, L)`

with:

`L = 1`.

Opposite cell edges are identified periodically.

Particles and true voids may cross computational-cell boundaries.

Wrapped or translated representations belong to the same physical object and
must not be counted as additional particles or voids.

No artificial particle-to-external-boundary or void-to-external-boundary
minimum clearance is imposed in the principal periodized domain.

### 20.2 Toroidal pair-distance policy

Particle-particle, particle-void, and void-void checks use minimum-image
toroidal distance.

Physical pair surface gap is:

`g_ij = d_tor(i,j) - r_i - r_j`.

This rule applies both inside the primary cell and across opposite periodic
boundaries.

### 20.3 Final production pair-clearance lock

The common production minimum surface-gap policy is:

`g_pp = 0.020`

`g_pv = 0.020`

`g_vv = 0.020`

or equivalently:

`g_pp = g_pv = g_vv = 0.020`.

The value is a project-specific computational geometry choice.

It is not claimed to be a universal materials-science spacing constant.

At production:

`h = 0.02048`

so the nominal ratio is:

`0.020 / 0.02048 = 0.9765625`.

This is only a nominal geometry/mesh-scale comparison and is not a claim that
every ligament contains a fixed number of finite elements.

### 20.4 Step-6 feasibility evidence

The analytical screen compared common-gap candidates:

- `0.015`;
- `0.020`;
- `0.025`.

A subsequent deterministic geometry-only screen used:

`particle_area_fraction_requested = 0.20`

with 32 diagnostic particle realizations per gap and defective corners:

- `(0.03, 1)`;
- `(0.03, 2)`;
- `(0.03, 4)`;
- `(0.0075, 4)`,

where each pair denotes:

`(void_area_fraction_requested, void_count)`.

All three candidate gaps achieved `32/32` particle-placement success and
`32/32` success for each tested defective corner.

For the selected `0.020` gap:

- particle attempt median/max:
  `34 / 48`;
- high-void `N_v = 1` void attempt median/max:
  `15.5 / 134`;
- high-void `N_v = 2`:
  `8.5 / 38`;
- high-void `N_v = 4`:
  `16 / 41`;
- smallest-void `N_v = 4`:
  `8 / 15`.

These results are geometry-feasibility diagnostics only.

They do not establish:

- stochastic placement-success probability;
- FEM accuracy;
- production-mesh transfer;
- local-response transfer;
- pilot authorization.

### 20.5 Finite placement-attempt controls

The production placement controls are:

`max_attempts_per_particle = 20000`

and:

`max_attempts_per_void = 20000`.

These are algorithmic feasibility controls.

They are not physical ML predictors and must not be changed selectively to
rescue an inconvenient realization.

### 20.6 Deterministic geometry-failure policy

If an admissible requested realization cannot be generated under the locked
topology, gaps, seed, and attempt limits, it is recorded as invalid geometry.

The workflow must not:

- relax the gap;
- increase the attempt budget only for the failing realization;
- substitute a different seed;
- rerun repeatedly until a convenient geometry appears;
- select or reject a realization based on its mechanical response.

A design point inside the locked physical M9 domain must not be silently
removed merely because an auxiliary crowding heuristic predicts difficulty.

Actual deterministic geometry-generation outcome governs geometry validity
under the current policy.

### 20.7 Top-level case/failure taxonomy

The top-level realization classifications are:

1. `invalid_design_input`
2. `invalid_geometry`
3. `mesh_failure`
4. `fem_failure`
5. `response_failure`
6. `success`

`invalid_design_input` means the requested physical state violates the locked
M9 design-domain or deterministic input contract.

`invalid_geometry` means the requested physical state is admissible but
geometry construction or geometry validation fails under the locked Step-6
rules.

`mesh_failure` means valid geometry exists but CAD, mesh generation,
conversion, or required mesh verification fails.

`fem_failure` means a valid mesh reaches the FEM stage but solve execution,
PETSc convergence, or required solve-level validation fails.

`response_failure` means the FEM solve is otherwise valid but a required
response extraction or response-validity check fails, is absent, or yields
invalid/non-finite required output.

`success` means all required active pipeline stages and outputs pass.

### 20.8 `not_applicable` semantics

`not_applicable` is not a top-level realization failure.

It is a field/subresponse applicability state.

A pristine successful realization may have valid global homogenized outputs
while:

`local_response_status = not_applicable`

for:

`K_vm_tail10_X`.

The pristine local response must not be fabricated as zero.

### 20.9 Native stage diagnostics

The top-level classification must not erase native evidence.

Retain where applicable:

- failure stage/type/reason;
- design-point and realization identity;
- particle and void RNG seeds;
- geometry identity/hash;
- failing object identity;
- placement attempts;
- mesh/CAD diagnostics;
- subprocess return code;
- exception information;
- PETSc convergence reason;
- PETSc iteration count;
- response/postprocessing diagnostics.

Exact final pilot-record field names remain assigned to Step 8.

### 20.10 M8 implementation boundary

The authenticated M8 periodized geometry generators remain validated
implementation foundations.

They must not be silently relabeled as final M9 production sources while their
existing metadata still declares M8 validation scope.

Any future production adaptation requires explicit M9/M10 schema, version, and
provenance authority.

This Step-6 lock does not modify protected M6/M7/M8 source code.

### 20.11 Transfer-validation boundary

The geometry-only Step-6 evidence does not establish transfer of the M8
production-mesh or local-response verification across the complete final M9
domain.

Step 9 remains mandatory for deliberately difficult/extreme final-domain
conditions.

### 20.12 Step-6 non-authorizations

Step 6 does not authorize:

- stochastic M9 pilot execution;
- M10 production FEM generation;
- machine-learning training;
- silent source-scope relabeling;
- gap relaxation;
- seed substitution;
- response-based realization selection.

### 20.13 Step-6 closure transition

M9 Step 6 remains closed at its authenticated scientific-design scope.

Its periodic-geometry, clearance, feasibility, invalid-case, and failure/QC
authorities remain unchanged and are inherited by Step 7.

---

## 21. M9 Step 7 — Stochastic reproducibility policy

### Status

**PASS / CONCEPTUALLY LOCKED**

M9 Step 7 locks deterministic physical-design identity, stochastic-realization
identity, particle/void seed derivation, RNG stream separation, replay
provenance requirements, non-overwrite behavior, and retry semantics.

This step does not determine the final number of repeated realizations.

That quantity remains owned by M9 Step 8.

Step 7 does not authorize stochastic pilot execution.

### 21.1 Design-identity namespace

The permanent M9 design-identity namespace is:

`composite-rve-m9-design-v1`

A physical design identity is computed only after the six physical inputs pass
the already locked M9 design-domain validation.

The identity layer uses exactly:

1. `Ep_over_Em`
2. `nu_matrix`
3. `nu_particle`
4. `particle_area_fraction_requested`
5. `void_area_fraction_requested`
6. `void_count`

No random seed, realization index, mesh quantity, solver quantity, response,
or failure state enters the physical design identity.

### 21.2 Canonical design serialization

Canonical key order is fixed as:

`Ep_over_Em`

`nu_matrix`

`nu_particle`

`particle_area_fraction_requested`

`void_area_fraction_requested`

`void_count`.

Continuous values are serialized as canonical finite decimal text.

The canonicalization rules are:

- equivalent decimal spellings collapse to the same text;
- scientific notation is expanded to fixed decimal notation;
- unnecessary trailing fractional zeros are removed;
- a terminal decimal point is removed;
- all signed-zero spellings collapse to `0`;
- no hidden rounding or quantization is performed by the identity layer;
- non-finite values are invalid;
- `void_count` is serialized as exact non-negative base-10 integer text.

Mapping insertion order must not affect identity.

The exact canonical material is UTF-8 text with no terminal newline.

The permanent material template is:

`composite-rve-m9-design-v1|Ep_over_Em=<canonical>|nu_matrix=<canonical>|nu_particle=<canonical>|particle_area_fraction_requested=<canonical>|void_area_fraction_requested=<canonical>|void_count=<canonical>`

Any explicit sampling precision or design-value quantization policy remains
owned by Step 8 and must occur before identity construction if Step 8 later
authorizes such a policy.

### 21.3 Full design digest and compact human design ID

Define:

`design_sha256 = SHA256(UTF8(canonical_design_material))`.

The complete 256-bit digest is permanent identity authority and must be stored.

The compact human-readable design ID is:

`M9D-<first 32 hexadecimal characters of design_sha256>`.

The human ID therefore uses the first 128 digest bits for compact identity.

The full 256-bit digest remains authoritative.

If an already registered compact human ID is encountered with a different full
design digest, that condition is a hard identity-collision error.

The compact human ID must never silently override a full-digest mismatch.

### 21.4 Realization identity

Stochastic realization indices are positive integers beginning at:

`1`.

Their canonical text rendering is decimal, left-zero-padded to a minimum width
of six characters.

Examples are:

- `1 -> 000001`;
- `9 -> 000009`;
- `10 -> 000010`;
- `999999 -> 999999`;
- `1000000 -> 1000000`.

The width is therefore a minimum width, not a maximum realization index.

Define:

`realization_id = <design_id>-R<rendered_realization_index>`.

A bare realization integer is not globally sufficient identity.

Every realization is bound to its physical design identity.

Multiple stochastic realizations at one physical design point therefore share
one `design_id` and use distinct positive realization indices.

The exact number of repeated realizations per design point remains assigned to
Step 8.

### 21.5 Seed namespace and derivation

The permanent M9 stochastic seed namespace is:

`composite-rve-m9-stochastic-v1`.

The seed derivation uses the full design SHA-256 digest rather than the compact
human ID.

For the particle stream:

`particle_seed_material = composite-rve-m9-stochastic-v1|design_sha256=<full_design_sha256>|realization=<rendered_realization_index>|stream=particle`

For the void stream:

`void_seed_material = composite-rve-m9-stochastic-v1|design_sha256=<full_design_sha256>|realization=<rendered_realization_index>|stream=void`

For either applicable stream:

`seed_digest = SHA256(UTF8(seed_material))`.

The RNG seed is the unsigned big-endian integer represented by the:

`first 16 bytes of seed_digest`.

This is a fixed 16-byte / 128-bit encoding.

The mathematical integer's ordinary bit length may be smaller than 128 when
the leading digest bits contain zeros.

That does not change the fixed seed-encoding width.

### 21.6 Particle/void stream domain separation

Particle and void randomness are separate deterministic streams.

The stream labels are exactly:

- `particle`;
- `void`.

The different stream labels produce different seed material and prevent the
particle and void streams from being silently coupled through one undifferentiated
seed.

For a defective realization:

- `particle_seed` is applicable;
- `void_seed` is applicable.

For a pristine realization:

- `particle_seed` remains applicable;
- no void-placement RNG stream is invoked;
- `void_seed_status = not_applicable`.

A fabricated numerical void seed must not be introduced merely to fill a table
for a pristine realization.

Raw seed integers are provenance and grouping information.

They are not ordinary ML predictors.

### 21.7 RNG construction

The locked M9 stochastic bit generator is:

`PCG64`.

The explicit construction is:

`Generator(PCG64(seed))`.

The implementation must not silently switch to another bit generator or to an
implicit default RNG construction while retaining the same M9 stochastic
schema/version label.

A future deliberate RNG change requires a new explicit stochastic
schema/version boundary.

### 21.8 Exact reference contract anchor

For the reference defective physical design:

- `Ep_over_Em = 10`;
- `nu_matrix = 0.30`;
- `nu_particle = 0.25`;
- `particle_area_fraction_requested = 0.125`;
- `void_area_fraction_requested = 0.01`;
- `void_count = 4`;

the canonical material is:

`composite-rve-m9-design-v1|Ep_over_Em=10|nu_matrix=0.3|nu_particle=0.25|particle_area_fraction_requested=0.125|void_area_fraction_requested=0.01|void_count=4`

and the locked reconstruction anchor is:

`design_sha256 = 150158a3e9e759750a2bebf6672ff2c3261ad95fdb713284e2453e71160413af`

`design_id = M9D-150158a3e9e759750a2bebf6672ff2c3`

`realization_id = M9D-150158a3e9e759750a2bebf6672ff2c3-R000001`

`particle_seed = 302080590121509650221841365288740422347`

`void_seed = 195733326785063538836689677512802722269`.

These values are deterministic contract anchors.

They do not authorize this reference design as a production pilot sample by
themselves.

### 21.9 Replay semantics

A raw seed alone is not complete exact-geometry replay authority.

Exact replay depends on the combination of:

- physical design identity;
- realization identity;
- applicable stream seeds;
- explicit RNG bit generator;
- generator implementation/version;
- generator source;
- RNG call pattern;
- execution-environment provenance.

A source change can alter the seed-to-geometry mapping even if the numerical
seed itself remains unchanged.

Therefore exact replay claims must be tied to source and environment
provenance rather than to seed alone.

### 21.10 Permanent replay-provenance categories

For every production realization, retain the following replay/provenance
categories:

1. `design_id`
2. `design_sha256`
3. `canonical_design_material`
4. `realization_id`
5. `realization_index`
6. `particle_seed`
7. `void_seed_or_not_applicable`
8. `rng_bit_generator`
9. `python_version`
10. `numpy_version`
11. `numpy_build_config_sha256`
12. `execution_environment_manifest_sha256`
13. `platform_system`
14. `platform_release`
15. `platform_machine`
16. `generator_schema_or_version`
17. `particle_generator_source_sha256`
18. `void_generator_source_sha256_or_not_applicable`
19. `geometry_identity_sha256`

These are required provenance categories.

Step 8 retains ownership of their exact final raw-record field names and
storage layout.

### 21.11 Authenticated environment/build anchors entering Step 7

The authenticated Step-7 audit environment included:

- Python `3.12.13`;
- NumPy `2.5.1`;
- DOLFINx `0.11.0`;
- platform machine `x86_64`.

The authenticated NumPy build-configuration digest was:

`98ea46e4ce383b714ca105d6cf0a98caeec0a6d2e69ff26ccefd89fa467490a5`.

The authenticated explicit execution-environment manifest digest was:

`26ab62c42f5dbb3eb7fe36e3ed6237a0c78e292de4d094fc71be0d2c6a1a30b2`.

These hashes are audit anchors for the environment used during the Step-7
replay investigation.

They are not a claim that future execution must silently ignore a deliberate,
documented environment change.

Any such change must be recorded explicitly in execution provenance and must
not be hidden behind an unchanged realization identity.

### 21.12 Observed replay evidence

Under the same:

- physical design identity;
- realization identity;
- derived seeds;
- explicit `PCG64`;
- generator source bytes;
- NumPy version;
- RNG call pattern;

the Step-7 read-only replay audit reproduced identical particle and void
geometry diagnostics for the reference defective realization.

The particle geometry identity reproduced as:

`ed56c671f7cf0b2c3cd7899ac58befaf0bc6c5bd414f19a499da224f76c6c632`.

The read-only replay result supports the locked reproducibility contract.

It is not production stochastic data.

### 21.13 Non-overwrite policy

Successful durable evidence must never be overwritten.

Failed durable evidence must never be overwritten.

Before any skip or retry decision, existing durable evidence must first be
authenticated against its expected scientific identity and provenance.

If existing evidence has an identity mismatch, the workflow must hard-stop.

If existing evidence is unreadable or cannot be authenticated, the workflow
must hard-stop rather than overwrite it.

New durable scientific artifacts must use exclusive-create semantics or an
equivalent mechanism that fails if the destination already exists.

A check-then-overwrite workflow is not an acceptable substitute for durable
non-overwrite semantics.

### 21.14 Retry semantics

Blind rerun-until-success behavior is forbidden.

Seed substitution after failure is forbidden.

Response-based realization replacement or cherry-picking is forbidden.

An authorized retry is permitted only after a documented causal remediation
or a verified transient execution failure.

An authorized retry must preserve:

- `design_id`;
- full `design_sha256`;
- `realization_id`;
- `realization_index`;
- `particle_seed`;
- `void_seed` when applicable.

A retry is therefore another execution attempt for the same scientific
realization, not a new stochastic realization.

The new attempt must be append-only and must preserve the prior failed
evidence.

### 21.15 Attempt identity

Execution-attempt identity is distinct from realization identity.

A realization may therefore have:

- attempt 1: failed;
- attempt 2: successful after documented remediation;

while both attempts retain the identical scientific `realization_id` and RNG
seed assignment.

The attempt index itself is execution provenance.

It is not an ordinary ML predictor.

Step 8 retains ownership of exact attempt-record field names, raw directory
layout, and filename conventions.

### 21.16 Failure-class retry boundary

The normal Step-7 retry semantics are:

- `success`:
  authenticate and skip; do not rerun;
- `invalid_design_input`:
  do not execute the same invalid request;
- `invalid_geometry`:
  retain evidence; no blind retry; retry only after documented causal
  remediation while preserving realization identity;
- `mesh_failure`:
  retain evidence; retry only after documented causal remediation or verified
  transient execution failure;
- `fem_failure`:
  retain evidence; retry only after documented causal remediation or verified
  transient execution failure;
- `response_failure`:
  retain evidence; retry only after documented causal remediation or verified
  transient execution failure.

Retry authorization must never be based on whether the mechanical response
looks desirable.

### 21.17 Repeated-realization extensibility

Adding a later positive realization index at the same physical design point
does not change any already assigned earlier:

- realization ID;
- particle seed;
- void seed.

This makes the identity/seed schedule append-only with respect to realization
index.

Step 8 may choose the required repeated-realization count without changing the
identity of earlier indices.

### 21.18 Step-7 / Step-8 ownership boundary

Step 7 locks:

- design identity semantics;
- canonical serialization;
- full design digest authority;
- compact design ID semantics;
- realization identity semantics;
- seed derivation;
- particle/void stream domain separation;
- explicit `PCG64` use;
- replay-provenance categories;
- no-overwrite behavior;
- append-only retry semantics;
- repeated-realization identity semantics.

Step 8 retains:

- exact repeated-realization count;
- final sampling strategy;
- pilot sample size;
- any explicit design-value sampling precision or quantization policy;
- exact raw field names;
- raw directory layout;
- filename conventions;
- final pilot record schema;
- pilot QC thresholds;
- stop conditions.

### 21.19 Step-7 non-authorizations

Step 7 does not authorize:

- stochastic M9 pilot execution;
- M10 production FEM generation;
- machine-learning training;
- final Step-8 sample size;
- final repeated-realization count;
- final raw-output directory layout;
- final filename conventions;
- silent source changes;
- silent RNG changes;
- seed substitution;
- response-based realization replacement;
- overwrite of prior durable evidence.

### 21.20 Remaining exact M9 sequence

M9 Steps 1-7 are complete at their currently authorized scientific-design
scope.

The next gate is:

#### Step 8 — Pilot design and QC lock

Lock:

- final sampling strategy;
- pilot size;
- repeated-realization count;
- exact pilot success/failure record schema;
- raw-output schema;
- metadata;
- QC thresholds/gates;
- stop conditions.

#### Step 9 — Targeted transfer-validation

Deliberately test difficult/extreme final-domain conditions before pilot
authorization.

#### Step 10 — Pilot authorization

Only after Steps 4-9 pass may the stochastic M9 pilot begin.

---

## 22. Machine-learning authorization boundary

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

## 23. Current checkpoint

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
- M9 Step 4A:
  `PASS / LOCKED`
- M9 Step 4B:
  `PASS / LOCKED`
- M9 Step 4 overall:
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 5:
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 6:
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 7:
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 8:
  `NOT STARTED`
- approximate M9 milestone progress:
  `57%`

The percentage is an approximate milestone-progress indicator, not a
mathematically exact project-completion measure.

---

## 24. Documentation and provenance policy

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
