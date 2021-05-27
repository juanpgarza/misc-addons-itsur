# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _

class MailComposeMessage(models.TransientModel):
    _inherit = 'mail.compose.message'

    active_model = fields.Char('modelo activo')
    active_id = fields.Integer('id activo')

    @api.model
    def default_get(self, fields_list):
        # import pdb; pdb.set_trace()
        res = super().default_get(fields_list)
        # res.setdefault(
        #     'autofollow_recipients',
        #     self.env.context.get('mail_post_autofollow', False))
        
        # import pdb; pdb.set_trace()

        res.setdefault(
            'active_id',
            self.env.context.get('active_id'))

        res.setdefault(
            'active_model',
            self.env.context.get('active_model'))

        # self.active_id = self.env.context['active_id']
        # self.active_model = self.env.context['active_model']

        return res


    @api.multi
    def send_mail(self, auto_commit=False):
        for wizard in self:
            super(MailComposeMessage, wizard).send_mail(auto_commit=auto_commit)
        # import pdb; pdb.set_trace()
        
        # self.env["mail.followers"].search([('res_model', '=', 'sale.order'),('res_id', '=', 8878),('partner_id', '=',1506)]).unlink()
        if self.active_model in ('sale.order','account.invoice'):
            
            # sale_order_id = self.env['sale.order'].browse(self.active_id)
            # partner_seguidor = self.env["mail.followers"].search([('res_model', '=', 'sale.order'),
            #                                             ('res_id', '=', sale_order_id.id),
            #                                             ('partner_id', '=',sale_order_id.partner_id.id)])

            document_record = self.env[self.active_model].browse(self.active_id)
            partner_seguidor = self.env["mail.followers"].search([('res_model', '=', self.active_model),
                                                        ('res_id', '=', document_record.id),
                                                        ('partner_id', '=',document_record.partner_id.id)])

            if partner_seguidor:
                # import pdb; pdb.set_trace()
                # partner_seguidor.unlink()
                # self.env["mail.followers"].search([('res_model', '=', 'sale.order'), ('res_id', '=', 9528), ('partner_id', '=',4444)]).subtype_ids
                # \\ubudoc\public\odoo-dev\12\pronto2020\src\addons\mail\models\mail_followers.py
                # self.env["mail.followers"].search([('res_model', '=', 'sale.order'), ('res_id', '=', 9528), ('partner_id', '=',4444)]).write({'subtype_ids': [(3, 1,_)]})
                partner_seguidor.write({'subtype_ids': [(3, 1,_)]})

        return True
