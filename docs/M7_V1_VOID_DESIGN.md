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
