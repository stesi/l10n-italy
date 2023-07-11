import logging




_logger = logging.getLogger(__name__)


import codicefiscale
from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError
from odoo.addons.l10n_it_fiscalcode_validation.libs.codicefiscale import codicefiscale as cf
class ResPartner(models.Model):
    _inherit = 'res.partner'
    is_fiscalcode_valid = fields.Boolean(compute='_is_fiscalcode_valid')
    def _is_fiscalcode_valid(self):
        for rp in self:
            rp.is_fiscalcode_valid = cf.is_valid(rp.fiscalcode or '')

    @api.constrains("fiscalcode","company_type")
    def validate_fiscalcode(self):
        for rp in self:
            if rp.company_type == "person" and rp.fiscalcode and not rp.is_fiscalcode_valid:
                raise ValidationError(_("The fiscal code is not valid"))

