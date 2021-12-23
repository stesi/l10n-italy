from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FatturapaAttachmentOut(models.Model):
    _inherit = 'fatturapa.attachment.out'

    def multiple_send_pec(self):
        for out in self:
            out.send_via_pec()
