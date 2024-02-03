# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    control_credit = fields.Boolean(string="Control de Credito")

    credit_group_ids = fields.Many2many('credit.group', string="Grupos de Credito")