# Darcy flow with heat advection and conduction, and elasticity
# [Mesh]
#   type = AnnularMesh
#   dim = 2
#   nr = 10
#   rmin = 1.0
#   rmax = 10
#   growth_r = 1.4
#   nt = 4
#   tmin = 0
#   tmax = 1.57079632679
# []

# [MeshModifiers]
#   [./make3D]
#     type = MeshExtruder
#     extrusion_vector = '0 0 12'
#     num_layers = 3
#     bottom_sideset = 'bottom'
#     top_sideset = 'top'
#   [../]
#   [./shift_down]
#     type = Transform
#     transform = TRANSLATE
#     vector_value = '0 0 -6'
#     depends_on = make3D
#   [../]
#   [./aquifer]
#     type = SubdomainBoundingBox
#     block_id = 1
#     bottom_left = '0 0 -2'
#     top_right = '10 10 2'
#     depends_on = shift_down
#   [../]
#   [./injection_area]
#     type = ParsedAddSideset
#     combinatorial_geometry = 'x*x+y*y<1.01'
#     included_subdomain_ids = 1
#     new_sideset_name = 'injection_area'
#     depends_on = 'aquifer'
#   [../]
#   [./rename]
#     type = RenameBlock
#     old_block_id = '0 1'
#     new_block_name = 'caps aquifer'
#     depends_on = 'injection_area'
#   [../]
# []

### FROM aquifer_caprock.i #####
[Mesh]
  type = GeneratedMesh
  dim = 3
  nx = 20
  xmin = 0
  xmax = 100
  ny = 10
  ymin = 0
  ymax = 50
  nz = 20
  zmin = 0
  zmax = 100
  block_id = '1 3'
  block_name = 'aquifer caps'
[]

# Defines the aquifer and caprock regions as well as the injection_area
[MeshModifiers]
  [./aquifer]
    type = SubdomainBoundingBox
    block_id = 1
    bottom_left = '0 0 0'
    top_right = '100 20 100'
  [../]
  [./caps]
    type = SubdomainBoundingBox
    block_id = 3
    bottom_left = '0 20 0'
    top_right = '100 50 100'
  [../]
  [./injection_area]
    type = BoundingBoxNodeSet
    new_boundary = 'injection_area'
    bottom_left = '0 0 50'
    top_right = '0 20 50'
  [../]
  [./extraction_area]
    type = BoundingBoxNodeSet
    new_boundary = 'extraction_area'
    bottom_left = '80 0 50'
    top_right = '80 20 50'
  [../]
[]
### END FROM aquifer_caprock.i #####

[GlobalParams]
  # displacements = 'disp_x disp_y disp_z'
  PorousFlowDictator = dictator
  biot_coefficient = 1.0
[]

[Variables]
  [./porepressure]
    initial_condition = 1.0E7
  [../]
  [./temperature]
    initial_condition = 300
    scaling = 1E-8
  [../]
  # [./disp_x]
  #   scaling = 1E-10
  # [../]
  # [./disp_y]
  #   scaling = 1E-10
  # [../]
  # [./disp_z]
  #   scaling = 1E-10
  # [../]
[]

[PorousFlowBasicTHM]
  porepressure = porepressure
  temperature = temperature
  coupling_type = ThermoHydro
  gravity = '0 0 0'
  fp = the_simple_fluid
  thermal_eigenstrain_name = thermal_contribution
  use_displaced_mesh = false
[]

[BCs]
  # [./constant_injection_porepressure]
  #   type = PresetBC
  #   variable = porepressure
  #   value = 1E6
  #   boundary = injection_area
  # [../]
  
  ### FROM aquifer_caprock.i #####
  [./inlet]
    type = PresetBC
    variable = porepressure
    value = 1.0E7
    boundary = injection_area # injects just at the screened area
    # boundary = left #right
    # boundary = bottom # top #bottom
    # boundary = back #front
  [../]
  [./outlet]
    type = PresetBC
    variable = porepressure
    value = 1.0E7
    boundary = extraction_area # injects just at the screened area
    # boundary = left #right
    # boundary = bottom # top #bottom
    # boundary = back #front
  [../]
  ### END FROM aquifer_caprock.i #####
  


  ### Same as 04.i ###
  [./constant_injection_temperature]
    type = PresetBC
    variable = temperature
    # value = 380
    value = 301
    boundary = injection_area
  [../]
  ### END Same as 04.i ###

  ### Different Roller BCs ###
  # [./roller_left]
  #   type = PresetBC
  #   variable = disp_x
  #   value = 0
  #   boundary = left
  # [../]
  # [./roller_bottom]
  #   type = PresetBC
  #   variable = disp_y
  #   value = 0
  #   boundary = bottom
  # [../]
  # [./roller_front_back]
  #   type = PresetBC
  #   variable = disp_z
  #   value = 0
  #   boundary = 'front back'
  # [../]
  ### END Different Roller BCs ###

  ### Original (comment out)
  # [./roller_tmax]
  #   type = PresetBC
  #   variable = disp_x
  #   value = 0
  #   boundary = tmax
  # [../]
  # [./roller_tmin]
  #   type = PresetBC
  #   variable = disp_y
  #   value = 0
  #   boundary = tmin
  # [../]
  # [./roller_top_bottom]
  #   type = PresetBC
  #   variable = disp_z
  #   value = 0
  #   boundary = 'top bottom'
  # [../]
  ### END Original (comment out)
  # [./cavity_pressure_x]
  #   type = Pressure
  #   variable = disp_x
  #   # boundary = injection_area
  #   boundary = left
  #   component = 0
  #   factor = 1E6
  #   use_displaced_mesh = false
  # [../]
  # [./cavity_pressure_y]
  #   type = Pressure
  #   # boundary = injection_area
  #   boundary = left
  #   variable = disp_y
  #   component = 1
  #   factor = 1E6
  #   use_displaced_mesh = false
  # [../]
