# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleChannel(models.Model):
    _name = 'sale.channel'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Canal de Venta"
    _rec_name = 'name'

    name = fields.Char()

    code = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('calyx_prueba_tecnica.secuencia'))

    journal_id = fields.Many2one('account.journal', string="Diario")

    stock_warehouse_id = fields.Many2one('stock.warehouse', string="Almacen")

    #auditlog_ids = fields.One2many('auditlog.log', 'res_id', string='Historial de cambios', readonly=True, copy=False)

