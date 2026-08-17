# M8 Stage-8 Local Target-Mesh Execution Checkpoint

## Status

**Progress checkpoint through authenticated STEP 632SD — 2026-08-17.**

This file records the durable execution state of the M8 local target-mesh study without modifying the permanent protocol authority.

The permanent `M8_TARGET_MESH_PROTOCOL.md` MUST NOT be edited during the current Stage-8 run sequence because the published Stage-8 writer authenticates its exact SHA256 before scientific execution.

This checkpoint is a progress/provenance record only. It does not itself claim final M8 target-mesh closure.

## 1. Permanent authority

- Repository: `/home/avishek/projects/composite-rve-research`
- Branch: `main`
- STEP 632SD publication authority before this documentation commit:
  `378e35278a49e9fc552bb8ebd114bdd2717194f7`
- `HEAD = origin/main = public GitHub main`
- divergence: `0 0`
- repository/index/worktree/untracked inventory: clean

Permanent protocol:

- `M8_TARGET_MESH_PROTOCOL.md`
- SHA256:
  `0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f`

Protected current authorities:

- `src/22_solve_m8_periodized_pbc.py`
  `90079e56df7f2a74cac3b301e81cbaa0ea520ebcd1987f1ac7f81f4a6ee12e5b`
- `src/23_generate_m8_periodized_void_microstructure.py`
  `88bf346e3168f7a31386c7587b24d7df83e5712344b1b6ccc60be788d652c9dd`
- `src/24_generate_m8_periodized_void_mesh.py`
  `c5a726bf0a3c0fe51875ba370d725b211722356a8b3eee6ff2fe505fb441a773`
- `src/25_solve_m8_periodized_void_pbc.py`
  `b97f5add78d712dee1dc7564e6dce3f6cf08e7c1bee9562522e3344483e230dc`
- `src/26_m8_local_response.py`
  `d73423d4e41fdc686e8bfd0825c0bead0c82103ec423fceb91e8b60d001bbaae`
- `src/27_run_m8_local_target_mesh_case.py`
  `a0fdb3992dbaa53f5210c8be62c71b1b78a5694a7bc33ee53a4e4dac1a75fa8e`
- `configs/03_parametric_rve_base.yaml`
  `f9dbb565bc2eeaa9166eac4a721de1f1d1f47474ecaf13ec567c5627614351dd`

Do not edit `M8_TARGET_MESH_PROTOCOL.md` during current Stage-8 runs because `src/27` embeds its exact SHA authority.

## 2. Scientific scope and locked model

Working title:

“An Active-Learning and Finite-Element Framework for Uncertainty-Aware Prediction of Defect-Sensitive Mechanical Properties in Particle-Reinforced Composites.”

Route:

- simulation + machine learning only;
- no laboratory experiments.

Model class:

- 2D;
- small-strain linear elasticity;
- plane stress;
- isotropic matrix and particle phases;
- perfect matrix-particle bonding;
- circular particles;
- circular true geometric matrix voids for defect cases.

Reference properties:

- `E_matrix = 1000`
- `nu_matrix = 0.30`
- `E_particle = 10000`
- `nu_particle = 0.25`

No universal-material claim is permitted.

## 3. Completed M8 prerequisite gates

The following are treated as authenticated and closed unless a real contradiction appears:

1. permanent target-mesh protocol installation;
2. periodized-void geometry implementation/validation;
3. periodized true-hole mesh implementation/validation;
4. void-capable PBC X/Y/XY validation;
5. R1 realization-1 controlled baseline/high-severity implementation confirmation;
6. six-realization pristine global target-mesh comparison;
7. cell/quadrature local-response validation and production quadrature-order lock.

All six predetermined pristine R1 realizations satisfy the global primary-response mesh gate between `h=0.02048` and `h=0.010` for `E_x/E_matrix`, `E_y/E_matrix`, and `G_xy/E_matrix`, with every individual difference <=1%.

Production quadrature degree is locked to `8`.

## 4. Controlled defect and local metric authority

Baseline:

- four true holes;
- radius `0.025`.

High severity:

- radius factor `1.10`;
- radius `0.0275`.

Paired states retain identical particle geometry, void IDs, void centers and void seed; only severity/radius changes.

Canonical void center fields:

- `center_x`
- `center_y`

Local metrics:

- `m8_matrix_vm_annulus_cell_tail10_v1`
- `m8_matrix_vm_annulus_quadrature_tail10_v1`

For X load:

`K_vm_tail10 = sigma_vm_tail10 / abs(Sigma_11)`

## 5. Stage-8 durable study contract

Case set:

