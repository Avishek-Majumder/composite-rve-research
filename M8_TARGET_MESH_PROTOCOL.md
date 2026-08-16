# M8 Final Target-Mesh and Local-Response Verification Protocol

## Status

**Permanent protocol — repository authority after authenticated installation.**

This document defines the operational protocol for the remaining M8
target-mesh and local-response verification stage.

This protocol does not itself claim target-mesh closure. Closure requires
successful execution and authentication of the scientific gates defined
below, followed by a separate permanent target-mesh checkpoint.

The already completed M8 RVE-size decision is not reopened.

## Permanent authority used by this protocol

- repository authority: `09f51200621c111214087a54fed4d0fca6f2d20f`
- M8 design record SHA-256: `6f645daa72dbffd7fb532315cad7518e8d6c6fa969104d7cd0aaaa1ca3625fa2`
- M8 permanent RVE protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- M8 permanent representativity checkpoint SHA-256: `0f129f26c63dbf173572189d6c28ef43cf310920f2f5d1c5e1775ab8649fe420`
- M7 design record SHA-256: `6bae86aa2302d2173ca235cc320af59dc326c4924143138ccadabdb6b014d814`

## Scientific scope

The remaining M8 verification remains limited to the established model
class:

- two-dimensional small-strain linear elasticity;
- plane stress;
- isotropic matrix and particle phases;
- perfectly bonded matrix-particle interfaces;
- circular particles;
- circular matrix-phase true geometric voids where defect cases are used;
- normalized/dimensionless publication-facing responses.

No claim of applicability to all materials is permitted.

## Representative RVE authority

The permanent M8 RVE-size checkpoint has already accepted:

- RVE level: R1
- side length: 1.0
- area: 1.0
- physical particle count: 16

The target-mesh study shall use R1.

The RVE-size study itself shall not be rerun merely because the target
mesh is changed.

## Stochastic verification-case policy

To avoid response-based case selection, the global target-mesh study
shall use **all six predetermined R1 particle realizations** from the
permanent RVE protocol.

No R1 realization shall be selected or omitted because its stiffness,
anisotropy, coupling, mesh response or local stress happens to be
convenient.

The target-mesh study shall reuse the already-generated and
independently authenticated R1 particle-geometry artifacts from the
completed RVE-size study.

An R1 particle geometry shall not be regenerated merely from the same
seed while its authenticated existing geometry artifact is available.

The existing physical particle centers, IDs, radii, periodic
representations and geometry identity must remain unchanged across the
target-mesh comparison.

## Deterministic R1 particle / void grouping

| R1 realization | Permanent particle seed | Void-seed material | Proposed void seed |
|---:|---:|---|---:|
| 1 | 15944426988753885521 | `m8-target-mesh-v1|R1|0001|void` | 3207221261761373063 |
| 2 | 14726087059387717211 | `m8-target-mesh-v1|R1|0002|void` | 14490274562564534771 |
| 3 | 16304908395315497179 | `m8-target-mesh-v1|R1|0003|void` | 67375861801655713 |
| 4 | 8543608591806175946 | `m8-target-mesh-v1|R1|0004|void` | 17970057940181508297 |
| 5 | 9043192476962390047 | `m8-target-mesh-v1|R1|0005|void` | 14626328133499005643 |
| 6 | 4715493001954948121 | `m8-target-mesh-v1|R1|0006|void` | 10523488795245530389 |

Void seeds are derived as:

`SHA256("m8-target-mesh-v1|R1|iiii|void")`

using the first eight digest bytes interpreted as an unsigned
big-endian integer.

These seeds are provenance/grouping metadata only.

## Final target-mesh ladder

The historical M8 design ladder is retained:

- candidate production mesh: `h = 0.02048`
- principal fine reference: `h = 0.010`
- optional coarse diagnostic: `h = 0.038`

The coarse mesh is diagnostic only and is not required for acceptance
when the reference/candidate comparison is already decisive.

The fine mesh is a numerical comparison reference and is not claimed to
be the exact continuum solution.

## Global-response verification

Each of the six pristine R1 periodized particle geometries shall be
meshed independently at:

- `h = 0.02048`
- `h = 0.010`

For each geometry and each mesh, execute all three permanent M8 PBC load
cases:

- X
- Y
- XY engineering shear

The same geometry identity, constituent properties, PBC formulation and
load amplitudes must be preserved across the two meshes.

For each mesh, assemble the complete in-plane homogenized stiffness
tensor and retain:

- `C / E_matrix`
- `E_x / E_matrix`
- `E_y / E_matrix`
- `G_xy / E_matrix`
- `nu_xy`
- `nu_yx`
- `C16 / E_matrix`
- `C26 / E_matrix`
- all permanent numerical hard-gate diagnostics.

### Global target-mesh hard gate

The operational interpretation of the historical `<= 1%` global rule
for this protocol is deliberately conservative:

