# M8 RVE Statistical Representativity Protocol

## Status

This document locks the statistical design for the M8 RVE-size
representativity study before ensemble generation or FEM execution.

It does not claim that any RVE level is representative yet.

The statistical study begins only after this protocol is independently
audited and committed.

## Scientific scope

The study concerns the existing M8 periodized two-phase particle
microstructures and the permanent periodic-boundary-condition solver.

The constitutive scope remains:

- two-dimensional
- small-strain
- linear elastic
- plane stress
- isotropic matrix and particle phases
- perfectly bonded particle/matrix interfaces
- circular particles
- no voids in this pristine RVE-size study

The matrix modulus is a reference scale. Publication-facing stiffness
and modulus quantities are therefore also reported normalized by
E_matrix.

## Separation of numerical questions

Element-level mesh convergence and statistical RVE representativity
are separate numerical questions.

This study changes RVE size and random realization while holding the
controlled microstructural density and constituent properties fixed.

The mesh size used here is a common screening resolution and is not,
by itself, the final M8 target-mesh decision.

## Locked RVE-size design

| Level | Side length | Area | Particle count |
|---|---:|---:|---:|
| R1 | 1.0 | 1.00 | 16 |
| R2 | 1.5 | 2.25 | 36 |
| R3 | 2.0 | 4.00 | 64 |
| R4 | 2.5 | 6.25 | 100 |
| R5 | 3.0 | 9.00 | 144 |

Particle radius = 0.05

Particle number density = 16.0

Analytical particle area fraction =
0.12566370614359174

The particle number density and analytical particle fraction are
identical across R1-R5.

The RVE-size variable is therefore not intentionally confounded with
particle radius, number density, or analytical particle fraction.

## Periodized stochastic ensemble

Every realization is generated independently using the permanent
periodized random-uniform rejection generator.

The stochastic geometry controls are locked across all RVE levels and
all realizations:

- minimum toroidal particle surface gap = 0.02
- maximum placement attempts per particle = 20000

The minimum-gap value is part of the stochastic geometry definition and
must not vary with RVE size or realization.

The maximum-attempt count is a deterministic generation/failure policy,
not a material parameter. It is held fixed so that invalid-placement
handling remains reproducible.

A realization that cannot be generated under these locked controls must
be recorded as invalid and must not be silently rerun with relaxed
spacing, a different attempt limit, or a substitute seed.

Periodic boundary-crossing particles are represented through the
existing toroidal wrapped-image policy.

No realization may be selected because its mechanical response appears
typical, isotropic, desirable, or close to another realization.

## Deterministic seed policy

Seed namespace:

`m8-rve-representativity-v1`

For RVE level L and one-based realization index i, the seed is defined
before any result is observed by:

`SHA256("m8-rve-representativity-v1|L|iiii")`

where `iiii` is the zero-padded four-digit realization index.

The first eight digest bytes are interpreted as one unsigned big-endian
64-bit integer.

This schedule extends deterministically beyond the initial pilot.

A failed or invalid predeclared seed must never be silently replaced by
a different seed. The failure must be recorded and diagnosed.

## Pilot ensemble

Initial pilot sample size per RVE level:

n0 = 6

Therefore the initial complete pilot contains:

5 RVE levels x 6 realizations = 30 independent microstructures.

The value six is a pilot minimum, not a declaration that six
realizations are statistically sufficient.

### Locked pilot seeds

| RVE | Realization | Seed |
|---|---:|---:|
| R1 | 1 | 15944426988753885521 |
| R1 | 2 | 14726087059387717211 |
| R1 | 3 | 16304908395315497179 |
| R1 | 4 | 8543608591806175946 |
| R1 | 5 | 9043192476962390047 |
| R1 | 6 | 4715493001954948121 |
| R2 | 1 | 8959588066430205224 |
| R2 | 2 | 2748981751842334585 |
| R2 | 3 | 14654959448747560437 |
| R2 | 4 | 10490406078943403795 |
| R2 | 5 | 14754115464194099490 |
| R2 | 6 | 15457697788873575750 |
| R3 | 1 | 1520765391204056186 |
| R3 | 2 | 16979900204114328306 |
| R3 | 3 | 10549065626574797093 |
| R3 | 4 | 7861334562030830773 |
| R3 | 5 | 16910014617435099714 |
| R3 | 6 | 11244707517112643570 |
| R4 | 1 | 7473245128805372283 |
| R4 | 2 | 5842223636676267490 |
| R4 | 3 | 15017694034673515666 |
| R4 | 4 | 8721460711076261101 |
| R4 | 5 | 14546067014408498300 |
| R4 | 6 | 13366916596302023254 |
| R5 | 1 | 1697541442752212169 |
| R5 | 2 | 4957153589961240624 |
| R5 | 3 | 8294668839306064549 |
| R5 | 4 | 138802719123899342 |
| R5 | 5 | 13653657189806206435 |
| R5 | 6 | 5708623245519862930 |

