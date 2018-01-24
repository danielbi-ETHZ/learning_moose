//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#ifndef ADDFUNCTIONACTION_H
#define ADDFUNCTIONACTION_H

#include "MooseObjectAction.h"

class AddFunctionAction;

template <>
InputParameters validParams<AddFunctionAction>();

/**
 * This class parses functions in the [Functions] block and creates them.
 */
class AddFunctionAction : public MooseObjectAction
{
public:
  AddFunctionAction(InputParameters params);

  virtual void act() override;
};

#endif // ADDFUNCTIONACTION_H
