# M9 — Final Parameter-Space and Stochastic-Pilot Design Record

**Project:** Composite-RVE Research

**Working title:** *An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.*

**Research route:** Simulation + Machine Learning only; no laboratory experiments.

**Milestone:** M9 — Final Parameter-Space Lock and Stochastic Pilot Dataset

**Record initiated:** 19 August 2026

**Current M9 state:** IN PROGRESS

**Closed M9 design gates at this checkpoint:** Steps 1, 2, 3A, 3B, 4, 5, 6, 7, and 8

**Next scientific gate:** Step 9 — Targeted Transfer-Validation

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

M9 Steps 1-8 are complete at their currently authorized scientific-design
scope.

The next gate is:

#### Step 9 — Targeted transfer-validation

Deliberately test difficult/extreme final-domain conditions under the
now-locked Step-8 pilot/FEM/QC contract before any stochastic-pilot
authorization.

#### Step 10 — Pilot authorization

Only after Steps 4-9 pass, and after the Step-9 transfer-validation
evidence has no unresolved contract failure, may the stochastic M9 pilot
be formally authorized.

Step-8 closure by itself does not create production design points, consume
production sampling seeds, register design IDs, create stochastic
realizations, authorize a writer implementation, or authorize pilot
execution.

---

## 22. M9 Step 8 — Pilot Design and QC Lock

### 22.1 Status and scientific boundary

**PASS / CONCEPTUALLY COMPLETE**

M9 Step 8 permanently locks the stochastic-pilot design and quality-control
contract that was deliberately left open by Steps 6 and 7.

This lock fixes:

- final sampling architecture;
- exact pilot design-point count;
- exact repeated-realization count;
- production sampling RNG namespace and stream separation;
- no-quantization sampling-value policy;
- exact sampling-coordinate and scaling semantics;
- exact sliced-LHS construction and optimization contract;
- deterministic final design-row ordering;
- raw-output namespace, path ownership and filename conventions;
- immutable JSON byte serialization;
- success/failure record families and field sets;
- per-realization production hard gates;
- repeat-level statistical reporting;
- append-only attempt, retry and failure-adjudication semantics;
- crash-durable no-clobber publication semantics;
- pilot pause/stop conditions.

Step 8 does **not** authorize:

- creation of the production LHS;
- consumption of production sampling RNG streams;
- creation or registration of production design IDs;
- creation of stochastic realizations;
- production FEM execution;
- implementation or execution of the final production writer;
- M10 generation;
- machine-learning training.

The stochastic M9 pilot remains unauthorized until Step 10.

### 22.2 Final sampling architecture

The permanent Step-8 sampling architecture identifier is:

`hybrid_pristine_independent_4D_LHS__defective_distance_guarded_sliced_5D_LHS`

The deterministic stratum order is:

1. `pristine_N0`;
2. `defective_N1`;
3. `defective_N2`;
4. `defective_N4`.

The defective slice order is therefore:

`N1, N2, N4`.

The final count is:

- `n_per_stratum = 12`;
- four strata;
- `48` physical design points;
- `12` pristine physical designs;
- `36` defective physical designs.

Void count is categorical/slice identity rather than a continuously scaled
LHS coordinate. No categorical distance is invented.

### 22.3 Unit-coordinate semantics

For the pristine branch the exact unit-coordinate order is:

1. `Ep_over_Em`;
2. `nu_matrix`;
3. `nu_particle`;
4. `particle_area_fraction_requested`.

For every defective slice the exact unit-coordinate order is:

1. `Ep_over_Em`;
2. `nu_matrix`;
3. `nu_particle`;
4. `particle_area_fraction_requested`;
5. `void_area_fraction_requested`.

Thus the four common continuous coordinates retain identical ordering
between pristine and defective designs.

The pristine state fixes:

- `void_area_fraction_requested = 0`;
- `void_count = 0`.

The defective slices assign:

- `void_count = 1`;
- `void_count = 2`;
- `void_count = 4`;

respectively.

Unit values are mapped to the already locked physical ranges using:

`scipy.stats.qmc.scale(sample, l_bounds, u_bounds)`

with the affine rule:

`(upper_bound - lower_bound) * unit_coordinate + lower_bound`.

The bounds remain:

- `Ep_over_Em`: `[2, 30]`;
- `nu_matrix`: `[0.25, 0.40]`;
- `nu_particle`: `[0.15, 0.30]`;
- `particle_area_fraction_requested`: `[0.08, 0.20]`;
- defective `void_area_fraction_requested`: `[0.0075, 0.03]`.

The value-formation order is:

`sample unit coordinates -> scale -> validate locked domain -> Step-7 canonicalize -> hash`.

Sampling-value quantization is:

`NONE`.

Pre-identity rounding, decimal-grid snapping, readability rounding, or
other mutation of sampled physical values is forbidden.

### 22.4 Pristine LHS constructor

The pristine branch uses:

`scipy.stats.qmc.LatinHypercube`

with:

- `d = 4`;
- `strength = 1`;
- `scramble = True`;
- `optimization = None`;
- explicit `rng = Generator(PCG64(pristine_lhs_seed))`.

The generation call is:

`sampler.random(n=12)`.

No SciPy `random-cd` or Lloyd optimization is used.

The permanent pristine sampling call-pattern identifier is:

`scipy_lhs_d4_strength1_scramble_true_optimization_none_random_n12_v1`.

### 22.5 Exact defective sliced-LHS constructor

The permanent custom defective constructor identifier is:

`m9_defective_sliced_lhs_3x12x5_v1`.

Let:

- number of slices `S = 3`;
- rows per slice `n = 12`;
- continuous dimensions `d = 5`.

Construction uses an explicit:

`Generator(PCG64(defective_sliced_lhs_seed))`.

For each dimension `j = 0..4`, in ascending order:

