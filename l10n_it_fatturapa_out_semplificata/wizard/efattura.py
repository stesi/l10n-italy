# from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (


from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (
    EFatturaOut as _EFatturaOut,
)
from lxml import etree
from odoo.exceptions import UserError
from odoo.modules.module import get_module_resource
import xmlschema
from odoo.addons.l10n_it_account.tools.account_tools import fpa_schema
# from odoo.addons.l10n_it_fatturapa_out.wizard.efattura import (fpa_schema)
# _fpa_schema_file = get_module_resource(
#     "l10n_it_account",
#     "tools",
#     "xsd",
#     "Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd",
# )
# _old_xsd_specs = get_module_resource(
#     "l10n_it_account", "tools", "xsd", "xmldsig-core-schema.xsd"
# )
#
#
# fpa_schema = (xmlschema.XMLSchema(
#     _fpa_schema_file,
#     locations={"http://www.w3.org/2000/09/xmldsig#": _old_xsd_specs},
#     validation="lax",
#     allow="local",
#     loglevel=20,
# ))

class EFatturaOut(_EFatturaOut):


    _fpa_schema_file = get_module_resource(
        "l10n_it_account",
        "tools",
        "xsd",
        "Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd",
    )
    _old_xsd_specs = get_module_resource(
        "l10n_it_account", "tools", "xsd", "xmldsig-core-schema.xsd"
    )


    fpa_schema = xmlschema.XMLSchema(
        _fpa_schema_file,
        locations={"http://www.w3.org/2000/09/xmldsig#": _old_xsd_specs},
        validation="lax",
        allow="local",
        loglevel=20,
    )

    def get_template_values(self):
        template_values = super().get_template_values()
        if 'formato_trasmissione' in template_values and self.partner_id.simplified_einvoice:
            template_values['formato_trasmissione'] = 'FSM10'
        return template_values

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
        # nel caso in cui il partner preveda la fattura semplificata devo validarlo diversamente
        if not self.partner_id.simplified_einvoice:
            _fpa_schema_file = get_module_resource(
                "l10n_it_account",
                "tools",
                "xsd",
                "Schema_del_file_xml_FatturaPA_versione_1.2.1.xsd",
            )
            _old_xsd_specs = get_module_resource(
                "l10n_it_account", "tools", "xsd", "xmldsig-core-schema.xsd"
            )

            fpa_schema = xmlschema.XMLSchema(
                _fpa_schema_file,
                locations={"http://www.w3.org/2000/09/xmldsig#": _old_xsd_specs},
                validation="lax",
                allow="local",
                loglevel=20,
            )
            errors = list(fpa_schema.iter_errors(root))
        else: # per ora invalidato controllo

            fpa_schema_file = get_module_resource(
                "l10n_it_fatturapa_out_semplificata",
                "data",
                "xsd",
                "schema_xsd_fattura_semplificata.xsd",
            )
            _old_xsd_specs = get_module_resource(
                "l10n_it_account", "tools", "xsd", "xmldsig-core-schema.xsd"
            )
            fpa_schema = xmlschema.XMLSchema(
                fpa_schema_file,
                locations={"http://www.w3.org/2000/09/xmldsig#": _old_xsd_specs},
                validation="lax",
                allow="local",
                loglevel=20,
            )
            errors = list(fpa_schema.iter_errors(root))
            # ok = True

        # if not ok:
        # errors = list(fpa_schema.iter_errors(root))
        if errors:
            # XXX - da migliorare?
            # i controlli precedenti dovrebbero escludere errori di sintassi XML
            # with open("/tmp/fatturaout.xml", "wb") as o:
            #    o.write(etree.tostring(root, xml_declaration=True, encoding="utf-8"))
            raise UserError("\n".join(str(e) for e in errors))

        content = etree.tostring(root, xml_declaration=True, encoding="utf-8")

        return content

    # def __init__(self, wizard, partner_id, invoices, progressivo_invio):
    #     res = super(EFatturaOut, self).__init__(wizard, partner_id, invoices, progressivo_invio)
    #     return res

# class EFatturaOut(EFatturaOutRCFIX):
#     def __init__(self, wizard, partner_id, invoices, progressivo_invio):
#         res = super(EFatturaOut, self).__init__(wizard, partner_id, invoices, progressivo_invio)
#         return res
