# M8 R4 Statistical Pilot Checkpoint

## Status

R4 initial statistical pilot: COMPLETE / PASS.

This checkpoint summarizes the six predetermined R4 realizations.

R4 satisfies the locked primary statistical precision requirement at the initial pilot size n = 6.

No additional R4 realizations are required by the current adaptive precision rule.

**This does NOT declare R4 statistically representative.**

Final RVE representativity requires comparison against the statistically resolved larger RVE level(s) under the locked M8 RVE Statistical Representativity Protocol.

## Repository provenance

- HEAD before checkpoint creation: `8af836ed334bd5b871daef8f8fd57d51affe262a`
- origin/main before checkpoint creation: `8af836ed334bd5b871daef8f8fd57d51affe262a`
- remote main before checkpoint creation: `8af836ed334bd5b871daef8f8fd57d51affe262a`
- protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- R1 checkpoint SHA-256: `df2a4efc79eedfa1b0b3778fb28eee802468f1cdb036755d156552b75e853ff7`
- R2 checkpoint SHA-256: `d8dfc366074615d43ed78a3958ac811dbc760cedb40fbddc4486065ef3abd6d4`
- R3 checkpoint SHA-256: `24ea2ec56d76281b16f59225e96f45be759550bda6c3993b63bf2d547b723056`
- periodized generator SHA-256: `63dc1bcd24324589f069013fc5f730477ece944b9c79626d8e7f94f7b3b30187`
- patched periodized mesher SHA-256: `0713c46add5395bce97d8bdf03e52050310889935921f306d958be076d9cc3cc`
- PBC solver SHA-256: `90079e56df7f2a74cac3b301e81cbaa0ea520ebcd1987f1ac7f81f4a6ee12e5b`
- material/config SHA-256: `f9dbb565bc2eeaa9166eac4a721de1f1d1f47474ecaf13ec567c5627614351dd`
- periodic-corner regression test SHA-256: `b89762fff46bb2810344099432be913efd878712bf9568554c969ec74c88c6f7`
- tracked/non-ignored repository state before checkpoint creation: clean

## Locked R4 design

- RVE level: R4
- side length: 2.5
- area: 6.25
- physical particle count: 100
- particle radius: 0.05
- particle number density: 16.0
- analytical particle area fraction: 0.12566370614359174
- common screening mesh size: 0.025
- initial pilot sample size: 6
- PBC load cases per realization: X, Y, XY engineering shear

## Tensor-audit evidence identities

| Realization | Seed | Tensor-audit SHA-256 | Schema |
|---:|---:|---|---|
| 1 | 7473245128805372283 | `f973d57d44e81bd4dffdf1aa2149fb5b23401dc6b18d3981131c5e4575c182f4` | `m8_rve_realization_tensor_audit_v1` |
| 2 | 5842223636676267490 | `7481f88da5d51899efc9d4683aaa012aa8ac44eb168d58e79b2d349002a1e7cd` | `m8_rve_realization_tensor_audit_v1` |
| 3 | 15017694034673515666 | `20748bff48e65ca3178205d541d339157855328eba0cd45c8fc4c3a4719cc0c3` | `m8_rve_realization_tensor_audit_v1` |
| 4 | 8721460711076261101 | `be23e1b6bff8962a164c7139ad9b8e01fb07dd296a877298b80001be4e876252` | `m8_rve_realization_tensor_audit_v1` |
| 5 | 14546067014408498300 | `60adba4efc4322b847bf2cb5b14880df71a65e4337670eb3e5ab42fed31bb0f6` | `m8_rve_realization_tensor_audit_v1` |
| 6 | 13366916596302023254 | `91c445ec1be49f7aa404a5cd0e0044f2411fdd943ea99dba1668aa142a8d95b9` | `m8_rve_realization_tensor_audit_v1` |

All six R4 realizations use the permanent current tensor-audit schema.

No raw tensor evidence was rewritten during statistical closure.

## Primary statistical precision

Confidence method: two-sided nominal 95% Student-t interval on the mean.

- n = 6
- degrees of freedom = 5
- t(0.975, 5) = 2.570581835636305
- locked relative confidence-half-width tolerance = 1.0%

| Quantity | Mean | Sample SD | CV (%) | 95% CI | Relative half-width (%) | Gate |
|---|---:|---:|---:|---:|---:|---|
| E_x / E_matrix | 1.185204415215368 | 0.001474727931553 | 0.124428150 | [1.183656783164846, 1.186752047265890] | 0.130579336 | PASS |
| E_y / E_matrix | 1.183716985249076 | 0.002149177356697 | 0.181561757 | [1.181461561934501, 1.185972408563651] | 0.190537379 | PASS |
| G_xy / E_matrix | 0.456453705307301 | 0.000292043213782 | 0.063980905 | [0.456147224750368, 0.456760185864234] | 0.067143842 | PASS |

