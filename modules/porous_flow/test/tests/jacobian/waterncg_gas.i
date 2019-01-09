# Tests correct calculation of properties derivatives in PorousFlowWaterNCG
# for conditions that give a single gas phase

[Mesh]
  type = GeneratedMesh
  dim = 2
  nx = 2
  ny = 2
[]

[GlobalParams]
  PorousFlowDictator = dictator
  gravity = '0 0 0'
[]

[Variables]
  [./pgas]
  [../]
  [./z]
  [../]
[]

[ICs]
  [./pgas]
    type = RandomIC
    min = 1e4
    max = 4e4
    variable = pgas
  [../]
  [./z]
    type = RandomIC
    min = 0.88
    max = 0.98
    variable = z
  [../]
[]

[Kernels]
  [./mass0]
    type = PorousFlowMassTimeDerivative
    variable = pgas
    fluid_component = 0
  [../]
  [./mass1]
    type = PorousFlowMassTimeDerivative
    variable = z
    fluid_component = 1
  [../]
  [./adv0]
    type = PorousFlowAdvectiveFlux
    variable = pgas
    fluid_component = 0
  [../]
  [./adv1]
    type = PorousFlowAdvectiveFlux
    variable = z
    fluid_component = 1
  [../]
[]

[UserObjects]
  [./dictator]
    type = PorousFlowDictator
    porous_flow_vars = 'pgas z'
    number_fluid_phases = 2
    number_fluid_components = 2
  [../]
  [./pc]
    type = PorousFlowCapillaryPressureVG
    m = 0.5
    alpha = 1
    pc_max = 1e3
  [../]
  [./fs]
    type = PorousFlowWaterNCG
    water_fp = water
    gas_fp = co2
    capillary_pressure = pc
  [../]
[]

[Modules]
  [./FluidProperties]
    [./co2]
      type = CO2FluidProperties
    [../]
    [./water]
      type = Water97FluidProperties
    [../]
  [../]
[]

[Materials]
  [./temperature]
    type = PorousFlowTemperature
    temperature = 50
  [../]
  [./temperature_nodal]
    type = PorousFlowTemperature
    temperature = 50
    at_nodes = true
  [../]
  [./waterncg]
    type = PorousFlowFluidState
    gas_porepressure = pgas
    z = z
    at_nodes = true
    temperature_unit = Celsius
    capillary_pressure = pc
    fluid_state = fs
  [../]
  [./waterncg_qp]
    type = PorousFlowFluidState
    gas_porepressure = pgas
    z = z
    temperature_unit = Celsius
    capillary_pressure = pc
    fluid_state = fs
  [../]
  [./permeability]
    type = PorousFlowPermeabilityConst
    permeability = '1e-12 0 0 0 1e-12 0 0 0 1e-12'
  [../]
  [./relperm0]
    type = PorousFlowRelativePermeabilityCorey
    n = 2
    phase = 0
    at_nodes = true
  [../]
  [./relperm1]
    type = PorousFlowRelativePermeabilityCorey
    n = 3
    phase = 1
    at_nodes = true
  [../]
  [./porosity]
    type = PorousFlowPorosityConst
    porosity = 0.1
    at_nodes = true
  [../]
[]

[Executioner]
  type = Transient
  solve_type = NEWTON
  dt = 1
  end_time = 1
  nl_abs_tol = 1e-12
[]

[Preconditioning]
  [./smp]
    type = SMP
    full = true
  [../]
[]

[AuxVariables]
  [./sgas]
    family = MONOMIAL
    order = CONSTANT
  [../]
[]

[AuxKernels]
  [./sgas]
    type = PorousFlowPropertyAux
    property = saturation
    phase = 1
    variable = sgas
  [../]
[]

[Postprocessors]
  [./sgas_min]
    type = ElementExtremeValue
    variable = sgas
    value_type = min
  [../]
  [./sgas_max]
    type = ElementExtremeValue
    variable = sgas
    value_type = max
  [../]
[]
