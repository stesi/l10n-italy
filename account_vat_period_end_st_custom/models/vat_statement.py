from odoo import models, fields, api, exceptions, _, SUPERUSER_ID
from odoo.exceptions import UserError, AccessError
from odoo.tools.misc import formatLang


def formatLangZero(env, value, digits=None, grouping=True, monetary=False, dp=False, currency_obj=False):
    if round(value, digits) >= 0:
        value = abs(value)
    return formatLang(env, value, digits, grouping, monetary, dp, currency_obj)


class VatPeriodEndStatementReport(models.AbstractModel):
    _inherit = "report.account_vat_period_end_statement.vat_statement"

    @api.model
    def _get_report_values(self, docids, data=None):
        res = super(VatPeriodEndStatementReport, self)._get_report_values(docids, data)
        res['formatLang'] = formatLangZero
        return res
