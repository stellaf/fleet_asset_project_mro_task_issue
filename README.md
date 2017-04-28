Fleet Asset Project MRO Task Issue for odoo 10
=============================
This module link the fleet, project, and asset (MRO)
when you create a vehicle
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

        * Knowing bugs: Backup your database before you install this apps. 
          The asset will not be removed when you uninstall this app. You need to remove all the maintenance orders/requests that you created, and then remove all the assets that are created.

    """,
