# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SalesOrderInherit(models.Model):
    _inherit = 'sale.order'

    #Canales de Venta
    sale_channel_id = fields.Many2one('sale.channel', string="Canal de Venta")