All three primary precision gates pass at n = 6.

Adaptive R4 sample expansion is not triggered.

## Ensemble-mean normalized stiffness tensor

Voigt order: [11, 22, 12].

```text
[ 1.300827778784850,  0.387574413024572, -0.000330526414028]
[ 0.387574413024572,  1.299193320216570, -0.000070322490773]
[-0.000330526414028, -0.000070322490773,  0.456454793197763]
```

Ensemble-mean tensor symmetry residual: 0.0000000000000000e+00

No isotropy projection or manual coupling zeroing was applied.

## Ensemble isotropy / coupling diagnostics

- normalized directional mean difference: 0.001255786676586
- mean C16/E_matrix: -0.000330526414028
- mean C26/E_matrix: -0.000070322490773
- mean single-realization A_E: 0.002443460257110
- maximum single-realization A_E: 0.004642497470896
- maximum |C16/E_matrix|: 0.001650635899824
- maximum |C26/E_matrix|: 0.001176665079789

These are convergence diagnostics only.

Individual realizations are not forced to be isotropic.

## Particle-fraction screening

- mean absolute meshed-fraction error: 0.004785765971793
- maximum absolute meshed-fraction error: 0.004807989287459
- permanent gate: <= 0.005
- status: PASS

## Maximum scientific diagnostics across R4

- algebraic_relative_residual: 7.6656204032077814e-15
- gauge_max_abs: 0.0000000000000000e+00
- hill_mandel_relative_mismatch: 9.1241061445907119e-15
- macro_strain_max_abs_error: 8.6736173798840355e-17
- periodic_normalized_error: 1.9407218887490529e-14
- weak_stationarity_error: 1.5321077739827159e-16
- global_symmetry_residual: 2.0788282990687716e-15
- C12_C21_relative_mismatch: 7.4765710707431043e-15
- C16_C61_relative_mismatch: 4.4144639414369839e-14
- C26_C62_relative_mismatch: 4.3015525421931488e-14

All permanent geometry, mesh, PBC, reciprocity, symmetry, positive-definiteness, Voigt/Reuss, periodicity, strain-recovery, algebraic-equilibrium, Hill-Mandel, weak-stationarity and gauge requirements passed for every contributing realization.

## Preserved execution and recovery history

The R4 pilot retained all predetermined seeds and physical geometries.

- Realization 3 exposed a periodic-corner mesher case. The mesher correction was permanently validated, the original failed evidence was preserved, and the same predetermined realization was retried. No replacement seed or cherry-picked geometry was used.
- Realization 3 tensor construction later encountered a wrapper-only schema-compatibility defect before durable tensor creation. The corrected tensor artifact was reconstructed from the already valid X/Y/XY evidence without a new FEM or PBC solve.
- Realization 5 meshing completed successfully. A later independent wrapper audit initially misinterpreted the historical source_geometry.geometry_sha256 field. Read-only recovery established that the field stores the canonical physical-geometry identity and the existing mesh was accepted without rerun.
- Realization 6 geometry passed its scientific audit before a shell-wrapper parser failure. Read-only authentication confirmed the already durable geometry. An incomplete/interrupted mesher-log pair was preserved, and a fresh mesher retry using the same geometry and predetermined seed produced the accepted mesh.

These recovery events did not alter the R4 stochastic sampling design and did not remove or replace a realization based on mechanical response.

## R4 statistical decision

1. Six predetermined R4 realizations were completed through authenticated tensor audits.
2. No realization was removed, replaced, or cherry-picked based on mechanical response.
3. All three primary nominal 95% Student-t confidence precision gates pass at n = 6.
4. Adaptive R4 sample expansion is therefore not triggered.
5. R4 is statistically resolved for the current precision stage.
6. R4 is NOT yet accepted as the representative RVE size.
7. The next size-study level is R5 under the already locked protocol.
8. Final representativity remains deferred until R5 is statistically resolved and the required cross-level size-stability comparisons are evaluated.

## Scope guard

Checkpoint creation performed:

- no geometry generation
- no mesh generation
- no FEM solve
- no MPC construction
- no isotropy projection
- no manual stiffness-coupling zeroing
- no modification of ignored raw R4 evidence
- no modification of R1, R2 or R3 checkpoint evidence
- no modification of M6/M7 physics or schemas
- no R5 execution
- no representativity declaration
