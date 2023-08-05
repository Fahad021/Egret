#  ___________________________________________________________________________
#
#  EGRET: Electrical Grid Research and Engineering Tools
#  Copyright 2019 National Technology & Engineering Solutions of Sandia, LLC
#  (NTESS). Under the terms of Contract DE-NA0003525 with NTESS, the U.S.
#  Government retains certain rights in this software.
#  This software is distributed under the Revised BSD License.
#  ___________________________________________________________________________


"""
This module contains several helper functions that are useful when
working with unit commitment models
"""

## some useful function decorators for building these dynamic models
from functools import wraps

def add_model_attr(attr, requires = {}):
    def actual_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwds):
            ## tag this function in the model with the appropriate attribute
            model = args[0]
            if hasattr(model, attr):
                raise Exception(
                    f"Exception adding {func.__name__}! Model already has {attr} {getattr(model, attr)}! You may only add one type of {attr}!"
                )
            # this checks to see if the required components were already added
            for base_attr in requires:
                if not hasattr(model, base_attr):
                    raise Exception(
                        f"Exception adding {func.__name__}! {func.__name__} requires some {base_attr} to be added first!"
                    )
                ## None in this context means there is no specific requirement
                if requires[base_attr] is None:
                    continue
                if getattr(model, base_attr) not in requires[base_attr]:
                    raise Exception(
                        f"Exception adding {func.__name__}! {func.__name__} requires one of: "
                        + ", ".join(requires[base_attr])
                        + ", to be added first."
                    )
            setattr(model, attr, func.__name__)
            return func(*args, **kwds)

        return wrapper

    return actual_decorator

## provides a view on grid_data attributes that
## is handy for building pyomo params
def build_uc_time_mapping(md_timeperiods):
    ## Assums the last key is time
    def uc_time_helper(_data):
        ## if there is no data,
        ## we return None to the initializer
        if _data is None:
            return None
        def init_rule(m, *key):
            ## last key is time
            pm_t = key[-1]
            key = key[:-1]
            if len(key) == 0:
                return get_time_attr(_data, pm_t)
            if len(key) == 1:
                key = key[0]
            return get_time_attr(_data[key], pm_t) if key in _data else None

        def get_time_attr(att, pm_t):
            if isinstance(att, dict):
                if 'data_type' in att and att['data_type'] == 'time_series':
                    return att['values'][md_timeperiods[pm_t-1]]
                else:
                    raise Exception("Unexpected dictionary {}".format(att))
            else:
                return att

        return init_rule

    return uc_time_helper
