# Moose variable system

## Overview

The current class hierarchy for Moose variables is shown below:

!media media/framework_development/moose_variable_hierarchy.svg
       caption=Moose variable hierarchy.
       style=width:50%;

`MooseVariableBase` is the primitive base class from which all variables
inherit. It includes methods for accessing the variable finite element type and
order, degress of freedom, scaling factor, name, and associated
`SystemBase`. Two classes inherit directly from `MooseVariableBase`:
`MooseVariableFEBase` and `MooseVariableScalar`. `MooseVariableScalar` represents a
Moose variable that is constant over the spatial domain. It has a number of
degrees of freedom equal to the order of the variable, e.g. the following
variable block would declare a `MooseVariableScalar` with two associated degrees
of freedom:

```
[AuxVariables]
  [./aux_scalar]
    order = SECOND
    family = SCALAR
  [../]
[]
```

`MooseVariableFEBase` is an abstract class that encompasses all finite-element type
variables; all variables that vary spatially ultimately inherit from
`MooseVariableFEBase`. The class implements all the relevant variable methods other
than those that return the actual variable solution or variable shape functions,
since the return type in
the latter case depends on whether the finite-element variable is scalar-valued
(single-component) or vector-valued (multi-component) in nature. The existence
of the `MooseVariableFEBase` class allows construction of containers that hold both single- and
multi-component finite element variables. This is useful for instance in the
`Assembly` class where we can abstract the coupling matrix entries or in
Jacobian computing
objects like `Kernels` when we want to fetch the numerical ID of the variable
using `coupled`. Moreoever, this design structure mirrors that of the `FE`
design in LibMesh, where `FEAbstract` is an abstract base class that implements
all methods independent of `FE` type and the class
template `FEGenericBase<T>` implements the type dependent methods analogous to
`MooseVariableFE<T>`.

`MooseVariableFE<T>` implements methods that return the variable's solution
and its associated shape functions. Additionally, it contains the methods
responsible for computing the variable solution at quadrature points given the
degree of freedom values computed from the previous non-linear
solution. "Standard" or "traditional" finite element variables that are
single-component are instantiated with the template argument `Real`; these hold
variables of finite element families `LAGRANGE`, `MONOMIAL`, `HERMITE`,
etc. Multi-component vector finite element variables are instantiated with the
template argument `RealVectorValue` and currently encompass the finite element
familes `NEDELEC_ONE` and `LAGRANGE_VEC`. The former is useful for
electromagnetic applications or for general PDEs that involve a curl
operation. The latter is potentially useful for tensor mechanic or Navier-Stokes
simulations where historically displacement or velocity variables have been
broken up component-wise. To hide the templating of the Moose variable system
from other framework code, `MooseVariableFE<Real>` and
`MooseVariableFE<RealVectorValue>` have been aliased to `MooseVariable` and
`VectorMooseVariable` respectively.

Finally, `MooseVariableConstMonomial` is a class that takes advantage of its
finite element type (constant value on an element) to optimize its solution
computing routines. Consequently, it overrides the `computeElemValues` and
similar methods of `MooseVariableFE<Real>`.

## Accessors

There are a myriad of ways to acess Moose variables from user interfaces. We'll
outline a few below.

### SystemBase

It's common for interface objects (`Kernel` objects for example) to have a `_sys`
member. The `_sys` member has the following variable accessor methods which take
a `THREAD_ID` and either a `std::string` variable name or `unsigned` variable ID
as arguments:

- `getVariable`: returns a reference to a `MooseVariableFEBase`. Useful when access
  to the variable finite element solution or shape functions is not needed
- `getFieldVariable`: this is a templated method that takes as its template
  argument either `Real` or `RealVectorValue` and returns a reference to a
  `MooseVariable` or a `VectorMooseVariable` respectively. Useful when the user
  knows and needs the complete type
- `getScalarVariable`: returns a reference to a `MooseVariableScalar`

These getter methods ultimately query different map containers in the `VariableWarehouse`.

### SubProblem

Another common interface object member is `_subproblem`. `_subproblem` has the
following acessors methods which take `THREAD_ID` and a `std::string` variable
name as arguments (note that acessors through variable IDs do not exist through
`SubProblem`):

- `getVariable`: returns a reference to a `MooseVariableFEBase`. Useful when access
  to the variable finite element solution or shape functions is not
  needed. Calls `SystemBase::getVariable`
- `getStandardVariable`: returns a reference to a
  `MooseVariable`. Useful when the user
  knows and needs the complete type. Calls `SystemBase::getFieldVariable<Real>`
- `getVectorVariable`: returns a reference to a
  `VectorMooseVariable`. Useful when the user
  knows and needs the complete type. Calls `SystemBase::getFieldVariable<RealVectorValue>`
- `getScalarVariable`: returns a reference to a `MooseVariableScalar`

Note that the template abstraction available in `SystemBase` is not available in
`SubProblem`. This is because the accessor methods in `SubProblem` are pure
virtual, i.e. their implementations are made in derived classes which eliminates
the choice of a templated accessor method in the base `SubProblem` class.

### Coupleable

Since most interface objects already supply the user with the primary variable,
the most common way a user should be accessing Moose variables is through
`Coupleable` methods. The following accessor methods return actual Moose
variable objects and take as arguments the variable name and the "component"
which is used when the user passes in multiple variables to a single
`CoupledVar` parameter:

- `getFEVar`: returns a pointer to a `MooseVariableFEBase`. Useful when access
  to the variable finite element solution or shape functions is not
  needed
- `getVar`: returns a pointer to a `MooseVariable`. Useful when the complete
  type is needed
- `getVectorVar`: returns a pointer to a `VectorMooseVariable`. Useful when the complete
  type is needed

When the user/developer wants access to multiple/all coupled variables, they can
call the following methods which take no arguments:

- `getCoupledMooseVars`: returns +all+ coupled Moose variables, i.e. both
  single-component `MooseVariables` and multi-component
  `VectorMooseVariables`. Consequently the return type is
  `std::vector<MooseVariableFEBase *>`
- `getCoupledStandardMooseVars`: returns all coupled single-component
  `MooseVariables` as a `std::vector<MooseVariable *>`
- `getCoupledVectorMooseVars`: returns all coupled multi-component
  `VectorMooseVariables` as a `std::vector<VectorMooseVariable *>`

Often times there is no need for the user/developer to access the actual Moose
variable object. Instead they require the variable finite element solution or
gradient. Some of these methods are exemplified below:

- `coupledValue`: takes a variable name (should correspond to a
  +single-component+ `MooseVariable`) and returns the finite element solution
  at the quadrature points (`VariableValue`)
- `coupledVectorValue`: takes a variable name (should correspond to a
  +multi-component+ `VectorMooseVariable`) and returns the finite element solution
  at the quadrature points (`VectorVariableValue`)
- `coupledGradient`: takes a variable name (should correspond to a
  +single-component+ `MooseVariable`) and returns the finite element solution gradient
  at the quadrature points (`VariableGradient`)
- `coupledCurl`: takes a variable name (should correspond to a
  +multi-component+ `VectorMooseVariable`) and returns the curl of the finite element solution
  at the quadrature points (`VectorVariableCurl`)
