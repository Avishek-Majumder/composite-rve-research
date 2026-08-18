# M0-M8 Evidence Manifest

## Status

**Permanent M0-M8 evidence manifest.**

This document records the evidence and provenance state available at the
post-M8 / pre-M9 boundary. It does not reopen M0-M8 science and it does not
authorize M9 execution.

Repository authority for this evidence snapshot:

`d26baa0099d027c7862a5d19d614577a0e18dfed`

HEAD tree object:

`39610e311d909b0a0be15eef1fc7f13fb1b5dd5a`

At this checkpoint:

- M0 through M8 remain scientifically closed.
- The permanent M8 reproducibility freeze is already committed, pushed and
  publicly authenticated.
- The permanent post-M8 independent audit is already committed, pushed and
  publicly authenticated.
- M9 scientific execution remains NOT STARTED.
- Machine learning remains unauthorized.

## 1. Purpose and evidence classes

This manifest distinguishes four evidence classes.

1. **Tracked/public repository authority.**
   These paths are part of the committed Git tree and therefore travel with
   the public repository at the authenticated commit.
2. **Local Git-ignored evidence.**
   These files are present in the current local repository filesystem but are
   intentionally not represented as normal tracked Git content.
3. **Audit-time derived inventories.**
   Canonical path/size/SHA256 inventory files were generated under `/tmp`
   during STEP 632TN to authenticate the current local evidence snapshot.
   Their hashes are recorded here, but the `/tmp` files themselves are not
   claimed to be permanent repository artifacts.
4. **External historical inputs.**
   Conversation-history and other externally supplied audit inputs are not
   silently treated as Git-tracked evidence unless a repository path is
   explicitly identified below.

The public Git repository and the local ignored evidence therefore represent
different provenance layers. Neither layer should be described as the other.

## 2. Committed-tree and Git-history authority

At STEP 632TN:

- authenticated commit: `d26baa0099d027c7862a5d19d614577a0e18dfed`
- HEAD tree object: `39610e311d909b0a0be15eef1fc7f13fb1b5dd5a`
- tracked file count: `73`
- canonical tracked-path inventory SHA256:
  `016acce6db70025a7b178be86051823d55f7051c4e7fb01aace5855d78c078b8`
- canonical tracked-tree-entry inventory SHA256:
  `7495f598c0fbb65f7591052b7800684495fcce816da08d43af744574829c48e0`
- Git history record count: `79`
- canonical reverse-history TSV SHA256:
  `ade7aec601f351d0452c762ca73102ce65c727a683aa5ba625093b4855ddbf56`

The tracked-path inventory was generated from the recursive full-tree listing
of the authenticated HEAD. The Git-history authority was generated as one
canonical TSV row per commit containing commit SHA, parent SHA(s), author
timestamp and subject, in reverse chronological construction order from the
repository root commit to HEAD.

Tracked top-level scope populations:

- `.vscode` — `1` tracked paths
- `configs` — `4` tracked paths
- `docs` — `4` tracked paths
- `figures` — `1` tracked paths
- `logs` — `1` tracked paths
- `meshes` — `1` tracked paths
- `notebooks` — `1` tracked paths
- `reproducibility` — `2` tracked paths
- `results` — `10` tracked paths
- `src` — `28` tracked paths
- `tests` — `5` tracked paths

These aggregate authorities establish the exact committed repository snapshot
used by this manifest without implying that every tracked file is itself a
scientific result.

## 3. Permanent closure / reproducibility authorities

The following permanent tracked files are central post-M8 authorities:

