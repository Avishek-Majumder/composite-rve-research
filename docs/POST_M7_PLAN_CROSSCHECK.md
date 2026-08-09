# Post-M7 Plan Cross-Check and Unresolved Requirements

**Date:** 9 August 2026

**Repository checkpoint audited:**
`e4d66a4ce674f1d67d6b9c0cdc16d9ae8641dea6`

**Formal milestone state at audit:**

- M0-M7: 100% COMPLETE.
- M8: NOT STARTED.
- Final stochastic defect-sensitive dataset: NOT YET GENERATED.
- Final research ML: NOT READY TO START.

---

## 1. Purpose

This record documents the explicit plan-versus-implementation
cross-check performed after formal M7 closure and before beginning M8.

The audit compared the original research planning, the approved
Secondary Planning roadmap, historical milestone records, the current
repository implementation, and the permanent M6/M7 validation state.

Its purpose is to prevent unresolved scientific or engineering
requirements from being lost as the project progresses.

This document does not reopen M0-M7.

It does not change any validated physics, geometry, mesh, response
definition, source code, schema, or prior milestone result.

It also does not authorize M8 implementation.

---

## 2. Overall Audit Conclusion

The project remains on the correct scientific path.

M0-M7 do not require rollback.

The inserted M4-M5 parametric and baseline-data work remains valid
because it was subsequently reclassified as foundation/baseline work
rather than being treated as the final stochastic research dataset.

M6 restored the required stochastic multi-particle microstructure
foundation.

M7 restored the required circular-defect and defect-sensitive-response
foundation.

The remaining roadmap from M8 onward remains necessary.

The principal audit conclusion is therefore:

> Preserve M0-M7 as formally completed, preserve M8 as NOT STARTED,
> and carry the unresolved requirements in this document forward to
> their explicitly assigned future gates.

---

## 3. Requirements Confirmed as Correctly Completed

The audit found the following major requirements to be aligned with
the research plan.

### 3.1 FEM and homogeneous validation

The project established the two-dimensional small-strain linear
elasticity foundation and analytically verified the homogeneous model
before expanding to heterogeneous composites.

### 3.2 Single-particle composite foundation

The project implemented matrix/particle material tagging, perfect
matrix-particle bonding, conforming meshing, and the first
heterogeneous elasticity response.

### 3.3 Element-level mesh convergence

The project completed element-level mesh-convergence work before
promoting the solver into broader parametric/stochastic use.

This remains distinct from stochastic RVE-size/statistical
representativity.

### 3.4 D0-PB baseline dataset

The M5 dataset remains useful as the centered-single-inclusion
perfect-bonding baseline and pipeline-regression dataset.

It is not the final stochastic defect-sensitive research dataset.

### 3.5 Random and clustered multi-particle geometry

M6 provides deterministic random/clustered multi-particle geometry,
stored random seeds, variable radii/positions, spacing constraints,
failure handling, conformal meshing, and validated elasticity
responses.

### 3.6 Circular matrix voids

M7 implements circular voids as true geometric holes rather than a
soft pseudo-material.

It preserves the underlying M6 particle geometry and records
independent void-seed provenance.

### 3.7 Gross-RVE global response

The permanent M7 global-response identifier is:

`m7_gross_rve_axial_v1`

The corresponding apparent axial response uses the gross RVE reference
area.

### 3.8 Defect-sensitive local response

The permanent Version-1 M7 candidate is:

`m7_matrix_vm_annulus_tail10_v1`

It uses matrix-cell von Mises stress in a void-scaled annular
neighborhood and an area-weighted upper 10% tail mean.

Raw local stress maxima remain diagnostic only.

The candidate is validated for continued research use but is not yet
promoted to the final ML target.

### 3.9 Random/clustered implementation coverage

Both random-particle and clustered-particle M6 branches have been
carried through the M7 geometry/mesh/FEM path.

This validates implementation coverage.

It does not establish a causal random-versus-clustered material-effect
comparison.

---

## 4. Audit Finding A — Target Particle Area-Fraction Control

### 4.1 Current implementation

The permanent M6 generator accepts controls including:

