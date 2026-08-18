# M8 Final Target-Mesh Decision Checkpoint

## Status

**Permanent M8 target-mesh decision checkpoint.**

M8 final target-mesh/local-target scientific decision: **COMPLETE / PASS**.

**Accepted production target mesh: `h = 0.02048`.**

**Fine numerical comparison reference: `h = 0.010`.**

**Selected M8 local metric: `m8_matrix_vm_annulus_quadrature_tail10_v1`.**

Production quadrature degree: `8`.

This conclusion is specific to the locked M8 computational study and does not claim universal applicability to all materials, constitutive laws, geometries or dimensions.

The `h = 0.010` mesh is retained as a numerical comparison reference and is not claimed to be the exact continuum solution.

## 1. Repository and permanent authority

- repository: `/home/avishek/projects/composite-rve-research`
- branch: `main`
- repository authority immediately before candidate creation:
  `5c1077b29d34fc3e2ba63af14090d888e860d4fa`
- `HEAD = origin/main = public GitHub main`
- divergence: `0 0`
- tracked/index/worktree authority: clean

Permanent protocol:

- `M8_TARGET_MESH_PROTOCOL.md`
- SHA256: `0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f`

Stage-8 execution checkpoint before final closure:

- `M8_STAGE8_LOCAL_TARGET_MESH_EXECUTION_CHECKPOINT.md`
- SHA256: `32c892f9b55e0af26e7e29760e2353333bc977884d82e763ff899a8f5889de69`

Protected scientific/config authorities:

- `src/22_solve_m8_periodized_pbc.py` — `90079e56df7f2a74cac3b301e81cbaa0ea520ebcd1987f1ac7f81f4a6ee12e5b`
- `src/23_generate_m8_periodized_void_microstructure.py` — `88bf346e3168f7a31386c7587b24d7df83e5712344b1b6ccc60be788d652c9dd`
- `src/24_generate_m8_periodized_void_mesh.py` — `c5a726bf0a3c0fe51875ba370d725b211722356a8b3eee6ff2fe505fb441a773`
- `src/25_solve_m8_periodized_void_pbc.py` — `b97f5add78d712dee1dc7564e6dce3f6cf08e7c1bee9562522e3344483e230dc`
- `src/26_m8_local_response.py` — `d73423d4e41fdc686e8bfd0825c0bead0c82103ec423fceb91e8b60d001bbaae`
- `src/27_run_m8_local_target_mesh_case.py` — `a0fdb3992dbaa53f5210c8be62c71b1b78a5694a7bc33ee53a4e4dac1a75fa8e`
- `configs/03_parametric_rve_base.yaml` — `f9dbb565bc2eeaa9166eac4a721de1f1d1f47474ecaf13ec567c5627614351dd`

## 2. Locked model and RVE authority

- representative RVE: `R1`
- side length: `1.0`
- gross RVE area: `1.0`
- physical particle count: `16`
- 2D small-strain linear elasticity
- plane stress
- isotropic matrix and particle phases
- perfect matrix-particle bonding
- circular particles
- circular true matrix voids for controlled defect cases
- `E_matrix = 1000`
- `nu_matrix = 0.30`
- `E_particle = 10000`
- `nu_particle = 0.25`

The earlier permanent M8 RVE-size decision remains closed and was not reopened.

## 3. Global target-mesh gate

All six predetermined pristine R1 realizations passed the permanent global primary-response gate comparing `h=0.02048` against the explicit `h=0.010` denominator.

For every realization, each of `E_x/E_matrix`, `E_y/E_matrix`, and `G_xy/E_matrix` remained within the locked `1%` individual tolerance.