- six R1 realizations;
- baseline + high severity;
- 12 defect cases.

Each case is run at:

- candidate `h=0.02048`;
- fine reference `h=0.010`.

Total durable runs:

- `24`.

Each durable run uses:

- X load only;
- macro amplitude `0.01`;
- quadrature degree `8`;
- exactly one FEM/PBC solve;
- homogenized response;
- cell + quadrature local metrics from the same solved field;
- deterministic JSON;
- exclusive-create output;
- full Git-ignored raw log.

## 6. Completed durable local runs — 8/24

No coarse/fine `delta_K` has yet been calculated.
No final local-metric selection has occurred.
No final target-mesh/local-target decision has occurred.

| Step | Realization | State | Mesh | Result SHA256 | Raw log SHA256 | Sigma_11 | Cell K | Quadrature K |
|---|---|---|---:|---|---|---:|---:|---:|
| 632RO | R1R1 | baseline | 0.02048 | `68602b451c493869d1bbb8bdaf35a53bd229d6f4aeb12bb54d8889d27c5a1b27` | `e218ca438ee647d36ae9becbfead4f11436ff2f451e7e8a479e8dafab398a3d6` | 12.789222870097124 | 1.7504808924633344 | 1.6889435327139473 |
| 632RQ | R1R1 | baseline | 0.010 | `6a834a13b026ca36fb3115e65e5b586965e3ce84754b1e4cd8883bacd001eb38` | `9eb8914d1e949da49b397fca2650c6611c7c37df6756c4a622e47553399ee1af` | 12.750227996162677 | 1.6829524939835325 | 1.6727088421126861 |
| 632RS | R1R1 | high_severity | 0.02048 | `ea7917390c2b32c131186a614430a8b48390104801d7b3527fa9edcfac8e0b67` | `99d00244a8eea55da417ab52f56aa775268fb493ccbf2f40d049ce803e7dc192` | 12.73081932537253 | 1.7024486351767578 | 1.6528381761580468 |
| 632RU | R1R1 | high_severity | 0.010 | `1f95eb4ba47213872fd3e2f8cb03de43ff6d895851383fc0cbbaabdef8227a12` | `a2032200d55473ef45a5908edf7946de571cab7878b64340d002f99c2ad18a45` | 12.687672490634483 | 1.6744049386597684 | 1.6603615730886858 |
| 632RW | R1R2 | baseline | 0.02048 | `72546e913286c84d58662f8cfbac9932f82e757d1070d1a9a55fafa577ff2552` | `0aa8bd5c0c3867f4810e556e90511bf51440d524b67eee299ce02ae107b6e0b0` | 12.726927936300166 | 1.6977423591808982 | 1.645451006093003 |
| 632RY | R1R2 | baseline | 0.010 | `aaa457f9ab3693a9fc798ae04fa925b67402776313b3afd46bc964c284d462ba` | `10fa28dba68117c20322f8436e2a7bc537a5626aed3b367c9fc0a84f54d4d2d5` | 12.688839139658317 | 1.6463529649899673 | 1.6414703423296806 |
| 632SA | R1R2 | high_severity | 0.02048 | `7046c0a0e1ddeff7c5f42ed7e05e2e6229371f8e45dfc82b8b2aea0da49f9f6f` | `c0df58fa858b9379e0d4a1b967debee47615d293563c4d2b27b198a30f1f6034` | 12.662762242328053 | 1.6862225005644604 | 1.6529458755216742 |
| 632SC | R1R2 | high_severity | 0.010 | `02ebbfc47f59f76d81578b93f35efcc7731aa26e2fc425146dadd252d3061c5d` | `e7096d7d1a00ca50953a506efbf4d4a2855ba3994ed4fae4ad9379b486ff0103` | 12.630117112458304 | 1.6554797908296013 | 1.6405948965435988 |

All eight results retain schema `m8_local_target_mesh_case_v1`, valid status, authenticated provenance, one-solve scope, and source/config/input immutability.

## 7. Important checker-only recoveries

The following were authenticated as checker/harness defects rather than scientific failures:

- 632RJ-A/B: `ast.literal_eval` incorrectly applied to `choices=[PRODUCTION_QUADRATURE_DEGREE]`; correct resolution is `[8]`.
- 632RJ-C/C-A: exclusive-create scanner missed `Path.open("x", ...)`; writer is correctly non-overwriting and deterministic.
- 632RN/RN-A: `ast.literal_eval` incorrectly applied to `MPC_PYTHON = Path(...)`; correct isolated Python path remained exact.
- 632RR/RR-A: checker expected nonexistent `void["center"]`; canonical fields are `center_x` and `center_y`.

