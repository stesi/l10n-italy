from odoo import models, fields, api
from odoo.addons.l10n_it_fatturapa_out.models import account

account.fatturapa_attachment_state_mapping['rejected'] = "rejected"


class AccountMove(models.Model):
    _inherit = 'account.move'

    fatturapa_state = fields.Selection(selection_add=[('rejected', 'Rejected')], ondelete={'rejected': 'cascade'})
