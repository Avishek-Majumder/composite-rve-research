# M8 R2 Statistical Pilot Checkpoint

## Status

R2 initial statistical pilot: COMPLETE / PASS.

This checkpoint summarizes the six predetermined R2 realizations.

R2 satisfies the locked primary statistical precision requirement
at the initial pilot size n = 6.

No additional R2 realizations are required by the current
adaptive precision rule.

**This does NOT declare R2 statistically representative.**

Final RVE representativity requires comparison against the
statistically resolved larger RVE levels under the locked
M8 RVE Statistical Representativity Protocol.

## Repository provenance

- HEAD: `47384063a36fea7687a7ef5b74afb77b7457f27c`
- origin/main: `47384063a36fea7687a7ef5b74afb77b7457f27c`
- protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- R1 checkpoint SHA-256: `df2a4efc79eedfa1b0b3778fb28eee802468f1cdb036755d156552b75e853ff7`
- tracked repository state before checkpoint creation: clean

## Locked R2 design

- RVE level: R2
- side length: 1.5
- area: 2.25
- physical particle count: 36
- particle radius: 0.05
- analytical particle area fraction: 0.12566370614359174
- common screening mesh size: 0.025
- initial pilot sample size: 6
- PBC load cases per realization: X, Y, XY engineering shear

## Tensor-audit evidence identities

| Realization | Seed | Tensor-audit SHA-256 | Schema |
|---:|---:|---|---|
| 1 | 8959588066430205224 | `8af5edda99ee6381db4a401ae5ae1774fe90c065a8747ce9f4f39140a729aacd` | `m8_rve_realization_tensor_audit_v1` |
| 2 | 2748981751842334585 | `821a0947e446a1021f1af2aa2193c6c968623b39733cb8bee5e96094722f9606` | `m8_rve_realization_tensor_audit_v1` |
| 3 | 14654959448747560437 | `464d872bd0a30f31b191882314c46bd6518c17fd5cd0ea7451fc32f4f6b6d608` | `m8_rve_realization_tensor_audit_v1` |
| 4 | 10490406078943403795 | `462bc4568961ec969bd41deeb02965012a8e6c08c70471865fb39893f81dc80c` | `m8_rve_realization_tensor_audit_v1` |
| 5 | 14754115464194099490 | `3036694bb5057d93c774a2f701a43237a93c47e96d9ccd08066f0c9001b03184` | `m8_rve_realization_tensor_audit_v1` |
| 6 | 15457697788873575750 | `97fdbe7fce69cb81a0c04d58d9affcbb34a72893e7f35dc21ee3812f3256af39` | `m8_rve_realization_tensor_audit_v1` |

All six R2 realizations use one permanent tensor-audit schema.

No raw tensor evidence was rewritten during statistical closure.

## Primary statistical precision

Confidence method: two-sided 95% Student-t interval on the mean.

- n = 6
- degrees of freedom = 5
- t(0.975, 5) = 2.570581835636305
- locked relative confidence-half-width tolerance = 1.0%

| Quantity | Mean | Sample SD | CV (%) | 95% CI | Relative half-width (%) | Gate |
|---|---:|---:|---:|---:|---:|---|
| E_x / E_matrix | 1.183821030253 | 0.002174482581 | 0.183683 | [1.181539050734, 1.186103009772] | 0.192764 | PASS |
| E_y / E_matrix | 1.186190937341 | 0.003010260856 | 0.253775 | [1.183031862312, 1.189350012369] | 0.266321 | PASS |
| G_xy / E_matrix | 0.456033266964 | 0.001021118513 | 0.223913 | [0.454961668804, 0.457104865124] | 0.234982 | PASS |

All three primary precision gates pass at n = 6.

## Ensemble-mean normalized stiffness tensor

Voigt order: [11, 22, 12].

```text
[1.298993276117, 0.387167465789, -0.000154294352]
[0.387167465789, 1.301607119448, 0.000234122537]
[-0.000154294352, 0.000234122537, 0.456041766527]
```

No isotropy projection or manual coupling zeroing was applied.

## Ensemble isotropy / coupling diagnostics

- normalized directional mean difference: 0.001999911494
- mean C16/E_matrix: -0.000154294352
- mean C26/E_matrix: 0.000234122537
- mean single-realization A_E: 0.002571978059
- maximum single-realization A_E: 0.008268144931
- maximum |C16/E_matrix|: 0.002535135787
- maximum |C26/E_matrix|: 0.004798456381

These are convergence diagnostics only.
Individual realizations are not forced to be isotropic.

## Particle-fraction screening

- mean absolute meshed-fraction error: 0.004755395518
- maximum absolute meshed-fraction error: 0.004792330653
- permanent gate: <= 0.005
- status: PASS

## Maximum scientific diagnostics across R2

- algebraic_relative_residual: 5.2236750922335490e-15
- periodic_normalized_error: 4.9602249391211828e-15
- macro_strain_max_abs_error: 7.1123662515049091e-17
- hill_mandel_relative_mismatch: 5.9835026049266681e-15
- weak_stationarity_error: 1.0177044392397268e-16
- gauge_max_abs: 0.0000000000000000e+00
- global_symmetry_residual: 1.2227253765892197e-15
- C12_C21_relative_mismatch: 4.4106792394156152e-15
- C16_C61_relative_mismatch: 1.8810709233047300e-13
- C26_C62_relative_mismatch: 6.0553736862864086e-14

All permanent geometry, mesh, PBC, reciprocity, symmetry,
positive-definiteness, Voigt/Reuss, periodicity, strain-recovery,
algebraic-equilibrium, Hill-Mandel, weak-stationarity and gauge
requirements passed for every contributing realization.

## R2 statistical decision

1. Six predetermined R2 realizations were completed.
2. No failed realization was replaced or cherry-picked.
3. All three primary 95% confidence precision gates pass.
4. Adaptive R2 sample expansion is therefore not triggered.
5. R2 is statistically resolved for the current precision stage.
6. R2 is NOT yet accepted as the representative RVE size.
7. The next size-study level is R3 under the already locked protocol.

## Scope guard

Checkpoint creation performed:

- no geometry generation
- no mesh generation
- no FEM solve
- no MPC construction
- no isotropy projection
- no modification of ignored raw R2 evidence
- no modification of R1 evidence
- no modification of M6/M7 physics or schemas
