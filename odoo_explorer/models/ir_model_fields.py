# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class IrModelFields(models.Model):
    _inherit = "ir.model.fields"
    
    # relation_type = fields.Selection(
    #     selection=[
    #         ('none', 'None'),
    #         ('from', 'From model'),
    #         ('to', 'To model'),
    #     ],
    #     default='none',
    #     compute="_compute_relation_type",
    #     store=True,
    # )

    # linked_model_technical_name = fields.Char(compute='_compute_linked_model_technical_name')
    #
    # @api.depends('model_id', 'relation', 'name')
    # def _compute_relation_type(self):
    #     active_id = self.env.context.get('active_id', False)
    #     for rec in self:
    #         rec.relation_type = 'none'
    #         if active_id:
    #             rec.relation_type = 'from' if active_id == rec.model_id.id else 'to'

    # @api.depends('relation_type')
    # def _compute_linked_model_technical_name(self):
    #     for rec in self:
    #         rec.linked_model_technical_name = rec.model_id.model if rec.relation_type == 'to' else rec.relation