1. For each coarse stratum `k = 0..11`, in ascending order:
   - call `rng.permutation(3)` exactly once, producing `p`;
   - call `rng.random(3)` exactly once, producing `jitter`;
   - for each slice `s = 0..2`, in ascending order, define the global
     36-stratum index:
     `g = 3*k + int(p[s])`;
   - assign the intermediate coordinate:
     `(g + float(jitter[s])) / 36`.

2. After all 12 coarse strata for that dimension have been populated,
   for each slice `s = 0..2`, in ascending order:
   - call `rng.permutation(12)` exactly once;
   - use that permutation to place the 12 intermediate coordinates into
     the stable sampler row slots `0..11` for that slice/dimension.

No other random call occurs in the sliced-LHS constructor.

This construction must preserve simultaneously:

- each defective slice as an exact 12-point five-dimensional LHS;
- the pooled 36 defective points as an exact 36-point five-dimensional
  LHS.

### 22.6 Distance-guarded defective optimizer

The permanent custom optimizer identifier is:

`m9_distance_guarded_within_slice_coordinate_swap_v1`.

It operates only on the defective sliced design.

It uses:

- explicit `Generator(PCG64(defective_swap_optimizer_seed))`;
- exactly `2000` sequential proposals;
- one within-slice, one-dimension coordinate swap per proposal.

For every proposal, random calls occur in exactly this order:

1. `s = int(rng.integers(0, 3))`;
2. `j = int(rng.integers(0, 5))`;
3. `a = int(rng.integers(0, 12))`;
4. `raw = int(rng.integers(0, 11))`;
5. `b = raw + (raw >= a)`.

Therefore `a` and `b` are always distinct.

The candidate swaps only:

`current[s, a, j] <-> current[s, b, j]`.

Row slots themselves never move.

The four guarded metrics are:

1. pooled five-dimensional centered discrepancy;
2. worst defective-slice five-dimensional centered discrepancy;
3. pooled five-dimensional minimum Euclidean pair distance;
4. worst defective-slice five-dimensional minimum Euclidean pair
   distance.

Centered discrepancy is evaluated with:

`scipy.stats.qmc.discrepancy(..., method="CD")`.

The floating comparison tolerance for values `a` and `b` is:

`64 * np.finfo(np.float64).eps * max(1.0, abs(a), abs(b))`.

Define tolerance-aware comparisons:

- non-worsening lower-is-better:
  `new <= old + tolerance`;
- non-worsening higher-is-better:
  `new + tolerance >= old`;
- strict lower-is-better improvement:
  `new < old - tolerance`.

A proposal is accepted only if all four hard guards hold:

- pooled CD does not worsen;
- worst-slice CD does not worsen;
- pooled minimum distance does not decrease;
- worst-slice minimum distance does not decrease;

**and** at least one discrepancy objective strictly improves:

- pooled CD strictly improves; or
- worst-slice CD strictly improves.

Proposals are applied sequentially. After an accepted swap, the accepted
candidate becomes the current state for the next proposal. A rejected
proposal leaves the current state unchanged.

No absolute centered-discrepancy threshold and no absolute minimum-distance
threshold is introduced.

### 22.7 Final row order and design-ID list order

The final deterministic row order is:

`pristine_N0 -> defective_N1 -> defective_N2 -> defective_N4`.

Within every stratum, row slots remain:

`sampler_row_index = 0..11`

in ascending order.

The optimizer swaps coordinate values while preserving row slots.

`pilot_plan.json` must list `design_ids` in exactly:

`stratum order -> sampler_row_index ascending`.

### 22.8 Production sampling RNG namespace and seeds

The permanent pilot sampling namespace is:

`composite-rve-m9-pilot-sampling-v1`.

This namespace is distinct from the Step-7 physical-realization namespace:

`composite-rve-m9-stochastic-v1`.

The sampling bit generator is:

`PCG64`.

Every sampling/optimizer stream uses:

`Generator(PCG64(seed))`.

The seed derivation rule is:

`SHA256(UTF8(seed_material))`

followed by interpreting the first 16 digest bytes as an unsigned
big-endian 128-bit integer.

The three permanent stream labels are:

1. `pristine_lhs`;
2. `defective_sliced_lhs`;
3. `defective_swap_optimizer`.

For `pristine_lhs`:

`seed_material = composite-rve-m9-pilot-sampling-v1|architecture=hybrid_pristine_independent_4D_LHS__defective_distance_guarded_sliced_5D_LHS|n_per_stratum=12|optimizer_proposals=2000|stream=pristine_lhs`

`seed_sha256 = 4aac34322ef2054cfe164694729687eca93eb1a9bff2d8300c2452db82436ba2`

`seed_uint128 = 99257005408988176079290369073919461356`

For `defective_sliced_lhs`:

`seed_material = composite-rve-m9-pilot-sampling-v1|architecture=hybrid_pristine_independent_4D_LHS__defective_distance_guarded_sliced_5D_LHS|n_per_stratum=12|optimizer_proposals=2000|stream=defective_sliced_lhs`

`seed_sha256 = 77f1d707634729957ea2f4598026937da4f79c1ec475a9abe0fa27d82c759798`

`seed_uint128 = 159433836344698851123241991176116933501`

For `defective_swap_optimizer`:

`seed_material = composite-rve-m9-pilot-sampling-v1|architecture=hybrid_pristine_independent_4D_LHS__defective_distance_guarded_sliced_5D_LHS|n_per_stratum=12|optimizer_proposals=2000|stream=defective_swap_optimizer`

`seed_sha256 = 0ee7cbc340ede6f11c19c2f23038f1f0affc1a6fa67d6550f5f56164044cfcdc`

`seed_uint128 = 19812745314046245613281732677175144944`

These production sampling seeds must not be replaced with the diagnostic
seeds used during the read-only Step-8 audits.

### 22.9 Sampling-design QC gates

The production sampling design must pass all of the following before any
design identity is registered:

