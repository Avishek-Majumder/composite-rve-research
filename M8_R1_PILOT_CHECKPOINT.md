# M8 R1 Statistical Pilot Checkpoint

## Status

R1 initial statistical pilot: COMPLETE / PASS.

This checkpoint summarizes the six predetermined R1 realizations.

R1 satisfies the locked primary statistical precision requirement
at the initial pilot size n = 6.

No additional R1 realizations are required by the current
adaptive precision rule.

**This does NOT declare R1 statistically representative.**

Final RVE representativity requires comparison against the
statistically resolved larger RVE levels under the locked
M8 RVE Statistical Representativity Protocol.

## Repository provenance

- HEAD: `f0c85959bc312182884a8b8a67994af9c232698f`
- origin/main: `f0c85959bc312182884a8b8a67994af9c232698f`
- protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- tracked repository state before checkpoint creation: clean

## Locked R1 design

- RVE level: R1
- side length: 1.0
- area: 1.0
- physical particle count: 16
- particle radius: 0.05
- analytical particle area fraction: 0.12566370614359174
- common screening mesh size: 0.025
- initial pilot sample size: 6
- PBC load cases per realization: X, Y, XY engineering shear

## Tensor-audit evidence identities

| Realization | Seed | Tensor-audit SHA-256 | Schema |
|---:|---:|---|---|
| 1 | 15944426988753885521 | `edc40f4418981aee15b0f8cb78ccb98535f5a2d079c9b558aab3886b9aaf22fa` | `m8_rve_realization_pbc_tensor_audit_v1` |
| 2 | 14726087059387717211 | `cc28c9d13c65790b776e21d6a0d1446d50d41a14a0b6d012b7c07877f1858820` | `m8_rve_realization_pbc_tensor_audit_v1` |
| 3 | 16304908395315497179 | `b42a52820991a49da450808f60204b40ab5e29b5a8542b99bfe5347a3bf3e5f1` | `m8_rve_realization_tensor_audit_v1` |
| 4 | 8543608591806175946 | `4efd6f5ab91edeef2978d796867aa34a195bba4bbe78f861af6b97d21da42920` | `m8_rve_realization_tensor_audit_v1` |
| 5 | 9043192476962390047 | `7711f024f2d86836382a89ec72a8fc0764e18e24c390d3c80a4899e424a066cf` | `m8_rve_realization_tensor_audit_v1` |
| 6 | 4715493001954948121 | `b26377f1aa18a0eb570930e2faaa19463960b3a10a20d4fb7bf4bc5faf5a65ff` | `m8_rve_realization_tensor_audit_v1` |

Historical schema differences were normalized read-only.
No historical raw evidence was rewritten or migrated.

## Primary statistical precision

Confidence method: two-sided 95% Student-t interval on the mean.

- n = 6
- degrees of freedom = 5
- t(0.975, 5) = 2.570581835636305
- locked relative confidence-half-width tolerance = 1.0%

| Quantity | Mean | Sample SD | CV (%) | 95% CI | Relative half-width (%) | Gate |
|---|---:|---:|---:|---:|---:|---|
| E_x / E_matrix | 1.182209502921 | 0.004680505028 | 0.395912 | [1.177297614132, 1.187121391710] | 0.415484 | PASS |
| E_y / E_matrix | 1.186074945288 | 0.006400637293 | 0.539649 | [1.179357888395, 1.192792002181] | 0.566327 | PASS |
| G_xy / E_matrix | 0.457029770304 | 0.001907043793 | 0.417269 | [0.455028450581, 0.459031090028] | 0.437897 | PASS |

All three primary precision gates pass at n = 6.

## Ensemble-mean normalized stiffness tensor

Voigt order: [11, 22, 12].

```text
[1.297856975686, 0.388028844295, -0.000362044636]
[0.388028844295, 1.302103217155, -0.000896249208]
[-0.000362044636, -0.000896249208, 0.457038687915]
```

No isotropy projection or manual coupling zeroing was applied.

## Ensemble isotropy / coupling diagnostics

- normalized directional mean difference: 0.003264339611
- mean C16/E_matrix: -0.000362044636
- mean C26/E_matrix: -0.000896249208
- mean single-realization A_E: 0.005047652348
- maximum single-realization A_E: 0.015625970110

These are convergence diagnostics only.
Individual realizations are not forced to be isotropic.

## Particle-fraction screening

- mean absolute meshed-fraction error: 0.004762678771
- maximum absolute meshed-fraction error: 0.004809805387
- permanent gate: <= 0.005
- status: PASS

## Maximum scientific diagnostics across R1

- algebraic_relative_residual: 3.6858577443211425e-15
- periodic_normalized_error: 1.6805133673525319e-15
- macro_strain_max_abs_error: 2.4286128663675299e-17
- hill_mandel_relative_mismatch: 4.6908446893848016e-15
- weak_stationarity_error: 1.0061396160665481e-16
- gauge_max_abs: 0.0000000000000000e+00
- global_symmetry_residual: 1.2624719852068358e-15
- C12_C21_relative_mismatch: 4.5612882405504647e-15
- C16_C61_relative_mismatch: 4.1902640317794706e-14
- C26_C62_relative_mismatch: 1.1511916014802161e-14

All permanent geometry, mesh, PBC, reciprocity, symmetry,
positive-definiteness, Voigt/Reuss, periodicity, strain-recovery,
algebraic-equilibrium, Hill-Mandel, weak-stationarity and gauge
requirements passed for every contributing realization.

## R1 statistical decision

1. Six predetermined R1 realizations were completed.
2. No failed realization was replaced or cherry-picked.
3. All three primary 95% confidence precision gates pass.
4. Adaptive R1 sample expansion is therefore not triggered.
5. R1 is statistically resolved for the current precision stage.
6. R1 is NOT yet accepted as the representative RVE size.
7. The next size-study level is R2 under the already locked protocol.

## Scope guard

Checkpoint creation performed:

- no geometry generation
- no mesh generation
- no FEM solve
- no MPC construction
- no isotropy projection
- no modification of ignored raw R1 evidence
- no modification of M6/M7 physics or schemas
