# M8 Scientific Methodology and Design Record

## RVE-Size Study + Homogenization BC/PBC Verification + Final Target-Mesh Verification

**Document status:** M8 design candidate for validation
**Milestone:** M8
**M8 implementation status at document creation:** NOT STARTED
**Production database status:** NOT GENERATED
**ML status:** NOT STARTED

---

## 1. Purpose

This document defines the scientific methodology that must be validated
before invasive M8 implementation begins.

M8 has three coupled objectives:

1. quantify stochastic RVE-size/statistical-representativity behavior;
2. verify the final homogenization boundary-condition strategy,
   including periodic boundary conditions where scientifically valid;
3. establish the final target-mesh policy for the macroscopic response
   and the defect-sensitive local-response candidate.

This document does not authorize M9 parameter-space lock, production
database generation, machine learning, active learning, uncertainty
calibration, or OOD analysis.

---

## 2. Scientific Model Class and Scope

The framework shall be described as a normalized/dimensionless
computational micromechanics framework for a defined class of:

- two-dimensional composite microstructures;
- small-strain linear elasticity;
- plane-stress constitutive behavior;
- isotropic matrix;
- isotropic particles;
- perfectly bonded matrix-particle interfaces;
- circular particles;
- circular matrix-phase voids;
- true geometric voids rather than soft pseudo-material regions.

The framework shall NOT be described as applicable to all materials.

The model does not currently represent plasticity, damage evolution,
debonding, fracture, viscoelasticity, fatigue, thermal coupling,
arbitrary three-dimensional particle shapes, or imperfect interfaces.

---

## 3. Reference-Modulus and Normalization Policy

The value

`E_matrix = 1000`

shall be treated as a reference elastic-modulus scale.

It shall not be presented as identification of one specific physical
matrix material.

The baseline stiffness ratio is

`E_particle / E_matrix = 10`.

Publication-facing M8 outputs shall retain dimensional values where
useful while also reporting normalized quantities including:

- `C_ij / E_matrix`;
- `E_x / E_matrix`;
- `E_y / E_matrix`;
- `G_xy / E_matrix`;
- particle area fraction;
- void area fraction;
- normalized geometric descriptors;
- the dimensionless local-response candidate `K_vm_tail10`.

Poisson ratios remain dimensionless.

Common elastic-modulus scaling is not treated as a new physical degree
of freedom during M8.

---

## 4. Protected M0-M7 State

M8 shall not silently modify or reinterpret the permanent M0-M7
validation record.

The following M7 identities remain protected:

- geometry schema:
  `m7_void_microstructure_v1`;
- mesh schema:
  `m7_void_mesh_diagnostics_v1`;
- elasticity schema:
  `m7_void_elasticity_v2`;
- global response:
  `m7_gross_rve_axial_v1`;
- local-response candidate:
  `m7_matrix_vm_annulus_tail10_v1`.

The existing M7 global response remains an:

**x-direction apparent axial response**

until M8 establishes the broader homogenized-response semantics.

Raw maximum local von Mises stress remains diagnostic only.

M8 shall not retroactively rewrite M7 validation claims.

---

## 5. Permanent Regression Gate

Before any invasive M8 source modification, the permanent regression
suite must pass.

At the start of Phase C the suite contains 15 passing tests protecting:

- area-weighted upper-tail numerical behavior;
- invalid numerical inputs;
- zero-void M6-to-M7 FEM regression;
- permanent M7 response semantics within that regression path;
- deterministic M7 geometry generation;
- independent void-seed behavior;
- controlled invalid-geometry rejection.

The suite must be rerun after every invasive M8 implementation unit.

A regression failure blocks further scientific implementation until
resolved.

---

## 6. RVE Representativity Is Not Mesh Convergence

Element-size convergence and statistical RVE representativity shall be
treated as separate questions.

Mesh refinement asks whether a fixed geometry is sufficiently
discretized.