- all pristine coordinates finite and inside the unit sampling domain;
- pristine design is an exact four-dimensional 12-point LHS;
- zero duplicate pristine design rows;
- all defective coordinates finite and inside the unit sampling domain;
- each defective slice is an exact five-dimensional 12-point LHS;
- pooled defective design is an exact five-dimensional 36-point LHS;
- zero duplicate defective design rows;
- optimized pooled centered discrepancy is not worse than raw sliced LHS;
- optimized worst-slice centered discrepancy is not worse than raw;
- optimized pooled minimum distance is not lower than raw;
- optimized worst-slice minimum distance is not lower than raw;
- the optimizer strictly improves at least one centered-discrepancy
  objective.

Allowed counts are:

- LHS violations: `0`;
- duplicate design rows: `0`;
- optimizer-contract failures: `0`.

The exact constructor/optimizer was challenged across 32 independent
diagnostic replicates before this lock. The structural LHS, duplicate,
finite-metric, and optimizer-contract failure counts were all zero.

The mixed pristine-plus-defective common-four-dimensional minimum-distance
comparison was better-or-equal to an independent reference in `21/32`
diagnostic replicates. That quantity is explicitly a diagnostic rather
than an optimizer hard guard and therefore does not create an additional
Step-8 acceptance threshold.

### 22.10 Repeated-realization contract

Every valid physical design point has exactly:

`8`

scheduled stochastic realization identities.

Their indices are:

`1, 2, 3, 4, 5, 6, 7, 8`.

The pilot therefore schedules:

`48 * 8 = 384`

stochastic realizations.

Repeated realizations at one design point are conditional samples of:

`Y | X_i`.

The Step-7 realization-ID and physical particle/void seed derivation
remains unchanged.

Later realization indices remain append-only and must not alter any
existing earlier realization identity or seed.

### 22.11 Repeat-level statistical reporting

For every response for which the statistic is semantically defined,
Step 8 requires reporting:

- sample mean;
- sample standard deviation with `ddof = 1`;
- sample coefficient of variation when the mean makes it well-defined;
- nominal two-sided 95% Student-t confidence interval on the mean.

Historical M8 variability was used only as planning evidence.

There is no Step-8 hard acceptance threshold on:

- stochastic confidence-interval width;
- coefficient of variation;
- realization failure rate.

No realization may be replaced because its response, CV, or confidence
interval is inconvenient.

### 22.12 Per-realization production hard-gate families

Every applicable realization must retain the reusable executable
production invariants selected during Step 8.

Required gate families are:

- authority and design identity;
- locked Step-6 geometry/feasibility;
- locked Step-7 seed identity;
- non-overwrite and retry provenance;
- physical geometry and area consistency;
- mesh and physical-tag integrity;
- periodic geometry and MPC integrity;
- PETSc convergence;
- gauge and periodic-field accuracy;
- algebraic residual;
- finite homogenized response;
- positive load-direction stiffness;
- Hill-Mandel energy consistency;
- defective local-response validity.

The principal retained numerical thresholds are:

- periodic geometry maximum error: `1e-10`;
- zero-gauge maximum absolute value: `1e-12`;
- periodic-field normalized maximum error: `1e-10`;
- constrained algebraic relative residual maximum: `1e-10`;
- Hill-Mandel relative mismatch maximum: `1e-5`;
- mesh area-fraction tolerance: `0.005`;
- area-closure absolute tolerance: `1e-10`;
- local-normalization absolute tolerance: `1e-12`;
- defective production quadrature degree: `8`;
- PETSc convergence reason: strictly `> 0`.

Required response validity includes:

- finite homogenized stresses;
- finite recovered stiffness values;
- positive requested load-direction stiffness;
- for defective cases, finite and non-negative `K_vm_tail10_X`.

The defective permanent local metric is:

`m8_matrix_vm_annulus_quadrature_tail10_v1`.

Its normalization is exactly:

`abs(Sigma_11)`

from the gross-RVE X-load response.

For pristine cases:

- global response remains required after successful FEM execution;
- local-response status is `not_applicable`;
- reason is `pristine_no_physical_voids`;
- `K_vm_tail10_X = null`;
- numerical zero substitution is forbidden.

### 22.13 Pilot and raw namespaces

The permanent pilot namespace is:

`composite-rve-m9-pilot-v1`.

The permanent raw root is:

`results/raw/05_m9_stochastic_pilot`.

The path hierarchy is:

```text
results/raw/05_m9_stochastic_pilot/
  sampling_provenance.json
  planning_failures/
    failure_<minimum-six-digit-index>.json
  pilot_plan.json
  designs/
    <design_id>/
      design.json
      realizations/
        <realization_id>/
          realization.json
          failure_adjudication.json   # only when terminally adjudicated
          attempt_diagnoses/
            attempt_<minimum-six-digit-index>.json
          retry_authorizations/
            attempt_<minimum-six-digit-index>.json
          attempts/
            attempt_<minimum-six-digit-index>/
              attempt_identity.json
              geometry/
              mesh/
              fem/
              response/
              attempt_result.json
              artifact_manifest.json
  pilot_completion_manifest.json
```

Path ownership is:

- pilot root -> one Step-8 pilot namespace;
- `<design_id>` -> one deterministic physical design state;
- `<realization_id>` -> one stochastic scientific realization;
- `attempt_<index>` -> one execution attempt for that same realization.

### 22.14 Schema namespace

The permanent Step-8 record schemas are:

- `m9_pilot_sampling_provenance_v1`;
- `m9_pilot_planning_failure_v1`;
- `m9_pilot_plan_v1`;
- `m9_pilot_design_v1`;
- `m9_pilot_realization_v1`;
- `m9_pilot_attempt_identity_v1`;
- `m9_pilot_attempt_result_v1`;
- `m9_pilot_attempt_artifact_manifest_v1`;
- `m9_pilot_attempt_diagnosis_v1`;
- `m9_pilot_retry_authorization_v1`;
- `m9_pilot_failure_adjudication_v1`;
- `m9_pilot_completion_manifest_v1`.