For **every one of the six R1 realizations**, each of

- `E_x / E_matrix`
- `E_y / E_matrix`
- `G_xy / E_matrix`

must have absolute relative difference between `h=0.02048` and
`h=0.010` no greater than 1%.

The complete normalized stiffness tensor remains recorded and audited,
but relative-percentage hard gates shall not be imposed on near-zero
normal-shear coupling terms.

For every positive primary response `q`, define the target-mesh
relative difference as:

`delta_q = abs(q_h02048 - q_h0010) / abs(q_h0010)`

where:

- `q_h02048` is the response obtained at `h = 0.02048`;
- `q_h0010` is the response obtained at `h = 0.010`.

The `h = 0.010` response is therefore the explicit comparison
denominator.

A non-finite or non-positive `h = 0.010` primary response cannot be
converted into a percentage PASS. It is a scientific failure requiring
diagnosis.

No ensemble averaging may hide an individual primary-response mesh
failure.

## Controlled M8 defect state

Before final target-mesh closure, M8 must confirm a periodized
defect-containing R1 path.

The baseline state uses the historical M8 validation construction:

- void count: 4
- baseline void radius: 0.025000000000000
- analytical baseline void fraction: 0.00785398163397448

A second higher-severity state is required.

This protocol locks the M7-validated radius-scaling logic for M8 validation:

- high-severity radius factor: 1.10
- high-severity void radius: 0.027500000000000
- analytical high-severity void fraction: 0.00950331777710913

The `1.10` factor is a **new M8 protocol choice derived from the
previously validated M7 severity logic**. It is not represented as a
value that had already been permanently locked for M8.

The baseline and high-severity states must use:

- identical underlying R1 particle geometry;
- identical void IDs;
- identical void centers;
- identical void seed;
- only the common void radius/severity changed.

## Periodized-void geometry requirements

M8 shall implement a new periodized-void extension without mutating the
protected M7 schemas or the existing pristine M8 schemas.

Void centers shall be interpreted on the same periodic torus as the M8
particle geometry.

Unlike the protected bounded M7 void construction, this periodized M8
construction shall impose **no minimum void-to-external-boundary
clearance**.

A void is permitted to cross an outer computational-cell boundary
because it represents one physical object on the periodic torus.

All void-particle and void-void spacing calculations shall use the
minimum-image/toroidal distance, including interactions across opposite
outer boundaries.

The same physical void crossing an outer boundary must be represented
through periodic images/cut pieces without double counting analytical
void area.

For this M8 validation protocol:

- minimum toroidal void-particle surface gap: `0.02`
- minimum toroidal void-void surface gap: `0.02`
- maximum placement attempts per void: `20000`

These are explicit new M8 validation controls, not M9 production
parameter ranges.

Void-center placement shall be performed using the **high-severity
radius** first.

If that high-severity geometry is valid, the baseline state reuses the
same centers with radius reduced to `0.025`.

This construction guarantees that changing severity does not move the
defect centers.

A deterministic requested case that fails geometric validity shall be
recorded as a failure. It shall not be silently replaced by a more
convenient mechanical realization.

## Controlled defect-state confirmation gate

Before the broad target-mesh execution begins, the first predetermined
case, R1 realization 1, shall be used as the implementation-confirmation
case.

The periodized-void geometry, conformal true-hole periodic mesh, PBC
solve and response extraction must pass all relevant permanent
geometry/mesh/PBC hard gates for both baseline and high severity.

This confirmation is an implementation gate, not the final statistical
target-mesh decision.

## Local-response metric study

The protected M7 identifier

`m7_matrix_vm_annulus_tail10_v1`

shall never be reused for altered M8 semantics.

The physical annulus semantics are retained explicitly.

For void `i` with physical center `c_i`, radius `r_i`, and a matrix
evaluation location `x`, define `d_T(x, c_i)` as the minimum-image
distance on the periodic RVE torus.

The M8 void-neighborhood annulus is:

`r_i < d_T(x, c_i) <= 2 * r_i`

Only matrix material is eligible.

For multiple voids, the neighborhood is the UNION of the individual
annuli.

A physical matrix contribution satisfying more than one void annulus is
counted exactly once.

For the cell-based candidate, `x` is the matrix-cell midpoint.

For the quadrature-based candidate, `x` is the physical quadrature-point
coordinate and the quadrature weight supplies the physical area weight.

M8 shall compare two explicitly new M8 response implementations:

1. `m8_matrix_vm_annulus_cell_tail10_v1`
   - ports the protected M7 cell-membership physical-annulus logic into
     the M8 periodized/PBC setting;
   - uses physical matrix-cell area weighting;
   - uses the upper 10% physical-area stress tail.

2. `m8_matrix_vm_annulus_quadrature_tail10_v1`
   - uses the same physical annulus definition;
   - evaluates annular membership at physical quadrature-point
     coordinates;
   - uses quadrature weights as area weights;
   - uses the same upper 10% physical-area tail definition.

