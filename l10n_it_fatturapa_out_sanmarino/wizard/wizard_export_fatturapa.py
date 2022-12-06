
import logging


from odoo import api, fields, models


_logger = logging.getLogger(__name__)


class WizardExportFatturapa(models.TransientModel):
    _inherit= "wizard.export.fatturapa"
    _description = "Export E-invoice"
    #
    # def exportInvoiceXML(self, partner, invoice_ids, attach=False, context=None):
    #     invoice_ids_el = self.env["account.move"].with_context(context).browse(invoice_ids)
    #     company_id = invoice_ids_el[0].company_id
    #     el = self.with_context(efattura_company=company_id)
    #     context.update({'efattura_company':company_id})
    #     return super(WizardExportFatturapa, el).exportInvoiceXML( partner, invoice_ids, attach, context)
    # def saveAttachment(self, fatturapa, number):
    #     company_id = fatturapa.invoices[0].company_id
    #     el = self.with_context(efattura_company=company_id)
    #     return super(WizardExportFatturapa, el).saveAttachment(fatturapa,number)
        # attach_obj = self.env["fatturapa.attachment.out"]
        # vat = attach_obj.get_file_vat()
        #
        # attach_str = fatturapa.to_xml(self.env)
        # attach_vals = {
        #     "name": "{}_{}.xml".format(vat, number),
        #     "datas": base64.encodebytes(attach_str),
        # }
        # return attach_obj.create(attach_vals)