A deliberate incompatible future schema/layout/RNG change requires an
explicit new version boundary.

### 22.15 Immutable JSON byte serialization

All permanent Step-8 JSON records use:

- UTF-8 encoding;
- no BOM;
- string object keys only;
- `sort_keys = True`;
- `ensure_ascii = True`;
- `allow_nan = False`;
- `indent = None`;
- `separators = (",", ":")`;
- exactly one terminal LF byte.

SHA-256 is calculated over the exact UTF-8 bytes including that terminal
LF.

Mapping insertion order must therefore not alter authenticated bytes.

### 22.16 Sampling-provenance record

`sampling_provenance.json` uses schema:

`m9_pilot_sampling_provenance_v1`.

Its top-level fields are exactly:

- `schema`;
- `sampling_namespace`;
- `sampling_architecture`;
- `sampling_value_quantization`;
- `n_per_stratum`;
- `optimizer_proposals`;
- `bit_generator`;
- `generator_construction`;
- `python_version`;
- `numpy_version`;
- `scipy_version`;
- `qmc_engine`;
- `qmc_strength`;
- `qmc_scramble`;
- `qmc_builtin_optimization`;
- `custom_optimizer`;
- `streams`;
- `repository_head`;
- `repository_tree`;
- `numpy_build_config_sha256`;
- `execution_environment_manifest_sha256`;
- `source_authorities`.

Every `streams` entry contains exactly:

- `stream`;
- `seed_material`;
- `seed_sha256`;
- `seed_uint128_decimal`;
- `bit_generator`;
- `generator_construction`;
- `producer`;
- `rng_call_pattern_id`.

`seed_uint128_decimal` is stored as an unsigned base-10 decimal string.

Producers/call-pattern IDs are:

- `pristine_lhs`:
  producer `scipy.stats.qmc.LatinHypercube`,
  call-pattern ID
  `scipy_lhs_d4_strength1_scramble_true_optimization_none_random_n12_v1`;
- `defective_sliced_lhs`:
  producer `project_sliced_lhs`,
  call-pattern ID `m9_defective_sliced_lhs_3x12x5_v1`;
- `defective_swap_optimizer`:
  producer `project_distance_guarded_optimizer`,
  call-pattern ID `m9_distance_guarded_swap_proposals_2000_v1`.

The `streams` array order is exactly:

1. `pristine_lhs`;
2. `defective_sliced_lhs`;
3. `defective_swap_optimizer`.

Every sampling `source_authorities` entry contains exactly:

- `role`;
- `repo_relative_path`;
- `git_blob_sha1`;
- `sha256`.

Required sampling-source roles are:

- `pilot_sampler`;
- `sliced_lhs_constructor`;
- `distance_guarded_optimizer`;
- `design_identity`;
- `raw_writer`.

Every required role must occur at least once.

The pair:

`(role, repo_relative_path)`

must be unique.

Sampling-source entries are ordered by:

`role -> repo_relative_path`

using UTF-8 lexicographic ordering.

Every referenced path must be tracked at the recorded sampling
`repository_head`.

The recorded `repository_tree` provides transitive tracked-source
authority.

### 22.17 Pilot-plan record

`pilot_plan.json` uses schema:

`m9_pilot_plan_v1`.

Its fields are exactly:

- `schema`;
- `pilot_namespace`;
- `sampling_namespace`;
- `sampling_architecture`;
- `sampling_value_quantization`;
- `n_per_stratum`;
- `strata`;
- `design_point_count`;
- `repeats_per_design`;
- `scheduled_realization_count`;
- `optimizer_proposals`;
- `sampling_provenance_sha256`;
- `design_ids`;
- `repository_head`;
- `repository_tree`;
- `project_status_sha256`;
- `m9_design_sha256`.


`strata` is exactly the ordered JSON array:

`["pristine_N0","defective_N1","defective_N2","defective_N4"]`

The `design_ids` array follows exactly the already locked order:

`stratum order -> sampler_row_index ascending`.

It is created once only after all 48 production sample rows have passed
locked-domain validation and their design identities exist.

It is immutable.

If any sampled row fails design validation, `pilot_plan.json` must remain
absent.

### 22.18 Design record

Every `<design_id>/design.json` uses schema:

`m9_pilot_design_v1`.

Its fields are exactly:

- `schema`;
- `design_id`;
- `design_sha256`;
- `canonical_design_material`;
- `stratum`;
- `sampling_unit_coordinates`;
- `physical_inputs`;
- `sampling_provenance_sha256`.


For a pristine design, `sampling_unit_coordinates` is an ordered JSON
array of length `4` in the exact coordinate order locked in Section 22.3.

For a defective design, `sampling_unit_coordinates` is an ordered JSON
array of length `5` in the exact defective-coordinate order locked in
Section 22.3.

`physical_inputs` is a JSON object containing exactly the six physical
input keys:

- `Ep_over_Em`;
- `nu_matrix`;
- `nu_particle`;
- `particle_area_fraction_requested`;
- `void_area_fraction_requested`;
- `void_count`.

The five continuous values are finite JSON numbers.

`void_count` is a non-negative JSON integer and not a Boolean value.

The record is created once and is immutable.

### 22.19 Realization record

Every `<realization_id>/realization.json` uses schema:

`m9_pilot_realization_v1`.

Its fields are exactly:

- `schema`;
- `design_id`;
- `design_sha256`;
- `canonical_design_material`;
- `realization_id`;
- `realization_index`;
- `particle_seed`;
- `void_seed_status`;
- `void_seed`;
- `rng_bit_generator`;
- `rng_namespace`.

`rng_namespace` is:

`composite-rve-m9-stochastic-v1`.

For defective realizations:

- `void_seed_status = applicable`;
- `void_seed` is the deterministic Step-7 void seed.

For pristine realizations:

- `void_seed_status = not_applicable`;
- `void_seed = null`.

A fabricated pristine numerical void seed is forbidden.

### 22.20 Attempt identity and attempt ID

