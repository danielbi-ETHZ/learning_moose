# SetupInterface (execute_on)

Most user-facing objects in MOOSE inherit from the SetupInterface class. This class provides two
features to objects. Foremost, it provides the the "execute_on" parameter, which, as the name
suggests, dictates when the object is to be executed. Secondly, it adds virtual setup methods that
allow derived classes to perform setup applications prior to execution.

## Execute On

Any object inheriting from the SetupInterface, that adds the `validParams<SetupInterface>` within its
own parameters, will have an "execute_on" parameter that can be set to various flags, the most common
flags are listed below.

| Execute Flag | Description |
| - | - |
INITIAL | Prior to the first time step.
TIMESTEP_BEGIN | Prior to the solve for each time step.
NONLINEAR | Prior do each non-linear iteration during the solve.
LINEAR | Prior do each linear iteration during the solve.
TIMESTEP_END | After the solve for each time step.
SUBDOMAIN | Executes when the subdomain (i.e., "blocks") change during calculations.

The "execute_on" parameter can be set to a single flag or multiple flags. For example, it may be
desirable to only execute an object initially because the state of the auxiliary computation does not
vary. In the input file snippet below, the [ElementLengthAux](/ElementLengthAux.md) computation only
needs to be computed initially, thus the "exeucte_on" parameter is set as such.

!listing test/tests/auxkernels/element_length/element_length.i block=AuxKernels

Alternatively, it is often desirable to run a computation with multiple execute flags. For example,
in the input file snippet below a [TimePeriod](/TimePeriod.md) control object that is responsible for
enabling in [Damper](/Dampers/index.md) object needs to be run initially and prior to each timestep
to guarantee that the damper is enabled when desired.

!listing test/tests/controls/time_periods/dampers/control.i block=Controls

Depending on the system these options or others will be available, since as discussed in
[Creating Custom Execute Flags](#creating-custom-execute-flags) custom flags may be added. The
complete list of execution flags is provided by MOOSE are listed in the "registerExecFlags" function.

!listing framework/src/base/MooseApp.C start=MooseApp::registerExecFlags() end=void

## Modifying Execute On

When creating objects that inherit from SetupInterface it is possible to set, add, or remove
available execute flags by retrieving and then modifying the `ExecFlagEnum` parameter. For example,
consider the snippet below (see [Output.C](/framework/src/outputs/Output.C)).

!listing framework/src/outputs/Output.C start=ExecFlagEnum end=setDocString include-end=True

First, the "execute_on" is retrieved for modification by using the "set" method. Notice, that a
second boolean argument is passed to "set", this second flag enables "quite mode". Quite mode will
modify the parameter silently as if the default was the modified parameter. In this case, the
parameter will be listed as un-modified by the user. That is, `InputParameters::isParamSetByUser`
returns false, if quite mode is not enabled this method would return true.

Second, the two new execution flags are added (`EXEC_FINAL` and `EXEC_FAILED`), therefore these
additional options are available to all classes (all Output objects in this case) that
inherit from this object.

Third, the default active flags are set to `EXEC_INITIAL` and `EXEC_TIMESTEP_END`, which
are the defaults for all Output objects.

Finally, the documentation string for the "execute_on" parameter for the Output objects is
update to reflect the changes made to the parameter. The `ExecFlagEnum` has a convenience function
that generates a documentation string that includes the available options in the string.


## Virtual Setup Methods

The SetupInterface includes virtual methods that correspond to the primary execute flags
with MOOSE, these methods are listed in the header as shown here.

!listing framework/include/interfaces/SetupInterface.h
         start=~SetupInterface()
         end=subdomainSetup
         include-end=True
         include-start=False
         strip-leading-whitespace=True

In general, these methods should be utilized to perform "setup" procedures prior to the calls to
execute for the corresponding execute flag.

!alert note
A few of the methods were created prior to the execute flags, thus the names do not correspond but
they remain as is to keep the API consistent: the "jacobianSetup" methods is called prior to the
"NONLINEAR" execute flag and the "residualSetup" is called prior to the "LINEAR" execute flag.


## Creating Custom Execute Flags

It is possible to create custom execute flags for an application. To create at utilize a custom
execute flag the following steps should be followed.

### 1. Declare and Define an Execute Flag

Within your application a new global `const` should be declared in a header file. For example, within
the `LevelSetApp` within MOOSE modules, there is a header (LevelSetTypes.h) that declares a new
flag (`EXEC_ADAPT_MESH`).

!listing modules/level_set/include/base/LevelSetTypes.h

This new global must be defined, which occurs in the corresponding source file. When
defining the new flags with a name and optionally an integer value.

!listing modules/level_set/src/base/LevelSetTypes.C

### 2. Register the Execute Flag

After the new flag(s) are declared and defined, it must be registered with MOOSE. This is
accomplished in similar fashion as object registration, simply add the newly created flag by calling
`registerExecFlag` with the `registerExecFlags` function of your application.

!listing modules/level_set/src/base/LevelSetApp.C
         start=LevelSetApp::registerExecFlags(Fac
         end=// Dynamic

!alert note
If your application does not have a `registerExecFlags` function, it must be
created. This can be done automatically by running the `add_exec_flag_registration.py` that is
located in the scripts directory within MOOSE.

### 3. Add the Execute Flag to InputParameters

After a flag is registered, it must be made available to the object(s) in which are desired to be
executed with the custom flag. This is done by adding this new flag to an existing objects valid
parameters. For example, the following adds the `EXEC_ADAPT_MESH` flag to a `Transfer` object.

!listing modules/level_set/src/transfers/LevelSetMeshRefinementTransfer.C strip-leading-whitespace=1 start=ExecFlagEnum end=params.set<bool>


### 4. Use the Execute Flag

Depending on what type of custom computation is desired, various MOOSE execution calls accept
execution flags, which will spawn calculations. For example, the `LevelSetProblem` contains
a custom method that uses the `EXEC_ADAPT_MESH` flag to preform
an additional [`MultiAppTransfer`](Transfers/index.md) execution.

!listing modules/level_set/src/base/LevelSetProblem.C strip-leading-whitespace=1 line=LevelSet::EXEC_ADAPT_MESH
