from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockDeliveryNote(models.Model):
    _inherit = "stock.delivery.note"

    def send_by_email(self):
        self.ensure_one()
        lang = self.env.context.get('lang')
        template_id = self.env['ir.model.data'].xmlid_to_res_id('stesi_delivery_note_send_email.mail_template_send_delivery_note', raise_if_not_found=False)
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'stock.delivery.note',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'custom_layout': "mail.mail_notification_paynow",
            'proforma': self.env.context.get('proforma', False),
            'force_email': True,
            'model_description': self.with_context(lang=lang).name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

