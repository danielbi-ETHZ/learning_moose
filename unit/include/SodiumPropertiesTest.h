//* This file is part of the MOOSE framework
//* https://www.mooseframework.org
//*
//* All rights reserved, see COPYRIGHT for full restrictions
//* https://github.com/idaholab/moose/blob/master/COPYRIGHT
//*
//* Licensed under LGPL 2.1, please see LICENSE for details
//* https://www.gnu.org/licenses/lgpl-2.1.html

#ifndef SODIUMPROPERTIESTEST_H
#define SODIUMPROPERTIESTEST_H

#include "gtest/gtest.h"

#include "MooseApp.h"
#include "Utils.h"
#include "FEProblem.h"
#include "AppFactory.h"
#include "GeneratedMesh.h"

#include "SodiumProperties.h"

class MooseMesh;
class FEProblem;

class SodiumPropertiesTest : public ::testing::Test
{
protected:
  void SetUp()
  {
    const char * argv[] = {"foo", NULL};

    _app = AppFactory::createAppShared("MooseUnitApp", 1, (char **)argv);
    _factory = &_app->getFactory();

    registerObjects(*_factory);
    buildObjects();
  }

  void registerObjects(Factory & factory) { registerUserObject(SodiumProperties); }

  void buildObjects()
  {
    InputParameters mesh_params = _factory->getValidParams("GeneratedMesh");
    mesh_params.set<MooseEnum>("dim") = "3";
    mesh_params.set<std::string>("name") = "mesh";
    mesh_params.set<std::string>("_object_name") = "name1";
    _mesh = libmesh_make_unique<GeneratedMesh>(mesh_params);

    InputParameters problem_params = _factory->getValidParams("FEProblem");
    problem_params.set<MooseMesh *>("mesh") = _mesh.get();
    problem_params.set<std::string>("name") = "problem";
    problem_params.set<std::string>("_object_name") = "name2";
    _fe_problem = libmesh_make_unique<FEProblem>(problem_params);

    // The sodium fluid properties
    InputParameters uo_pars = _factory->getValidParams("SodiumProperties");
    _fe_problem->addUserObject("SodiumProperties", "fp", uo_pars);
    _fp = &_fe_problem->getUserObject<SodiumProperties>("fp");
  }

  std::shared_ptr<MooseApp> _app;
  std::unique_ptr<MooseMesh> _mesh;
  std::unique_ptr<FEProblem> _fe_problem;
  Factory * _factory;
  const SodiumProperties * _fp;
};

#endif // SODIUMPROPERTIESTEST_H
