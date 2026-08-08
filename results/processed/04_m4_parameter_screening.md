# M4 Parameter-Space Screening

## Purpose

Record the numerical screening performed before defining the actual
M4 sampling space.

No defect type has been introduced.

The verified model assumptions remain:

- dimension: 2
- assumption: plane_stress
- interface: perfect_bonding
- small-strain linear elasticity

## Verified M4 baseline

Configuration:

`configs/03_parametric_rve_base.yaml`

Working mesh selected in M3:

`global_size = 0.02048`

Baseline response:

- cell count: 5704
- effective modulus: 1184.4588076691466
- effective Poisson response: 0.3014325439907935
- analytical particle fraction: 0.12566370614359174

## Parameter-screening conclusions

### 1. Prescribed displacement magnitude

Diagnostic:

`ux = 0.01 -> 0.005`

Result:

- stress and strain scaled linearly
- effective modulus unchanged
- effective Poisson response unchanged

Classification:

**FIXED SIMULATION CONTROL**

For the current linear-elastic effective-property problem,
prescribed displacement magnitude is not required as an ML input.

Baseline retained:

`prescribed_x_displacement = 0.01`

### 2. Absolute geometric scale

Diagnostic:

All lengths scaled by 2 while preserving relative geometry,
macroscopic strain, and relative mesh resolution.

Result:

- cell count unchanged
- particle fraction unchanged
- effective modulus unchanged
- effective Poisson response unchanged

Classification:

**REDUNDANT ABSOLUTE SCALE**

The parameter space should use relative/dimensionless geometry rather
than absolute RVE size for the current scale-free continuum model.

### 3. Common Young's-modulus scale

Diagnostic:

- matrix E: 1000 -> 2000
- particle E: 10000 -> 20000
- stiffness ratio remained 10

Result:

- effective modulus scaled by 2
- effective Poisson response unchanged
- normalized effective modulus E_eff / E_matrix unchanged

Classification:

**ANALYTICALLY SEPARABLE SCALE**

A later design decision is still required on whether to:

- fix a reference matrix modulus and sample stiffness contrast, or
- retain dimensional modulus scale as an explicit input.

No decision is made here.

### 4. Particle radius / particle fraction

Diagnostic:

`radius = 0.20 -> 0.18`

Result:

- analytical particle fraction change: -19.0%
- effective-modulus change: -3.2941895028182664%
- effective-Poisson change: -0.08489461402595591%

Classification:

**STRONG CANDIDATE PARAMETER**

The later sampling variable should preferably be expressed using a
dimensionless geometric quantity such as particle fraction or
relative radius.

No sampling bounds are selected here.

### 5. Particle-to-matrix stiffness contrast

Diagnostic:

`E_particle / E_matrix = 10 -> 5`

Result:

- effective-modulus change: -2.645299077712984%
- effective-Poisson change: -0.6337417301776177%

Classification:

**STRONG CANDIDATE PARAMETER**

No sampling bounds are selected here.

### 6. Particle Poisson ratio

Diagnostic:

`particle nu = 0.25 -> 0.30`

Result:

- effective-modulus change: +0.004434453491054813%
- effective-Poisson change: +0.46006470302158603%

Classification:

**CANDIDATE PARAMETER**

Its influence is substantially stronger on effective Poisson response
than on effective modulus.

No sampling bounds are selected here.

### 7. Matrix Poisson ratio

Diagnostic:

`matrix nu = 0.30 -> 0.25`

Result:

- effective-modulus change: +0.0708769986974576%
- effective-Poisson change: -14.998591437373591%

Classification:

**STRONG CANDIDATE PARAMETER**

Matrix Poisson ratio strongly influences the effective Poisson
response in the present RVE.

No sampling bounds are selected here.

### 8. Particle horizontal position

Diagnostics:

- centered: center_x = 0.50
- right: center_x = 0.60
- mirror-left: center_x = 0.40

Right-versus-centered effective-modulus change:

+0.22047047749609075%

Mirror comparison:

- E_eff difference: 0.001062233001811027%
- effective-Poisson difference: 0.001096786331370341%

Classification:

**CONDITIONAL CANDIDATE**

The response is position-sensitive and mirror-consistent, but the
effect may depend on the current finite-RVE boundary-condition
formulation.

Do not adopt center_x as a final sampling variable until the
boundary-condition implications are explicitly resolved.

### 9. Particle transverse position

Diagnostics:

- centered: center_y = 0.50
- upper: center_y = 0.60
- mirror-lower: center_y = 0.40

Upper-versus-centered changes:

- effective modulus: -0.016728536810306185%
- effective Poisson response: +0.22657486005270258%

Mirror comparison:

- E_eff difference: 0.00027521678866997037%
- effective-Poisson difference: 0.00009474137967139128%

Classification:

**CONDITIONAL CANDIDATE**

The response is position-sensitive and highly mirror-consistent, but
the same boundary-condition caution applies as for center_x.

## Sampling tooling verified

SciPy 1.18.0 is installed in the `composite-sim` environment.

Verified capabilities:

- `scipy.stats.qmc.LatinHypercube`
- deterministic sampling using an explicit RNG seed
- `qmc.scale`
- `qmc.discrepancy`

No physical sampling ranges or production sample counts have yet
been selected.

## M4 guardrails retained

- No defect type has been introduced.
- Interface remains `perfect_bonding`.
- Plane-stress formulation remains unchanged.
- M3 working-mesh decision remains unchanged.
- Local stress extrema are not assumed fully mesh-converged.