Attempt indices are positive integers beginning at `1`.

Their decimal rendering has a minimum width of six digits and no defined
maximum.

Define:

`attempt_id = <realization_id>-A<minimum-six-digit-positive-attempt-index>`.

Define the directory:

`attempt_<minimum-six-digit-positive-attempt-index>`.

Attempt indices are never reused.

Directory reservation consumes the attempt index even if execution is
interrupted before the identity file commits.

`attempt_identity.json` uses schema:

`m9_pilot_attempt_identity_v1`.

Its fields are exactly:

- `schema`;
- `attempt_index`;
- `attempt_id`;
- `design_id`;
- `design_sha256`;
- `realization_id`;
- `realization_index`;
- `particle_seed`;
- `void_seed_status`;
- `void_seed`;
- `retry_authorization_sha256`;
- `repository_head`;
- `repository_tree`;
- `source_authorities`;
- `environment_authorities`;
- `execution_started_at_utc`.


For attempt index `1`:

`retry_authorization_sha256 = null`.

For every attempt index greater than `1`, an authenticated immutable retry
authorization must already exist before `attempt_identity.json` commits.

For such a retry:

`retry_authorization_sha256`

must equal the SHA-256 of that exact retry-authorization record.

It must be durably committed before scientific stage execution.

### 22.21 Source-authority schema

Every `source_authorities` entry contains exactly:

- `role`;
- `repo_relative_path`;
- `git_blob_sha1`;
- `sha256`.

Required roles are:

- `pilot_orchestrator`;
- `design_identity`;
- `raw_writer`;
- `geometry_generator`;
- `mesh_generator`;
- `fem_solver`;
- `local_response_evaluator`.

Entries are ordered by:

`role`, then `repo_relative_path`

using UTF-8 lexicographic ordering.

Every path must be tracked at the attempt repository HEAD.

The repository tree digest provides transitive tracked-source authority.

### 22.22 Environment-authority schema

`environment_authorities` contains exactly:

- `conda_default_env`;
- `python_version`;
- `numpy_version`;
- `numpy_build_config_sha256`;
- `scipy_version`;
- `gmsh_version`;
- `dolfinx_version`;
- `petsc_version`;
- `mpi4py_version`;
- `mpi_size`;
- `platform_system`;
- `platform_release`;
- `platform_machine`;
- `execution_environment_manifest_sha256`.

Actual authenticated execution values are recorded.

Silent environment substitution is forbidden.

### 22.23 Timestamp contract

Permanent execution timestamps use exactly:

`YYYY-MM-DDTHH:MM:SS.ffffffZ`.

They are:

- UTC;
- timezone-aware before rendering;
- exactly six fractional-second digits.

### 22.24 Stage status and failure-stage contract

Attempt stage keys are exactly:

- `geometry`;
- `mesh`;
- `fem`;
- `response`.

Stage-status values are:

- `success`;
- `failure`;
- `skipped`.

`not_applicable` is not used as a top-level pipeline stage status for a
valid design. Subresponse non-applicability is represented inside response
applicability.


In `attempt_result.json`, `stage_status` is a JSON object containing
exactly these four keys:

- `geometry`;
- `mesh`;
- `fem`;
- `response`.

The exact mappings are:

`invalid_geometry`:
`geometry=failure, mesh=skipped, fem=skipped, response=skipped`

`mesh_failure`:
`geometry=success, mesh=failure, fem=skipped, response=skipped`

`fem_failure`:
`geometry=success, mesh=success, fem=failure, response=skipped`

`response_failure`:
`geometry=success, mesh=success, fem=success, response=failure`

`success`:
`geometry=success, mesh=success, fem=success, response=success`

`invalid_design_input` has no attempt-stage object because it is intercepted
at the planning boundary before legal attempt identity exists.

Attempt `failure_stage` values are:

- `geometry`;
- `mesh`;
- `fem`;
- `response`.

Successful attempts use:

`failure_stage = null`.

The failure mapping is:

- `invalid_geometry -> geometry`;
- `mesh_failure -> mesh`;
- `fem_failure -> fem`;
- `response_failure -> response`.

`invalid_design_input` is a planning failure at:

`design_validation`

before legal design identity exists.

### 22.25 Raw stage leaf filenames

The declared stage paths are:

```text
geometry/geometry.json
geometry/stdout.log
geometry/stderr.log

mesh/mesh.msh
mesh/mesh_diagnostics.json
mesh/stdout.log
mesh/stderr.log

fem/pbc_X.json
fem/pbc_X.stdout.log
fem/pbc_X.stderr.log
fem/pbc_Y.json
fem/pbc_Y.stdout.log
fem/pbc_Y.stderr.log
fem/pbc_XY.json
fem/pbc_XY.stdout.log
fem/pbc_XY.stderr.log
fem/tensor_audit.json

response/response.json
response/stdout.log
response/stderr.log
```

A failed stage may legitimately contain only a subset of its declared
paths.

An unproduced file must never be fabricated to make a directory look
complete.

### 22.26 Attempt-result record

`attempt_result.json` uses schema:

`m9_pilot_attempt_result_v1`.

Its fields are exactly:

- `schema`;
- `attempt_index`;
- `attempt_id`;
- `design_id`;
- `design_sha256`;
- `realization_id`;
- `realization_index`;
- `top_level_classification`;
- `failure_stage`;
- `failure_reason`;
- `stage_status`;
- `response_applicability`;
- `response_summary`;
- `execution_completed_at_utc`.

Top-level classifications are exactly:

- `invalid_design_input`;
- `invalid_geometry`;
- `mesh_failure`;
- `fem_failure`;
- `response_failure`;
- `success`.

In ordinary realization-attempt directories,
`invalid_design_input` cannot occur because that condition is intercepted
before design identity formation and stored as a planning failure.


`response_applicability` is a JSON object containing exactly:

- `global_response`;
- `local_response`.

For a pristine realization it is exactly:

`{"global_response":"applicable","local_response":"not_applicable"}`

