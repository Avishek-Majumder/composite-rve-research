# M7 Version-1 Circular Void Scientific Design

## Status

Milestone:

M7 — Circular Void Defects + Defect-Sensitive Response Definition

This document records the scientific and implementation decisions that
must be explicit before permanent M7 void code is introduced.

The validated M6 implementation remains unchanged and serves as the
regression foundation.

---

## 1. Preserved mechanics

M7 preserves the following established mechanics unless a later,
explicitly announced validation step changes them:

- two-dimensional computational representation;
- small-strain linear elasticity;
- plane stress;
- isotropic matrix;
- isotropic reinforcing particles;
- perfect matrix-particle bonding;
- RVE width = 1.0;
- RVE height = 1.0;
- matrix Young's modulus = 1000.0;
- matrix Poisson's ratio = 0.30;
- particle Young's modulus = 10000.0;
- particle Poisson's ratio = 0.25;
- prescribed x displacement = 0.01;
- current M6 left-x, right-prescribed-x, bottom-left-y restraint;
- effective axial modulus and effective Poisson response remain useful
  global response quantities;
- raw local stress maxima remain diagnostic only.

No PBC is introduced in M7.

Final homogenization BC/PBC verification remains M8.

The M5/M6 mesh size 0.02048 remains a validation/reference mesh.
M7 may use multiple meshes to study the defect-sensitive response,
but final stochastic target-mesh verification remains M8.

---

## 2. Version-1 void physical representation

A Version-1 defect is a true circular geometric hole.

A void is NOT represented as:

- an elastic third material;
- a very-soft pseudo-material;
- a damaged particle;
- a particle-matrix debond;
- a crack.

The void contains no two-dimensional material cells.

Its internal boundary is traction free.

This isolates geometric matrix porosity as the Version-1 defect
mechanism and avoids conflating porosity with particle failure,
debonding, cracking, or a constitutive damage model.

---

## 3. Void location restriction

Version-1 voids are matrix-phase voids.

A valid void must remain completely separated from:

1. every reinforcing particle;
2. every other void;
3. the external RVE boundary.

Therefore M7 must explicitly support:

- minimum void-particle surface spacing;
- minimum void-void surface spacing;
- minimum void-boundary surface spacing.

Version-1 configured minimum void-spacing values must be finite and
strictly positive.

A valid generated geometry must preserve those positive clearances.
A small numerical tolerance may be used only for floating-point
comparison; it must not turn physical tangency into an accepted
Version-1 geometry.

Version-1 voids must not:

- cut through particles;
- lie inside particles;
- touch particles;
- touch or intersect another void;
- touch or intersect the external RVE boundary.

Particle voids, interfacial voids, particle cracking and debonding are
outside the Version-1 defect model.

---

## 4. Void generation architecture

M7 must NOT rewrite or silently alter the validated M6 particle
generator.

Instead, the permanent M7 void generator should consume an already
valid M6 geometry record and augment it with deterministic void
geometry.

This preserves:

- the original M6 particle realization;
- particle seed provenance;
- arrangement family provenance;
- exact M6 regression capability.

Void generation receives its own independent random seed.

Proposed Version-1 void-placement family:

    random_uniform_matrix_void_rejection_v1

Version-1 does not require clustered void placement.

The particle arrangement may still be either validated M6 family:

    random_uniform_rejection_v1

or:

    clustered_bounded_disk_rejection_v1

The void generator therefore varies defects independently on top of
an existing particle microstructure.

---

## 5. Required Version-1 void parameters

The M7 geometry schema must explicitly record at least:

- void seed;
- requested void count;
- void radius minimum;
- void radius maximum;
- minimum void-particle spacing;
- minimum void-void spacing;
- minimum void-boundary spacing;
- maximum placement attempts;
- placement algorithm/version;
- NumPy version;
- random bit generator;
- source M6 geometry provenance.

Each generated void must record:

- void ID;
- center x;
- center y;
- radius.

---

