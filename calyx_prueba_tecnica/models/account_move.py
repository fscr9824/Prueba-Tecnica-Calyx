# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    #Canales de Venta
    sale_channel_id = fields.Many2one('sale.channel', string="Canales de Venta")
