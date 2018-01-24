//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#ifndef INITIALCONDITIONWAREHOUSE_H
#define INITIALCONDITIONWAREHOUSE_H

#include "MooseObjectWarehouseBase.h"
#include "MooseTypes.h"

class InitialCondition;

/**
 * Warehouse for storing initial conditions
 */
class InitialConditionWarehouse : public MooseObjectWarehouseBase<InitialCondition>
{
public:
  InitialConditionWarehouse();

  /**
   * Initial setup
   */
  void initialSetup(THREAD_ID tid);

  /**
   * Add object to the warehouse.
   */
  void addObject(std::shared_ptr<InitialCondition> object, THREAD_ID tid);

  /**
   * Get a list of dependent UserObjects for this exec type
   * @return a set of dependent user objects
   */
  std::set<std::string> getDependObjects() const;

protected:
  ///@{
  /// Variable name to block/boundary IDs for error checking
  std::vector<std::map<std::string, std::set<BoundaryID>>> _boundary_ics;
  std::vector<std::map<std::string, std::set<SubdomainID>>> _block_ics;
  ///@}
};

#endif /* INITIALCONDITIONWAREHOUSE_H */
