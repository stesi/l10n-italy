from odoo import _, api, fields, models
from odoo.exceptions import UserError


class WizardInvoiceManageAsset(models.TransientModel):
    _inherit = "wizard.invoice.manage.asset"


class WizardAssetsGenerateDepreciations(models.TransientModel):
    _inherit = "wizard.asset.generate.depreciation"


class WizardAssetJournalReport(models.TransientModel):
    _inherit = "wizard.asset.journal.report"


class WizardAssetPrevisionalReport(models.TransientModel):
    _inherit = "wizard.asset.previsional.report"