For the M8 X PBC load, define the normalized local response as:

`K_vm_tail10 = sigma_vm_tail10 / abs(Sigma_11)`

where `Sigma_11` is the gross-RVE homogenized macroscopic X-load stress.

Raw maximum von Mises stress remains diagnostic only.

The quadrature implementation must receive its own numerical-validation
gate before full execution. Its quadrature order shall not be silently
chosen without that implementation evidence.

Following the authenticated R1 realization-1 baseline `h = 0.02048` X-load
quadrature sensitivity study, the production quadrature degree is locked to
`8`, the highest qualified candidate in the validated degree range `1..8`.
For degrees `5`, `6`, `7`, and `8`, the authenticated `K_vm_tail10` values
were `1.6964432100582205`, `1.6848696213086505`, `1.6821426180475985`, and
`1.6889435327139473`, respectively. The full degree-5-to-8 range is
`0.846718184097%` relative to the degree-8 value. This sensitivity is bounded
but non-monotonic and is retained as empirical quadrature-sensitivity
provenance; it is not a claim of monotone convergence or mathematical
exactness of the annulus-masked local metric. Degree `4` was deliberately not
required because another lower-order rule would not provide higher-order
evidence for the selected degree-8 production rule.

## Local target-mesh verification case set

After controlled defect implementation is authenticated, use all six R1
particle realizations at both locked defect severities.

This gives:

- 6 baseline-severity cases;
- 6 high-severity cases;
- 12 total local verification cases.

Each case shall be evaluated at:

- `h = 0.02048`
- `h = 0.010`

using the X PBC load required by the `Sigma_11` normalization.

No case shall be removed because its local response is inconvenient.

## Local metric-selection rule

The M7-style cell method and quadrature candidate shall both be retained
during the discretization study.

The final local metric may be selected only after confirming:

- deterministic repeated extraction;
- finite positive-void response;
- identical physical annulus semantics;
- valid gross-RVE normalization;
- acceptable behavior at both severities;
- explicit comparison of mesh dependence.

A new metric may be preferred only with documented evidence.

The protected M7 identifier remains unchanged regardless of the M8
decision.

## Local target-mesh acceptance

For the ultimately accepted M8 local metric, compare `h=0.02048` with
`h=0.010` across all 12 defect-containing verification cases.

For each predeclared defect-containing case, define:

`delta_K = abs(K_h02048 - K_h0010) / abs(K_h0010)`

where `K_h0010` is the `h = 0.010` fine-reference value.

Both compared local responses must be finite, and the fine-reference
`K_h0010` must be strictly positive.

If any one of the 12 predeclared cases has invalid geometry, failed mesh,
failed FEM/PBC mechanics, invalid response extraction, non-finite local
response, or non-positive fine-reference normalization, the final local
target-mesh gate remains unresolved/failed pending diagnosis.

The median local relative difference shall be calculated over exactly
the 12 predeclared valid case differences.

It shall never be calculated over a reduced response-selected subset.

The historical M8 acceptance targets are retained:

- median absolute relative difference <= 3%;
- no individual verification case > 5%.

Both severity levels must be represented in the accepted evidence.

The target mesh shall not be accepted solely because the global
stiffness quantities converge.

If the local criteria fail, M8 must evaluate one or more of:

- deterministic local refinement around void neighborhoods;
- the geometry-consistent quadrature method;
- a finer global target mesh.

The failed evidence shall remain preserved.

## Required scientific execution order

The remaining sequence is locked as:

1. permanent protocol review and installation;
2. periodized-void geometry implementation and validation;
3. periodized true-hole mesh implementation and validation;
4. void-capable PBC X/Y/XY mechanics validation;
5. R1 realization-1 controlled baseline/high-severity confirmation;
6. six-case pristine global target-mesh comparison;
7. local cell/quadrature metric implementation validation;
8. twelve-case two-severity local target-mesh study;
9. final target-mesh/local-target decision;
10. permanent M8 target-mesh checkpoint and M8 closure documentation.

Later work shall not be executed before the preceding scientific gate is
authenticated.

## Scope guard

This protocol does not itself:

- generate geometry;
- generate a mesh;
- construct an MPC;
- run FEM;
- reconstruct existing R1-R5 tensors;
- alter the accepted RVE size;
- alter M0-M7 schemas;
- alter existing pristine M8 schemas;
- select an M9 parameter space;
- create a production database;
- promote a final ML response;
- run machine learning.

## Permanent protocol decision state

After this protocol is installed, committed, pushed and independently
authenticated, the next authorized scientific stage is periodized-void
geometry implementation and validation.

No target-mesh solve is authorized before the required periodized-void
geometry, mesh and mechanics implementation gates are separately
authenticated in the locked scientific execution order.