## Mechanical response per valid realization

Every valid microstructure used for mechanical representativity must
use the same constituent configuration and must execute all three
permanent PBC macroscopic load cases:

- X
- Y
- XY engineering shear

The three columns are assembled into the complete 3x3 engineering-Voigt
homogenized stiffness tensor.

Per-realization scientific hard gates already established in the
permanent solver must pass, including:

- PETSc convergence
- constrained algebraic equilibrium
- deterministic gauge validity
- periodic fluctuation consistency
- recovered macroscopic strain
- Hill-Mandel consistency
- weak stationarity
- finite stiffness response
- positive load-direction stiffness

A realization that fails a scientific hard gate is not silently
discarded and replaced.

## Common screening mesh

RVE-size statistical screening mesh size:

h = 0.025

This preserves common local discretization resolution across R1-R5.

The permanent mesher's existing geometric, periodic, cell-tag,
positive-area, and particle-fraction validity gates remain mandatory.

The final publication-facing target-mesh decision remains a separate
M8 mesh-sensitivity gate.

## Ensemble quantities to retain

For every RVE level, retain the complete per-realization normalized
stiffness tensor C/E_matrix and the derived engineering responses.

Primary statistical precision quantities are:

- E_x / E_matrix
- E_y / E_matrix
- G_xy / E_matrix

Also retain and report:

- nu_xy
- nu_yx
- C11 / E_matrix
- C22 / E_matrix
- C12 / E_matrix
- C66 / E_matrix
- C16 / E_matrix
- C26 / E_matrix
- complete normalized stiffness tensor
- meshed particle fraction
- all solver hard-gate diagnostics

Single-realization isotropy is not imposed.

## Statistical estimators

For each RVE level and each retained scalar response, compute:

- arithmetic sample mean
- unbiased sample standard deviation with ddof=1
- coefficient of variation where the mean is safely nonzero
- minimum
- maximum
- nominal 95 percent Student-t confidence interval on the mean

For a primary positive response q with n realizations, the nominal
Student-t 95 percent confidence half-width is:

H_q = t_(0.975,n-1) * s_q / sqrt(n)

and its relative half-width is:

r_q = H_q / abs(mean(q))

## Statistical precision hard gate

Confidence level:

0.95

Primary relative confidence-half-width tolerance:

0.01

Equivalently, the 95 percent confidence half-width must be no greater
than 1 percent of the sample mean for each of:

- E_x / E_matrix
- E_y / E_matrix
- G_xy / E_matrix

The initial six realizations are evaluated first.

If a level fails the precision gate, its sample count is increased
using the already predeclared deterministic seed sequence.

Additional realizations are added without changing the acceptance
tolerance.

There is no scientific PASS caused solely by reaching a computational
budget limit.

If resource constraints prevent the confidence criterion from being
reached, the level remains statistically unresolved.

## Adaptive sample-size rule

After the pilot, the observed mean and unbiased sample standard
deviation are used as planning estimates for the additional sample size
required by the locked precision criterion.

For each primary response q at current sample size n, define
n_req,q as the smallest integer m greater than n satisfying:

t_(0.975,m-1) * s_q / sqrt(m)
/
abs(mean(q))
<= 0.01

where the current observed mean(q) and s_q are held fixed while
searching over candidate m.

The next deterministic target sample count for that RVE level is:

n_target =
max(n_req,Ex, n_req,Ey, n_req,Gxy)

The realization indices n+1 through n_target are then generated using
the already locked deterministic seed schedule.

If all three primary precision gates already pass at the current sample
size, no additional realization is added.

After expansion, all statistics are recomputed from the complete sample.
If any primary precision gate still fails, the same deterministic
planning calculation is repeated using the updated complete-sample
statistics.

The final sample count is therefore data-informed through observed
dispersion rather than chosen as an arbitrary universal constant.

Because this rule permits repeated adaptive inspection of the sample,
the Student-t intervals are treated as nominal precision diagnostics.
The protocol does not claim time-uniform 95 percent sequential coverage.

There is no seed selection based on the sign, magnitude, desirability,
isotropy, or direction of a mechanical response.

No predeclared realization may be removed because its response moves
the mean in a preferred direction.

## Tensor-level size-stability diagnostic

For every RVE level k, form the ensemble-mean normalized stiffness
tensor:

Cbar_k / E_matrix

For two levels k and j, define the relative Frobenius shift:

