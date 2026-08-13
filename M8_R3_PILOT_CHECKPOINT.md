# M8 R3 Statistical Pilot Checkpoint

## Status

R3 initial statistical pilot: COMPLETE / PASS.

This checkpoint summarizes the six predetermined R3 realizations.

R3 satisfies the locked primary statistical precision requirement
at the initial pilot size n = 6.

No additional R3 realizations are required by the current
adaptive precision rule.

**This does NOT declare R3 statistically representative.**

Final RVE representativity requires comparison against the
statistically resolved larger RVE levels under the locked
M8 RVE Statistical Representativity Protocol.

## Repository provenance

- HEAD before checkpoint creation: `5b1ba7f116b620031392709736c51e08ea0a06e2`
- origin/main before checkpoint creation: `5b1ba7f116b620031392709736c51e08ea0a06e2`
- remote main before checkpoint creation: `5b1ba7f116b620031392709736c51e08ea0a06e2`
- protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- R1 checkpoint SHA-256: `df2a4efc79eedfa1b0b3778fb28eee802468f1cdb036755d156552b75e853ff7`
- R2 checkpoint SHA-256: `d8dfc366074615d43ed78a3958ac811dbc760cedb40fbddc4486065ef3abd6d4`
- tracked/non-ignored repository state before checkpoint creation: clean

## Locked R3 design

- RVE level: R3
- side length: 2.0
- area: 4.0
- physical particle count: 64
- particle radius: 0.05
- particle number density: 16.0
- analytical particle area fraction: 0.12566370614359174
- common screening mesh size: 0.025
- initial pilot sample size: 6
- PBC load cases per realization: X, Y, XY engineering shear

## Tensor-audit evidence identities

| Realization | Seed | Tensor-audit SHA-256 | Schema |
|---:|---:|---|---|
| 1 | 1520765391204056186 | `46351f65f442ad4b085d1810b9e7da5ec061c6c475929dd40af48fe7bc190337` | `m8_rve_realization_tensor_audit_v1` |
| 2 | 16979900204114328306 | `7eb7aad02ce4d12a7490049a5d0fd238715ccb47d0d2d91256ed6bac86010280` | `m8_rve_realization_tensor_audit_v1` |
| 3 | 10549065626574797093 | `ead9dcbdc4d55f4f74adc61fc41486a50975ecc4014129183c4a6a3c388b9a92` | `m8_rve_realization_tensor_audit_v1` |
| 4 | 7861334562030830773 | `1fa9d22d581eebd636804d452682723535f43153ef71189d9a0b0b3b61531076` | `m8_rve_realization_tensor_audit_v1` |
| 5 | 16910014617435099714 | `5887607e8faf686f8a72b512c2483337753e4051fa4596c23150059da2412a62` | `m8_rve_realization_tensor_audit_v1` |
| 6 | 11244707517112643570 | `e8fc5767ea7663941d987fdaf4cadbad8b29e76df999a7136bd47759e427d753` | `m8_rve_realization_tensor_audit_v1` |

All six R3 realizations use the permanent current tensor-audit schema.

No raw tensor evidence was rewritten during statistical closure.

## Primary statistical precision

Confidence method: two-sided 95% Student-t interval on the mean.

- n = 6
- degrees of freedom = 5
- t(0.975, 5) = 2.570581835636305
- locked relative confidence-half-width tolerance = 1.0%

| Quantity | Mean | Sample SD | CV (%) | 95% CI | Relative half-width (%) | Gate |
|---|---:|---:|---:|---:|---:|---|
| E_x / E_matrix | 1.183589018999 | 0.002421108236 | 0.204556 | [1.181048221729, 1.186129816270] | 0.214669 | PASS |
| E_y / E_matrix | 1.185572742844 | 0.002654684705 | 0.223916 | [1.182786822103, 1.188358663586] | 0.234985 | PASS |
| G_xy / E_matrix | 0.456269853075 | 0.000562421340 | 0.123265 | [0.455679628077, 0.456860078074] | 0.129359 | PASS |

All three primary precision gates pass at n = 6.

Adaptive R3 sample expansion is not triggered.

## Ensemble-mean normalized stiffness tensor

Voigt order: [11, 22, 12].

```text
[ 1.298944398783,  0.387409212962, -0.000857188362]
[ 0.387409212962,  1.301120099900,  0.000129093615]
[-0.000857188362,  0.000129093615,  0.456272012276]
```

No isotropy projection or manual coupling zeroing was applied.

## Ensemble isotropy / coupling diagnostics

- normalized directional mean difference: 0.001674620853
- mean C16/E_matrix: -0.000857188362
- mean C26/E_matrix: 0.000129093615
- mean single-realization A_E: 0.002810993595
- maximum single-realization A_E: 0.007272197216
- maximum |C16/E_matrix|: 0.002045371867
- maximum |C26/E_matrix|: 0.001940884107

These are convergence diagnostics only.

Individual realizations are not forced to be isotropic.

## Particle-fraction screening

- mean absolute meshed-fraction error: 0.004767962903
- maximum absolute meshed-fraction error: 0.004817338011
- permanent gate: <= 0.005
- status: PASS

## Maximum scientific diagnostics across R3

- algebraic_relative_residual: 5.6183953518502212e-15
- periodic_normalized_error: 2.9273458657108620e-15
- macro_strain_max_abs_error: 7.9797279894933126e-17
- hill_mandel_relative_mismatch: 1.0879771499002992e-14
- weak_stationarity_error: 1.4918621893400541e-16
- gauge_max_abs: 0.0000000000000000e+00
- global_symmetry_residual: 8.9698737191502817e-16
- C12_C21_relative_mismatch: 3.2276089501015408e-15
- C16_C61_relative_mismatch: 3.0519753778794998e-13
- C26_C62_relative_mismatch: 2.1801951456301519e-13

All permanent geometry, mesh, PBC, reciprocity, symmetry,
positive-definiteness, Voigt/Reuss, periodicity, strain-recovery,
algebraic-equilibrium, Hill-Mandel, weak-stationarity and gauge
requirements passed for every contributing realization.

## R3 statistical decision

1. Six predetermined R3 realizations were completed.
2. No failed realization was replaced or cherry-picked.
3. All three primary 95% confidence precision gates pass.
4. Adaptive R3 sample expansion is therefore not triggered.
5. R3 is statistically resolved for the current precision stage.
6. R3 is NOT yet accepted as the representative RVE size.
7. The next size-study level is R4 under the already locked protocol.
8. Final representativity remains deferred until the required larger statistically resolved levels are available for cross-level comparison.

## Scope guard

Checkpoint creation performed:

- no geometry generation
- no mesh generation
- no FEM solve
- no MPC construction
- no isotropy projection
- no manual stiffness-coupling zeroing
- no modification of ignored raw R3 evidence
- no modification of R1 or R2 evidence
- no modification of M6/M7 physics or schemas
- no representativity declaration
