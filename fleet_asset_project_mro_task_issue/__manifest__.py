# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addon by stella.fredo@gmail.com based on 
#    fleet_analytic_account app from CLEARCORP S.A. (<http://clearcorp.co.cr>).
#    AURIUM TCHNOLOGIES (<http://auriumtechnologies.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    "name" : 'Fleet Asset Project MRO Task Issue',
    "version" : '10.0.1.0',
    "author" : 'Stella Fredö@Sweden',
    'complexity': 'advanced',
    "description":  """
Fleet Asset Project MRO Task Issue
=============================
This module link the fleet, project, and asset (MRO)
when you create one vehicle
-------------
        * one project with the same vehicle name will be created under the project menu.
        * one asset with the same vehicle name will be created under the maintenance menu.
        * The smart buttons to this vehicles are added to each vehicle's form, for 
             * task
             * issue
             * attachmen
             * Maintenance requestas
             * Maintenance orders
        * menu for task, issues, maintenance request and maintenance orders are added to fleet_vehicle menu
        * the existed vehicle will also have asset/project created for it.

        * Knowing bugs: 
		* Backup your database before you install this apps. 
        * If you uninstall the apps, you shall manually remove all the assets created by this apps. by remove all the maintenance orders/requests first.
		* If you uninstall the apps, you shall manually remove all the project/analytic accounts created by this apps. by remove all the maintenance orders/requests first.
    """,
    "category": 'Managing vehicles tasks and issues',
    "sequence": 3,
    "website" : "https://se.linkedin.com/in/stella-fredö-94401014",
    "images" : [],
    "depends" : [
                 'fleet',
                 'account',
                 'analytic',
                 'project',
                 'project_issue',
                 'asset',
                 'mro',
                 'mro_order_duration',
                 ],
    "data" : ['fleet_asset_project_mro_task_issue_view.xml'],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [],
    "test" : [],
    "auto_install": False,
    'post_init_hook': 'post_init_hook',
    "application": False,
    "installable": True,
    'license': 'AGPL-3',
}