- particle count;
- particle-radius minimum;
- particle-radius maximum;
- particle spacing;
- boundary spacing;
- random seed.

It computes and records the realized:

`particle_area_fraction`

after geometry generation.

### 4.2 Gap

The permanent M6 generator does not currently provide a first-class
requested target particle-area-fraction input with an associated
realization tolerance.

Therefore:

> realized particle area fraction is measured, but final
> target-area-fraction generation is not yet a production-grade
> controlled variable.

### 4.3 Why this matters

Particle area fraction is intended to be an important physical
parameter in the final stochastic study.

It must therefore be possible to distinguish clearly between:

- requested/nominal particle area fraction;
- realized particle area fraction;
- realization tolerance/error.

This is also important when changing RVE size because representativity
comparisons should not be confounded by uncontrolled changes in
nominal reinforcement fraction.

### 4.4 Ownership

M8 must ensure that RVE-size and BC/PBC comparisons use appropriately
controlled nominal particle fraction.

M9 owns the final production-grade parameter-space lock and should
finalize the permanent requested-versus-realized particle-area-fraction
policy before pilot generation.

This finding does not reopen M6.

---

## 5. Audit Finding B — Target Void Area-Fraction Control

### 5.1 Current implementation

The permanent M7 generator accepts controls including:

- void count;
- void-radius minimum;
- void-radius maximum;
- void-particle spacing;
- void-void spacing;
- void-boundary spacing;
- independent void seed.

It computes and records:

`void_area_fraction`

after geometry generation.

### 5.2 Gap

The permanent M7 generator does not currently expose a first-class
target void-area-fraction input with a final realization tolerance.

### 5.3 Why this matters

Void severity/fraction is intended to become a controlled physical
variable in the final defect-sensitive study.

Final production work must therefore distinguish between:

- requested/nominal void area fraction;
- realized void area fraction;
- realization tolerance/error.

### 5.4 Ownership

M8 may use controlled validation geometries as needed for
response/mesh/BC studies.

M9 should finalize the production-grade target void-area-fraction
policy before the stochastic pilot dataset.

This finding does not reopen M7.

---

## 6. Audit Finding C — RVE Representativity Is Still Unresolved

Element-level mesh convergence does not establish stochastic RVE
representativity.

M8 must quantify RVE-size/statistical-representativity behavior across
multiple realizations.

The study should prevent changes in nominal physical parameters from
being mistaken for RVE-size effects.

At minimum, the M8 study must explicitly define:

- RVE sizes tested;
- particle/void parameter states held fixed;
- number of realizations/seeds per state;
- convergence/statistical summary quantities;
- acceptance logic;
- runtime/mesh implications.

No production stochastic database should be generated before this
question is resolved.

---

## 7. Audit Finding D — Homogenization BC/PBC and Microstructure Compatibility

The currently validated displacement boundary conditions remain valid
for the completed baseline/M6/M7 validation work.

They are not yet the final production homogenization strategy.

M8 owns the final homogenization BC/PBC verification.

A specific issue must be considered:

> the current random-particle generator keeps particles strictly
> inside the RVE and enforces external boundary spacing.

Therefore, if periodic boundary conditions are considered for final
production work, M8 must evaluate the compatibility of:

- the stochastic microstructure representation;
- boundary-crossing/periodization policy;
- geometric periodicity requirements;
- displacement constraints;
- homogenized response definition.

M8 must not simply add periodic displacement constraints to the
existing geometry and assume that the resulting stochastic ensemble
is automatically appropriate.

The microstructure representation and homogenization boundary
conditions must be verified together.

---

## 8. Audit Finding E — Final Global-Response Semantics

The permanent M7 response is:

`m7_gross_rve_axial_v1`

and currently reports the x-direction apparent axial modulus under the
validated loading condition.

Before the final stochastic parameter-space/data schema is locked, the
project must explicitly decide whether the primary ML response is
represented as:

- x-direction apparent/effective modulus;
- normalized modulus, for example relative to matrix modulus;
- or a broader in-plane homogenized quantity requiring additional
  loading states.