D_C(k,j) =
|| Cbar_k - Cbar_j ||_F
/
|| Cbar_j ||_F

Locked size-stability tolerance:

0.01

A candidate level must have a mean normalized stiffness tensor within
1 percent, in Frobenius norm, of every larger tested RVE level.

In addition, the ensemble means of:

- E_x / E_matrix
- E_y / E_matrix
- G_xy / E_matrix

must each change by no more than 1 percent relative to every larger
tested RVE level.

Poisson-ratio evolution, stiffness coupling terms, and ensemble
anisotropy are retained as scientific diagnostics and reported rather
than artificially forced to zero.

## Final representativity acceptance rule

R1, R2, R3, R4, and R5 are evaluated in increasing physical size.

A tested level is eligible for acceptance only if at least one strictly
larger tested RVE level exists as a statistically resolved comparator.

Therefore, within the initial R1-R5 study, R1 through R4 may be
acceptance candidates and R5 serves as the largest comparison level.
R5 cannot itself be accepted solely because no larger level exists.

The accepted RVE level is the smallest eligible tested level Rk for
which all of the following are true:

1. Its primary nominal 95 percent Student-t precision gates pass.
2. Every larger tested level used for comparison also has statistically
   resolved primary means.
3. At least one strictly larger statistically resolved comparison level
   exists.
4. The normalized mean stiffness-tensor shift from Rk to every larger
   tested level is no greater than 1 percent.
5. The mean E_x/E_matrix, E_y/E_matrix, and G_xy/E_matrix shifts from
   Rk to every larger tested level are each no greater than 1 percent.
6. All contributing realizations passed the existing geometry, mesh,
   MPC, FEM, periodicity, equilibrium, and energy-consistency gates.
7. No failed realization was silently replaced or cherry-picked.

If none of R1 through R4 satisfies these requirements against the
resolved larger levels through R5, M8 must not claim that an RVE size
has yet been established.

The size study must then be extended beyond R5 before R5 can become an
acceptance candidate, or the statistical design must be scientifically
revisited.

## Bias and fluctuation diagnostics

Random dispersion and systematic finite-size drift are treated as
different phenomena.

For publication diagnostics, record the decrease of standard deviation
with increasing RVE side length.

Because this is a 2D study, an L^-1 standard-deviation trend is a useful
central-limit-type reference diagnostic for a periodized ensemble.

Also inspect the drift of ensemble means with RVE size.

An L^-2 bias trend may be plotted as a theoretical reference diagnostic
for suitable periodized ensembles, but it is not a hard gate here
because the rigorous assumptions of the corresponding stochastic
homogenization theory are not identical to this hard-core particle
generator.

Observed data determine the actual M8 conclusion.

## Ensemble isotropy diagnostics

The underlying random circular-particle construction is intended to
have no preferred material direction.

Nevertheless, isotropy is not imposed on any individual realization.

For each RVE level, report at minimum:

A_E =
abs(mean(E_x) - mean(E_y))
/
(0.5 * (mean(E_x) + mean(E_y)))

and the ensemble-mean normalized coupling terms:

mean(C16) / E_matrix

mean(C26) / E_matrix

These are convergence diagnostics, not values to be manually zeroed.

## Publication reporting requirement

The final M8 RVE-size report must show, for every tested RVE level:

- final number of valid independent realizations
- deterministic seed provenance
- sample means
- sample standard deviations
- coefficients of variation
- 95 percent confidence intervals
- normalized mean stiffness tensor
- engineering-response means
- RVE-size stability differences
- anisotropy/coupling diagnostics
- any failed realization and its reason
- mesh resolution used for the statistical screening

The conclusion must distinguish:

- random sampling uncertainty
- systematic RVE-size dependence
- element-level mesh sensitivity

## Literature basis

Kanit et al. (2003), International Journal of Solids and Structures,
40, 3647-3679.
DOI: 10.1016/S0020-7683(03)00143-4

Ghossein and Levesque (2012), International Journal of Solids and
Structures, 49, 1387-1398.
DOI: 10.1016/j.ijsolstr.2012.02.021

Schneider, Josien and Otto (2022), Journal of the Mechanics and Physics
of Solids, 158, 104652.
DOI: 10.1016/j.jmps.2021.104652

Clozeau, Josien, Otto and Xu (2024), Foundations of Computational
Mathematics, 24, 1305-1387.
DOI: 10.1007/s10208-023-09613-y

## Scope guard

This protocol does not generate geometry.

This protocol does not generate a mesh.

This protocol does not import a DOLFINx mesh.

This protocol does not construct an MPC.

This protocol does not perform an FEM solve.

This protocol does not declare any RVE level statistically
representative.

Computational RVE-size representativity begins only after this design
is independently audited and accepted.