## 6. Required geometry diagnostics

The generated M7 metadata must distinguish valid from invalid geometry.

It must report explicit failure reasons.

Required diagnostics include at least:

- requested void count reached;
- minimum void-particle surface gap;
- minimum void-void surface gap;
- minimum void-boundary surface gap;
- particle spacing still valid;
- particle-boundary spacing still valid;
- analytical particle area;
- analytical particle area fraction;
- analytical void area;
- analytical void area fraction;
- analytical solid area;
- matrix area;
- total placement attempts.

For this two-dimensional model use:

- particle area fraction;
- void area fraction;
- 2D particle fraction;
- 2D void fraction.

Do not describe these as measured true 3D volume fractions.

---

## 7. Version-1 meshing topology

The permanent M7 mesher should be implemented separately from the
validated M6 mesher.

The intended OpenCASCADE topology is:

1. create the rectangular RVE;
2. create circular void disks;
3. subtract the void disks from the RVE material region;
4. create the particle disks;
5. fragment the remaining matrix region with the particle disks so
   matrix-particle interfaces are conformal;
6. synchronize OpenCASCADE;
7. identify and validate matrix, particle and void-boundary entities;
8. create physical groups;
9. generate the two-dimensional mesh;
10. transfer physical tags to DOLFINx;
11. verify geometry and topology numerically.

This design intentionally combines geometric subtraction for holes
with conformal fragmentation for material interfaces.

---

## 8. Physical tagging

Preserve the established material-cell meaning:

    matrix cell tag   = 1
    particle cell tag = 2

A void receives no 2D material-cell tag because no material exists
inside the hole.

The M7 mesher must additionally create a physical facet group named:

    void_boundary

for the internal circular hole boundaries.

The exact facet-tag integer must be explicit and tested in the
permanent mesher.

The void-boundary tag is needed for:

- topology verification;
- later void-neighborhood response extraction;
- possible local mesh controls;
- provenance and diagnostics.

---

## 9. Area accounting with voids

Define:

    gross_rve_area = width * height

    particle_area = sum of particle disk areas

    void_area = sum of void disk areas

    matrix_area =
        gross_rve_area
        - particle_area
        - void_area

    solid_area =
        matrix_area
        + particle_area

Therefore:

    solid_area =
        gross_rve_area
        - void_area

The permanent M7 mesh must verify these relations against CAD and
DOLFINx mesh integration.

Unlike M6:

    matrix_area + particle_area

is NOT equal to the gross RVE area once voids exist.

This distinction must never be hidden.

---

## 10. Void-aware macroscopic stress normalization

The M6 solver currently averages stress over its entire material
domain, which equals the full RVE area because M6 contains no void.

That denominator cannot be reused silently after geometric holes are
introduced.

For the porous M7 RVE, the provisional macroscopic axial stress will
use the gross RVE reference area:

    macro_sigma_xx =
        integral_over_solid(sigma_xx dA)
        / gross_rve_area

The void contributes zero stress because it contains no material.

The imposed macroscopic axial strain remains:

    macro_epsilon_xx =
        prescribed_x_displacement / width

A provisional void-aware apparent axial modulus is therefore:

    E_eff_void =
        macro_sigma_xx
        / macro_epsilon_xx

This definition is for M7 defect trend and consistency validation.

Final homogenization BC/PBC verification remains M8.

The existing M6-style solid-domain averages should be retained where
useful as clearly named regression diagnostics rather than silently
relabelled as the porous macroscopic average.

---

## 11. Effective Poisson response

M7 must not silently assume that the old M6 solid-domain
average-epsilon-yy definition is automatically the final porous-RVE
homogenized lateral response.

During M7 it may be retained as a regression/diagnostic quantity.

Any new void-aware macroscopic lateral-strain definition must be
explicitly defined and verified before being promoted.

Final homogenization interpretation remains subject to M8 BC/PBC
verification.

---

## 12. Defect-sensitive stress response

Raw element-wise or point-wise maximum stress remains diagnostic only.