RVE representativity asks whether the statistical apparent response of
a stochastic microstructure is sufficiently stable with increasing
domain size.

M8 shall therefore use multiple statistically independent particle
realizations at every tested RVE size.

No single-realization RVE-size study may be called an RVE convergence
study.

---

## 7. M8 Controlled RVE-Size Grid

The initial square-RVE side-length candidates are:

| Level | Lx | Ly | Relative area |
|---|---:|---:|---:|
| R1 | 1.0 | 1.0 | 1.00 |
| R2 | 1.5 | 1.5 | 2.25 |
| R3 | 2.0 | 2.0 | 4.00 |
| R4 | 2.5 | 2.5 | 6.25 |

An optional extension:

`R5 = 3.0 x 3.0`

shall be executed only if R1-R4 do not establish an acceptable
representativity decision.

Increasing RVE size shall increase the number of microstructural
features rather than scaling every particle radius with RVE size.

Otherwise the ratio of the RVE dimension to the microstructural length
scale would not actually increase.

---

## 8. Validation-Only Nominal Particle-Fraction Control

M8 requires a controlled particle fraction so RVE-size effects are not
confounded with reinforcement-fraction changes.

M8 shall NOT build the final production-grade requested-fraction
generator. That remains an M9 responsibility.

For the controlled M8 RVE-size study, use a monodisperse validation
state:

`particle radius = 0.05`.

Use the following particle counts:

| RVE side L | Particle count |
|---:|---:|
| 1.0 | 16 |
| 1.5 | 36 |
| 2.0 | 64 |
| 2.5 | 100 |
| 3.0, if required | 144 |

Because particle count scales with `L^2`, the analytical nominal
particle area fraction is identical at every level:

`phi_particle = 0.12566370614359174`

approximately 12.566%.

Realized analytical and meshed fractions shall both be recorded.

This is an M8 validation construction only.

It does not become the M9 final particle-fraction parameterization.

---

## 9. Controlled Defect State for M8

RVE and homogenization verification shall first include a pristine
zero-void state to isolate global homogenization behavior.

A low-defect paired validation state shall then use:

`void radius = 0.025`.

Use void counts:

| RVE side L | Void count |
|---:|---:|
| 1.0 | 4 |
| 1.5 | 9 |
| 2.0 | 16 |
| 2.5 | 25 |
| 3.0, if required | 36 |

This keeps the analytical nominal void fraction constant:

`phi_void = 0.007853981633974483`

approximately 0.7854%.

The defective realization shall reuse the same underlying particle
geometry as its pristine partner and use an independently recorded
void seed.

This pairing permits direct separation of the controlled defect effect
from particle-realization variability.

The final production void-fraction policy remains an M9 task.

---

## 10. Multiple-Realization Statistical Design

For each required RVE-size state, begin with:

`n = 10`

independent particle realizations.

Each particle realization shall have a permanently recorded particle
seed.

For the controlled defective state, each particle realization shall
receive an independent permanently recorded void seed.

Seed integers are provenance and grouping metadata.

They shall not be interpreted as continuous physical predictors.

For every response quantity record:

- per-realization value;
- arithmetic mean;
- sample standard deviation;
- coefficient of variation where meaningful;
- standard error;
- two-sided 95% Student-t confidence interval;
- relative confidence-interval half-width;
- mesh cell count;
- runtime;
- geometry/mesh/solver validity;
- failure reason where applicable.

If statistical precision is inadequate or the size trend is ambiguous,
increase to:

`n = 20`

for the affected state before drawing a representativity conclusion.

No convergence conclusion may be manufactured by discarding valid
realizations because they are inconvenient.

### 10.1 Representativity-Envelope Challenge States

The monodisperse random state defined above is the baseline controlled
RVE-size construction.

It shall NOT be the sole basis for a general M8 RVE-size decision.

Before M8 closure, the candidate RVE size must also be challenged on at
least:

1. a random/uniform particle ensemble;
2. a clustered particle ensemble using the already validated M6
   clustered-microstructure capability;
