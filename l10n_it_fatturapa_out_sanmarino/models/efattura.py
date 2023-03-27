from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import EFatturaOut


class EFatturaOutStesi(EFatturaOut):

    def get_id_fiscale_iva(partner, prefer_fiscalcode=False):
        id_paese = partner.country_id.code
        if partner.vat:
            if (id_paese == "IT" and partner.vat.startswith("IT")) or partner.country_id.force_export_vat:
                id_codice = partner.vat[2:]
            else:
                id_codice = partner.vat
        elif partner.fiscalcode or id_paese == "IT":
            id_codice = False
        else:
            id_codice = "99999999999"

        if prefer_fiscalcode and partner.fiscalcode:
            id_codice = partner.fiscalcode

        return {
            "id_paese": id_paese,
            "id_codice": id_codice,
        }
