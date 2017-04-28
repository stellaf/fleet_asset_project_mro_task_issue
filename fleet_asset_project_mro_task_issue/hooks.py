# -*- coding: utf-8 -*-
# © 2016 Michael Viriyananda
# 2017 upgraded it to odoo 10, and add some sql safty guard command, by stella.fredo@gmail.com
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from . import fleet_asset_project_mro_task_issue
from odoo.api import Environment

def post_init_hook(cr, pool):
    """
    This post-init-hook will update all existing issue assigning them the
    corresponding sequence code.
    """
    cr.execute(
        'SELECT id, name, asset_id, analytic_account_id '
        'FROM fleet_vehicle '
        'ORDER BY id'
        )
    env = api.Environment(cr, SUPERUSER_ID, {})
    fleet_obj = env['fleet.vehicle']
    
    for fleet_data in cr.fetchall():
        fleet_record=fleet_obj.browse(fleet_data[0])
        acount_obj=env['account.analytic.account']
        asset_obj=env['asset.asset']
        if not fleet_data[3]:
            fleet_record.write({'name':fleet_data[1]})
        if not fleet_data[2]:
            fleet_record.write({'name':fleet_data[1]})