3. a pristine state;
4. a controlled defect-containing state.

Random and clustered comparisons should use matched nominal particle
fraction, particle-radius scale, constituent properties and mesh policy
as closely as the validated geometry constraints permit.

Requested and realized fraction differences must be recorded rather
than hidden.

Clustering may introduce a larger characteristic correlation scale than
the random/uniform state, so an RVE size accepted only for the random
ensemble shall not automatically be declared representative for the
clustered ensemble.

### 10.2 Conditional RVE Decision and M9 Recheck Trigger

M8 shall report the RVE decision together with the exact validation
envelope over which it was established.

The M8 RVE conclusion is therefore conditional on the tested:

- particle area-fraction range;
- particle-radius/size-distribution range;
- random versus clustered morphology;
- stiffness ratio;
- Poisson ratios;
- void fraction/severity;
- response quantity;
- homogenization boundary condition.

M9 owns the final production parameter-space lock.

If the M9 parameter domain materially extends beyond the M8 validation
envelope in a way expected to alter microstructural correlation length
or apparent-property variability, M9 must trigger a targeted RVE
representativity recheck before approving the production database.

This recheck is a safeguard, not a reopening of M8 as a whole.


---

## 11. Statistical RVE Acceptance Logic

The initial representativity decision shall focus on the periodized
ensemble and the accepted homogenization formulation.

For the principal non-negligible in-plane stiffness components:

- `C11 / E_matrix`;
- `C22 / E_matrix`;
- `C12 / E_matrix`;
- `C66 / E_matrix`;

the initial acceptance target is:

1. relative difference between the two largest evaluated RVE-size
   ensemble means is no greater than 2%;
2. relative 95% confidence-interval half-width at the candidate final
   size is no greater than 2.5%;
3. the full ensemble-mean stiffness tensor is stable between the two
   largest evaluated sizes according to

   `||mean(C_L2) - mean(C_L1)||_F / ||mean(C_L1)||_F <= 0.02`;

4. no unresolved finite-size mean-shift trend remains materially larger
   than the observed realization uncertainty.

The normal-shear coupling terms, conventionally represented by
`C16`, `C26` and their symmetric counterparts, shall also be retained.

Because their ensemble means may legitimately approach zero for a
statistically isotropic generating process, relative-percentage errors
are not appropriate when their denominator is near zero.

For those components M8 shall instead report:

- their dimensional values;
- `C16 / E_matrix` and `C26 / E_matrix`;
- corresponding confidence intervals;
- their trend with RVE size;
- stiffness-matrix symmetry residuals.

No individual stochastic realization shall be forced to have zero
normal-shear coupling.

If R4 fails the RVE criteria, R5 shall be considered.

If the criteria remain unsatisfied, M8 shall report that no tested RVE
size was sufficient rather than declaring false convergence.

Realization-level directional anisotropy is expected and is not a
failure by itself.

Statistical isotropy shall be examined at the ensemble level rather
than imposed on every realization.

---

## 12. Random Error, Finite-Size Mean Shift, and Systematic Bias

M8 shall distinguish three related but non-identical concepts.

### 12.1 Random or realization error

Random error quantifies realization-to-realization fluctuations of the
apparent response at fixed RVE size.

It shall be quantified using sample variance, standard deviation,
standard error and confidence intervals.

### 12.2 Observed finite-size mean shift

Changes in ensemble means between finite RVE sizes shall initially be
reported as:

**finite-size mean shift**

or

**finite-size trend**.

A difference between the means of two finite RVE sizes is not, by
itself, a direct measurement of the true systematic bias relative to
the unknown infinite-volume effective property.

### 12.3 Systematic error or bias

The term systematic error/bias shall be used quantitatively only when a
defensible reference is available.

Possible references include:

- a substantially larger RVE/ensemble shown to provide materially
  smaller finite-size error;
- an independently validated analytical or numerical reference;
- a justified asymptotic/extrapolation procedure supported by the
  observed data.