For a defective realization it is exactly:

`{"global_response":"applicable","local_response":"applicable"}`

This field describes scientific applicability. It does not claim that a
failed attempt actually produced a valid response.

For a successful attempt:

`failure_reason = null`.

For every failed realization attempt:

`failure_reason`

is a non-empty UTF-8 string.

For a failure attempt:

`response_summary = null`.

Valid partial native stage artifacts remain durable evidence but are not
promoted into a fabricated success response summary.

### 22.27 Success response-summary schema

A successful response summary contains exactly these top-level groups:

- `Cbar_over_Em`;
- `engineering_constants`;
- `local_response`.

`Cbar_over_Em` contains:

- `C11`;
- `C12`;
- `C16`;
- `C21`;
- `C22`;
- `C26`;
- `C61`;
- `C62`;
- `C66`.

All nine actually recovered normalized components are retained. No
isotropy or orthotropy projection is introduced.

`engineering_constants` contains:

- `Ex_over_Em`;
- `Ey_over_Em`;
- `Gxy_over_Em`;
- `nu_xy`;
- `nu_yx`.

`local_response` contains:

- `status`;
- `reason`;
- `metric_id`;
- `K_vm_tail10_X`.

For pristine success:

- `status = not_applicable`;
- `reason = pristine_no_physical_voids`;
- `metric_id = m8_matrix_vm_annulus_quadrature_tail10_v1`;
- `K_vm_tail10_X = null`.

For defective success:

- `status = valid`;
- `metric_id = m8_matrix_vm_annulus_quadrature_tail10_v1`;
- `K_vm_tail10_X` is finite and non-negative.

### 22.28 Artifact-manifest record

`artifact_manifest.json` uses schema:

`m9_pilot_attempt_artifact_manifest_v1`.

Its fields are exactly:

- `schema`;
- `attempt_index`;
- `attempt_id`;
- `design_id`;
- `design_sha256`;
- `realization_id`;
- `files`.

Each `files` entry contains exactly:

- `relative_path`;
- `sha256`;
- `size_bytes`;
- `role`.

Permitted artifact roles are:

- `attempt_identity`;
- `geometry_record`;
- `geometry_stdout`;
- `geometry_stderr`;
- `mesh_file`;
- `mesh_diagnostics`;
- `mesh_stdout`;
- `mesh_stderr`;
- `fem_load_response`;
- `fem_stdout`;
- `fem_stderr`;
- `tensor_audit`;
- `response_record`;
- `response_stdout`;
- `response_stderr`;
- `attempt_result`.

Manifest file entries are ordered by:

`relative_path`

using ascending UTF-8 byte lexicographic ordering.

Relative paths must be unique.

The manifest hashes all committed files inside that attempt except the
manifest itself.

The artifact manifest is the final immutable commit marker for an attempt.

No scientific file may be written after it commits.

### 22.29 Append-only and crash-state semantics

The raw attempt states are interpreted as:

- no attempt directory -> `not_started`;
- attempt directory but identity absent ->
  `interrupted_preidentity_reservation`;
- identity present but unreadable/unauthenticated ->
  unresolved hard stop;
- identity committed, result absent ->
  started incomplete execution;
- result committed, manifest absent ->
  terminal result not yet committed as a complete attempt;
- manifest present but authentication fails ->
  attempt-manifest invalid hard stop;
- manifest committed and all hashes authenticate ->
  committed attempt.


An occupied attempt directory that is not an authenticated committed
attempt must be represented, when formally diagnosed, by an immutable
realization-level diagnosis record at:

`designs/<design_id>/realizations/<realization_id>/attempt_diagnoses/attempt_<minimum-six-digit-index>.json`.

Its schema is:

`m9_pilot_attempt_diagnosis_v1`.

Its fields are exactly:

- `schema`;
- `design_id`;
- `design_sha256`;
- `realization_id`;
- `realization_index`;
- `attempt_index`;
- `attempt_id`;
- `raw_state`;
- `retry_authorization_sha256`;
- `diagnosis_reason`;
- `retained_file_records`;
- `diagnosed_at_utc`;
- `repository_head`;
- `repository_tree`;
- `project_status_sha256`;
- `m9_design_sha256`.

Permitted diagnosis `raw_state` values are exactly:

- `interrupted_preidentity_reservation`;
- `identity_unreadable_or_unauthenticated`;
- `identity_committed_result_absent`;
- `result_committed_manifest_absent`;
- `manifest_authentication_failed`.

`diagnosis_reason` is a non-empty UTF-8 string.

Every `retained_file_records` entry contains exactly:

- `relative_path`;
- `sha256`;
- `size_bytes`.

The retained-file scope is every regular file recursively present inside
the attempt directory at diagnosis time.

Paths are relative to that attempt directory and are ordered by ascending
UTF-8 byte lexicographic order.

The attempt-diagnosis record is stored outside the attempt directory.

After diagnosis commits, mutation of that diagnosed attempt directory is
forbidden.

For attempt index `1`:

`retry_authorization_sha256 = null`.

For a later retry attempt, the diagnosis records the authenticated retry
authorization SHA-256 if that authorization had committed before the
interruption. Otherwise the field is `null`.

The attempt-diagnosis record is immutable.

Any syntactically valid existing attempt directory consumes its index.

Incomplete attempt directories are never reused.

The next retry index is one plus the highest existing attempt-directory
index, but execution of that retry is forbidden until all existing attempt
evidence has been authenticated or formally diagnosed.

### 22.30 Crash-durable no-clobber publication

Exclusive `"x"` creation alone is collision protection, not a complete
crash-durability boundary.

Permanent immutable files use the tested same-filesystem publication
sequence:

1. reserve required directory and synchronize its parent directory;
2. create a same-directory staging file exclusively;
3. write complete bytes;
4. flush userspace buffering;
5. `fsync` the staging file;
6. synchronize the containing directory as required;
7. hard-link the staged inode to the final path with no-clobber semantics;
8. `fsync` the containing directory;
9. authenticate final bytes;
10. unlink the staging alias;
11. `fsync` the containing directory again.

