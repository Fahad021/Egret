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
modifying the data dictionary
"""
import egret.model_library.transmission.tx_calc as tx_calc
from egret.model_library.defn import BasePointType, ApproximationType
import numpy as np

def create_dicts_of_ptdf(md,base_point=BasePointType.FLATSTART):
    branches = dict(md.elements(element_type='branch'))
    buses = dict(md.elements(element_type='bus'))
    branch_attrs = md.attributes(element_type='branch')
    bus_attrs = md.attributes(element_type='bus')

    reference_bus = md.data['system']['reference_bus']
    ptdf = tx_calc.calculate_ptdf(branches,buses,branch_attrs['names'],bus_attrs['names'],reference_bus,base_point)
    phi_from, phi_to = tx_calc.calculate_phi_constant(branches,branch_attrs['names'],bus_attrs['names'],ApproximationType.PTDF)

    _len_branch = len(branch_attrs['names'])
    _mapping_branch = {i: branch_attrs['names'][i] for i in list(range(0,_len_branch))}

    _len_bus = len(bus_attrs['names'])
    _mapping_bus = {i: bus_attrs['names'][i] for i in list(range(0,_len_bus))}

    for idx,branch_name in _mapping_branch.items():
        branch = md.data['elements']['branch'][branch_name]
        _row_ptdf = {bus_attrs['names'][i]: ptdf[idx,i] for i in list(range(0,_len_bus))}
        branch['ptdf'] = _row_ptdf

    for idx, bus_name in _mapping_bus.items():
        bus = md.data['elements']['bus'][bus_name]
        _row_phi_from = {branch_attrs['names'][i]: phi_from[idx, i] for i in list(range(0, _len_branch)) if phi_from[idx, i] != 0.}
        bus['phi_from'] = _row_phi_from

        _row_phi_to = {branch_attrs['names'][i]: phi_to[idx, i] for i in list(range(0, _len_branch)) if phi_to[idx, i] != 0.}
        bus['phi_to'] = _row_phi_to


def create_dicts_of_ptdf_losses(md,base_point=BasePointType.SOLUTION):
    branches = dict(md.elements(element_type='branch'))
    buses = dict(md.elements(element_type='bus'))
    branch_attrs = md.attributes(element_type='branch')
    bus_attrs = md.attributes(element_type='bus')

    reference_bus = md.data['system']['reference_bus']
    ptdf_r, ldf, ldf_c = tx_calc.calculate_ptdf_ldf(branches,buses,branch_attrs['names'],bus_attrs['names'],reference_bus,base_point)
    phi_from, phi_to = tx_calc.calculate_phi_constant(branches,branch_attrs['names'],bus_attrs['names'],ApproximationType.PTDF_LOSSES)
    phi_loss_from, phi_loss_to = tx_calc.calculate_phi_loss_constant(branches,branch_attrs['names'],bus_attrs['names'],ApproximationType.PTDF_LOSSES)

    _len_branch = len(branch_attrs['names'])
    _mapping_branch = {i: branch_attrs['names'][i] for i in list(range(0,_len_branch))}

    _len_bus = len(bus_attrs['names'])
    _mapping_bus = {i: bus_attrs['names'][i] for i in list(range(0,_len_bus))}

    for idx,branch_name in _mapping_branch.items():
        branch = md.data['elements']['branch'][branch_name]
        _row_ptdf_r = {bus_attrs['names'][i]: ptdf_r[idx,i] for i in list(range(0,_len_bus))}
        branch['ptdf_r'] = _row_ptdf_r

        _row_ldf = {bus_attrs['names'][i]: ldf[idx,i] for i in list(range(0,_len_bus))}
        branch['ldf'] = _row_ldf

        branch['ldf_c'] = ldf_c[idx]

    for idx, bus_name in _mapping_bus.items():
        bus = md.data['elements']['bus'][bus_name]
        _row_phi_from = {branch_attrs['names'][i]: phi_from[idx,i] for i in list(range(0,_len_branch)) if phi_from[idx, i] != 0.}
        bus['phi_from'] = _row_phi_from

        _row_phi_to = {branch_attrs['names'][i]: phi_to[idx,i] for i in list(range(0,_len_branch)) if phi_to[idx, i] != 0.}
        bus['phi_to'] = _row_phi_to

        _row_phi_loss_from = {branch_attrs['names'][i]: phi_loss_from[idx,i] for i in list(range(0,_len_branch)) if phi_loss_from[idx, i] != 0.}
        bus['phi_loss_from'] = _row_phi_loss_from

        _row_phi_loss_to = {branch_attrs['names'][i]: phi_loss_to[idx,i] for i in list(range(0,_len_branch)) if phi_loss_to[idx, i] != 0.}
        bus['phi_loss_to'] = _row_phi_loss_to