If no defensible reference exists, M8 shall not relabel finite-size
mean shifts as measured systematic bias.

M8 shall nevertheless examine whether the finite-size trend is small
relative to realization uncertainty and engineering acceptance limits.

No asymptotic power-law convergence rate shall be claimed unless the
observed data genuinely support such a fit.

Computational cost shall be reported together with statistical
precision.

---

## 13. Snapshot Versus Periodized Ensemble Policy

The existing M6 stochastic geometry is a snapshot-style ensemble:

- particles are strictly inside the RVE;
- boundary clearance is imposed;
- particles do not wrap across opposite boundaries.

This representation remains valid for its completed M6/M7 purposes.

It shall NOT be treated as a geometrically periodic stochastic cell.

M8 shall explicitly distinguish:

### 13.1 Snapshot ensemble

The protected M6-style geometry.

It may be used for:

- legacy-response regression;
- boundary-condition sensitivity diagnostics;
- comparison with the historical implementation.

Periodic displacement constraints shall NOT be applied to this geometry
and described as a periodic microstructure.

### 13.2 Periodized ensemble

A new M8 geometry representation shall be implemented only after this
design is checkpointed.

For the periodized ensemble:

- particle centers are sampled on a two-dimensional torus;
- particle-particle distances use minimum-image/toroidal distance;
- particles crossing one outer boundary are represented by the
  corresponding periodic images/cut pieces on the opposite boundary;
- paired outer boundaries must have geometrically compatible material
  occupancy;
- the same principle applies to periodic voids;
- particle/void spacing must also be verified periodically across
  opposite boundaries.

The periodized representation shall receive a new M8 schema.

Existing M6/M7 schemas shall never be mutated to mean periodic geometry.

---

## 14. Boundary-Crossing and Wrapping Policy

For periodized geometry, a particle or void is permitted to cross the
computational-cell boundary.

Crossing is not treated as truncation of the physical feature.

Instead, the feature is interpreted as one object on the periodic
torus.

All wrapped pieces must preserve:

- original feature ID;
- original radius;
- original unwrapped center;
- periodic-image translation;
- source random seed;
- total analytical feature area counted once.

The mesher must avoid double-counting wrapped feature area.

Opposite-boundary geometry must match under the periodic translation
map.

---

## 15. Homogenization Boundary-Condition Families

M8 shall distinguish three response formulations.

### 15.1 Protected legacy M7 axial formulation

The established M7 x-loading boundary conditions remain available as a
historical validation baseline.

They shall not be silently relabeled as the final homogenization
formulation.

### 15.2 Kinematic uniform boundary conditions

For KUBC, impose the affine macroscopic displacement

`u(x) = E_bar x`

on the complete external RVE boundary.

KUBC shall be evaluated on periodized geometries as a finite-size
comparison to PBC.

It may also be evaluated on snapshot geometries for boundary-sensitivity
diagnostics.

### 15.3 Periodic boundary conditions

For PBC, write:

`u(x) = E_bar x + v(x)`

where the displacement fluctuation `v` is periodic.

For paired boundary points:

`v(x_plus) = v(x_minus)`.

Equivalently:

`u(x_plus) - u(x_minus) =
 E_bar (x_plus - x_minus)`.

Opposing boundary tractions must be anti-periodic in the converged
solution.

A rigid-body translation must be removed using a mathematically
explicit reference constraint or equivalent zero-mean condition.

PBC may only be used on a geometrically compatible periodized
microstructure.

---

## 16. PBC Software-Backend Policy

At the Phase-C preflight:

- DOLFINx environment version reports `0.11.0`;
- `dolfinx_mpc` is not installed.

The mathematical PBC formulation is independent of the software
backend.

M8 shall NOT install an MPC package into the validated
`composite-sim` environment merely because it exposes a periodic API.

Before choosing an MPC backend, M8 must perform a separate compatibility
gate against the live DOLFINx/PETSc stack.