[]

[AuxVariables]
  # [./stress_rr]
  #   family = MONOMIAL
  #   order = CONSTANT
  # [../]
  # [./stress_pp]
  #   family = MONOMIAL
  #   order = CONSTANT
  # [../]
  ## From aquifer_caprock.i ##
  [./porosity]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./permeability_x]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./permeability_xy]
    family = MONOMIAL
    order = CONSTANT
  [../]
  [./permeability_y]
    family = MONOMIAL
    order = CONSTANT
  [../]
  ## END From aquifer_caprock.i ##
[]

[AuxKernels]
  # [./stress_rr]
  #   type = RankTwoScalarAux
  #   rank_two_tensor = stress
  #   variable = stress_rr
  #   scalar_type = RadialStress
  #   point1 = '0 0 0'
  #   point2 = '0 0 1'
  # [../]
  # [./stress_pp]
  #   type = RankTwoScalarAux
  #   rank_two_tensor = stress
  #   variable = stress_pp
  #   scalar_type = HoopStress
  #   point1 = '0 0 0'
  #   point2 = '0 0 1'
  # [../]
  ## From Aquifer_caprock.i ##
  [./porosity]
    type = MaterialRealAux
    property = PorousFlow_porosity_qp
    variable = porosity
  [../]
  [./permeability_x]
    type = MaterialRealTensorValueAux
    property = PorousFlow_permeability_qp
    column = 0
    row = 0
    variable = permeability_x
  [../]
  [./permeability_xy]
    type = MaterialRealTensorValueAux
    property = PorousFlow_permeability_qp
    column = 0
    row = 1
    variable = permeability_xy
  [../]
  [./permeability_y]
    type = MaterialRealTensorValueAux
    property = PorousFlow_permeability_qp
    column = 0
    row = 0
    variable = permeability_y
  [../]
  ## END From Aquifer_caprock.i ##
[]

[Modules]
  [./FluidProperties]
    [./the_simple_fluid]
      type = SimpleFluidProperties
      bulk_modulus = 2E9
      viscosity = 1.0E-3
      density0 = 1000.0
      thermal_expansion = 0.0002
      cp = 4194
      cv = 4186
      porepressure_coefficient = 0
    [../]
  [../]
[]

[Materials]
  [./porosity]
    # type = PorousFlowPorosityConst # For a constant porosity (i.e. unaffected by strains, temp etc.)
    # porosity = 0.1                 # The porosity if PorousFlowPorosityConst is used
    type = PorousFlowPorosity  #if you want porosity to change as a function of mechanical strains, porepressure, temperature, minearl precip
    porosity_zero = 0.1        #initial porosity if PorousFlowPorosity is used
    thermal = true
    fluid = false
    mechanical = false
    chemical = false
    thermal_expansion_coeff = 0.001 
  [../]
  [./biot_modulus]
    type = PorousFlowConstantBiotModulus
    solid_bulk_compliance = 2E-7
    fluid_bulk_modulus = 1E7
  [../]
  [./permeability_aquifer]
    type = PorousFlowPermeabilityConst
    block = aquifer
    permeability = '1E-14 0 0   0 1E-14 0   0 0 1E-14'
  [../]
  [./permeability_caps]
    type = PorousFlowPermeabilityConst
    block = caps
    permeability = '1E-16 0 0   0 1E-16 0   0 0 1E-16'
  [../]

  [./thermal_expansion]
    type = PorousFlowConstantThermalExpansionCoefficient
    drained_coefficient = 0.003
    fluid_coefficient = 0.0002
  [../]
  [./rock_internal_energy]
    type = PorousFlowMatrixInternalEnergy
    density = 2500.0
    specific_heat_capacity = 1200.0
  [../]
  [./thermal_conductivity]
    type = PorousFlowThermalConductivityIdeal
    dry_thermal_conductivity = '10 0 0  0 10 0  0 0 10'
    block = 'caps aquifer'
  [../]

  # [./elasticity_tensor]
  #   type = ComputeIsotropicElasticityTensor
  #   youngs_modulus = 5E9
  #   poissons_ratio = 0.0
  # [../]
  # [./strain]
  #   type = ComputeSmallStrain
  #   eigenstrain_names = thermal_contribution
  # [../]
  # [./thermal_contribution]
  #   type = ComputeThermalExpansionEigenstrain
  #   temperature = temperature
  #   thermal_expansion_coeff = 0.001 # this is the linear thermal expansion coefficient
  #   eigenstrain_name = thermal_contribution
  #   stress_free_temperature = 293
  # [../]
  # [./stress]
  #   type = ComputeLinearElasticStress
  # [../]
[]

[Preconditioning]
  active = basic
  [./basic]
    type = SMP
    full = true
    petsc_options = '-ksp_diagonal_scale -ksp_diagonal_scale_fix'
    petsc_options_iname = '-pc_type -sub_pc_type -sub_pc_factor_shift_type -pc_asm_overlap'
    petsc_options_value = ' asm      lu           NONZERO                   2'
  [../]
  [./preferred_but_might_not_be_installed]
    type = SMP
    full = true
    petsc_options_iname = '-pc_type -pc_factor_mat_solver_package'
    petsc_options_value = ' lu       mumps'
  [../]
[]

[Executioner]
  type = Transient
  solve_type = Newton
  end_time = 0.2E6 #100 days of injeciton
  # end_time = 8.64E6 #100 days of injeciton
  dt = 1E5
  # end_time = 1E6
  # dt = 1E5
  nl_abs_tol = 1E-10
[]

[Outputs]
  exodus = true
[]
