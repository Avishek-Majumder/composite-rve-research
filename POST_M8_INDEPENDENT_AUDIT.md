# Post-M8 Independent Audit

## Status

**Permanent post-M8 independent-audit checkpoint.**

This checkpoint records the independent post-M8 audit performed before
authorization of M9.

Current repository authority:

`a129b7056df0e4ce94ea27aa1fb4f1430eb984d6`

At this checkpoint:

- M0 through M8 are accepted as scientifically and procedurally closed.
- M9 scientific execution remains NOT STARTED.
- Machine learning remains unauthorized.
- No M0-M8 milestone is reopened by this audit.
- No FEM/PBC solve, geometry generation, remeshing, response recalculation,
  target-mesh reselection or ML execution is authorized by this document.

## 1. Audit scope

The audit considered the complete available M0-M8 project history together
with the local repository/codebase and its Git/provenance state.

The audit scope included:

1. scientific sequencing and internal coherence;
2. consistency between recorded conversation claims and repository evidence;
3. source, protocol, checkpoint and result provenance;
4. Git history, HEAD/origin/public synchronization and cleanliness;
5. tracked versus Git-ignored raw evidence;
6. permanent result/checkpoint hashes where available;
7. environment and runtime reproducibility;
8. checker/harness failures versus actual scientific/source failures;
9. whether previously closed gates remain genuinely closed;
10. whether progression toward M9 remains scientifically justified.

This is an independent computational-project audit. It is not laboratory
validation and does not convert numerical reference solutions into exact
continuum truth.

## 2. Overall verdict

**PASS WITH DOCUMENTED CAVEATS — M0-M8 ACCEPTED; NO ROLLBACK OR BROAD RERUN REQUIRED.**

The available evidence supports the conclusion that the project remains
scientifically coherent, reproducible to the level documented by its
permanent authorities, correctly sequenced, and on-track for the next
planned milestone after completion of the remaining Pre-M9 closure work.

The audit found no contradiction that requires reopening M0-M8, changing an
authenticated scientific decision, rerunning the full M8 campaign, or
reselecting the accepted RVE or production target mesh.

The audit also found no basis to authorize M9 early. The remaining Pre-M9
documentation/provenance prerequisites must close first.

## 3. M8 closure remains authoritative

M8 remains permanently closed.

The audit accepts the existing M8 conclusions within the stated computational
scope, including:

- accepted representative RVE: R1;
- accepted production target mesh: `h = 0.02048`;
- fine mesh `h = 0.010` is a numerical reference, not exact continuum truth;
- the selected local target-mesh metric remains the authenticated
  quadrature-local matrix von-Mises annulus tail metric;
- production quadrature degree remains 8;
- Stage-8 durable local-target-mesh evidence remains 24 results;
- no M8 result is upgraded into a claim of universal material applicability.

This audit does not change any M8 result or decision.

## 4. Permanent documentary authorities

The following authenticated M8 authorities remain unchanged:

- `PROJECT_STATUS.md`
  SHA256: `7244166071e19b73db68b9a093c77e7fd5bb6a35df1b4fb44d9e6d48bfe695be`
- `M8_TARGET_MESH_CHECKPOINT.md`
  SHA256: `2cc4b55f15a5da2f9d6922de8032ad14b736e8768329ed90f22f4f08d9e1f5a8`
- `M8_RVE_REPRESENTATIVITY_CHECKPOINT.md`
  SHA256: `0f129f26c63dbf173572189d6c28ef43cf310920f2f5d1c5e1775ab8649fe420`
- `M8_TARGET_MESH_PROTOCOL.md`
  SHA256: `0d993cdfe0739b21a6ef34d8d74d72491a10682a3f6968824df25010c8ebb55f`
- `M8_STAGE8_LOCAL_TARGET_MESH_EXECUTION_CHECKPOINT.md`
  SHA256: `32c892f9b55e0af26e7e29760e2353333bc977884d82e763ff899a8f5889de69`

The current public repository authority after the environment-freeze closure is:

`a129b7056df0e4ce94ea27aa1fb4f1430eb984d6`

## 5. M8 compatibility-environment reproducibility closure

The dedicated M8 compatibility environment has now been permanently frozen.

Permanent authorities:

- `M8_REPRODUCIBILITY_CHECKPOINT.md`
  SHA256: `123fb448da8a5588596748b8ed32e7f42cd071eb5c32d15ab301a396d887f820`
- `reproducibility/M8_COMPAT_ENVIRONMENT_EXPLICIT.txt`
  SHA256: `750960332adb5719ee1b0197f6d7b128d338f53abf42a88137bb4b18bbbee392`
- `reproducibility/M8_COMPAT_PIP_REQUIREMENTS.txt`
  SHA256: `b88104196c8e2f9f91748ec0fed2943c61d2b2f7d899ee8d821827eda9f8e925`

The protected parent environment remains separate from the M8 compatibility
environment.

The authenticated parent-to-M8 package delta is exactly the intended two MPC
packages:

- `dolfinx_mpc`
- `libdolfinx_mpc`

No common protected-parent package version/build/channel was changed.

