import logging




_logger = logging.getLogger(__name__)



from odoo import models, fields, api,_
from odoo.exceptions import UserError,ValidationError
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    is_pos_account_move_line = fields.Boolean(compute='_compute_is_pos_account_move_line')
    def _compute_is_pos_account_move_line(self):
        for aml in self:
            pos_session = self.env['pos.session'].search([('move_id','=',aml.move_id.id)])
            aml.is_pos_account_move_line = len(pos_session)>0
    def _compute_margin_from_pos_session(self):
        for aml in self:
            if aml.is_pos_account_move_line and len(aml.tax_ids.filtered(lambda t: t.margin_tax))>0:
                pos_session = self.env['pos.session'].search([('move_id', '=', aml.move_id.id)])
                margin = sum(pos_session.order_ids.lines.filtered(lambda l: l.tax_ids.filtered(lambda t: t.margin_tax)).mapped('margin'))
                aml.margin = margin
                aml.move_id._recompute_tax_lines()
