# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CreditGroup(models.Model):
    _name = 'credit.group'
    _description = "Query para el procesamiento de asientos de TPV"
    _rec_name = 'name'

    name = fields.Char(string="Nombre")

    code = fields.Char(string="Código")

    sale_channel_id = fields.Many2one('sale.channel', string="Canal de Venta")

    conversion_currency_id = fields.Many2one(
        'res.currency',  default=lambda self: self.env.company.currency_id
    )

    credit_global = fields.Monetary(currency_field='conversion_currency_id', string="Credito Global")

    credit_used = fields.Monetary(currency_field='conversion_currency_id', string="Credito Utilizado", compute="_compute_calculate_credit")

    credit_available = fields.Monetary(currency_field='conversion_currency_id', string="Credito Disponible", compute="_compute_calculate_credit")

    #FUNCIONES CALCULADAS

    @api.depends('credit_global')
    def _compute_calculate_credit(self):
        for registry in self:
            registry.credit_used = 10000
            registry.credit_available = registry.credit_global - registry.credit_used 