Existing final destination -> hard stop.

Ordinary overwrite, `open(..., "w")`, `Path.replace`, `os.replace`, or
check-then-overwrite semantics are forbidden for final durable scientific
evidence.

The non-production ext4 preflight confirmed the required syscall and
filesystem support on the current repository filesystem. It did not
simulate power loss.

### 22.31 Attempt commit order

One attempt uses this order:

1. reserve attempt directory;
2. durably commit `attempt_identity.json`;
3. execute and close geometry outputs;
4. execute and close mesh outputs;
5. execute and close FEM outputs;
6. execute and close response outputs;
7. durably commit `attempt_result.json`;
8. hash all durable attempt files;
9. durably commit `artifact_manifest.json` as final marker.

No log handle may remain open at artifact-manifest commit.

An undeclared scientific write after manifest commit is a contract breach.

### 22.32 Retry contract

Blind rerun-until-success is forbidden.

Seed substitution after failure is forbidden.

Response-based realization replacement or cherry-picking is forbidden.

An authorized retry requires either:

- documented causal remediation; or
- verified transient execution failure.

It preserves:

- `design_id`;
- full `design_sha256`;
- `realization_id`;
- `realization_index`;
- `particle_seed`;
- applicable `void_seed`.

It changes only:

- attempt index;
- execution provenance associated with that attempt.


Every retry attempt with index greater than `1` requires an immutable
authorization record at:

`designs/<design_id>/realizations/<realization_id>/retry_authorizations/attempt_<minimum-six-digit-index>.json`.

Its schema is:

`m9_pilot_retry_authorization_v1`.

Its fields are exactly:

- `schema`;
- `design_id`;
- `design_sha256`;
- `realization_id`;
- `realization_index`;
- `authorized_attempt_index`;
- `authorized_attempt_id`;
- `prior_attempt_index`;
- `prior_attempt_id`;
- `prior_evidence_kind`;
- `prior_evidence_sha256`;
- `authorization_basis`;
- `authorization_reason`;
- `authorized_at_utc`;
- `repository_head`;
- `repository_tree`;
- `project_status_sha256`;
- `m9_design_sha256`.

`prior_evidence_kind` is exactly one of:

- `artifact_manifest`;
- `attempt_diagnosis`.

The referenced prior evidence is the immediately preceding occupied
attempt index.

Before retry authorization, all existing attempt directories must either:

- authenticate as committed attempts through their artifact manifests; or
- be covered by immutable attempt-diagnosis evidence.

The only authorization-basis values are:

- `documented_causal_remediation`;
- `verified_transient_execution_failure`.

`authorization_reason` is a non-empty UTF-8 string.

The retry-authorization record is immutable.

The retry sequence is:

1. authenticate all existing attempt evidence;
2. select the next never-used attempt index;
3. reserve that attempt directory and synchronize its parent;
4. durably commit the retry-authorization record;
5. durably commit `attempt_identity.json` binding the authorization hash;
6. begin scientific stage execution.

A crash after directory reservation but before retry authorization leaves
an `interrupted_preidentity_reservation` whose diagnosis has:

`retry_authorization_sha256 = null`.

A crash after retry authorization commits but before attempt identity
commits leaves the same raw-state class, but its diagnosis binds the
authenticated retry-authorization SHA-256.

Retry authorization does not override the existing rule that a successful
authenticated realization attempt is skipped rather than rerun.

Earlier failed evidence remains durable.

### 22.33 Failure-adjudication contract

A realization-level terminal failure is recorded at:

`designs/<design_id>/realizations/<realization_id>/failure_adjudication.json`.

The schema is:

`m9_pilot_failure_adjudication_v1`.

Its fields are exactly:

- `schema`;
- `design_id`;
- `design_sha256`;
- `realization_id`;
- `realization_index`;
- `terminal_attempt_index`;
- `terminal_attempt_id`;
- `terminal_attempt_manifest_sha256`;
- `terminal_top_level_classification`;
- `adjudication_status`;
- `adjudication_reason`;
- `adjudicated_at_utc`;
- `repository_head`;
- `repository_tree`;
- `project_status_sha256`;
- `m9_design_sha256`.

The only Step-8 adjudication status is:

`terminal_no_retry_in_this_pilot_namespace`.

Allowed terminal classifications are:

- `invalid_geometry`;
- `mesh_failure`;
- `fem_failure`;
- `response_failure`.

A failure adjudication is immutable.

Once failure is terminally adjudicated, retry in the same pilot namespace
is forbidden.

### 22.34 Invalid-design-input planning boundary

Locked-domain validation occurs:

`after scale -> before canonicalization and design hash`.

Therefore an `invalid_design_input` has:

- no `design_id`;
- no `realization_id`;
- no `attempt_id`;
- no stochastic-realization-attempt identity.

It is stored as a pilot planning failure under:

`planning_failures/failure_<minimum-six-digit-index>.json`.

The schema is:

`m9_pilot_planning_failure_v1`.

Fields are exactly:

- `schema`;
- `failure_index`;
- `failure_classification`;
- `failure_stage`;
- `failure_reason`;
- `stratum`;
- `sampler_row_index`;
- `sampling_unit_coordinates`;
- `scaled_physical_inputs`;
- `sampling_provenance_sha256`;
- `repository_head`;
- `repository_tree`;
- `detected_at_utc`.


`sampling_unit_coordinates` retains the ordered JSON-array shape applicable
to the sampled stratum.

`scaled_physical_inputs` uses the same exact six-key JSON object shape and
numeric-type contract as `physical_inputs` in Section 22.18.

Required values are:

- `failure_classification = invalid_design_input`;
- `failure_stage = design_validation`.

Planning failures are ordered by deterministic stratum order followed by
sampler row index.

If any production sampling row fails domain validation:

