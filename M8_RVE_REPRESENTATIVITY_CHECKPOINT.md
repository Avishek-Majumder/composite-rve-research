# M8 RVE Representativity Decision Checkpoint

## Status

M8 RVE-size representativity decision: COMPLETE / PASS.

**R1 is accepted as the representative RVE size under the locked initial R1-R5 M8 representativity protocol.**

- accepted RVE level: R1
- accepted side length: 1.0
- accepted area: 1.0
- physical particle count: 16
- common statistical screening mesh size: 0.025

R1 is selected because it is the smallest eligible statistically resolved level satisfying every locked tensor-level and primary-mean size-stability requirement against every larger resolved level R2-R5.

This conclusion is specific to the locked M8 computational representativity study and does not claim universal representativity for all materials, constitutive laws, geometries, or dimensions.

The publication-facing target-mesh decision remains a separate M8 mesh-sensitivity gate.

## Repository provenance

- repository authority before this candidate: `d88691280f1f5934160a2231229a11bfcf4f7c03`
- protocol SHA-256: `9942968e247a7c38150757de9d22150cb889b933f71df750e3ca490b9b41d100`
- R1 checkpoint SHA-256: `df2a4efc79eedfa1b0b3778fb28eee802468f1cdb036755d156552b75e853ff7`
- R2 checkpoint SHA-256: `d8dfc366074615d43ed78a3958ac811dbc760cedb40fbddc4486065ef3abd6d4`
- R3 checkpoint SHA-256: `24ea2ec56d76281b16f59225e96f45be759550bda6c3993b63bf2d547b723056`
- R4 checkpoint SHA-256: `9850bb698e054d777b832fdf56f0b6888e88b8630c344cfda42714662a12eaba`
- R5 checkpoint SHA-256: `6c42c0c6d22208e6303b8565d5aea68260c073d96d6fcb78d93ef15e727eeec9`

## Locked cross-level acceptance rule

- relative normalized mean-tensor Frobenius-shift tolerance: 1.0%
- E_x/E_matrix mean-shift tolerance: 1.0%
- E_y/E_matrix mean-shift tolerance: 1.0%
- G_xy/E_matrix mean-shift tolerance: 1.0%
- each eligible candidate is compared against every larger resolved level
- the smallest eligible level satisfying every gate is accepted
- R5 is the largest comparison level and is not self-accepted solely by size

## Statistically resolved level summary

| Level | Side | Particles | E_x/E_matrix mean | E_y/E_matrix mean | G_xy/E_matrix mean |
|---|---:|---:|---:|---:|---:|
| R1 | 1.0 | 16 | 1.182209502921000 | 1.186074945288000 | 0.457029770304000 |
| R2 | 1.5 | 36 | 1.183821030253000 | 1.186190937341000 | 0.456033266964000 |
| R3 | 2.0 | 64 | 1.183589018999000 | 1.185572742844000 | 0.456269853075000 |
| R4 | 2.5 | 100 | 1.185204415215368 | 1.183716985249076 | 0.456453705307301 |
| R5 | 3.0 | 144 | 1.185836327352432 | 1.183980614549467 | 0.456374634398983 |

All five R1-R5 statistical levels are resolved.

## Pairwise locked size-stability results

| Smaller | Larger | Tensor shift (%) | E_x shift (%) | E_y shift (%) | G_xy shift (%) | Gate |
|---|---|---:|---:|---:|---:|---|
| R1 | R2 | 0.130827177 | 0.136129304 | 0.009778531 | 0.218515493 | PASS |
| R1 | R3 | 0.125224585 | 0.116553639 | 0.042359480 | 0.166549954 | PASS |
| R1 | R4 | 0.223429860 | 0.252691625 | 0.199199646 | 0.126204474 | PASS |
| R1 | R5 | 0.243842088 | 0.305845280 | 0.176888938 | 0.143552217 | PASS |
| R2 | R3 | 0.060422532 | 0.019602349 | 0.052143110 | 0.051852234 | PASS |
| R2 | R4 | 0.159885052 | 0.116721212 | 0.208998614 | 0.092109745 | PASS |
| R2 | R5 | 0.168903717 | 0.169947324 | 0.186685725 | 0.074799827 | PASS |
| R3 | R4 | 0.143265811 | 0.136296844 | 0.156773757 | 0.040278396 | PASS |
| R3 | R5 | 0.161070810 | 0.189512524 | 0.134472497 | 0.022959498 | PASS |
| R4 | R5 | 0.034063669 | 0.053288310 | 0.022266353 | 0.017325877 | PASS |

All ten smaller-to-larger pairwise locked size-stability gates pass.

## Candidate acceptance summary

| Candidate | Larger comparators | Max tensor shift (%) | Max E_x shift (%) | Max E_y shift (%) | Max G_xy shift (%) | Gate |
|---|---|---:|---:|---:|---:|---|
| R1 | R2, R3, R4, R5 | 0.243842088 | 0.305845280 | 0.199199646 | 0.218515493 | PASS |
| R2 | R3, R4, R5 | 0.168903717 | 0.169947324 | 0.208998614 | 0.092109745 | PASS |
| R3 | R4, R5 | 0.161070810 | 0.189512524 | 0.156773757 | 0.040278396 | PASS |
| R4 | R5 | 0.034063669 | 0.053288310 | 0.022266353 | 0.017325877 | PASS |

Passing eligible candidates: R1, R2, R3, R4.

R1 has a maximum locked shift of 0.305845280% across all required R1-to-larger-level comparisons.

## Final locked RVE-size decision

1. R1-R5 are all statistically resolved.
2. R1 has four strictly larger resolved comparators: R2, R3, R4 and R5.
3. Every R1 tensor-level comparison is within the locked 1% tolerance.
4. Every R1 E_x/E_matrix mean comparison is within the locked 1% tolerance.
5. Every R1 E_y/E_matrix mean comparison is within the locked 1% tolerance.
6. Every R1 G_xy/E_matrix mean comparison is within the locked 1% tolerance.
7. All contributing realization-level scientific hard gates were already authenticated in the permanent statistical checkpoints.
8. No failed realization was silently replaced or cherry-picked.
9. R1 is the smallest eligible tested level.
10. Therefore R1 is accepted as the representative RVE size under the locked R1-R5 M8 protocol.

No extension beyond R5 is required by the current locked RVE-size acceptance rule.

## Interpretation boundary

The R1 acceptance establishes statistical RVE-size stability for the locked pristine, periodized, two-phase particle-reinforced M8 study: 2D, small-strain, linear-elastic, plane-stress, isotropic constituent phases, perfectly bonded interfaces, circular particles, and no voids in the RVE-size study.

It does not establish a universal RVE size for arbitrary materials or microstructures.

It also does not replace the separate publication-facing target-mesh sensitivity decision.

## Scope guard

Checkpoint-candidate creation performed:

- no geometry generation
- no mesh generation
- no MPC construction
- no FEM solve
- no tensor reconstruction
- no statistical pilot recalculation
- no additional stochastic realization generation
- no isotropy projection
- no manual coupling zeroing
- no modification of R1-R5 checkpoint evidence
- no repository checkpoint installation
- no Git staging
- no Git commit
- no Git push

The only newly created output from this step is this temporary checkpoint candidate under /tmp.
