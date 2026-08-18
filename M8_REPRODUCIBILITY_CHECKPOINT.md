# M8 Reproducibility Environment Checkpoint

## Status

**Permanent M8 reproducibility environment checkpoint.**

M8 scientific work remains permanently closed at repository authority:

`b078281cbd6c46e58e5e6979cc4d24227ad1f932`

This checkpoint records the runtime/environment authority used for the
periodized MPC/PBC work completed during M8. It does not reopen,
recalculate, or reinterpret any M8 scientific result.

## 1. Environment lineage

Protected parent environment:

`composite-sim`

M8 compatibility environment:

`composite-sim-m8-mpc-compat`

The authenticated package comparison establishes:

- protected-parent package count: `369`
- M8-compatibility package count: `371`
- packages present only in protected parent: `0`
- changed common package versions/builds/channels: `0`
- packages added only to M8 compatibility environment: `2`

Exact additions:

- `dolfinx_mpc=0.11.0=py312h1d9f1b0_0` from `conda-forge`
- `libdolfinx_mpc=0.11.0=py312hc907639_0` from `conda-forge`

Therefore the M8 compatibility environment is the protected parent
scientific stack plus the exact DOLFINx-MPC compatibility dependency
pair; no authenticated common package was upgraded, downgraded, or
otherwise replaced.

## 2. Platform/runtime authority

- operating context: WSL2 Linux
- Conda platform: `linux-64`
- architecture: `x86_64`
- glibc: `2.39`
- Python: `3.12.13`
- NumPy: `2.5.1`
- SciPy: `1.18.0`
- mpi4py: `4.1.2`
- MPICH: `5.0.1`
- PETSc: `3.25.4`
- petsc4py: `3.25.4`
- UFL: `2026.1.0`
- Basix: `0.11.0`
- DOLFINx: `0.11.0`
- dolfinx_mpc: `0.11.0` Conda package authority
- Gmsh: `4.15.2` installed through pip

The authenticated single-rank `mpiexec` probe successfully imported
and exercised MPI/PETSc/DOLFINx/DOLFINx-MPC runtime identity.

## 3. Protected parent environment authority

Tracked protected-parent file:

`environment.yml`

SHA-256:

`f2e655e9999b4dc65a65c087517ac138f9e8e6e9fc344e6bf45dad32f56f9d67`

The protected parent file remains unchanged and is not replaced by the
M8 compatibility freeze.

## 4. Exact same-platform Conda authority

Temporary candidate:

`M8_COMPAT_ENVIRONMENT_EXPLICIT.txt`

SHA-256:

`750960332adb5719ee1b0197f6d7b128d338f53abf42a88137bb4b18bbbee392`

Line count:

`375`

This explicit specification records the exact Conda package artifacts
for the authenticated `linux-64` M8 compatibility environment.

It is a same-platform reproduction authority and is not claimed to be
a portable lock for arbitrary operating systems or architectures.

## 5. Pip-only authority

Temporary candidate:

`M8_COMPAT_PIP_REQUIREMENTS.txt`

SHA-256:

`b88104196c8e2f9f91748ec0fed2943c61d2b2f7d899ee8d821827eda9f8e925`

Exact content:

`gmsh==4.15.2`

Authenticated pip-only package count:

`1`

## 6. Saved environment variables

Authenticated saved Conda environment-variable count:

`0`

No additional saved Conda environment-variable state is required to
describe the M8 compatibility environment.

## 7. Reproduction boundary

For same-platform reconstruction, the exact Conda explicit
specification records the resolved Conda artifacts.

The pip-only requirement must then restore the separately installed
Gmsh Python package.

This checkpoint records the environment state that existed at M8
closure. It does not claim that future package repositories, mirrors,
operating systems, hardware, or external system libraries will remain
unchanged indefinitely.

## 8. Scientific boundary

Creation of the reproducibility freeze:

- performs no geometry generation;
- performs no mesh generation;
- performs no MPC scientific solve;
- performs no FEM/PBC solve;
- performs no response integration;
- recalculates no scientific statistic;
- reselects no RVE size;
- reselects no target mesh;
- reselects no local metric;
- starts no M9 work;
- performs no machine learning.

M8 scientific conclusions remain those already authenticated by the
permanent M8 closure commit.

## 9. Repository-governance state

At candidate creation:

- `HEAD = origin/main = public GitHub main`
- M8 closure commit:
  `b078281cbd6c46e58e5e6979cc4d24227ad1f932`
- repository/index/worktree: clean

No permanent reproducibility file has yet been installed.

M9 remains NOT STARTED.

Machine learning remains unauthorized.

## Hash-strengthened pip artifact authority

The pip-only M8 compatibility dependency is not merely version-pinned.
For the authenticated M8 same-platform Linux x86-64 reproduction record,
the selected binary distribution is:

- package: `gmsh==4.15.2`
- wheel: `gmsh-4.15.2-py2.py3-none-manylinux_2_24_x86_64.whl`
- wheel SHA256: `4076a948ce22625330d1413d4982e22b5c69fc2f0f7951f5df64c778cf54108c`
- requirement:
  `gmsh==4.15.2 --hash=sha256:4076a948ce22625330d1413d4982e22b5c69fc2f0f7951f5df64c778cf54108c`
- pip verification mode: `--require-hashes`
- distribution restriction: `--only-binary=:all:`
- dependency mode for this isolated pip supplement: `--no-deps`

The wheel metadata identifies Gmsh version `4.15.2`, and the wheel's
`gmsh.py` was independently shown to be byte-identical to the module
installed in `composite-sim-m8-mpc-compat`.

This is a same-platform reproducibility authority for the authenticated
M8 Linux x86-64 environment. It is not a claim that this specific wheel
is portable to arbitrary operating systems or architectures.

M9 remains NOT STARTED.

Machine learning remains unauthorized.
