# -*- coding: utf-8 -*-
import datetime
from requests import post
from odoo import models, fields, api
from odoo.exceptions import UserError, AccessError, ValidationError, except_orm
import dateutil.parser
import json
from io import BytesIO
import xlwt
import base64

class CreditGroupWizard(models.TransientModel):
    _name = 'wizard.credit.group'
    _description = 'wizard'

    credit_groups_id = fields.Many2one('credit.group')

    report = fields.Binary('Descargar xls', filters='.xls', readonly=True)
    name = fields.Char('File Name', size=32)
    state = fields.Selection([('choose', 'choose'), ('get', 'get')], default='choose')

    def print_xls(self):
        fp = BytesIO()
        wb = xlwt.Workbook(encoding='utf-8')
        writer = wb.add_sheet('Nombre de hoja')

        #FUENTES
        header_content_style = xlwt.easyxf("font: name Helvetica size 80 px, bold 1, height 200;")
        sub_header_style = xlwt.easyxf("font: name Helvetica size 10 px, height 170; "
                                       "borders: left thin, right thin, top thin, bottom thin;")
        sub_header_content_style = xlwt.easyxf("font: name Helvetica size 10 px, bold 1, height 170;") 
        #

        row = 0
        col = 0

        writer.write_merge(col, col, 0, 4, "Informe de Credito", header_content_style)

        col += 1
        writer.write_merge(col, col, 0, 2, "Información de Grupo", header_content_style)
        
        col += 1

        writer.write_merge(col, col, 0, 0, "Nombre del Grupo", sub_header_content_style)
        writer.write_merge(col, col, 1, 1, "Código del Grupo", sub_header_content_style)
        writer.write_merge(col, col, 2, 2, "Canal de Venta", sub_header_content_style)

        col += 1

        credit_group = self.env['credit.group'].search([('id','=',self.credit_groups_id.id)], limit=1)
        writer.write_merge(col, col, 0, 0, credit_group.name, sub_header_content_style)
        writer.write_merge(col, col, 1, 1, credit_group.code, sub_header_content_style)
        writer.write_merge(col, col, 2, 2, credit_group.sale_channel_id.name, sub_header_content_style)

        col += 2

        writer.write_merge(col, col, 0, 3, "Información de Clientes", header_content_style)

        col += 1
        
        writer.write_merge(col, col, 0, 0, "Nombre de Cliente", sub_header_content_style)
        writer.write_merge(col, col, 1, 1, "Número de Documento", sub_header_content_style)
        writer.write_merge(col, col, 2, 2, "Telefono", sub_header_content_style)
        writer.write_merge(col, col, 3, 3, "Correo Electronico", sub_header_content_style)

        col += 1

        res_partner_ids = self.env['res.partner'].search([('credit_group_ids', 'in',self.credit_groups_id.ids)])
        for res_partner in res_partner_ids: 
            writer.write_merge(col, col, 0, 0, res_partner.name, sub_header_content_style)
            writer.write_merge(col, col, 1, 1, res_partner.vat, sub_header_content_style)
            writer.write_merge(col, col, 2, 2, res_partner.phone, sub_header_content_style)
            writer.write_merge(col, col, 3, 3, res_partner.email, sub_header_content_style)
            col += 1

        col += 2

        writer.write_merge(col, col, 0, 3, "Ordenes de Ventas", header_content_style)
        
        col += 1

        writer.write_merge(col, col, 0, 0, "Número", sub_header_content_style)
        writer.write_merge(col, col, 1, 1, "Fecha", sub_header_content_style)
        writer.write_merge(col, col, 2, 2, "Importe Total", sub_header_content_style)

        col += 1
        
        sale_order_ids = self.env['sale.order'].search([('sale_channel_id', '=', credit_group.sale_channel_id.id)])
        for sale_order in sale_order_ids: 
            writer.write_merge(col, col, 0, 0, sale_order.name, sub_header_content_style)
            writer.write_merge(col, col, 1, 1, str(sale_order.date_order), sub_header_content_style)
            writer.write_merge(col, col, 2, 2, sale_order.amount_total, sub_header_content_style)
            col += 1

        col += 2

        writer.write_merge(col, col, 0, 3, "Facturas de Ventas", header_content_style)

        col += 1

        writer.write_merge(col, col, 0, 0, "Número", sub_header_content_style)
        writer.write_merge(col, col, 1, 1, "Fecha", sub_header_content_style)
        writer.write_merge(col, col, 2, 2, "Importe Adeudado", sub_header_content_style)

        col += 1

        account_move_ids = self.env['account.move'].search([('sale_channel_id', '=', credit_group.sale_channel_id.id)])
        for account_move in account_move_ids: 
            writer.write_merge(col, col, 0, 0, account_move.name, sub_header_content_style)
            writer.write_merge(col, col, 1, 1, str(account_move.date), sub_header_content_style)
            writer.write_merge(col, col, 2, 2, account_move.amount_total, sub_header_content_style)
            col += 1
        col += 1


        wb.save(fp)

        out = base64.encodebytes(fp.getvalue())
        self.write({'state': 'get', 'report': out, 'name': 'Reporte de Credito.xls'})

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'wizard.credit.group',
            'view_mode': 'form',
            'view_type': 'form',
            'res_id': self.id,
            'views': [(False, 'form')],
            'target': 'new',
        }