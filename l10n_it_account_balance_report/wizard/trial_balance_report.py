# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models

REPORT_TYPES = ("profit_loss", "balance_sheet")


class TrialBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.trial_balance"

    @api.model
    def _get_data(
        self,
        account_ids,
        journal_ids,
        partner_ids,
        company_id,
        date_to,
        date_from,
        foreign_currency,
        only_posted_moves,
        show_partner_details,
        hide_account_at_0,
        unaffected_earnings_account,
        fy_start_date,
    ):
        total_amount, accounts_data, partners_data =  super(TrialBalanceReport, self)._get_data( account_ids,
        journal_ids,
        partner_ids,
        company_id,
        date_to,
        date_from,
        foreign_currency,
        only_posted_moves,
        show_partner_details,
        hide_account_at_0,
        unaffected_earnings_account,
        fy_start_date)

        if 'remove_id_profit_loss' in self.env.context:
            id_profit_loss = -1
            for account_id in accounts_data.values():
                if account_id['code'] == '999999':
                    id_profit_loss = account_id['id']
            if id_profit_loss > -1:
                del accounts_data[id_profit_loss]


        return total_amount, accounts_data, partners_data

