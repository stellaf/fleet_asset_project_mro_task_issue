# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Addon by CLEARCORP S.A. <http://clearcorp.co.cr> and AURIUM TECHNOLOGIES <http://auriumtechnologies.com>
#
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
import string
from lxml import etree
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.safe_eval import safe_eval

class FleetVehicle(models.Model):

    _inherit = 'fleet.vehicle'

    @api.model
    def create(self, vals):
        acount_obj=self.env['account.analytic.account']
        asset_obj=self.env['asset.asset']
        fleet_id = super(FleetVehicle, self).create(vals)
        account_id=acount_obj.create({'name':self._vehicle_name_get(fleet_id),'use_tasks':True,'use_issues':True})
        asset_id=asset_obj.create({'name':self._vehicle_name_get(fleet_id),'model':self.model_id.name,'asset_number':self.license_plate,'criticality':'0','maintenance_state_id.id':'21'})
        fleet_id.write({'analytic_account_id':account_id.id,'asset_id':asset_id.id})
        return fleet_id
         
    @api.multi
    def write(self, vals):
        acount_obj=self.env['account.analytic.account']
        asset_obj=self.env['asset.asset']
        res = super(FleetVehicle, self).write(vals)
        if not self.analytic_account_id:
            account_id=acount_obj.create({'name':self._vehicle_name_get(self),'use_tasks':True,'use_issues':True})
            self.write({'analytic_account_id':account_id.id})
        if not self.asset_id:
            asset_id=asset_obj.create({'name':self._vehicle_name_get(self),'model':self.model_id.name,'asset_number':self.license_plate,'criticality':'0','maintenance_state_id.id':'21'})
            self.write({'asset_id':asset_id.id })
        self.analytic_account_id.write({'analytic_account_id':self.analytic_account_id.id, 'name':self.name,'use_tasks':True,'use_issues':True})
        self.asset_id.write({'asset_id':self.asset_id.id,'name':self._vehicle_name_get(self),'model':self.model_id.name,'asset_number':self.license_plate,'criticality':'0','maintenance_state_id.id':'21'})
        return res

    @api.multi
    def unlink(self):
        self.env['account.analytic.account'].search([('id', '=', self.analytic_account_id.id)]).unlink()
        self.env['asset.asset'].search([('id', '=', self.asset_id.id)]).unlink()
        return super(FleetVehicle,self).unlink()
   
    @api.multi
    def _compute_mrorequest_count(self):
        mrorequest_obj=self.env['mro.request']
        self.mrorequest_count=len(mrorequest_obj.search([('asset_id', '=', self.asset_id.id)]).ids)

    @api.multi
    def _compute_mroorder_count(self):
        asset_obj=self.env['asset.asset']
        self.mroorder_count=asset_obj.search([('id', '=', self.asset_id.id)]).mro_count

    @api.multi
    def _compute_attached_docs_count(self):
        project_obj = self.env['project.project']
        self.doc_count=project_obj.search([('analytic_account_id', '=', self.analytic_account_id.id)]).doc_count

    @api.multi
    def _count_vehicle_task(self):
        project_obj = self.env['project.project']
        self.task_count=len(project_obj.search([('analytic_account_id', '=', self.analytic_account_id.id)]).task_ids)

    @api.multi
    def _count_vehicle_issue(self):
        issue_obj = self.env['project.project']
        self.issue_count=len(issue_obj.search([('analytic_account_id', '=', self.analytic_account_id.id)]).issue_ids)
 
    @api.multi
    def _vehicle_name_get(self,record):
        res = (record.model_id.brand_id.name + '/' + record.model_id.name + '/' + record.license_plate).strip(" ")
        return res

    @api.multi
    def action_view_alltasks(self):
        action = self.env.ref('project.act_project_project_2_project_task_all')
        active_id = self.env['project.project'].search([('analytic_account_id', '=', self.analytic_account_id.id)]).id
        context = {'group_by': 'stage_id', 'search_default_project_id': [active_id], 'default_project_id': active_id, }
        return {
            'key2':'tree_but_open',
            'name': action.name,
            'res_model': 'project.task',
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'res_id': active_id,
            'views': action.views,
            'target': action.target,
            'context':context,
            'nodestroy': True,
            'flags': {'form': {'action_buttons': True}}
        }

    @api.multi
    def action_view_allissues(self):
        action = self.env.ref('project_issue.act_project_project_2_project_issue_all')
        active_id = self.env['project.project'].search([('analytic_account_id', '=', self.analytic_account_id.id)]).id
        context = {'group_by': 'stage_id', 'search_default_project_id': [active_id], 'default_project_id': active_id,}
        return {
            'name': action.name,
            'res_model': 'project.issue',
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'views': action.views,
            'target': action.target,
            'res_id': active_id,
            'context':context,
            'nodestroy': True,
            'flags': {'form': {'action_buttons': True}}
        }

    @api.multi
    def action_view_attachments(self):
        order_by ='state DESC'
        return self.env['project.project'].search([('analytic_account_id', '=', self.analytic_account_id.id)]).attachment_tree_view()

    @api.multi
    def action_view_mro_request(self):
        active_ids = self.env['asset.asset'].search([('id', '=', self.asset_id.id)]).ids
        domain = "[('asset_id','in',[" + ','.join(map(str, active_ids)) + "])]"
        action = self.env.ref('mro.action_requests')
        context={'search_default_open': 1,'search_default_asset_id': [self.asset_id.id],'default_asset_id': self.asset_id.id,}
        return {
            'name': action.name,
            'res_model': 'mro.request',
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'views': action.views,
            'res_id': active_ids,
            'domain':domain,
            'context':context,
            'target': action.target,
            'nodestroy': True,
            'flags': {'form': {'action_buttons': True}}
        }

    @api.multi
    def action_view_mroorders(self):
        active_ids = self.env['asset.asset'].search([('id', '=', self.asset_id.id)]).ids
        domain = "[('asset_id','in',[" + ','.join(map(str, active_ids)) + "])]"
        action = self.env.ref('mro.action_orders')
        context={'search_default_open': 1,'search_default_asset_id': [self.asset_id.id],'default_asset_id': self.asset_id.id,}
        return {
            'name': action.name,
            'res_model': 'mro.order',
            'help': action.help,
            'type': action.type,
            'view_type': action.view_type,
            'view_mode': action.view_mode,
            'views': action.views,
            'res_id': active_ids,
            'domain':domain,
            'context':context,
            'target': action.target,
            'nodestroy': True,
            'flags': {'form': {'action_buttons': True}}
        }

    analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account')
    asset_id = fields.Many2one('asset.asset',string='Asset id')
    task_count = fields.Integer(compute=_count_vehicle_task, string="Vehicle Tasks" , multi=True)
    issue_count = fields.Integer(compute=_count_vehicle_issue, string="Vehicle Issues" , multi=True)
    doc_count = fields.Integer(compute=_compute_attached_docs_count, string="Number of documents attached",multi=True)
    mroorder_count = fields.Integer(compute= _compute_mroorder_count, string="Number of mro orders",multi=True)
    mrorequest_count = fields.Integer(compute= _compute_mrorequest_count, string="Number of mro request",multi=True)
    
class  fleet_vehicle_log_services(models.Model):

    _inherit = 'fleet.vehicle.log.services'
    invoice_id = fields.Many2one('account.invoice',string='Facture')


class Project(models.Model):
    _inherit = "project.project"

    @api.multi
    def attachment_tree_view(self):
        self.ensure_one()
        domain = [
            '|',
            '&', ('res_model', '=', 'project.project'), ('res_id', 'in', self.ids),
            '&', ('res_model', '=', 'project.task'), ('res_id', 'in', self.task_ids.ids)]
        order_by ='create_date DESC'
        return {
            'name': _('Attachments'),
            'domain': domain,
            'res_model': 'ir.attachment',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,kanban,form',
            'view_type': 'form',
            'help': _('''<p class="oe_view_nocontent_create">
                        Documents are attached to the tasks and issues of your project.</p><p>
                        Send messages or log internal notes with attachments to link
                        documents to your project.
                    </p>'''),
            'limit': 80,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }
