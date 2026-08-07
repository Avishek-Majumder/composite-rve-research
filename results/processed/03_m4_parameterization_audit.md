# M4 Parameterization Audit

## Purpose

Audit the verified single-particle FEM model before converting it into
a reproducible parameter-driven RVE simulation engine.

No FEM/model assumptions were changed during this audit.

## Currently configurable and actively used

### Geometry

- `geometry.width`
- `geometry.height`

### Matrix material

- `matrix.youngs_modulus`
- `matrix.poissons_ratio`

### Particle material and geometry

- `particle.youngs_modulus`
- `particle.poissons_ratio`
- `particle.center_x`
- `particle.center_y`
- `particle.radius`

### Loading

- `loading.prescribed_x_displacement`

### Mesh

- `mesh.global_size`

The mesh size can also be overridden for one run with `--mesh-size`.

## Configuration values currently used only for reporting

- `model.name`
- `model.assumption`
- `model.interface`

`model.assumption: plane_stress` does not currently select the
constitutive formulation. Plane stress is implemented directly in
the solver.

`model.interface: perfect_bonding` does not currently select an
interface formulation. Perfect bonding is implicit in the shared
conforming displacement function space used by the matrix and
particle.

## Structural assumptions currently hard-coded

- Two-dimensional model.
- Rectangular RVE beginning at `(0, 0)`.
- One circular particle.
- One matrix region and one particle region.
- Matrix physical tag `1`.
- Particle physical tag `2`.
- Physical group names `matrix` and `particle`.
- Plane-stress constitutive formulation.
- Shared displacement field representing perfect bonding.
- First-order Lagrange displacement space.
- Uniaxial loading in the x direction.
- Left boundary has `ux = 0`.
- Right boundary has prescribed `ux`.
- Bottom-left vertex has `uy = 0` to remove rigid translation.
- No body force.
- Uniform global mesh size.
- Direct PETSc solve using `preonly` + `lu`.

## Hard-coded verification/output behavior

- Total-area absolute tolerance: `1.0e-10`.
- Particle-fraction error tolerance: `0.005`.
- Average axial-strain tolerance: `1.0e-8`.
- Effective modulus uses average `sigma_xx / epsilon_xx`.
- Effective Poisson response uses `-epsilon_yy / epsilon_xx`.
- Fixed displacement figure path:
  `figures/03_single_particle_displacement.png`.
- Fixed stress figure path:
  `figures/04_single_particle_sigma_xx.png`.
- Numerical results are printed to the terminal rather than written
  as a run-specific machine-readable record.

## Configuration/execution limitation

The solver currently loads only:

`configs/02_single_particle.yaml`

The configuration path is hard-coded and there is no general
`--config` argument.

## M3 working-mesh decision retained

For later global/effective-property simulations, M3 selected:

`global_size = 0.02048`

The existing YAML still contains `global_size = 0.05`.

No value was changed during this audit.

The working-mesh decision does not imply convergence of every local
stress extremum.

## M4 guardrails retained

- Interface assumption remains `perfect_bonding`.
- No defect type has been introduced.
- Established M2/M3 FEM assumptions remain unchanged.
