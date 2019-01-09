# Example Input file for injecting into an aquifer (bottom) with a caprock above
# Shows how to define a 3D mesh with block_ids for aquifer and caprock
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
  block_name = 'aquifer caprock'
[]

# Defines the aquifer and caprock regions as well as the injection_area
[MeshModifiers]
  [./aquifer]
    type = SubdomainBoundingBox
    block_id = 1
    bottom_left = '0 0 0'
    top_right = '100 20 100'
  [../]
  [./caprock]
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

[GlobalParams]
  PorousFlowDictator = dictator
[]

## Tells it to solve for porepressure
[Variables]
  [./porepressure]
    initial_condition = 1.0E7
  [../]
[]

[PorousFlowBasicTHM]
  porepressure = porepressure
  coupling_type = Hydro
  gravity = '0 0 0'
  fp = the_simple_fluid
[]

[BCs]
  [./inlet]
    type = PresetBC
    variable = porepressure
    value = 1.1E7
    boundary = injection_area # injects just at the screened area
    # boundary = left #right
    # boundary = bottom # top #bottom
    # boundary = back #front
  [../]
  ### uncomment for an outlet BC is desired
  [./outlet]
    type = PresetBC
    variable = porepressure
    value = 1.0E7
    boundary = extraction_area
    # boundary = bottom
    # boundary = back
  [../]
[]

[Modules]
  [./FluidProperties]
    [./the_simple_fluid]
      type = SimpleFluidProperties
      bulk_modulus = 2E9
      viscosity = 1.0E-3
      density0 = 1000.0
    [../]
  [../]
[]

[Materials]
  [./porosity]
    type = PorousFlowPorosity
    porosity_zero = 0.1
  [../]
  [./biot_modulus]
    type = PorousFlowConstantBiotModulus
    biot_coefficient = 0.8
    solid_bulk_compliance = 2E-7
    fluid_bulk_modulus = 1E7
  [../]
  ## Below shows how to assign different permeability to aquifer and caprock
  [./permeability_aquifer]
    type = PorousFlowPermeabilityConst
    block = aquifer
    permeability = '1E-13 0 0   0 1E-13 0   0 0 1E-13'
  [../]
  [./permeability_caprock]
    type = PorousFlowPermeabilityConst
    block = caprock
    permeability = '1E-16 0 0   0 1E-16 0   0 0 1E-16'
  [../]
[]

[AuxVariables]
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
  end_time = 1E6
  dt = 1E5
  nl_abs_tol = 1E-10
[]

[Outputs]
  exodus = true
[]