M7 must not declare:

- maximum sigma_xx;
- maximum von Mises stress;
- maximum principal stress;

as the final downstream ML target merely because the solver can
calculate them.

The primary M7 candidate family will instead be a normalized,
region-based high-stress statistic in matrix material surrounding
the voids.

Conceptually:

    K_sigma =
        robust_high_stress_statistic_in_void_neighborhood
        / abs(macro_sigma_xx)

The void-neighborhood statistic must:

- use matrix material only;
- use a geometrically defined physical neighborhood around voids;
- avoid dependence on a single integration point or element;
- account for cell/area weighting where necessary;
- remain reproducible;
- be evaluated over multiple mesh sizes;
- show acceptable mesh robustness before becoming a primary ML
  response.

Candidate stress fields may include:

- von Mises stress;
- maximum principal tensile stress;
- axial stress.

Candidate robust statistics may include:

- area-weighted high percentiles;
- area-averaged upper-tail stress;
- physically defined annular-region averages.

The final field, neighborhood and statistic are NOT locked by this
document.

They must be selected from M7 validation evidence.

### 12.1 Version-1 validation candidate selected after STEP 564

STEP 564 completed the local-response implementation preflight and
confirmed that the required cell-field, interpolation and geometry
capabilities are available in the validated software environment.

The following metric is therefore locked as the FIRST M7
defect-sensitive validation candidate:

    metric_id =
        m7_matrix_vm_annulus_tail10_v1

This decision does NOT yet promote the metric to the final downstream
machine-learning target. Promotion requires the controlled physical
trend and response-specific mesh-robustness evidence required later in
M7.

#### Stress field

Use the plane-stress von Mises equivalent stress in MATRIX MATERIAL
ONLY:

    sigma_vm =
        sqrt(
            sigma_xx^2
            - sigma_xx * sigma_yy
            + sigma_yy^2
            + 3 * tau_xy^2
        )

Particle cells are excluded from the statistic.

Void interiors contain no material cells and therefore cannot
contribute.

The von Mises field is used here as a scalar stress-concentration
indicator. It is NOT interpreted as a validated matrix failure,
yielding or damage criterion because Version 1 contains no plasticity,
failure or damage constitutive model.

#### Geometric void neighborhood

For void i with center c_i and radius r_i, define its Version-1
matrix-neighborhood annulus using cell midpoint x_c:

    r_i
        < distance(x_c, c_i)
        <= 2 * r_i

Only cells carrying the matrix material tag are eligible.

For multiple voids, the neighborhood is the UNION of all qualifying
matrix cells.

A cell satisfying more than one void annulus is counted exactly once.

The outer radius therefore scales with the physical void radius rather
than with mesh size.

The midpoint rule is an explicit discrete neighborhood-selection rule
and must itself be tested through the M7 response-specific mesh study.

#### Robust upper-tail statistic

Let A_N be the total physical area of all matrix cells in the union
void neighborhood.

Set:

    upper_tail_area_fraction = 0.10

Sort neighborhood matrix cells by sigma_vm from highest to lowest.

Accumulate physical cell area until exactly:

    0.10 * A_N

has been included.

If the final cutoff cell would exceed the required upper-tail area,
use only the required fractional area weight from that final cell.

Define:

    sigma_vm_tail10 =
        area_weighted_mean_sigma_vm
        over the highest-stress 10 percent
        of neighborhood matrix area

This definition intentionally uses physical cell-area weighting rather
than treating every mesh cell as an equal statistical observation.

#### Normalized defect-sensitive candidate

Define:

    K_vm_tail10 =
        sigma_vm_tail10
        / abs(macro_sigma_xx)

where macro_sigma_xx is the already validated M7 gross-RVE
macroscopic axial stress.

A valid positive-void record therefore requires:

    abs(macro_sigma_xx) > 0

and a non-empty positive-area matrix neighborhood.

#### Zero-void behavior

For a zero-void regression case there is no void neighborhood.

