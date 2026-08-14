# M8 R5 Statistical Pilot Checkpoint

## Status

R5 initial statistical pilot: COMPLETE / PASS.

This checkpoint summarizes the six predetermined R5 realizations.

R5 satisfies the locked primary statistical precision requirement at the initial pilot size n = 6.

No additional R5 realizations are required by the current adaptive precision rule.

**This does NOT declare R5 statistically representative.**

Within the locked initial R1-R5 design, R5 is the largest statistically resolved comparison level. Final RVE representativity requires the locked cross-level size-stability comparisons.

## Repository provenance

- HEAD before checkpoint creation: `12a2febe2c651540f24cb600570686965757998b`
- origin/main before checkpoint creation: `12a2febe2c651540f24cb600570686965757998b`
- remote main before checkpoint creation: `12a2febe2c651540f24cb600570686965757998b`
- protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- R1 checkpoint SHA-256: `df2a4efc79eedfa1b0b3778fb28eee802468f1cdb036755d156552b75e853ff7`
- R2 checkpoint SHA-256: `d8dfc366074615d43ed78a3958ac811dbc760cedb40fbddc4486065ef3abd6d4`
- R3 checkpoint SHA-256: `24ea2ec56d76281b16f59225e96f45be759550bda6c3993b63bf2d547b723056`
- R4 checkpoint SHA-256: `9850bb698e054d777b832fdf56f0b6888e88b8630c344cfda42714662a12eaba`
- periodized generator SHA-256: `63dc1bcd24324589f069013fc5f730477ece944b9c79626d8e7f94f7b3b30187`
- periodized mesher SHA-256: `0713c46add5395bce97d8bdf03e52050310889935921f306d958be076d9cc3cc`
- PBC solver SHA-256: `90079e56df7f2a74cac3b301e81cbaa0ea520ebcd1987f1ac7f81f4a6ee12e5b`
- material/config SHA-256: `f9dbb565bc2eeaa9166eac4a721de1f1d1f47474ecaf13ec567c5627614351dd`
- periodic-corner regression test SHA-256: `b89762fff46bb2810344099432be913efd878712bf9568554c969ec74c88c6f7`
- tracked/non-ignored repository state before checkpoint creation: clean

## Locked R5 design

- RVE level: R5
- side length: 3.0
- area: 9.0
- physical particle count: 144
- particle radius: 0.05
- particle number density: 16.0
- analytical particle area fraction: 0.12566370614359174
- common screening mesh size: 0.025
- initial pilot sample size: 6
- PBC load cases per realization: X, Y, XY engineering shear

## Tensor-audit evidence identities

| Realization | Seed | Tensor-audit SHA-256 | Schema |
|---:|---:|---|---|
| 1 | 1697541442752212169 | `ba6442428f97ce0286c03fa747868d791180c58ecb50bf7d0a8b38befe5db682` | `m8_rve_realization_tensor_audit_v1` |
| 2 | 4957153589961240624 | `67ddf2b819d9f636bb13e6c5cbb11ada61d972095de92e1f145586b0b1763cf2` | `m8_rve_realization_tensor_audit_v1` |
| 3 | 8294668839306064549 | `f1a6e0d9a9fa800be79c5e4b6be4573c4f64ac83cd4e3dbc25441db33b624d78` | `m8_rve_realization_tensor_audit_v1` |
| 4 | 138802719123899342 | `77b3de2c1ed5a7bfd65efc04158c44be37ba520399fdbdf584a782966e79fa00` | `m8_rve_realization_tensor_audit_v1` |
| 5 | 13653657189806206435 | `c67ad7f4d574887f3527ee9ffb9d04da1d28603e6b9f8af23c3dc5f36f5a72ae` | `m8_rve_realization_tensor_audit_v1` |
| 6 | 5708623245519862930 | `a6acaf990ff3a13eb248065b04d34fdd8f02601e8f62122d8bd0e7dd9f721aee` | `m8_rve_realization_tensor_audit_v1` |

All six R5 realizations use the permanent current tensor-audit schema.

No raw R5 tensor evidence was rewritten during statistical closure.

## Primary statistical precision

Confidence method: two-sided nominal 95% Student-t interval on the mean.

- n = 6
- degrees of freedom = 5
- t(0.975, 5) = 2.570581835636305
- locked relative confidence-half-width tolerance = 1.0%

| Quantity | Mean | Sample SD | CV (%) | 95% CI | Relative half-width (%) | Gate |
|---|---:|---:|---:|---:|---:|---|
| E_x / E_matrix | 1.185836327352432 | 0.001110874618615 | 0.093678579 | [1.184670535936202, 1.187002118768663] | 0.098309639 | PASS |
| E_y / E_matrix | 1.183980614549467 | 0.001609426422844 | 0.135933511 | [1.182291625101544, 1.185669603997390] | 0.142653471 | PASS |
| G_xy / E_matrix | 0.456374634398983 | 0.000642345691693 | 0.140749648 | [0.455700533936987, 0.457048734860980] | 0.147707697 | PASS |

