# Test for rayleigh damping implemented using HHT time integration
#
# The test is for an 1D bar element of  unit length fixed on one end
# with a ramped pressure boundary condition applied to the other end.
# zeta and eta correspond to the stiffness and mass proportional rayleigh damping
# alpha, beta and gamma are HHT time integration parameters
# The equation of motion in terms of matrices is:
#
# M*accel + (eta*M+zeta*K)*[(1+alpha)vel-alpha vel_old]
# + alpha*(K*disp - K*disp_old) + K*disp = P(t+alpha dt)*Area
#
# Here M is the mass matrix, K is the stiffness matrix, P is the applied pressure
#
# This equation is equivalent to:
#
# density*accel + eta*density*[(1+alpha)vel-alpha vel_old]
# + zeta*[(1+alpha)*d/dt(Div stress)- alpha*d/dt(Div stress_old)]
# + alpha *(Div stress - Div stress_old) +Div Stress= P(t+alpha dt)
#
# The first two terms on the left are evaluated using the Inertial force kernel
# The next three terms on the left involving zeta and alpha are evaluated using
# the DynamicStressDivergenceTensors Kernel
# The residual due to Pressure is evaluated using Pressure boundary condition
#
# The system will come to steady state slowly after the pressure becomes constant.
# Alpha equal to zero will result in Newmark integration.

[Mesh]
  type = GeneratedMesh
  dim = 3
  nx = 1
  ny = 1
  nz = 1
  xmin = 0.0
  xmax = 0.1
  ymin = 0.0
  ymax = 1.0
  zmin = 0.0
  zmax = 0.1
[]


[Variables]
  [./disp_x]
  [../]
  [./disp_y]
  [../]
  [./disp_z]
  [../]
[]

[AuxVariables]
  [./vel_x]
  [../]
  [./accel_x]
  [../]
  [./vel_y]
  [../]
  [./accel_y]
  [../]
  [./vel_z]
  [../]
  [./accel_z]
  [../]
  [./stress_yy]
    order = CONSTANT
    family = MONOMIAL
  [../]
  [./strain_yy]
    order = CONSTANT
    family = MONOMIAL
  [../]

[]

[Kernels]
  [./DynamicTensorMechanics]
    displacements = 'disp_x disp_y disp_z'
    zeta = 0.1
    alpha = 0.11
  [../]
  [./inertia_x]
    type = InertialForce
    variable = disp_x
    eta=0.1
    alpha = 0.11
  [../]
  [./inertia_y]
    type = InertialForce
    variable = disp_y
    eta=0.1
    alpha = 0.11
  [../]
  [./inertia_z]
    type = InertialForce
    variable = disp_z
    eta = 0.1
    alpha = 0.11
  [../]

[]

[AuxKernels]
  [./accel_x] # These auxkernels are only to check output
    type = TestNewmarkTI
    displacement = disp_x
    variable = accel_x
    first = false
  [../]
  [./accel_y]
    type = TestNewmarkTI
    displacement = disp_y
    variable = accel_y
    first = false
  [../]
  [./accel_z]
    type = TestNewmarkTI
    displacement = disp_z
    variable = accel_z
    first = false
  [../]
  [./vel_x]
    type = TestNewmarkTI
    displacement = disp_x
    variable = vel_x
  [../]
  [./vel_y]
    type = TestNewmarkTI
    displacement = disp_y
    variable = vel_y
  [../]
  [./vel_z]
    type = TestNewmarkTI
    displacement = disp_z
    variable = vel_z
  [../]
  [./stress_yy]
    type = RankTwoAux
    rank_two_tensor = stress
    variable = stress_yy
    index_i = 0
    index_j = 1
  [../]
  [./strain_yy]
    type = RankTwoAux
    rank_two_tensor = total_strain
    variable = strain_yy
    index_i = 0
    index_j = 1
  [../]

[]


[BCs]
  [./top_y]
    type = DirichletBC
    variable = disp_y
    boundary = top
    value=0.0
  [../]
  [./top_x]
    type = DirichletBC
    variable = disp_x
    boundary = top
    value=0.0
  [../]
  [./top_z]
    type = DirichletBC
    variable = disp_z
    boundary = top
    value=0.0
  [../]
  [./bottom_x]
    type = DirichletBC
    variable = disp_x
    boundary = bottom
    value=0.0
  [../]
  [./bottom_z]
    type = DirichletBC
    variable = disp_z
    boundary = bottom
    value=0.0
  [../]
  [./Pressure]
    [./Side1]
      boundary = bottom
      function = pressure
      disp_x = disp_x
      disp_y = disp_y
      disp_z = disp_z
      factor = 1
      alpha  = 0.11
    [../]
  [../]
[]

[Materials]
  [./Elasticity_tensor]
    type = ComputeElasticityTensor
    block = 0
    fill_method = symmetric_isotropic
    C_ijkl = '210e9 0'
  [../]

  [./strain]
    type = ComputeSmallStrain
    block = 0
    displacements = 'disp_x disp_y disp_z'
  [../]

  [./stress]
    type = ComputeLinearElasticStress
    block = 0
  [../]

  [./density]
    type = GenericConstantMaterial
    block = 0
    prop_names = 'density'
    prop_values = '7750'
  [../]

[]

[Executioner]
  type = Transient
  start_time = 0
  end_time = 2
  dt = 0.1

  # Time integrator scheme
  scheme = "newmark-beta"
[]


[Functions]
  [./pressure]
    type = PiecewiseLinear
    x = '0.0 0.1 0.2 1.0 2.0 5.0'
    y = '0.0 0.1 0.2 1.0 1.0 1.0'
    scale_factor = 1e9
  [../]
[]

[Postprocessors]
  [./_dt]
    type = TimestepSize
  [../]
  [./disp]
    type = NodalMaxValue
    variable = disp_y
    boundary = bottom
  [../]
  [./vel]
    type = NodalMaxValue
    variable = vel_y
    boundary = bottom
  [../]
  [./accel]
    type = NodalMaxValue
    variable = accel_y
    boundary = bottom
  [../]
  [./stress_yy]
    type = ElementAverageValue
    variable = stress_yy
  [../]
  [./strain_yy]
    type = ElementAverageValue
    variable = strain_yy
  [../]
[]

[Outputs]
  file_base = 'rayleigh_hht_out'
  exodus = true
  perf_graph = true
[]