| Realization | Authenticated comparison SHA256 | Gate |
|---|---|---|
| R1R1 | `633d51aa1d150c40cf036e842faafd0dd3e6ae2eebf11439892a54f83682e900` | PASS |
| R1R2 | `cc02c88d51449ba850a82da5f4ef2b84e28b70bca1883f21651188a313f25f51` | PASS |
| R1R3 | `9e4e7c8d897114ad41d3106a404c89cc53e920ecf64b092e24056b062c2b3414` | PASS |
| R1R4 | `6fe7e8daff4ca72ab1ff2655fc7efcf335e634a4591da99f6b314f473e358f9c` | PASS |
| R1R5 | `44d721632caa46077bf9f7bebd4fb4cfbad0a535d3e88ab69da4b61c173a7e5a` | PASS |
| R1R6 | `0c30d42d03db100b53e60a8b9297afeb7417eda14c430eb5fd1407708afd975f` | PASS |

No ensemble averaging was used to hide an individual primary-response failure.

Near-zero normal-shear coupling terms were retained and audited but were not subjected to brittle relative-percentage hard gates.

## 4. Controlled defect study

Baseline defect state:

- four physical true holes
- radius `0.025`

High-severity defect state:

- four physical true holes
- radius factor `1.10`
- radius `0.0275`

Paired baseline/high-severity states retain identical particle geometry, physical void IDs, void centers and void seed; only the common void radius/severity changes.

The Stage-8 local study contains exactly:

- 6 realizations
- 2 severities
- 2 mesh levels
- 24 durable FEM/PBC results
- 12 paired defect cases

Each durable result used X load, macro amplitude `0.01`, quadrature degree `8`, one FEM/PBC solve, homogenized response, and both local-response implementations from the same solved field.

## 5. Durable Stage-8 provenance