The explicit Conda authority is intentionally a same-platform Linux x86-64
reproduction record. It is not a claim of universal cross-platform
bit-identical portability.

The pip-installed Gmsh dependency is separately version- and artifact-hash
pinned.

## 6. Evidence and provenance caveat

The project deliberately keeps most raw simulation outputs outside normal Git
tracking.

Current local evidence inventory at audit time:

- `results/raw` files: `733`
- tracked files under `results/raw`: `2`
- ignored-untracked files under `results/raw`: `731`
- M8 target-mesh raw inventory: `305`
- Stage-8 durable JSON results: `24`

Therefore the public Git repository alone is not the complete historical raw
evidence archive.

This is a provenance limitation that must be documented explicitly; it is not
evidence that the authenticated scientific results are invalid.

A separate `M0_M8_EVIDENCE_MANIFEST.md` must record the available tracked and
Git-ignored evidence, durable authorities, and any historical/transient
evidence limitations before M9 begins.

## 7. Historical checker/harness failures

Several M8 failures were correctly diagnosed as checker/harness defects rather
than scientific defects.

The governing rule remains:

**A checker failure must first be classified as checker/harness versus
scientific/source failure before any authenticated science is changed.**

Examples include failures caused by:

- brittle Markdown spacing assumptions;
- duplicate global literal counts instead of section-scoped checks;
- line-coordinate or envelope assumptions;
- ambiguous substring matching such as `python` versus `cpython`;
- EOF/whitespace checks that require byte-level diagnosis.

Authenticated science must not be altered merely to satisfy a brittle checker.

## 8. Non-reopen rules

M0-M8 must not be reopened or broadly rerun unless new evidence establishes a
real contradiction, provenance break, scientific defect or invalidated
assumption.

The following are not sufficient reasons by themselves to reopen closed work:

- a brittle checker assumption;
- a cosmetic documentation preference;
- a different but scientifically equivalent implementation style;
- a desire to regenerate already authenticated output without new evidence.

If a genuine contradiction appears, it must be isolated, classified and
documented before any corrective scientific runtime is authorized.

## 9. Remaining Pre-M9 closure requirement

After this audit checkpoint itself is independently audited and permanently
installed, the remaining required Pre-M9 provenance artifact is:

`M0_M8_EVIDENCE_MANIFEST.md`

Until that manifest is permanently closed:

- M9 remains NOT STARTED.
- Machine learning remains unauthorized.

## 10. Mandatory M9 safeguards

M9 must begin only after all Pre-M9 prerequisites are committed, pushed,
publicly authenticated and the repository is clean.

Before authorizing the M9 stochastic pilot, M9 must deliberately lock:

1. the current literature/novelty position and publication framing;
2. final model inputs and output definitions;
3. normalization and units conventions;
4. final parameter ranges;
5. material-property anchors and allowed variation;
6. geometry feasibility and failure constraints;
7. random-seed and repeated-realization policy;
8. pilot sampling design and case-count policy;
9. per-run provenance and non-overwrite policy;
10. pilot QC/failure classification rules.

Specific numerical parameter ranges are **not** pre-authorized by this audit.
They must be justified and frozen during M9.

Before the pilot is authorized for production use, targeted transfer-validation
must be performed at scientifically difficult and/or extreme intended
production conditions rather than relying only on previously convenient M8
conditions.

## 11. Mandatory M10 safeguards

M10 must generate the main FEM database only from the final M9-locked
authority.

M10 must preserve:

- deterministic case identifiers and random seeds;
- geometry/material/input metadata;
- solver/runtime provenance;
- environment/repository authority;
- explicit success/failure status;
- non-overwrite raw outputs;
- durable QC summaries;
- grouping/realization identifiers needed for later leakage-safe validation;
- explicit records of invalid or failed cases rather than silently deleting
  them.

Dataset schema or scientific definitions must not change silently after M10
production begins.

Machine-learning training remains unauthorized until the M10 FEM dataset and
its QC/provenance gates are formally closed.

## 12. Scientific claim boundary

The project remains a normalized/dimensionless computational micromechanics
framework for the defined class of 2D isotropic, small-strain,
linear-elastic, plane-stress, perfectly bonded particle-reinforced composite
RVEs with circular particles and circular true matrix voids where applicable.

The audit does not support a claim that the framework works for all materials.

The audit does not provide experimental validation.

## 13. Final independent-audit decision

The independent post-M8 audit finds:

- no scientific contradiction requiring M0-M8 rollback;
- no need for a broad M8 rerun;
- no reason to alter the accepted RVE or target mesh;
- no identified environment-reproducibility gap remaining after the dedicated
  M8 compatibility freeze;
- a known raw-evidence/public-repository completeness limitation that must be
  documented by the evidence manifest;
- continued scientific justification for proceeding to M9 only after the
  remaining Pre-M9 closure artifacts are complete.

**POST-M8 INDEPENDENT AUDIT VERDICT: PASS WITH DOCUMENTED CAVEATS.**

M8 remains permanently closed.

M9 remains NOT STARTED.

Machine learning remains unauthorized.