- protected parent environment: `environment.yml` — bytes `7896`; SHA256 `f2e655e9999b4dc65a65c087517ac138f9e8e6e9fc344e6bf45dad32f56f9d67`
- PROJECT_STATUS: `PROJECT_STATUS.md` — bytes `30615`; SHA256 `7244166071e19b73db68b9a093c77e7fd5bb6a35df1b4fb44d9e6d48bfe695be`
- M8 target-mesh checkpoint: `M8_TARGET_MESH_CHECKPOINT.md` — bytes `16535`; SHA256 `2cc4b55f15a5da2f9d6922de8032ad14b736e8768329ed90f22f4f08d9e1f5a8`
- M8 representativity checkpoint: `M8_RVE_REPRESENTATIVITY_CHECKPOINT.md` — bytes `6159`; SHA256 `0f129f26c63dbf173572189d6c28ef43cf310920f2f5d1c5e1775ab8649fe420`
- M8 target-mesh protocol: `M8_TARGET_MESH_PROTOCOL.md` — bytes `15540`; SHA256 `0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f`
- M8 Stage-8 checkpoint: `M8_STAGE8_LOCAL_TARGET_MESH_EXECUTION_CHECKPOINT.md` — bytes `11817`; SHA256 `32c892f9b55e0af26e7e29760e2353333bc977884d82e763ff899a8f5889de69`
- M8 reproducibility checkpoint: `M8_REPRODUCIBILITY_CHECKPOINT.md` — bytes `5362`; SHA256 `123fb448da8a5588596748b8ed32e7f42cd071eb5c32d15ab301a396d887f820`
- M8 Conda explicit freeze: `reproducibility/M8_COMPAT_ENVIRONMENT_EXPLICIT.txt` — bytes `30979`; SHA256 `750960332adb5719ee1b0197f6d7b128d338f53abf42a88137bb4b18bbbee392`
- M8 hashed pip supplement: `reproducibility/M8_COMPAT_PIP_REQUIREMENTS.txt` — bytes `92`; SHA256 `b88104196c8e2f9f91748ec0fed2943c61d2b2f7d899ee8d821827eda9f8e925`
- post-M8 independent audit: `POST_M8_INDEPENDENT_AUDIT.md` — bytes `10367`; SHA256 `51a51adbd10abd41e961cc02a7d4d7fff5d603d433c5a2887249e9c7d039118d`

These authorities supplement, rather than replace, the complete 73-file Git
tree and its history.

## 4. Tracked result evidence

Exactly `10` paths are tracked under `results` at this snapshot.

Their tracked-path list SHA256 is:

`14666dbdbe4d0bf1be5db924c2635cbfeb6e05c716a5d7389eac7749aa4bfdc7`

Exact tracked result-file content authorities:

- `results/processed/.gitkeep` — bytes `0`; SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `results/processed/01_mesh_convergence_summary.csv` — bytes `2460`; SHA256 `d6ef1658dc56f51b67e94ccb4dcac9da665f897b5f94acaa0478f5caab4caae6`
- `results/processed/02_m3_mesh_convergence_verification.md` — bytes `3825`; SHA256 `98772ccd64b4406b3e375d95e5051079d44ca815a1198d3d5c5f32315271b9ff`
- `results/processed/03_m4_parameterization_audit.md` — bytes `3098`; SHA256 `c4eb4fdcf9a4a00e62549e83bd8dfde6918d6f07de8f25ec9ed017a7e646812a`
- `results/processed/04_m4_parameter_screening.md` — bytes `5350`; SHA256 `64e71b0396878703ba485d65e6a0ea267bf494c942f833a493575bba3ce63515`
- `results/processed/05_m4_sampling_domain_verification.md` — bytes `5624`; SHA256 `0a157771abd09980f6a508693cd8750a2481bb2d17016540751080eaa5faedd0`
- `results/processed/06_m4_lhs_initial_design.csv` — bytes `13656`; SHA256 `541ec9239b8f403e1d7d1f394b128324199039aca1678a98bce38a9c8f577b5c`
- `results/processed/07_m5_initial_fem_dataset.csv` — bytes `39209`; SHA256 `e48e9eb731b6e13eb15b33ab643722a9d72e8bdb933bf24d9c1c3847776c17d1`
- `results/raw/.gitkeep` — bytes `0`; SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `results/raw/01_mesh_convergence_runs.csv` — bytes `2408`; SHA256 `17aca35adc0f801b7db78bf68492d19a3d42c5d2bfed862c152a309c7bd5d5d7`

The `.gitkeep` entries are repository placeholders and should not be
misrepresented as substantive scientific result content.

The tracked documentary/reproducibility scope contains `27` paths with
canonical path-list SHA256:

`dabf10a474eeec33b1f0fadf02c6229b12c0256891f1e925e7586a1fbce6f420`

## 5. Current local raw-evidence snapshot

The current `results/raw` filesystem contains exactly:

- total regular files: `733`
- tracked files: `2`
- ignored-untracked files: `731`
- non-ignored-untracked files: `0`
- symlinks: `0`

Tracked raw paths are:

- `results/raw/.gitkeep`
- `results/raw/01_mesh_convergence_runs.csv`

Canonical path-list authorities:

- tracked raw path-list SHA256:
  `5e5c93b6c0b88be93d23b6376b3ff5c97c0baf9396df2099eca0b7d81393a6ed`
- ignored raw path-list SHA256:
  `2a425f53669ca766b3ef45fe0573d250fb88fe4af6e2a64b347d74af632c9a51`