| Step | Case | State | Mesh h | Durable result SHA256 | Successful raw-log SHA256 |
|---|---|---|---:|---|---|
| 632RO | R1R1 | baseline | 0.02048 | `68602b451c493869d1bbb8bdaf35a53bd229d6f4aeb12bb54d8889d27c5a1b27` | `e218ca438ee647d36ae9becbfead4f11436ff2f451e7e8a479e8dafab398a3d6` |
| 632RQ | R1R1 | baseline | 0.010 | `6a834a13b026ca36fb3115e65e5b586965e3ce84754b1e4cd8883bacd001eb38` | `9eb8914d1e949da49b397fca2650c6611c7c37df6756c4a622e47553399ee1af` |
| 632RS | R1R1 | high_severity | 0.02048 | `ea7917390c2b32c131186a614430a8b48390104801d7b3527fa9edcfac8e0b67` | `99d00244a8eea55da417ab52f56aa775268fb493ccbf2f40d049ce803e7dc192` |
| 632RU | R1R1 | high_severity | 0.010 | `1f95eb4ba47213872fd3e2f8cb03de43ff6d895851383fc0cbbaabdef8227a12` | `a2032200d55473ef45a5908edf7946de571cab7878b64340d002f99c2ad18a45` |
| 632RW | R1R2 | baseline | 0.02048 | `72546e913286c84d58662f8cfbac9932f82e757d1070d1a9a55fafa577ff2552` | `0aa8bd5c0c3867f4810e556e90511bf51440d524b67eee299ce02ae107b6e0b0` |
| 632RY | R1R2 | baseline | 0.010 | `aaa457f9ab3693a9fc798ae04fa925b67402776313b3afd46bc964c284d462ba` | `10fa28dba68117c20322f8436e2a7bc537a5626aed3b367c9fc0a84f54d4d2d5` |
| 632SA | R1R2 | high_severity | 0.02048 | `7046c0a0e1ddeff7c5f42ed7e05e2e6229371f8e45dfc82b8b2aea0da49f9f6f` | `c0df58fa858b9379e0d4a1b967debee47615d293563c4d2b27b198a30f1f6034` |
| 632SC | R1R2 | high_severity | 0.010 | `02ebbfc47f59f76d81578b93f35efcc7731aa26e2fc425146dadd252d3061c5d` | `e7096d7d1a00ca50953a506efbf4d4a2855ba3994ed4fae4ad9379b486ff0103` |
| 632SE-B | R1R3 | baseline | 0.02048 | `01871330b0a720c4ceed041896875046646859bd739e332b33df03ca7952eab9` | `41864be1870d40bfba4e531d7ec18ab1a6f37c945d8adbc12d2b07e07588a1ce` |
| 632SF | R1R3 | baseline | 0.010 | `4993876ce707eb0dadbb5ed29c68add5f42a8264775b307ad1a900d6efeb0338` | `cc17692bb80a8ae15c6721d5a4fb93f59a423f38128d1377928bf4d106c3c1f8` |
| 632SG | R1R3 | high_severity | 0.02048 | `bce60c51d7af0d9d5bdfd957fa2144f1e10254c51ca97a3e5838b43c5ced5821` | `563070ea00d9649f50b58a06ac3837d95533c67a6e32013c15cb44d6c32a66aa` |
| 632SH | R1R3 | high_severity | 0.010 | `7f482c9ae890f27aa322b70571bc6946d5b8c498ab9a4e1a3969c1e2503caeeb` | `8034415ee195b3ed3456c4bbb1875a2a3092e5b95bbb6425b1be0e3547f4fff9` |
| 632SI | R1R4 | baseline | 0.02048 | `666d523d8983335f09e04c4e14ac2e6dce81c58566c7a9a58864315fd39ae0bf` | `96199c49b6e7ac28efecd4d07f939edab4f16fba5c3f81993897a7876f1b0431` |
| 632SJ | R1R4 | baseline | 0.010 | `100af3457f42fa53843a36da8a2ccb466ea8618b052c2f8e9e536d87e621b364` | `143fcb15afb653f23f44d30fdc1c93f8f9b9174bc79cc8eec5083dc53a9779d7` |
| 632SK | R1R4 | high_severity | 0.02048 | `bfe83c004080ae55b7c5af2097013ce6be63c886f6f1fd00cebb37fa9a2d2d2e` | `472729fc7c21cddef6945ffce8e1386048a36ac3e93ae0bb93b305635a034d76` |
| 632SL | R1R4 | high_severity | 0.010 | `7c0486486657b739c02ebe86a4a5df958f2f905458ec79fe2ff1be7b50c69dc5` | `949b6280f6a7dd721fb414b528a351d9823bffba745a37463a9bb0866952e0e5` |
| 632SM | R1R5 | baseline | 0.02048 | `5388f1913b9562746612adf6c53289e37619a665479b73b5f23b346fb80e7d61` | `92fcb3e2cf5b2d1ca48efcb6e11a1736809c532d0bd45d22efa1deafc76f75c4` |
| 632SN | R1R5 | baseline | 0.010 | `0657d509f8bef075b6abdae4eb16d8c3ea10f946708f044f635b9f9f664dc1c2` | `e49392085bf0f8057505e8d8c611fab2f7932fb30f7678fd88c8e9bf3eef5811` |
| 632SO | R1R5 | high_severity | 0.02048 | `e9193147582e0e4f10dbc5b2ea02b791ba04734809abb51f44de7440d68ccc9a` | `1f2103abed9079e40f9617034db49f5086deeddc94e2327ca7df91a031fae5a7` |
| 632SP | R1R5 | high_severity | 0.010 | `6c2b21e34e8c623f7e3ef06740b6323c14aef3dcb23f40577876646adf2296cc` | `7bb0fc39a16aa9cc8296b566b0ad428af83b6092caf855624a2f82225fea183f` |
| 632SQ | R1R6 | baseline | 0.02048 | `3113971b9a47cc9ff960d4f6cea2007bfb938c9005b35b6d5d48a7a7fca0c82f` | `465f8cf59e949c0c8e52339cc8d1e6318b06b9bfb5908f506fffce079bd7b175` |
| 632SR | R1R6 | baseline | 0.010 | `b738a92189d834146606af9dc471189341f50aba77f100fac5b87b069d859a9b` | `bec0f576fc2c006992490dc0698a381d4aa4b38b7a8036a12f832114adfeb037` |
| 632SS | R1R6 | high_severity | 0.02048 | `1ec496daff791bf786d89d00ffeef840923e470339bfb88f7c4302220a328c3d` | `6ef74cd85a84d42d9a958df3427a06c9e98f5100ffcd0269f50fbe62dc33183a` |
| 632ST | R1R6 | high_severity | 0.010 | `91f8eb26a3dcf250faa710ec9f315379102116d316cf846d5a3f5c6dd64e59b3` | `6a2169c967d70fbcc1852307da86984ff0edf821e5e3d9b55459ec71e3e254b7` |

