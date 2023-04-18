<<<<<<< HEAD
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class ScmPurchaseView(models.TransientModel):
    _name = 'scm.purchase.view'
    _description = 'Wizard SCM Purchase'

    def _get_default_location(self):
        return self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)],
                                                  limit=1).lot_stock_id

    location_id = fields.Many2one('stock.location', string='Stock Location',
                                  domain=[('usage', '=', 'internal')],default=_get_default_location, required=True)

    def open_table(self):
        self.ensure_one()
        ctx = dict(
            self._context,
            search_default_productgroup=True,
            search_default_location_id=self.location_id.id)

        action = self.env['ir.model.data'].xmlid_to_object('scm_abc.scm_purchase_action')
        if not action:
            action = {
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'scm.purchase',
                'type': 'ir.actions.act_window',
            }
        else:
            action = action[0].read()[0]

        action['domain'] = ([('location_id', '=', self.location_id.id)])
        action['name'] = _('SCM ABC')
        action['context'] = ctx
        return action
=======
# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models, fields, _


class ScmPurchaseView(models.TransientModel):
    _name = 'scm.purchase.view'
    _description = 'Wizard SCM Purchase'

    def _get_default_location(self):
        return self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)],
                                                  limit=1).lot_stock_id

    location_id = fields.Many2one('stock.location', string='Stock Location',
                                  domain=[('usage', '=', 'internal')],default=_get_default_location, required=True)

    def open_table(self):
        self.ensure_one()
        ctx = dict(
            self._context,
            search_default_productgroup=True,
            search_default_location_id=self.location_id.id)

        action = self.env['ir.model.data'].xmlid_to_object('scm_abc.scm_purchase_action')
        if not action:
            action = {
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'scm.purchase',
                'type': 'ir.actions.act_window',
            }
        else:
            action = action[0].read()[0]

        action['domain'] = ([('location_id', '=', self.location_id.id)])
        action['name'] = _('SCM ABC')
        action['context'] = ctx
        return action
>>>>>>> 291cf88f137f7da43aafb1270b86f6565dba0dbc