- complete raw filesystem path-list SHA256:
  `e124b3270e492c7295bce4251733dfbc1a13b1540f7e243192ef138b4822861d`

The tracked and ignored-untracked raw pathsets together cover all `733`
regular files exactly. No raw file falls outside that classification in this
snapshot.

## 6. Cryptographic raw-content snapshot authority

STEP 632TN generated an audit-time canonical content inventory with one row
per local raw file in this exact format:

`classification<TAB>repository-relative-path<TAB>byte-size<TAB>sha256<LF>`

Rows were sorted by repository-relative path.

The resulting `733`-record audit-time content-manifest SHA256 is:

`38b17709c6b0d4259cbca88652e4cec96126d7e9ef7a5a313c41b27447b22e7a`

This SHA256 is a permanent record of the audit-time inventory identity once
this Markdown document is eventually committed, but the temporary TSV used to
calculate it is **not** itself claimed to be committed or permanently stored.

Top-level raw bucket authorities:

- `.gitkeep` — files `1`; bytes `0`; canonical content-manifest SHA256 `f33d5d61d04a0cc0763e40ba725d30780bfbb9378ebd142f39a6c251472c44e5`
- `01_mesh_convergence_runs.csv` — files `1`; bytes `2408`; canonical content-manifest SHA256 `4c479d303b57db7ee736717fc86b4a582191d6c2867b52a6a98f9037480812b3`
- `02_m5_initial_dataset` — files `60`; bytes `165151`; canonical content-manifest SHA256 `c652008f181b63d4a6987f7455c614f25c284bfd9f64b59ea00d6d68055889d8`
- `03_m8_rve_representativity` — files `366`; bytes `35425339`; canonical content-manifest SHA256 `4e2af0c84b09fd16532261c23ea3c5ea397d08da6735779af5a1c44843288dc6`
- `04_m8_target_mesh` — files `305`; bytes `34968477`; canonical content-manifest SHA256 `e87306ff77c9e6371cc8bee76005af4925e595d152dfc7918581ed7204a0bc80`

This cryptographic inventory allows a future audit to detect whether a
regenerated canonical local evidence inventory still matches this snapshot.
It does not contain or reconstruct the underlying ignored file bytes if those
files are later lost.

## 7. Milestone-oriented raw-evidence mapping

The current top-level `results/raw` layout is:

- `.gitkeep`
- `01_mesh_convergence_runs.csv`
- `02_m5_initial_dataset/`
- `03_m8_rve_representativity/`
- `04_m8_target_mesh/`

Authenticated milestone-oriented counts are:

- M5 raw bucket: `60` files
- M8 RVE representativity raw bucket: `366` files
- M8 target-mesh raw bucket: `305` files
- Stage-8 durable JSON results within the target-mesh evidence: `24`

The absence of a dedicated milestone-named raw directory must not be
interpreted as proof that no evidence exists for that milestone.

In particular:

- M3 has the tracked raw mesh-convergence record together with tracked
  processed convergence evidence.
- M4 has tracked parameterization, parameter-screening, sampling-domain and
  LHS-design records under `results/processed`.
- M5 has both the local raw bucket and the tracked processed initial FEM
  dataset.
- M6 and M7 do not have dedicated top-level raw buckets in the current layout;
  their repository provenance must therefore be read together with tracked
  source, design/checkpoint documentation, processed evidence where
  applicable, and Git history.
- M8 has dedicated local raw representativity and target-mesh evidence
  together with permanent tracked protocols, checkpoints, reproducibility
  records and the post-M8 independent audit.

This mapping documents the repository as it exists. It does not invent
historical raw files that are not present.

## 8. Other generated evidence scopes

STEP 632TN classified the principal generated-evidence directories as:

- `results/raw` — filesystem files `733`; tracked `2`; ignored-untracked `731`
- `results/processed` — filesystem files `8`; tracked `8`; ignored-untracked `0`
- `logs` — filesystem files `61`; tracked `1`; ignored-untracked `60`
- `meshes` — filesystem files `1`; tracked `1`; ignored-untracked `0`
- `figures` — filesystem files `8`; tracked `1`; ignored-untracked `7`

Across those five scopes there are exactly:

- canonical evidence-scope records: `811`
- tracked records: `13`
- ignored-untracked records: `798`
- canonical evidence-scope content-manifest SHA256:
  `ddc12a1ddaf0f7cb59bf9b6db1f52fbccf7c3a24eea8d4f5767050753d6fdfae`