No authenticated science was altered for those checker failures.

## 8. STEP 632SD closure

STEP 632SD was read-only.

It:

- reauthenticated all eight completed durable cases;
- reauthenticated protected source/config/public authority;
- performed no FEM/PBC solve;
- wrote no scientific/source byte;
- calculated no `delta_K`;
- performed no cross-case comparison;
- made no metric or target-mesh decision;
- performed no ML.

Target-mesh inventory remained exactly:

- `272` files.

Repository remained:

- clean;
- zero divergence;
- `HEAD = origin/main = public GitHub main = 378e35278a49e9fc552bb8ebd114bdd2717194f7`.

## 9. Exact next scientific case — STEP 632SE

Next case:

- R1 realization 3;
- baseline;
- `h=0.02048`;
- X load;
- macro amplitude `0.01`;
- quadrature degree `8`.

Geometry family:

- path:
  `results/raw/04_m8_target_mesh/periodized_void_geometry/R1/realization_0003/geometry_family.json`
- SHA256:
  `1252cba96a003788d1f8df8f67fa60ea4866cd9cc156e197aea6be79ac7197c1`

Candidate mesh:

- path:
  `results/raw/04_m8_target_mesh/periodized_void_mesh/R1/realization_0003/baseline/h_0p02048/mesh.msh`
- SHA256:
  `ce594ea912dad303b49c7d580b149789fe921182690bbecfbd762c6b00fc191f`

Candidate diagnostics:

- path:
  `results/raw/04_m8_target_mesh/periodized_void_mesh/R1/realization_0003/baseline/h_0p02048/mesh_diagnostics.json`
- SHA256:
  `a31d7b0ae67725d5a3b451fd7b06348074a24488e75edddf4282c7767137c4ef`

Reserved durable output:

`results/raw/04_m8_target_mesh/local_target_mesh_cases/R1/realization_0003/baseline/h_0p02048/local_response.json`

Reserved raw log:

`results/raw/04_m8_target_mesh/_logs/step_632SE_R1R3_baseline_h_0p02048_local_target_mesh_case.log`

At STEP 632SD closure both reserved paths were absent and Git-ignored.

STEP 632SE was command-locked but NOT executed.

## 10. Remaining work

Remaining durable local executions:

- `16`.

They are all four state/mesh combinations for R1R3, R1R4, R1R5 and R1R6:

1. baseline `h=0.02048`
2. baseline `h=0.010`
3. high_severity `h=0.02048`
4. high_severity `h=0.010`

After all 24 durable runs are complete:

For each of exactly 12 predeclared defect cases:

`delta_K = abs(K_h02048 - K_h0010) / abs(K_h0010)`

with `h=0.010` as denominator.

Both cell and quadrature candidates must remain until metric selection.

Final local target-mesh acceptance:

- median absolute relative difference `<=3%`;
- no individual case `>5%`;
- both severities represented;
- no cherry-picking.

If the local gate fails, preserve failed evidence and diagnose protocol-authorized refinement/finer-mesh paths.

Then:

1. choose final local metric from documented evidence;
2. make final target-mesh/local-target decision;
3. create permanent M8 target-mesh checkpoint;
4. create/update M8 closure documentation;
5. commit/push/authenticate M8 closure;
6. only then transition beyond M8.

No ML before M8 closure.

## 11. Git/raw-data governance

Scientific JSON results and full solver logs are Git-ignored by design.

Do not force-add them merely to make them public.

Their durability/provenance is maintained through:

- local retained raw artifacts;
- exact paths;
- exact SHA256 hashes;
- tracked source/protocol/checkpoint documentation;
- clean commits and public GitHub synchronization for tracked authorities.

This checkpoint file itself is intended to be tracked.

Recommended commit subject:

`M8: checkpoint Stage-8 local study through 632SD`

## 12. Progress

At STEP 632SD closure:

- durable local execution progress: `8/24 = 33.33%`
- durable runs remaining: `16/24 = 66.67%`
- approximate overall M8 progress: `~92%`

The overall percentage is an approximate milestone-progress indicator.

## 13. Continuation rule

At the beginning of the next chat:

1. reread/recover all available project memory/context first;
2. authenticate the documentation checkpoint commit if published;
3. authenticate `HEAD`, `origin/main`, public GitHub main, clean status and protected hashes;
4. confirm STEP 632SE output/log remain absent;
5. execute STEP 632SE only;
6. stop and inspect the complete output before any further step.

Do not calculate `delta_K` yet.
Do not select the final local metric yet.
Do not make the final target-mesh decision yet.
Do not start M9 or ML.