Therefore:

    K_vm_tail10 = not_applicable

It must NOT be silently encoded as physical zero.

The global M7 response and M6 zero-void regression remain valid
independently of this local metric.

#### Diagnostics retained

The following may be recorded for validation/diagnostic purposes:

- neighborhood matrix-cell count;
- neighborhood matrix area;
- upper-tail effective area;
- raw maximum neighborhood sigma_vm;
- area-weighted neighborhood mean sigma_vm;
- sigma_vm_tail10;
- K_vm_tail10;
- per-mesh extraction status.

The raw maximum remains diagnostic only and must not replace
K_vm_tail10 merely because it has a larger numerical value.

#### Acceptance before promotion

This Version-1 candidate may become a primary downstream response only
after M7 demonstrates:

- deterministic extraction for identical geometry, mesh and seeds;
- finite and reproducible positive-void values;
- controlled defect-severity behavior with fixed underlying particle
  geometry;
- explicit rejection/reporting of response-extraction failures;
- response-specific comparison over multiple mesh sizes;
- acceptable mesh robustness of K_vm_tail10;
- continued separation between M7 validation evidence and the later
  final M8 production target-mesh verification.

If these checks fail, the metric must be revised explicitly rather
than silently changing its field, neighborhood, upper-tail fraction or
normalization.

---

## 13. Required M7 trend checks

Before accepting the void implementation, M7 must demonstrate
physically coherent trends under controlled comparisons.

Controlled comparisons must hold the underlying M6 particle geometry
fixed while changing only the void realization or void severity when
the purpose is to isolate the defect effect.

Examples of required questions include:

- Does adding void area reduce apparent axial stiffness in controlled
  comparisons?
- Does increasing void severity produce a sensible change in the
  defect-sensitive stress response?
- Are results deterministic for identical particle and void seeds?
- Are invalid particle/void geometries rejected before meshing/FEM?
- Does the no-void limit reproduce the validated M6 mechanics?

No trend may be attributed purely to void severity if particle
geometry, particle area fraction or other confounding parameters also
changed.

---

## 14. Failure handling and provenance

Permanent M7 records must preserve enough information to distinguish:

- geometry-generation failure;
- CAD/topology failure;
- mesh failure;
- physical-tag failure;
- solver failure;
- response-extraction failure.

Failure reasons must be explicit and machine readable.

Successful records must preserve:

- source M6 geometry identity/provenance;
- particle seed;
- void seed;
- geometry schema/version;
- mesher schema/version;
- solver/result schema/version;
- material assumptions;
- loading;
- mesh size;
- particle area fraction;
- void area fraction;
- geometry checks;
- mesh checks;
- PETSc convergence state;
- response-definition version.

---


## 14A. Version-1 local-response validation evidence

The Version-1 local response
`m7_matrix_vm_annulus_tail10_v1` has completed its M7
validation-candidate checks.

This section records the evidence actually observed. It does not impose
a retrospective numerical acceptance threshold and does not claim a
formal Richardson-extrapolation or Grid Convergence Index analysis.

### Controlled defect-severity evidence

A fixed underlying six-particle realization and fixed two-void center
locations were used. Only both void radii were multiplied by a common
scale.

The tested common radius scales were:

- 0.50;
- 0.75;
- 1.00;
- 1.10.

The corresponding void area fractions were:

- 0.0016127410222277249;
- 0.0036286673000123807;
- 0.0064509640889108995;
- 0.007805666547582189.

At the M7 reference mesh size `h = 0.02048`, apparent axial modulus
decreased strictly as void severity increased:

- scale 0.50: 1085.0365519439365;
- scale 0.75: 1079.8227575683811;
- scale 1.00: 1071.8890527671476;
- scale 1.10: 1067.891679487993.

The corresponding `K_vm_tail10` values were:

- scale 0.50: 1.8133452206383758;
- scale 0.75: 1.9313331459247476;
- scale 1.00: 1.8289987573743496;
- scale 1.10: 1.8715610121388946.

