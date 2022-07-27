# from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
from odoo.addons.l10n_it_fatturapa_out_rc.wizard.efattura import (
    EFatturaOut as EFatturaOut,
)
from lxml import etree
from odoo.exceptions import UserError


class EFatturaOut(EFatturaOut):

    # def get_template_values(self):
    #     template_values = super().get_template_values()
    #     return template_values

    def to_xml(self, env):
        """Create the xml file content.
        :return: The XML content as str.
        """
        # content = super(EFatturaOut, self).to_xml(env)
        self.env = env

        template_values = self.get_template_values()
        if not self.partner_id.simplified_einvoice:
            content = env.ref("l10n_it_fatturapa_out.account_invoice_it_FatturaPA_export")._render(template_values)
        else:
            content = env.ref("l10n_it_fatturapa_out_semplificata.account_invoice_it_FatturaPA_semplificata_export")._render(template_values)
        # 14.0 - occorre rimuovere gli spazi tra i tag
        root = etree.fromstring(content, parser=etree.XMLParser(remove_blank_text=True))
        # già che ci siamo, validiamo con l'XMLSchema dello SdI
        ok, errors = self.validate(root)
        if not ok:
            # XXX - da migliorare?
            # i controlli precedenti dovrebbero escludere errori di sintassi XML
            # with open("/tmp/fatturaout.xml", "wb") as o:
            #    o.write(etree.tostring(root, xml_declaration=True, encoding="utf-8"))
            raise UserError("\n".join(str(e) for e in errors))
        content = etree.tostring(root, xml_declaration=True, encoding="utf-8")
        return content

    def __init__(self, wizard, partner_id, invoices, progressivo_invio):
        res = super(EFatturaOut, self).__init__(wizard, partner_id, invoices, progressivo_invio)
        return res

# class EFatturaOut(EFatturaOutRCFIX):
#     def __init__(self, wizard, partner_id, invoices, progressivo_invio):
#         res = super(EFatturaOut, self).__init__(wizard, partner_id, invoices, progressivo_invio)
#         return res