A finite stochastic RVE can exhibit realization-level directional
anisotropy even when the generating process is statistically
isotropic.

The final manuscript and dataset terminology must therefore avoid
silently equating a single x-loading response with a fully isotropic
effective Young's modulus unless the required verification supports
that interpretation.

### Ownership

M8 should establish the homogenization-response interpretation.

M9 should lock the final dataset field names and normalization policy.

Where useful, both dimensional and normalized responses should be
preserved rather than discarding one representation prematurely.

---

## 9. Audit Finding F — Local-Metric Geometric/Discretization Sensitivity

The M7 local metric showed substantially better mesh behavior than
the raw local maximum and was correctly retained as the Version-1
candidate.

However, the permanent local-neighborhood extraction uses discrete
mesh-cell membership for the scaled void-annulus region.

The M7 validation evidence showed that neighborhood area can change
noticeably with mesh refinement even when the final normalized
`K_vm_tail10` response is comparatively stable.

Therefore M8 must not interpret M7 metric validation as final
production target-mesh verification.

M8 should explicitly examine whether to retain the current
neighborhood-membership method or adopt a more geometrically accurate
integration/local-refinement strategy.

The raw maximum must remain diagnostic only.

---

## 10. Audit Finding G — Additional Independent Validation Remains

The project has strong internal checks including:

- analytical homogeneous verification;
- regression testing through validated terminal workflows;
- element-level mesh studies;
- zero-void regression;
- geometry/mesh/FEM validity gates;
- physical-trend checks.

However, the broader plan retains additional independent validation,
including appropriate analytical/theoretical comparisons and selected
published numerical benchmarks.

Where applicable, future validation should consider comparisons such
as:

- Voigt/Reuss bounds;
- Hashin-Shtrikman-type bounds;
- Mori-Tanaka-type estimates;
- selected published numerical homogenization results.

Not every comparison will be appropriate for every stochastic/defect
case.

The comparison must be physically matched to the assumptions of the
case being tested.

### Ownership

This validation expansion should be completed before approval of the
main production simulation database.

M8/M9 are the appropriate gates to decide and record the final
benchmark set.

---

## 11. Audit Finding H — Permanent Automated Regression Tests Are Missing

At the audited M7 closure checkpoint:

`tests/`

contains only:

`.gitkeep`

There are no permanent automated regression-test files.

This does not invalidate M0-M7 because those milestones were
extensively validated through explicit terminal gates.

However, the codebase is now sufficiently complex that permanent
automated regression protection is desirable before major
homogenization/PBC changes.

High-value initial regression candidates include:

1. pure area-weighted upper-tail numerical tests;
2. zero-void M6-to-M7 global-response regression;
3. deterministic repeated M7 geometry generation;
4. invalid-geometry rejection;
5. schema/response-identifier checks.

This is an engineering/reproducibility safeguard rather than a change
to the research physics.

It should be addressed before or at the M8 implementation preflight,
before invasive homogenization changes are allowed to modify the
solver path.

---

## 12. Audit Finding I — Random Seed Is Provenance, Not a Physical Scalar Feature

Random seeds must continue to be stored permanently because they are
required for deterministic regeneration and provenance.

However, the numeric seed value itself has no direct mechanical
meaning.

For final ML work, the seed should normally serve as:

- realization identifier;
- reproducibility provenance;
- grouping/replicate identifier;
- link between repeated realizations at the same physical parameter
  point.

It should not silently become an ordinary continuous numeric predictor.

Physical microstructure variables and/or derived descriptors should
carry the predictive meaning.

Multiple realizations at common physical parameter states should later
support estimation of microstructure-induced response variability.

### Ownership

M9 should lock seed/provenance semantics.

M10 should generate the required multiple realizations.

M11-M13 should preserve grouping and separate realization variability
from surrogate uncertainty.

---

## 13. Audit Finding J — Literature and Novelty Refresh

The overall combination of FEM-generated RVE data, machine learning,
active learning, and uncertainty-aware modeling is an active research
area.

Therefore the final novelty claim must not rely merely on combining
those broad components.

