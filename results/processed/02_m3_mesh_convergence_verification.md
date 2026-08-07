# M3 Mesh Convergence and Composite Verification

## Model

Single-particle particle-reinforced composite.

- Assumption: 2D plane stress
- Interface: perfect bonding
- Matrix Young's modulus: 1000.0
- Matrix Poisson's ratio: 0.30
- Particle Young's modulus: 10000.0
- Particle Poisson's ratio: 0.25
- Particle radius: 0.20
- Prescribed axial displacement: 0.01

## Mesh-refinement study

Six systematically refined meshes were evaluated while keeping the
physical problem unchanged.

| Mesh size | Total cells | Effective axial modulus |
| ---: | ---: | ---: |
| 0.050000 | 1028 | 1185.0360066857736 |
| 0.040000 | 1550 | 1184.749423713406 |
| 0.032000 | 2448 | 1184.6157474631816 |
| 0.025600 | 3806 | 1184.5203693269168 |
| 0.020480 | 5704 | 1184.4588076691466 |
| 0.016384 | 8954 | 1184.423602454499 |

## Global-response convergence

Successive effective-modulus differences decreased to:

- 0.0241893%
- 0.0112844%
- 0.00805205%
- 0.00519745%
- 0.00297235%

At mesh size 0.02048, relative to the finest tested mesh:

- Effective axial modulus difference: 0.00297235%
- Effective Poisson-response difference: 0.01131596%

The global/effective composite response therefore shows strong
mesh stabilization over the tested refinement sequence.

## Particle-geometry convergence

The absolute particle-fraction error decreased monotonically from:

0.0012195607140616516

to:

0.00013940948111426654

between the coarsest and finest tested meshes.

This confirms systematic improvement of the polygonal representation
of the circular particle interface with refinement.

## Local-stress sensitivity

At the finest refinement, the latest successive differences were:

- Matrix sigma_xx minimum: 2.281099%
- Matrix sigma_xx maximum: 0.628472%
- Particle sigma_xx minimum: 0.435270%
- Particle sigma_xx maximum: 0.077629%

Therefore, the global/effective response is strongly stabilized, but
all local stress extrema must not be claimed to be fully mesh-converged.
The matrix sigma_xx minimum remains notably mesh-sensitive.

## Practical working mesh

For later simulations focused on global/effective properties, the
selected practical working mesh is:

- global_size = 0.02048
- total cells in the reference model = 5704

This choice reduces the reference-model cell count by approximately
36% relative to the finest tested mesh while retaining extremely close
agreement in the global effective response.

This working-mesh choice is not a claim that every local interface
stress extremum is converged.

## MPI verification

The global_size = 0.02048 model was independently solved using two MPI
ranks.

Serial effective axial modulus:
1184.4588076691466

Two-rank MPI effective axial modulus:
1184.4588076691493

The serial and two-rank results agree essentially to floating-point
precision.

## Composite modulus sanity check

Using the analytical particle fraction:

0.12566370614359174

the simple Voigt/Reuss estimates were:

- Reuss estimate: 1127.5194449852283
- FEM effective modulus at global_size 0.02048: 1184.4588076691466
- Voigt estimate: 2130.973355292326

The FEM effective modulus lies between these simple estimates.

This is used only as an independent micromechanics sanity check and is
not treated as proof of exactness for the specific 2D plane-stress
boundary-value problem.

## M3 scientific conclusion

The single-particle composite's important global mechanical response
is not an artifact of the original global_size = 0.05 mesh.

Mesh refinement demonstrates strong stabilization of the effective
axial modulus and effective Poisson response, systematic improvement
of the circular-particle geometry representation, and reproducibility
between serial and two-rank MPI execution.

Local stress extrema remain more mesh-sensitive than global quantities
and must be reported with that qualification.
