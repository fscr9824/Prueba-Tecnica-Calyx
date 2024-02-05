# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class CreditGroup(models.Model):
    _name = 'credit.group'
    _description = "Grupos de Creditos"
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
    
    #CONTRAINSTS

    @api.constrains('code')
    def _check_code(self):
        for rec in self:
            duplicates = self.env['credit.group'].search([('code', '=', rec.code)])
            if len(duplicates) > 1:
                raise ValidationError('¡El valor del Código ya existe!')
            if rec.code.endswith('026'):
                 raise ValidationError('¡El valor del Código No puede contener 026!')

    #FUNCIONES CALCULADAS

    @api.depends('credit_global', 'sale_channel_id')
    def _compute_calculate_credit(self):
        for registry in self:
            if registry.sale_channel_id:
                credit = 0
                account_moves = self.env['account.move'].search([('state','not in',['cancel','done']),('sale_channel_id','=',registry.sale_channel_id.id)])
                if account_moves:
                    for account_move in account_moves:
                        credit += account_move.amount_total
                sale_orders = self.env['sale.order'].search([('sale_channel_id','=',registry.sale_channel_id.id),('invoice_status','=','to invoice')])
                if sale_orders:
                    for sale_order in sale_orders:
                        credit += sale_order.amount_total
                registry.credit_used = credit
                registry.credit_available = registry.credit_global - registry.credit_used
            else:
                registry.credit_used = False
                registry.credit_available = False