No monotonic direction is required for `K_vm_tail10`. The controlled
study demonstrated that the metric responds to defect severity while
the global stiffness response follows the expected decreasing trend.

The transformed scale-1.00 case reproduced the original source
geometry's global response, local response and solver record exactly.

### Response-specific mesh evidence at scale 1.00

The same physical geometry was evaluated at three verifier-valid mesh
sizes:

- `h = 0.03800`;
- `h = 0.02048`;
- `h = 0.01000`.

The respective cell counts were:

- 1976;
- 6046;
- 23675.

The `K_vm_tail10` values were:

- 1.8397895885212097;
- 1.8289987573743496;
- 1.820025149678451.

Relative to the finest tested comparison mesh `h = 0.01000`, the
`h = 0.02048` differences were:

- apparent axial modulus: 0.002493056480088191;
- `sigma_vm_tail10`: 0.007435834006159118;
- `K_vm_tail10`: 0.004930485547127743;
- raw maximum von Mises stress: 0.13627808739202557.

The finest tested mesh is a comparison reference only and is not
declared to be the exact continuum solution.

### Extreme-severity mesh spot checks

The low-severity scale 0.50 and high-severity scale 1.10 cases were
also compared between `h = 0.02048` and `h = 0.01000`.

For scale 0.50:

- `K_vm_tail10` relative difference:
  0.035741662489806474;
- `sigma_vm_tail10` relative difference:
  0.034880717785263936;
- raw maximum von Mises relative difference:
  0.11871579520020649;
- apparent axial modulus relative difference:
  0.0008928568943107427.

For scale 1.10:

- `K_vm_tail10` relative difference:
  0.025530948181384218;
- `sigma_vm_tail10` relative difference:
  0.028155315078885666;
- raw maximum von Mises relative difference:
  0.11439791710509453;
- apparent axial modulus relative difference:
  0.0025590323745521733.

Across the tested low, baseline and high severity cases, the largest
observed `h = 0.02048` versus `h = 0.01000` relative difference in
`K_vm_tail10` was therefore 0.035741662489806474.

This observed value is an evidence summary, not a newly imposed
post-hoc pass/fail threshold.

### M7 decision

`m7_matrix_vm_annulus_tail10_v1` is accepted as the Version-1
defect-sensitive **M7 validation candidate**.

This means that it may be used for the remaining M7 validation work
because it has demonstrated:

- deterministic extraction for identical input and mesh;
- valid real solved-field extraction;
- controlled defect-severity sensitivity;
- substantially lower mesh sensitivity than the raw local stress
  maximum in the tested cases;
- response-specific mesh evidence across low, baseline and high
  severity cases.

The raw local stress maximum remains diagnostic only.

This M7 decision does **not** promote `K_vm_tail10` to the final
machine-learning target and does **not** establish final production
mesh adequacy.

Final stochastic target-mesh verification, final homogenization
boundary-condition/PBC verification and any final ML-target promotion
remain M8 responsibilities.


## 15. M7/M8 scope boundary

M7 owns:

- circular matrix void geometry;
- void validity rules;
- void provenance;
- void-capable conformal topology/meshing;
- void-capable FEM solution;
- controlled defect trend checks;
- robust defect-sensitive response definition;
- M7 response-specific mesh robustness evidence.

M7 does NOT own:

- final RVE-size/statistical-representativity study;
- final homogenization BC/PBC selection;
- final production stochastic target-mesh verification;
- final stochastic parameter-space lock;
- stochastic pilot dataset;
- production FEM database;
- machine-learning training.

Those remain in later milestones, beginning with M8.

---

## 16. Implementation protection rule

Validated M6 permanent files must remain intact.

M7 should add new versioned files rather than converting the M6
generator, mesher or solver in place.

This preserves:

- reproducibility;
- exact M5/M6 regression capability;
- milestone provenance;
- clean scientific comparison between no-void and void-aware paths.