The `logs` and `figures` ignored content is local evidence/provenance support,
not public Git content.

The single tracked entries in `logs`, `meshes` and `figures` may include
repository placeholders; path existence alone must not be interpreted as
substantive scientific evidence.

## 9. Repository-wide ignored-artifact boundary

The complete repository-wide ignored-untracked inventory contains `813`
paths with canonical path-list SHA256:

`4b1a1c71fc0116ccaed57a4aa21c618e9ba8483e4d8e32731156285fa829cb81`

Top-level breakdown:

- `figures` — `7` ignored-untracked paths
- `logs` — `60` ignored-untracked paths
- `results` — `731` ignored-untracked paths
- `src` — `12` ignored-untracked paths
- `tests` — `3` ignored-untracked paths

The evidence-scope audit cryptographically inventoried the evidence-bearing
`results`, `logs` and `figures` scopes described above.

The additional ignored paths under `src` and `tests` were inventoried as
ignored repository artifacts but were not semantically promoted to
scientific evidence merely because they exist. Their presence therefore must
not be used to make a scientific provenance claim without a separate
content-level classification.

## 10. Public-repository completeness limitation

The public Git repository is **not** the complete historical raw evidence
store for M0-M8.

At this snapshot:

- only `2` of the `733` `results/raw` files are tracked;
- `731` raw files are local and Git-ignored;
- `60` log files are local and Git-ignored;
- `7` figure files are local and Git-ignored.

Therefore cloning the public repository alone does not reproduce the complete
local raw/log/figure filesystem used during the work.

This is a documented provenance limitation, not a reason to reopen accepted
M0-M8 science.

The cryptographic inventory hashes in this manifest authenticate the current
local snapshot, but hashes are not backups: they cannot recover ignored file
content if the underlying local files are deleted or lost.

## 11. Historical and external-evidence limitation

The post-M8 independent audit records that the available M0-M8 project
history and local repository/codebase were considered together.

This Git evidence manifest does not silently claim that externally supplied
conversation-history DOCX files or other non-repository inputs are part of
the committed Git tree.

Unless such external artifacts are separately preserved and cryptographically
catalogued, this manifest authenticates the repository and the current local
ignored-evidence snapshot, not every external historical input ever used
during the project.

This distinction prevents the public repository from being described as more
complete than the evidence supports.

## 12. Reproducibility interpretation

For the authenticated M8 environment, the permanent reproducibility
checkpoint and its exact Conda/pip authorities remain the environment source
of truth.

For current local ignored evidence, this document records inventory hashes,
counts and provenance boundaries. It does not turn ignored files into tracked
files and does not authorize mass inclusion of raw solver output in normal
Git.

No FEM/PBC solve, geometry generation, remeshing, response recalculation,
target-mesh reselection, or machine-learning execution is performed or
authorized by this manifest.

## 13. Scientific non-reopen boundary

This evidence manifest does not alter any M0-M8 scientific result.

M0-M8 should only be reopened if genuinely new evidence establishes a real
scientific contradiction, invalidated result, provenance break or
reproducibility defect.

A missing dedicated raw directory name, an intentionally Git-ignored raw
artifact, or a brittle checker failure is not by itself sufficient reason to
change authenticated science.

The accepted M8 scientific decisions therefore remain unchanged.

## 14. Pre-M9 lifecycle boundary

This permanent manifest is the third required Pre-M9 closure artifact.
Pre-M9 closure is complete only when this manifest has been installed,
staged, committed, pushed and publicly authenticated together with the two
already permanent prerequisites:

1. permanent M8 compatibility-environment reproducibility freeze;
2. permanent post-M8 independent-audit checkpoint;
3. permanent M0-M8 evidence manifest.

At this manifest checkpoint:

- this manifest does not authorize M9 scientific execution;
- M9 remains NOT STARTED;
- Machine learning remains unauthorized.

## 15. Final evidence-manifest classification

The current repository/local evidence snapshot is internally classifiable and
cryptographically inventoryable without reopening M0-M8 science.

**CURRENT-SCOPE M0-M8 EVIDENCE INVENTORY: COMPLETE FOR THE AUTHENTICATED
REPOSITORY AND DETECTED LOCAL EVIDENCE PATHS, WITH HISTORICAL/EXTERNAL
COMPLETENESS LIMITATIONS DOCUMENTED.**

This statement does **not** claim that every historical raw artifact ever
generated has survived, that all ignored evidence is publicly reproducible,
or that every external conversation/audit input is stored in Git.

M9 remains NOT STARTED.

Machine learning remains unauthorized.
