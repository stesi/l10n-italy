# Copyright 2018-2019 Simone Rubino - Agile Business Group
# Copyright 2021 Kevin Poli - AIR s.r.l.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id')
    def onchange_partner_corrispettivi_sale(self):
        self.corrispettivi = self.partner_id.use_corrispettivi

    @api.onchange('fiscal_position_id')
    def _compute_tax_id(self):
        res = super(SaleOrder, self)._compute_tax_id()
        if self.fiscal_position_id:
            self.corrispettivi = self.fiscal_position_id.corrispettivi
        return res

    corrispettivi = fields.Boolean()


    def _prepare_invoice(self):
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        journal_model = self.env['account.journal']
        if self.corrispettivi:
            invoice_vals['journal_id'] = journal_model \
                .get_corr_journal(self.company_id).id
        elif invoice_vals['journal_id']:
            # Be sure that the selected journal is not corrispettivi
            journal = journal_model.browse(invoice_vals['journal_id'])
            if journal.corrispettivi:
                # Default journal chosen by invoice is a corrispettivi,
                # then do the same as account_invoice to look for another
                # one that is not corrispettivi
                invoice_vals['journal_id'] = \
                    self.get_default_journal_not_corr().id
        return invoice_vals

    def get_default_journal_not_corr(self):
        # Copied from account_invoice default behavior
        if self._context.get('default_journal_id', False):
            journal = self.env['account.journal'] \
                          .browse(self._context.get('default_journal_id'))
            if not journal.corrispettivi:  # with this tiny modification
                return journal
        move_type = self._context.get('default_move_type', 'out_invoice')


        journal_with_currency = False
        journal_types = self._context.get('default_move_journal_types', ['sale'])
        company_id = self._context \
            .get('company_id', self.env.user.company_id.id)
        domain = [
            ('type', 'in', journal_types),
            ('company_id', '=', company_id),
            ('corrispettivi', '=', False)  # with this tiny modification
        ]
        if self._context.get('default_currency_id'):
            currency_clause = [
                ('currency_id', '=', self._context.get('default_currency_id'))]
            journal_with_currency = self.env['account.journal'] \
                .search(domain + currency_clause, limit=1)
        return journal_with_currency \
            or self.env['account.journal'].search(domain, limit=1)