- hard stop before design identity registration;
- preserve the immutable planning-failure evidence;
- `pilot_plan.json` must remain absent.

### 22.35 Pilot-completion contract

`pilot_completion_manifest.json` uses schema:

`m9_pilot_completion_manifest_v1`.

Its fields are exactly:

- `schema`;
- `pilot_plan_sha256`;
- `sampling_provenance_sha256`;
- `scheduled_design_count`;
- `scheduled_realization_count`;
- `accounted_realization_count`;
- `classification_counts`;
- `unresolved_realization_ids`;
- `attempt_evidence_records`;
- `realization_resolutions`;
- `completion_status`.


`classification_counts` is a JSON object containing exactly:

- `success`;
- `invalid_geometry`;
- `mesh_failure`;
- `fem_failure`;
- `response_failure`.

All five values are non-negative JSON integers and not Boolean values.

Their sum equals:

`scheduled_realization_count`.

`invalid_design_input` is absent from completion classification counts
because it is a pre-identity planning failure and prevents creation of the
pilot plan.

`attempt_evidence_records` contains exactly one entry for every occupied
attempt directory.

Every entry contains exactly:

- `design_id`;
- `realization_id`;
- `realization_index`;
- `attempt_index`;
- `attempt_id`;
- `evidence_kind`;
- `evidence_sha256`.

`evidence_kind` is exactly one of:

- `artifact_manifest`;
- `attempt_diagnosis`.

An authenticated committed attempt is represented by the SHA-256 of its
immutable artifact manifest.

An occupied noncommitted or untrusted attempt is represented by the
SHA-256 of its immutable attempt-diagnosis record.

One occupied attempt directory has exactly one of those two evidence kinds
in the completion manifest.

Attempt-evidence records are ordered by:

`pilot_plan design_ids order -> realization_index ascending -> attempt_index ascending`.

The attempt-evidence record count is at least `384` and may exceed `384`
because append-only retries consume additional attempt indices.

Any occupied attempt directory lacking one authenticated evidence record
blocks completion.

It may be created only when all 384 scheduled realization identities have
a terminal authenticated resolution, the unresolved count is zero, and every
occupied attempt index is represented by exactly one authenticated
`attempt_evidence_records` entry.

Therefore, in a committed completion manifest:

`unresolved_realization_ids = []`.

Every `realization_resolutions` entry contains exactly:

- `design_id`;
- `realization_id`;
- `realization_index`;
- `resolution_status`;
- `terminal_attempt_index`;
- `terminal_attempt_id`;
- `terminal_attempt_manifest_sha256`;
- `terminal_top_level_classification`;
- `failure_adjudication_sha256`.

Resolution-status values are:

- `success`;
- `adjudicated_failure`.

For success:

`failure_adjudication_sha256 = null`.

For adjudicated failure:

`failure_adjudication_sha256`

is required and authenticates the immutable failure-adjudication record.

Resolution records are ordered by:

`pilot_plan design_ids order -> realization_index 1..8`.

Thus there are exactly 384 ordered resolution slots.

Completion-status values are:

- `complete_all_success`;
- `complete_with_adjudicated_failures`.

`unresolved` is a runtime accounting state, not a permitted immutable
completion resolution.

If any realization remains unresolved, the completion manifest must remain
absent.

A tracked checkpoint created later must authenticate the completed raw
completion-manifest SHA-256. The Git-ignored raw completion manifest alone
is not final Git provenance.

### 22.36 Pilot pause and stop conditions

Before starting any new realization, the pilot must pause on:

- repository or authority mismatch;
- design-ID or seed-identity mismatch;
- existing output collision or overwrite risk;
- locked geometry-contract violation;
- mesh hard-gate failure;
- PBC/FEM hard-gate failure;
- response hard-gate failure;
- non-finite required output;
- unexpected schema or provenance mismatch;
- unreadable or unauthenticated existing attempt evidence.

On a realization failure:

1. retain durable evidence;
2. pause for diagnosis;
3. do not silently substitute seed or realization;
4. authorize a retry only under the locked Step-7/Step-8 retry rule.

Pilot evidence accounting can be called complete only after all 384
scheduled realization identities receive terminal authenticated resolution.

Evidence accounting completion is not automatically a scientific PASS.

There is no failure-rate acceptance threshold.

M10 remains blocked by any unresolved realization or unadjudicated contract
failure.

### 22.37 Step-8 closure interpretation

The final locked Step-8 design is:

- sampling architecture:
  `hybrid_pristine_independent_4D_LHS__defective_distance_guarded_sliced_5D_LHS`;
- `12` physical design points per stratum;
- `48` physical design points total;
- `8` stochastic realizations per physical design point;
- `384` scheduled stochastic realization identities;
- no sampling-value quantization;
- explicit domain-separated `PCG64` sampling RNG;
- custom exact sliced defective constructor;
- custom distance-guarded coordinate-swap optimizer with 2000 proposals;
- append-only immutable raw evidence;
- exact per-realization hard-gate inheritance;
- descriptive Student-t repeat reporting without invented stochastic
  acceptance thresholds.

No production sampling stream was consumed in selecting or validating this
contract.

No production LHS point, physical design value, design ID, stochastic
realization, execution attempt, or M9 raw production directory was created
by the pre-lock diagnostic work.

**Next scientific gate: M9 Step 9 — Targeted Transfer-Validation.**

The stochastic M9 pilot remains **NOT AUTHORIZED**.

---

## 23. Machine-learning authorization boundary

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

## 24. Current checkpoint

At the current authenticated checkpoint:

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
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 9:
  `NEXT`
- stochastic M9 pilot:
  `NOT AUTHORIZED`
- approximate M9 milestone progress:
  `~64%`

The percentage is an approximate milestone-progress indicator, not a
mathematically exact project-completion measure. The milestone still
includes targeted transfer-validation, formal pilot authorization, and the
later stochastic-pilot execution/evidence cycle.

---

## 25. Documentation and provenance policy

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
