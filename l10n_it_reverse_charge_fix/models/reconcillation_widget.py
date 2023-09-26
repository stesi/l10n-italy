from odoo import api, fields, models, _

from odoo.addons.account_accountant.models.reconciliation_widget import \
    AccountReconciliation as OdooAccountReconciliation


def _get_query_reconciliation_widget_receivable_payable_lines(self, statement_line, domain=[]):
    domain = domain + [
        ('account_id.internal_type', 'in', ('receivable', 'payable')),
    ]
    tables, where_clause, where_params = self._prepare_reconciliation_widget_query(statement_line, domain=domain)

    query = '''
        SELECT ''' + self._get_query_select_clause() + '''
        FROM ''' + tables + '''
        WHERE ''' + where_clause + '''
    '''
    return query, where_params


OdooAccountReconciliation._get_query_reconciliation_widget_receivable_payable_lines = _get_query_reconciliation_widget_receivable_payable_lines