All 24 durable results remain Git-ignored scientific evidence by design.

All 24 successful raw logs remain Git-ignored scientific evidence by design.

The original failed STEP 632SE launch remains separately preserved:

- path: `results/raw/04_m8_target_mesh/_logs/step_632SE_R1R3_baseline_h_0p02048_local_target_mesh_case.log`
- SHA256: `f7f4de5877bed954067bb6d0fe22018d2923e04ce92efe35b7f31cbf71cbd443`
- failure evidence: one failed launch / traceback and zero permanent success markers

The later STEP 632SE-B retry is the authenticated successful R1R3 baseline `h=0.02048` result and is distinguishable from the preserved failed launch.

## 6. Local metric selection

Two M8-specific candidates were retained through the complete discretization study:

- `m8_matrix_vm_annulus_cell_tail10_v1`
- `m8_matrix_vm_annulus_quadrature_tail10_v1`

Both use the same physical toroidal void-annulus semantics and the same upper-10%-physical-area tail definition.

Both candidates passed the numerical acceptance thresholds.

Cell candidate evidence:

- median `delta_K`: `2.2370492190193936%`
- maximum `delta_K`: `4.626673376925477%`
- disposition: valid and numerically acceptable but not selected

Quadrature candidate evidence:

- median `delta_K`: `0.48368166407152385%`
- maximum `delta_K`: `1.1265826061942061%`
- baseline median: `0.5365858663861713%`
- high-severity median: `0.4272664777113654%`

The quadrature candidate was selected because it retained the same intended physical annulus/tail semantics, reproduced deterministic Stage-7 degree-8 extraction evidence, remained finite and valid at both severities, and showed substantially lower median and worst-case mesh dependence.

Selected metric:

`m8_matrix_vm_annulus_quadrature_tail10_v1`

Selected method:

`physical_quadrature_point_annulus_membership_with_physical_quadrature_area_weights`

Production quadrature degree:

`8`

The protected M7 identifier `m7_matrix_vm_annulus_tail10_v1` remains unchanged and was not relabeled.

## 7. Selected-metric 12-case target-mesh evidence

`delta_K = abs(K_h02048 - K_h0010) / abs(K_h0010)`

with `h=0.010` used as the fine-reference denominator for every case.

| Case | State | K(h=0.02048) | K(h=0.010) | delta_K (%) |
|---|---|---:|---:|---:|
| R1R1 | baseline | 1.68894353271395 | 1.67270884211269 | 0.970562849465 |
| R1R1 | high_severity | 1.65283817615805 | 1.66036157308869 | 0.453117986623 |
| R1R2 | baseline | 1.645451006093 | 1.64147034232968 | 0.242505981416 |
| R1R2 | high_severity | 1.65294587552167 | 1.6405948965436 | 0.752835389412 |
| R1R3 | baseline | 1.66377533136578 | 1.65452773918091 | 0.558926391252 |
| R1R3 | high_severity | 1.63325642204059 | 1.63654208507478 | 0.200768624538 |
| R1R4 | baseline | 1.7456710155425 | 1.74014596745906 | 0.317504863773 |
| R1R4 | high_severity | 1.7249198734446 | 1.74457394000489 | 1.126582606194 |
| R1R5 | baseline | 1.81499233218143 | 1.82591499800891 | 0.598202317161 |
| R1R5 | high_severity | 1.82317293108598 | 1.83052091605002 | 0.401414968800 |
| R1R6 | baseline | 1.67585664096011 | 1.68451920248591 | 0.514245341520 |
| R1R6 | high_severity | 1.67560803488525 | 1.68078359320455 | 0.307925323654 |

Selected-metric summary:

- case count: `12/12`
- baseline cases: `6/6`
- high-severity cases: `6/6`
- median `delta_K`: `0.48368166407152385%`
- maximum `delta_K`: `1.1265826061942061%`
- median criterion: `<=3%` — PASS
- individual-case criterion: no case `>5%` — PASS
- no case removed or response-selected