A compatibility experiment should occur in an isolated or otherwise
reversible environment before the protected research environment is
changed.

Possible implementation routes may include:

- a verified DOLFINx-MPC version;
- a carefully validated custom multi-point-constraint formulation;
- another technically justified DOLFINx-compatible approach.

The backend shall be selected only after direct capability validation.

---

## 17. Required Macroscopic Loading Cases

The final M8 homogenization verification shall use three independent
two-dimensional macroscopic strain cases.

Use Voigt strain convention:

`[epsilon_11, epsilon_22, gamma_12]`

with

`gamma_12 = 2 epsilon_12`.

### Load X

`epsilon_11 = 0.01`

all other imposed macroscopic strain components zero.

### Load Y

`epsilon_22 = 0.01`

all other imposed macroscopic strain components zero.

### Load XY

`gamma_12 = 0.01`

therefore

`epsilon_12 = epsilon_21 = 0.005`.

These three load cases allow construction of the in-plane homogenized
stiffness matrix.

---

## 18. Macroscopic Stress and Strain Definitions

For KUBC/PBC, the imposed macroscopic strain tensor is `E_bar`.

The macroscopic stress shall be defined by gross-RVE averaging:

`Sigma = (1 / A_gross) integral_over_solid sigma dA`.

The void phase contributes zero stress through absence of solid
material.

The gross RVE area remains:

`A_gross = Lx * Ly`.

The microscopic strain is defined only in the solid domain.

For periodic and affine homogenization, consistency between imposed
macroscopic strain and the appropriate volume/boundary measures shall
be explicitly verified.

---

## 19. Homogenized In-Plane Stiffness Tensor

Use stress Voigt vector:

`[sigma_11, sigma_22, sigma_12]`

and strain Voigt vector:

`[epsilon_11, epsilon_22, gamma_12]`.

For the three unit-amplitude-normalized load cases, construct:

`Sigma = C_hom E`.

The complete numerical in-plane stiffness matrix shall be retained.

Do NOT force individual stochastic realizations to be isotropic.

The following shall be diagnostics:

- `C11` versus `C22`;
- `C12` versus `C21`;
- normal-shear coupling terms;
- matrix symmetry;
- positive definiteness.

The tensor rather than one x-direction scalar shall be the primary M8
homogenization object.

---

## 20. Derived Engineering Responses

Where the homogenized stiffness matrix is nonsingular and physically
valid, compute the compliance matrix:

`S_hom = inverse(C_hom)`.

Derived engineering quantities shall include:

`E_x = 1 / S11`

`E_y = 1 / S22`

`G_xy = 1 / S33`

`nu_xy = -S12 / S11`

`nu_yx = -S12 / S22`.

Retain both dimensional and normalized values.

The M7 apparent axial modulus remains separately preserved for
regression/history and is not overwritten.

M9 will lock which of these fields become final ML targets/features.

---

## 21. Homogenization Verification Gates

Before PBC can be accepted, each tested case must satisfy:

1. solver convergence;
2. complete material tagging;
3. correct gross/solid area accounting;
4. periodic slave/master pairing completeness;
5. periodic displacement-fluctuation constraint satisfaction;
6. global force equilibrium;
7. opposing-boundary traction compatibility where measured;
8. finite macroscopic stress and strain;
9. positive-definite symmetrized homogenized stiffness;
10. Hill-Mandel energetic consistency.

Initial numerical tolerances:

- periodic displacement mismatch:
  relative or normalized error <= `1e-8`;
- global equilibrium residual:
  relative error <= `1e-8`;
- homogenized stiffness symmetry:
  `||C-C^T||_F / ||C||_F <= 1e-5`;
- Hill-Mandel relative energy mismatch:
  <= `1e-5`.

These are initial numerical acceptance tolerances.

If solver/discretization evidence demonstrates that a tolerance requires
revision, the revision must be documented rather than silently changed.

---

## 22. Boundary-Condition Comparison Design

BC verification shall be staged.