All three primary precision gates pass at n = 6.

Adaptive R5 sample expansion is not triggered.

## Ensemble-mean normalized stiffness tensor

Voigt order: [11, 22, 12].

```text
[ 1.301342784155613,  0.387395300659850, -0.000141369181052]
[ 0.387395300659850,  1.299305319168625,  0.000055371115815]
[-0.000141369181052,  0.000055371115815,  0.456375497608129]
```

Ensemble-mean tensor symmetry residual: 0.0000000000000000e+00

No isotropy projection or manual coupling zeroing was applied.

## Ensemble isotropy / coupling diagnostics

- normalized directional mean difference: 0.001566123332274
- mean C16/E_matrix: -0.000141369181052
- mean C26/E_matrix: 0.000055371115815
- mean single-realization A_E: 0.001781958688098
- maximum single-realization A_E: 0.003005126732697
- maximum |C16/E_matrix|: 0.001517903604030
- maximum |C26/E_matrix|: 0.001038898036038

These are convergence diagnostics only.

Individual realizations are not forced to be isotropic.

## Particle-fraction screening

- mean absolute meshed-fraction error: 0.004801048069998
- maximum absolute meshed-fraction error: 0.004809025400343
- permanent gate: <= 0.005
- status: PASS

## Maximum scientific diagnostics across R5

- algebraic_relative_residual: 5.5158683004780147e-15
- gauge_max_abs: 0.0000000000000000e+00
- hill_mandel_relative_mismatch: 1.3017790164265033e-14
- macro_strain_max_abs_error: 1.4224732503009818e-16
- periodic_normalized_error: 2.5652223401007035e-14
- weak_stationarity_error: 9.5602538231610708e-17
- global_symmetry_residual: 2.6083832873802629e-15
- C12_C21_relative_mismatch: 9.3989471094636361e-15
- C16_C61_relative_mismatch: 4.4823213817567485e-14
- C26_C62_relative_mismatch: 1.7874590696465020e-14

All permanent geometry, mesh, PBC, reciprocity, symmetry, positive-definiteness, Voigt/Reuss, periodicity, strain-recovery, algebraic-equilibrium, Hill-Mandel, weak-stationarity and gauge requirements passed for every contributing realization.

## Preserved execution and recovery history

The R5 pilot retained all six predetermined seeds and physical realizations.

- R5 realization 1 required read-only recovery authentication around already-created geometry and mesh evidence. Valid evidence was preserved rather than replaced.
- An initial R5 realization-1 mesh-log scan falsely matched benign numerical error labels; corrected authentication accepted the existing mesh without regeneration.
- The first R5 realization-1 X wrapper attempt failed before the FEM solve because of wrapper syntax. The permanent X solve was subsequently executed without replacing the stochastic realization.
- R5 realization 5 tensor construction first encountered an off-by-one explicit-file sys.argv guard before scientific tensor assembly. The failed wrapper evidence was preserved, and the tensor was constructed from the already authenticated X/Y/XY evidence using the corrected explicit Python route without any FEM rerun.
- R5 realization 6 X evidence already existed when a later wrapper reached overwrite protection. Read-only recovery authenticated the existing result. A later log-scan false positive on numerical labels ending in `_ERROR=` was corrected without rerunning the X solve.
- R5 realization 6 tensor construction created the durable tensor successfully, while a later wrapper completion-marker check failed. Explicit read-only recovery independently authenticated the existing durable tensor without reconstruction.

These recovery events did not alter the R5 stochastic sampling design, remove a realization, substitute a seed, or select evidence based on mechanical response.

## R5 statistical decision

1. Six predetermined R5 realizations were completed through authenticated tensor audits.
2. No realization was removed, replaced, or cherry-picked based on mechanical response.
3. All three primary nominal 95% Student-t confidence precision gates pass at n = 6.
4. Adaptive R5 sample expansion is therefore not triggered.
5. R5 is statistically resolved for the current precision stage.
6. R5 is the largest statistically resolved comparison level in the initial R1-R5 design.
7. R5 is NOT accepted as a representative RVE solely because it is the largest tested level.
8. All five initial RVE levels R1-R5 are now statistically resolved.
9. Final representativity remains deferred to the locked cross-level tensor and engineering-response size-stability comparisons.

## Scope guard

Checkpoint creation performed:

- no geometry generation
- no mesh generation
- no FEM solve
- no MPC construction
- no tensor reconstruction
- no adaptive R5 realization generation
- no isotropy projection
- no manual stiffness-coupling zeroing
- no modification of ignored raw R5 evidence
- no modification of R1, R2, R3 or R4 checkpoint evidence
- no modification of M6/M7 physics or schemas
- no cross-level representativity calculation
- no representative-RVE declaration
