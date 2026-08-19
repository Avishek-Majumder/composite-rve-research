# M9 — Final Parameter-Space and Stochastic-Pilot Design Record

**Project:** Composite-RVE Research

**Working title:** *An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.*

**Research route:** Simulation + Machine Learning only; no laboratory experiments.

**Milestone:** M9 — Final Parameter-Space Lock and Stochastic Pilot Dataset

**Record initiated:** 19 August 2026

**Current M9 state:** IN PROGRESS

**Closed M9 design gates at this checkpoint:** Steps 1, 2, 3A, 3B, 4, and 5

**Next scientific gate:** Step 6 — Geometry, Defect, and Feasibility Lock

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

### 19.12 Remaining exact M9 sequence

M9 Steps 1-5 are now complete at their currently authorized scope.

The remaining scientific sequence is:

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
- M9 Step 4A:
  `PASS / LOCKED`
- M9 Step 4B:
  `PASS / LOCKED`
- M9 Step 4 overall:
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 5:
  `PASS / CONCEPTUALLY COMPLETE`
- M9 Step 6:
  `NOT STARTED`
- approximate M9 milestone progress:
  `34%`

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