### Stage BC-1

Use a small deterministic homogeneous or simple inclusion cell to
validate the mathematical implementation.

### Stage BC-2

Use the same geometrically periodized stochastic cells under:

- KUBC;
- PBC.

The comparison shall initially use at least:

- R1;
- R3;

with at least five common realizations per selected size.

Use identical microstructures for paired BC comparisons.

### Stage BC-3

If KUBC and PBC responses remain materially different at the largest
RVE size, the RVE-size study shall quantify whether the gap contracts
with increasing size.

A uniform-traction/SUBC implementation is not mandatory at the start of
M8.

It becomes a conditional validation extension if:

- KUBC/PBC behavior cannot be interpreted;
- an independent benchmark requires it;
- or energetic/bounding verification would materially strengthen the
  conclusion.

---

## 23. Homogeneous Analytical Sanity Check

Before heterogeneous PBC results are trusted, M8 shall verify a
homogeneous plane-stress cell.

For isotropic plane stress:

`C11 = C22 = E / (1 - nu^2)`

`C12 = C21 = nu E / (1 - nu^2)`

`C66 = E / (2 (1 + nu))`.

All coupling components that should vanish must be approximately zero.

The numerical homogenized tensor must reproduce the analytical
homogeneous tensor within an explicitly recorded tolerance.

This test must work for x, y, and shear loading.

---

## 24. Independent Physical/Numerical Validation Plan

M8 shall strengthen validation beyond internal regression.

Candidate independent checks include:

- homogeneous analytical plane-stress recovery;
- Voigt-type upper estimates where assumptions permit;
- Reuss-type lower estimates where meaningful and non-degenerate;
- Hashin-Shtrikman-type comparisons only after confirming the exact
  dimensional/constitutive assumptions;
- Mori-Tanaka-type comparisons only when its assumptions match the
  simulated configuration;
- a selected published numerical homogenization case whose dimensional
  and constitutive assumptions are compatible.

No analytical or published comparison shall be forced into the paper
if its assumptions are incompatible with the current 2D plane-stress
model.

M9 shall lock the final benchmark set and literature-supported
real-material anchors.

---

## 25. Local Defect Metric — Protected Version 1

The protected M7 local candidate remains:

`m7_matrix_vm_annulus_tail10_v1`.

Its strengths established in M7 include:

- real solved-field response;
- physical localization around geometric voids;
- area-weighted upper-tail statistic;
- substantially lower mesh sensitivity than raw maximum stress.

Its known limitation is that annular membership is currently based on
discrete matrix-cell membership.

Therefore changing mesh size changes the represented annulus area.

M8 shall not promote the Version-1 metric to a final ML target without
further geometric/discretization verification.

---

## 26. M8 Local-Metric Verification Strategy

M8 shall compare the protected Version-1 method with at least one
geometry-consistent candidate evaluation.

The preferred candidate is a quadrature-weighted annular evaluation:

- retain the same locked physical annulus definition as M7 Version 1;
- evaluate matrix von Mises stress at quadrature points;
- determine annular membership using physical point coordinates;
- use quadrature weights as physical area weights;
- compute the same upper 10% physical-area tail statistic.

The purpose is not to silently replace M7.

The purpose is to determine whether geometric quadrature reduces
discretization dependence.

If a new metric is accepted, it must receive a new identifier.

The M7 Version-1 identifier shall never be reused for changed semantics.

Raw local maximum stress remains diagnostic only.

---

## 27. Final Target-Mesh Verification

The existing candidate production mesh remains:

`h = 0.02048`.

The principal fine reference remains:

`h = 0.010`.

A coarse diagnostic level:

`h = 0.038`

may be retained where useful.

### Global-response acceptance

For selected stochastic/periodized representative cases and all three
macroscopic load cases, the relative difference between `h=0.02048`
and `h=0.010` shall initially be required to remain:

`<= 1%`

for the primary normalized global stiffness quantities.

### Local-response acceptance

