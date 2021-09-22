# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class IrModel(models.Model):
    _inherit = "ir.model"

    related_field_qty = fields.Integer(compute="_compute_related_field_qty")
    related_field_from_ids = fields.Many2many(comodel_name="ir.model.fields", compute="_compute_related_field_from_ids")
    related_field_to_ids = fields.Many2many(comodel_name="ir.model.fields", compute="_compute_related_field_to_ids")

    @api.depends('field_id')
    def _compute_related_field_qty(self):
        for rec in self:
            # related_fields = self.env['ir.model.fields'].search([('ttype', 'in', ['many2one', 'many2many', 'one2many', 'many2one_reference']), '|', ('model_id', '=', self.id), ('relation', '=', self.model)])
            rec.related_field_qty = len(rec.related_field_from_ids) + len(rec.related_field_to_ids)

    @api.depends('field_id')
    def _compute_related_field_from_ids(self):
        for rec in self:
            rec.related_field_from_ids = rec.field_id.filtered(lambda f: f.ttype in ['many2one', 'many2many', 'one2many'])

    def _compute_related_field_to_ids(self):
        for rec in self:
            rec.related_field_to_ids = self.env['ir.model.fields'].search([('ttype', 'in', ['many2one', 'many2many', 'one2many']), ('relation', '=', self.model)])

    def action_show_related_fields(self):
        return {
            "name": _("Related fields for %s" % self.model),
            "type": 'ir.actions.act_window',
            "res_model": 'ir.model.fields',
            "views": [
                [self.env.ref('odoo_explorer.ir_model_fields_relations_tree').id, "tree"],
            ],
            "target": 'self',
            "context": {
                **self.env.context,
            },
            "domain": [('id', 'in', self.related_field_from_ids.ids + self.related_field_to_ids.ids)]
        }

    def action_model_pathfinder(self):
        action = self.env.ref('odoo_explorer.model_pathfinder_wizard_action').read()[0]
        action['context'] = {
            **self.env.context,
            'default_start_model_id': self.id,
        }
        action['target'] = 'new'
        return action
