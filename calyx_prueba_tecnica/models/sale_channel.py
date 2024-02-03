# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleChannel(models.Model):
    _name = 'sale.channel'
    #_inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Query para el procesamiento de asientos de TPV"
    _rec_name = 'name'

    name = fields.Char()

    code = fields.Char(default=lambda self: self.env['ir.sequence'].next_by_code('calyx_prueba_tecnica.secuencia'))

    journal_id = fields.Many2one('account.journal', string="Diario")

    stock_warehouse_id = fields.Many2one('stock.warehouse', string="Almacen")

    #auditlog_ids = fields.One2many('auditlog.log', 'res_id', string='Historial de cambios', readonly=True, copy=False)



    # def create(self, vals):
    #     if 'company_id' in vals:
    #         self = self.with_company(vals['company_id'])
    #     if vals.get('name', _('New')) == _('New'):
    #         seq_date = None
    #         if 'date_order' in vals:
    #             seq_date = fields.Datetime.context_timestamp(self, fields.Datetime.to_datetime(vals['date_order']))
    #         vals['name'] = self.env['ir.sequence'].next_by_code('sale.order', sequence_date=seq_date) or _('New')