For selected defect-containing cases, compare the accepted local metric
at `h=0.02048` and `h=0.010`.

Initial acceptance targets are:

- median relative difference across verification cases <= 3%;
- no individual verification case > 5%.

If these criteria fail, M8 shall evaluate:

- local refinement around void neighborhoods;
- quadrature-based metric evaluation;
- or a finer global target mesh.

No target mesh shall be accepted solely because the global modulus is
converged while the local target is not.

### 27.1 Defect-Severity Coverage for Local Target Verification

The local target-mesh decision shall not be based only on one mild
defect state.

At least two controlled defect-severity levels shall be included:

- a baseline defect state;
- a higher-severity state that remains geometrically valid.

Where practical, the comparison shall hold the underlying particle
geometry and void centers fixed while changing the controlled void
radius/severity, following the scientific logic already validated in
M7.

The final local-target mesh decision must therefore demonstrate
robustness across more than one defect severity.


---

## 28. Local Refinement Policy

Local mesh refinement is permitted as an M8 candidate only if required
by the final local-response verification.

If introduced, it must:

- preserve conformal true-hole geometry;
- preserve matrix/particle tagging;
- preserve periodic boundary compatibility where PBC is used;
- have a deterministic refinement rule;
- record bulk and local target sizes;
- be compared against a sufficiently fine uniform reference.

Local refinement shall not be introduced merely to obtain visually
smoother stress contours.

---

## 29. RVE Study Execution Order

After this document is reviewed and checkpointed, M8 scientific
implementation shall proceed in the following order:

1. PBC/software-backend capability experiment;
2. homogeneous analytical homogenization prototype;
3. periodized particle-geometry prototype;
4. periodic meshing/boundary-pair validation;
5. x/y/shear PBC solver prototype;
6. KUBC/PBC paired verification;
7. regression-suite revalidation;
8. controlled RVE-size pilot;
9. full multiple-realization RVE study;
10. controlled defect-state confirmation;
11. final global target-mesh verification;
12. local-metric geometric/discretization study;
13. final target-mesh/local-target decision;
14. M8 documentation and closure.

Each item must still be executed through one-step terminal gates.

---

## 30. Failure and Stop Rules

A case shall not be silently discarded.

Failures must retain:

- case identity;
- particle seed;
- void seed where relevant;
- requested geometry;
- realized geometry;
- failure stage;
- failure reason;
- mesh information where mesh generation began;
- solver diagnostics where solve began.

If a geometry state has systematically high rejection probability, M8
shall treat that as a design finding rather than repeatedly sampling
until only convenient geometries remain.

---

## 31. M8/M9 Scope Boundary

M8 owns:

- controlled RVE-size/statistical-representativity verification;
- snapshot versus periodized representation decision;
- final homogenization BC/PBC verification;
- macroscopic loading/response semantics;
- full in-plane homogenization interpretation;
- final target-mesh verification;
- local-response discretization verification;
- methodology-specific benchmark evidence;
- continued regression protection.

M8 does NOT own final production parameterization.

M9 owns:

- final physical/nondimensional parameter ranges;
- literature-supported parameter ranges;
- one or preferably two real-material anchor systems;
- production-grade requested-versus-realized particle-fraction policy;
- production-grade requested-versus-realized void-fraction policy;
- final particle/void distributions;
- final seed/provenance semantics;
- final dataset schema;
- final ML response field names;
- final benchmark set;
- stochastic pilot dataset;
- end-to-end failure/provenance audit.

M8 validation-only fractions and radii shall not silently become M9
production ranges.

---

## 32. Publication-Facing Interpretation Guard

M8 results may support statements about the defined normalized
two-dimensional linear-elastic composite class.

They shall not support claims about all materials.

A finite stochastic realization shall not be called isotropic merely
because the constituent materials and generating process are
statistically isotropic.

One x-loading result shall not be called the full isotropic effective
Young's modulus.

Any eventual isotropy claim must be based on the homogenized tensor and
statistical evidence across realizations.

