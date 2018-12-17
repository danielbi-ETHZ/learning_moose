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
  nx = 10
  xmin = 0
  xmax = 100
  ny = 10
  ymin = 0
  ymax = 50
  nz = 10
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
    initial_condition = 300.
    scaling = 1E-8
  [../]
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
  [./inlet]
    type = PresetBC
    variable = porepressure
    value = 1.0E7
    # value = 0.0
    boundary = injection_area # injects just at the screened area
    # boundary = left #right
    # boundary = bottom # top #bottom
    # boundary = back #front
  [../]
  [./outlet]
    type = PresetBC
    variable = porepressure
    value = 1.0E7
    # value = 0.0
    boundary = extraction_area # injects just at the screened area
  [../]
  [./constant_injection_temperature]
    type = PresetBC
    variable = temperature
    value = 300.
    # value = 300
    boundary = injection_area
  [../]
  [./constant_extraction_temperature]
    type = PresetBC
    variable = temperature
    value = 300.
    # value = 300
    boundary = extraction_area
  [../]
[]

[AuxVariables]
  [./density_water]
    order = CONSTANT
    family = MONOMIAL
  [../]
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
[]

[AuxKernels]
  [./density_water]
    type = PorousFlowPropertyAux
    variable = density_water
    property = density
    phase = 0
    execute_on = timestep_end
  [../]
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
[]

[Modules]
  [./FluidProperties]
    [./the_simple_fluid]
      type = SimpleFluidProperties
      bulk_modulus = 2.0E9
      viscosity = 1.0E-3
      density0 =1056.5406146754945 # 995.012 #density at P = 0, T = 0
      thermal_expansion = 0.0002 # fluid thermal volumetric expansion coefficient (alpha_f)
      # thermal_expansion = 0.0000
      cp = 4194
      cv = 4186
      porepressure_coefficient = 1.0 # The enhtalpy is internal energy + P/density * porepressure_coefficient
    [../]
  [../]
[]

[Materials]
  [./porosity]
    type = PorousFlowPorosityConst # For a constant porosity (i.e. unaffected by strains, temp etc.)
    porosity = 0.1                 # The porosity if PorousFlowPorosityConst is used
    # type = PorousFlowPorosity  #if you want porosity to change as a function of mechanical strains, porepressure, temperature, minearl precip
    # porosity_zero = 0.1        #initial porosity if PorousFlowPorosity is used
    # thermal = true
    # fluid = false
    # mechanical = false
    # chemical = false
    # thermal_expansion_coeff = 0.001 
  [../]
  [./biot_modulus]
    type = PorousFlowConstantBiotModulus
    solid_bulk_compliance = 2.E-7
    biot_coefficient = 1.0 # default is 1.0
    fluid_bulk_modulus = 2.E9
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
  [./thermal_expansion]  ## Required by PorousFlowBasicTHM_MassTimeDerivative
    type = PorousFlowConstantThermalExpansionCoefficient
    drained_coefficient = 0.000 # drained volumetric thermal expansion coefficient (alpha_T)
    fluid_coefficient = 0.0002  # fluid thermal volumetric expansion coefficient (alpha_f)
    # drained_coefficient = 0.003
    # fluid_coefficient = 0.0002   
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