## 8. Final M8 target-mesh decision

The candidate production mesh `h=0.02048` is **ACCEPTED** for the locked M8 computational framework.

Decision basis:

1. the representative RVE remains the already accepted R1;
2. all six pristine R1 global target-mesh primary-response gates pass;
3. all 24 predeclared local-study durable executions are valid and authenticated;
4. both defect severities are represented;
5. the final M8 local metric is `m8_matrix_vm_annulus_quadrature_tail10_v1`;
6. the selected metric passes the median `<=3%` local criterion;
7. all 12 selected-metric cases pass the individual `<=5%` criterion;
8. no realization or severity was cherry-picked or omitted;
9. `h=0.010` remains the numerical fine reference, not an exact continuum claim.

Formal decision state:

- `FINAL_M8_TARGET_MESH_DECISION = ACCEPT_CANDIDATE_H_0P02048`
- `FINAL_M8_TARGET_MESH_LABEL = h_0p02048`
- `FINAL_M8_TARGET_MESH_SIZE = 0.02048`
- `FINAL_M8_FINE_REFERENCE_LABEL = h_0p010`
- `FINAL_M8_FINE_REFERENCE_SIZE = 0.010`
- `FINAL_M8_LOCAL_METRIC_ID = m8_matrix_vm_annulus_quadrature_tail10_v1`
- `FINAL_M8_LOCAL_TARGET_DECISION = PASS`

## 9. Checker/harness recovery provenance

Authenticated checker-only defects were not allowed to mutate valid science.

The final target-mesh decision specifically includes:

- STEP 632SX: stopped because a brittle literal grep did not match checkpoint Markdown formatting;
- STEP 632SX-A: read-only diagnosis proved the permanent protocol/checkpoint thresholds were scientifically unchanged;
- corrected STEP 632SX retry: semantic wording authentication passed and the final scientific target-mesh/local-target decision passed.

Earlier checker/harness recoveries recorded by the Stage-8 execution checkpoint also remain part of M8 provenance.

## 10. Interpretation boundary

This checkpoint supports the accepted target mesh and selected local metric only for the established M8 model class and verification protocol.

It does not establish:

- a universal mesh size for arbitrary materials or microstructures;
- exact continuum convergence of the fine reference;
- applicability to nonlinear, plastic, fracture, thermal, contact or three-dimensional physics;
- an M9 parameter-space definition;
- a production stochastic database;
- machine-learning validity.

## 11. Scope guard

The final M8 target-mesh/local-target decision and checkpoint preparation reused authenticated permanent/global/local evidence only.

They performed:

- no geometry generation
- no mesh generation
- no MPC construction
- no FEM/PBC solve
- no response integration rerun
- no additional scientific `delta_K` study after the authenticated comparison
- no local-metric reselection after the authenticated selection
- no target-mesh reselection after the authenticated decision
- no machine learning
- no M9 work
- no modification of scientific raw results/logs
- no modification of permanent source/config/protocol authority
- no modification or relabeling of the protected M7 metric

The scientific decision therefore records closure of the locked M8 target-mesh/local-response verification gates without manufacturing new simulation evidence during documentation.

## 12. M8 repository-closure sequencing

At the scientific state represented by this checkpoint, the M8 target-mesh/local-target decision is complete.

Permanent M8 milestone closure additionally requires repository-governance completion:

1. install this checkpoint as tracked `M8_TARGET_MESH_CHECKPOINT.md`;
2. create/update the M8 closure documentation, including the concise `PROJECT_STATUS.md`;
3. audit exact staged bytes;
4. commit the M8 closure documentation;
5. push and authenticate `HEAD = origin/main = public GitHub main`;
6. verify zero divergence and a clean repository;
7. only then classify M8 as permanently closed and consider transition beyond M8.

Git-ignored scientific JSON results and full raw logs remain durable local provenance and must not be force-added merely to publish them.

No M9 scientific execution or machine learning is authorized before permanent M8 repository closure.
