#  ___________________________________________________________________________
#
#  EGRET: Electrical Grid Research and Engineering Tools
#  Copyright 2019 National Technology & Engineering Solutions of Sandia, LLC
#  (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
#  Government retains certain rights in this software.
#  This software is distributed under the Revised BSD License.
#  ___________________________________________________________________________

"""
This module has a number of utilities to assist in writing declarations for variables and constraints
"""
import pyomo.environ as pe

def declare_var(varname, model, index_set, **kwargs):
    # if user provides bounds as dict of tuple, translate it
    # into something that Pyomo understands
    if kwargs and 'bounds' in kwargs and isinstance(kwargs['bounds'], dict):
        d = kwargs['bounds']
        bounds_rule = lambda m, k: (d[k][0], d[k][1])
        kwargs['bounds'] = bounds_rule

    # create var if index set is None
    if index_set is None:
        model.add_component(varname, pe.Var(**kwargs))
    else:
        pyomo_index_set = pe.Set(initialize=index_set, ordered=True)
        model.add_component(f"_var_{varname}_index_set", pyomo_index_set)

        # now create the var
        model.add_component(varname, pe.Var(pyomo_index_set, **kwargs))

def declare_set(setname, model, index_set, **kwargs):
    # transform the index set into a Pyomo Set
    if 'ordered' not in kwargs:
        # add ordered=True if the user did not specify anything
        kwargs['ordered'] = True
    pyomo_index_set = pe.Set(initialize=index_set, **kwargs)
    model.add_component(setname, pyomo_index_set)
    return pyomo_index_set