Before the final parameter space and manuscript claims are locked, the
project should perform a current literature/novelty refresh.

The strongest intended contribution package should be evaluated around
the combined value of:

- explicit circular defect geometry;
- stochastic random/clustered particle microstructures;
- a robust defect-sensitive response;
- controlled active-learning-versus-random FEM-budget comparison;
- calibrated uncertainty;
- separation of realization variability from model uncertainty;
- deliberate OOD evaluation;
- reproducible simulation/data provenance.

This cross-check document records the need for that refresh.

It is not itself the final literature review or novelty claim.

### Ownership

Perform the refresh before or during M9 parameter-space lock and again
during final manuscript preparation if needed.

---

## 14. Audit Finding K — Repository Reproducibility Documentation

The repository has strong milestone/status/design records, but a
publication-facing README/reproduction entry point remains future work.

This is not an M8 blocker.

Before final reproducibility release, documentation should make it easy
to understand:

- research purpose;
- supported environment;
- principal schemas;
- principal scripts;
- validation workflows;
- dataset/provenance organization;
- how to reproduce selected cases.

This belongs to later reproducibility/manuscript preparation unless an
earlier engineering need makes it useful sooner.

---

## 15. Pre-M8 Requirements Carried Forward

The following findings must remain visible when M8 is eventually
announced.

### Required before or during M8

1. Preserve all M0-M7 validated source files and assumptions.
2. Add permanent automated regression protection before invasive
   homogenization/PBC changes.
3. Define a scientifically controlled nominal particle-fraction policy
   for RVE-size comparisons.
4. Define any required controlled void-severity/fraction policy for
   M8 defect-response comparisons.
5. Treat RVE-size convergence separately from element-level mesh
   convergence.
6. Verify microstructure representation and homogenization BC/PBC
   together.
7. Resolve the final homogenized/global-response interpretation.
8. Revisit local-response neighborhood geometric/mesh sensitivity.
9. Establish final primary-target mesh evidence without retroactively
   redefining M7 validation claims.

### Explicitly not completed by M8 alone

M8 must not silently claim completion of:

- final stochastic parameter-space lock;
- production-grade target fraction parameterization for all variables;
- final stochastic pilot dataset;
- main stochastic FEM database;
- final ML target promotion;
- machine-learning training;
- active learning;
- uncertainty calibration;
- OOD evaluation.

Those remain later milestones.

---

## 16. Requirements Carried to M9 and Later

### M9

M9 should explicitly lock:

- final physical parameter space;
- requested versus realized particle-area-fraction policy;
- requested versus realized void-area-fraction policy;
- allowed particle/void size/count distributions;
- seed policy;
- final result schema;
- global-response field naming/normalization;
- provisional/final local-response target status;
- provenance fields;
- failure/status taxonomy;
- selected independent benchmark checks;
- pilot acceptance criteria.

A limited stochastic pilot must pass before main production.

### M10

M10 should generate the main quality-controlled FEM database with
multiple realizations/seeds per relevant physical parameter state.

### M11

M11 should use grouped/leakage-safe validation and must not treat
numeric random-seed values as ordinary physical predictors.

### M12

M12 should compare active learning against random sampling under equal
FEM budgets using repeated runs/seeds.

### M13

M13 should perform quantitative uncertainty calibration, distinguish
realization variability from model uncertainty, and conduct deliberate
OOD evaluation.

### M14

M14 should complete final ablations, figures, reproducibility evidence,
literature/novelty positioning, and manuscript analysis.

---

## 17. Closure Decision from This Cross-Check

The audit decision is:

- M0-M7 remain formally complete.
- M6 is not reopened.
- M7 is not reopened.
- D0-PB remains baseline/regression data only.
- No final stochastic dataset exists yet.
- No final research ML has started.
- M8 remains NOT STARTED.
- The approved M8-M14 roadmap remains the correct high-level path.
- The unresolved requirements in this document must be resolved at
  their assigned future gates.

The next action after this record is validated and checkpointed is not
automatic M8 implementation.

M8 should begin only after an explicit milestone transition
confirmation and an M8 preflight that incorporates this document.
