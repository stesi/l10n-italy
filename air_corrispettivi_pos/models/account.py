from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.model
    def api_public_user(self):
         public_user=self.env.ref('base.public_user').partner_id.id
         return public_user
