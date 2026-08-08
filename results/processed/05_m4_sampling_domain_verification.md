# M4 Sampling-Domain Verification

## Purpose

Document the proposed first perfect-bonding M4 parameter domain and
the numerical evidence supporting retention of the M3 working mesh
for effective-property dataset generation.

No defect type has been introduced.

The established model assumptions remain:

- dimension: 2
- assumption: plane_stress
- interface: perfect_bonding
- small-strain linear elasticity

## Normalized parameterization

The first M4 perfect-bonding sampling space uses four normalized or
material parameters:

1. particle area fraction, phi_p
2. particle-to-matrix stiffness ratio, E_particle / E_matrix
3. matrix Poisson ratio, nu_matrix
4. particle Poisson ratio, nu_particle

Fixed simulation controls:

- geometry.width = 1.0
- geometry.height = 1.0
- particle.center_x = 0.5
- particle.center_y = 0.5
- matrix.youngs_modulus = 1000.0
- loading.prescribed_x_displacement = 0.01
- mesh.global_size = 0.02048

Derived quantities:

- particle.radius =
  sqrt(phi_p * width * height / pi)
- particle.youngs_modulus =
  stiffness_ratio * matrix.youngs_modulus

The normalized mapping exactly reproduces the verified baseline:

- phi_p = 0.12566370614359174
- stiffness ratio = 10.0
- radius = 0.2
- particle Young's modulus = 10000.0

## Proposed first sampling domain

- particle area fraction:
  0.05 <= phi_p <= 0.30

- particle-to-matrix stiffness ratio:
  2.0 <= E_particle / E_matrix <= 20.0

- matrix Poisson ratio:
  0.20 <= nu_matrix <= 0.40

- particle Poisson ratio:
  0.15 <= nu_particle <= 0.35

All verified baseline parameter values lie inside these bounds.

For the normalized 1 x 1 RVE:

- phi_p = 0.05 gives radius = 0.126156626101008
- phi_p = 0.30 gives radius = 0.30901936161855165
- minimum particle-to-boundary clearance at phi_p = 0.30:
  0.19098063838144835

Therefore the centered circular particle remains strictly inside the
RVE throughout the proposed particle-fraction interval.

## Lower-corner FEM verification

Test point:

- phi_p = 0.05
- stiffness ratio = 2.0
- nu_matrix = 0.20
- nu_particle = 0.15
- mesh size = 0.02048

Result:

- cell count = 5688
- analytical particle fraction = 0.05
- meshed particle fraction = 0.04978398413861924
- particle-fraction error = 0.00021601586138075834
- effective modulus = 1030.6871327997894
- effective Poisson response = 0.19898653287189544
- all stored FEM verification flags passed

Classification:

**LOWER DOMAIN CORNER VERIFIED**

## Upper-corner FEM verification

Test point:

- phi_p = 0.30
- stiffness ratio = 20.0
- nu_matrix = 0.40
- nu_particle = 0.35

Working-mesh result at h = 0.02048:

- cell count = 5698
- analytical particle fraction = 0.30
- meshed particle fraction = 0.29978133083710395
- particle-fraction error = 0.00021866916289603466
- effective modulus = 1626.4724442012891
- effective Poisson response = 0.3852447662008514
- all stored FEM verification flags passed

Classification:

**UPPER DOMAIN CORNER VERIFIED**

## Upper-corner three-level mesh study

Three systematically refined mesh sizes were tested:

- h3 = 0.02048
- h2 = 0.01024
- h1 = 0.00512

Refinement ratio:

- r = 2.0

### Effective modulus

Values:

- h = 0.02048:
  1626.4724442012891
- h = 0.01024:
  1626.0598070652052
- h = 0.00512:
  1625.9684360747958

Successive differences:

- 0.02048 -> 0.01024:
  0.0253765042522456%
- 0.01024 -> 0.00512:
  0.0056194811893111206%

Formal grid-convergence quantities:

- observed order p = 2.1750655667697933
- Richardson extrapolated value =
  1625.9424493407412
- finest-grid GCI = 0.001997788939042879%
- medium-grid GCI = 0.009021633456686712%
- asymptotic-range ratio =
  0.9999438083457861
- working mesh vs Richardson estimate =
  0.03259616358271793%

### Effective Poisson response

Values:

- h = 0.02048:
  0.3852447662008514
- h = 0.01024:
  0.385447611131137
- h = 0.00512:
  0.38550885944146007

Successive differences:

- 0.02048 -> 0.01024:
  0.05262581072699766%
- 0.01024 -> 0.00512:
  0.015887653116921273%

Formal grid-convergence quantities:

- observed order p = 1.7276352959567698
- Richardson extrapolated value =
  0.3855353526975733
- finest-grid GCI = 0.008590352551032746%
- medium-grid GCI = 0.028454439689858627%
- asymptotic-range ratio =
  1.0001589017769323
- working mesh vs Richardson estimate =
  0.07537220508797624%

## Production-mesh decision

Retain:

`mesh.global_size = 0.02048`

for M4 perfect-bonding dataset generation when the primary FEM
targets are:

- effective axial modulus
- effective Poisson response

The upper-domain three-grid study shows systematic convergence and
asymptotic-range ratios approximately equal to 1.

The working-mesh deviation from the Richardson-extrapolated value at
the tested demanding upper corner is below 0.1% for both primary
effective-property targets.

## Important limitation

This production-mesh decision applies to domain-averaged effective
properties.

Local stress extrema remain diagnostic quantities and are not claimed
to be fully mesh-converged.

## Sampling status

The proposed parameter domain has now passed:

- normalized-mapping verification
- geometric feasibility checks
- lower-corner FEM verification
- upper-corner FEM verification
- upper-corner three-level mesh convergence verification

Production Latin-hypercube samples have NOT yet been generated.

No production sample count has yet been selected.

## Guardrails retained

- No defect type has been introduced.
- Interface remains perfect_bonding.
- Plane-stress formulation remains unchanged.
- Particle center remains fixed at (0.5, 0.5).
- Prescribed displacement remains 0.01.
- Matrix Young's modulus remains 1000.0.
