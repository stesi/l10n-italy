from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

STANDARD_ADDRESSEE_CODE = "0000000"

class ResPartner(models.Model):
    _inherit = 'res.partner'

    simplified_einvoice = fields.Boolean(string="Simplified E-Invoice", index=True)
    STANDARD_ADDRESSEE_CODE = "0000000"

    def _check_ftpa_partner_data(self):
        for partner in self:
            if partner.electronic_invoice_subjected:
                if not partner.simplified_einvoice:
                    super(ResPartner, partner)._check_ftpa_partner_data()
                else:
                    if partner.is_pa and (
                        not partner.ipa_code or len(partner.ipa_code) != 6
                    ):
                        raise ValidationError(
                            _(
                                "As a Public Administration, partner %s IPA Code "
                                "must be 6 characters long."
                            )
                            % partner.name
                        )
                    if (
                        partner.company_type == "person"
                        and not partner.company_name
                        and (not partner.lastname or not partner.firstname)
                    ):
                        raise ValidationError(
                            _(
                                "As a natural person, partner %s "
                                "must have Name and Surname."
                            )
                            % partner.name
                    )
                if not partner.is_pa and not partner.codice_destinatario:
                    raise ValidationError(
                        _("Partner %s must have Addresse Code. Use %s if unknown")
                        % (partner.name, STANDARD_ADDRESSEE_CODE)
                    )
                if (
                    not partner.is_pa
                    and partner.codice_destinatario
                    and len(partner.codice_destinatario) != 7
                ):
                    raise ValidationError(
                        _("Partner %s Addressee Code must be 7 characters long.")
                        % partner.name
                    )
                if partner.pec_destinatario:
                    if partner.codice_destinatario != STANDARD_ADDRESSEE_CODE:
                        raise ValidationError(
                            _(
                                "Partner %s has Addressee PEC %s, "
                                "the Addresse Code must be %s."
                            )
                            % (
                                partner.name,
                                partner.pec_destinatario,
                                STANDARD_ADDRESSEE_CODE,
                            )
                        )
                if (
                    not partner.vat
                    and not partner.fiscalcode
                    and partner.country_id.code == "IT"
                ):
                    raise ValidationError(
                        _("Italian partner %s must have VAT Number or Fiscal Code.")
                        % partner.name
                    )