---

## 33. Software Environment Guard

The validated environment currently contains:

- Python 3.12;
- NumPy 2.5.1;
- SciPy 1.18.0;
- Gmsh 4.15.2;
- DOLFINx 0.11.0;
- UFL 2026.1.0;
- petsc4py 3.25.4;
- mpi4py 4.1.2.

At Phase-C preflight:

`dolfinx_mpc` was NOT installed.

No package shall be installed into the validated environment as an
incidental side effect of scientific implementation.

Any dependency change requires:

1. explicit purpose;
2. compatibility verification;
3. environment impact review;
4. reproducible installation record;
5. regression-suite revalidation.

---

## 34. Literature Basis Used for M8 Design

The design is informed by the following primary literature.

### RVE statistical representativity

T. Kanit, S. Forest, I. Galliet, V. Mounoury, D. Jeulin.

"Determination of the size of the representative volume element for
random composites: statistical and numerical approach."

International Journal of Solids and Structures, 40, 3647-3679, 2003.

DOI:

`10.1016/S0020-7683(03)00143-4`

### Periodized versus snapshot matrix-inclusion ensembles

M. Schneider, M. Josien, F. Otto.

"Representative volume elements for matrix-inclusion composites -
a computational study on the effects of an improper treatment of
particles intersecting the boundary and the benefits of periodizing
the ensemble."

Journal of the Mechanics and Physics of Solids, 158, 104652, 2022.

DOI:

`10.1016/j.jmps.2021.104652`

### Periodization-bias theory

N. Clozeau, M. Josien, F. Otto, Q. Xu.

"Bias in the representative volume element method: periodize the
ensemble instead of its realizations."

Foundations of Computational Mathematics.

DOI:

`10.1007/s10208-023-09613-y`

### Linear-elastic random/systematic error and fixed-fraction control

S. K. Ravichandran, B. H. Nguyen, M. Schneider.

"Quantifying the systematic and the random error for linear elastic
particle-reinforced composites and reducing the variance by fixing the
volume fraction."

Computational Mechanics, 77, 935-955, 2026.

DOI:

`10.1007/s00466-025-02694-2`

This work directly reinforces the need to distinguish random error from
systematic bias and provides current evidence that controlled volume
fraction can be used as a variance-reduction strategy.

It is methodological support rather than a direct validation benchmark
for the present two-dimensional plane-stress model.

### Recent parameter-dependence of RVE size

X. Shi, M. Chen, J. Zhang, J. Shao.

"Representative volume element size for elastic modulus of random
composites."

International Journal of Mechanical Sciences, 321, 111659, 2026.

DOI:

`10.1016/j.ijmecsci.2026.111659`

This study provides recent evidence that RVE size can depend on
inclusion volume fraction, inclusion geometry/size distribution,
elastic-modulus ratio and inclusion gathering.

It therefore supports reporting the M8 RVE decision together with its
tested microstructural/constitutive envelope rather than treating one
validation state as universal.

It is not used as a direct numerical benchmark for the present model.


These references motivate the statistical and periodization questions.

They do not replace direct validation of the present mechanical model.

---

## 35. Software Documentation Basis

The Phase-C preflight verified that the current official FEniCSx
documentation lists the DOLFINx 0.11 release family.

DOLFINx-MPC documentation exposes multi-point periodic-constraint APIs,
but the package was not installed in the validated project environment
at Phase-C preflight.

A software API being available does not by itself establish
compatibility with this specific environment.

Compatibility must be tested before dependency adoption.

---

## 36. M8 Design Acceptance Condition

This design record is not considered permanent until:

1. its complete contents are reviewed;
2. the permanent 15-test regression suite still passes;
3. repository scope contains only this intended document;
4. its SHA-256 is recorded;
5. no protected M0-M7 source changed;
6. Git diff checks pass;
7. the document is checkpointed only after explicit validation.

Until then:

**M8 scientific implementation remains NOT STARTED.**
