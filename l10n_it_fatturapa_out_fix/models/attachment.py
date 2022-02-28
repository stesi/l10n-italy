# Copyright 2014 Davide Corio
# Copyright 2016-2018 Lorenzo Battistini - Agile Business Group

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FatturaPAAttachment(models.Model):
    _inherit = "fatturapa.attachment.out"
    @api.model
    def get_file_vat(self):
        company = self.env.context.get('efattura_company',self.env.company)
        if company.fatturapa_sender_partner:
            if not company.fatturapa_sender_partner.vat:
                raise UserError(
                    _("Partner %s TIN not set.")
                    % company.fatturapa_sender_partner.display_name
                )
            vat = company.fatturapa_sender_partner.vat
        else:
            if not company.vat:
                raise UserError(_("Company %s TIN not set.") % company.display_name)
            vat = company.vat
        vat = vat.replace(" ", "").replace(".", "").replace("-", "")
        return vat
