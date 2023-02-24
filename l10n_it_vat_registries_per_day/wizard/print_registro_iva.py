# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import Warning as UserError


class WizardRegistroIva(models.TransientModel):
    _inherit = "wizard.registro.iva"
    only_totals_per_day = fields.Boolean(string="Prints only totals per day")
    @api.onchange('only_totals_per_day')
    def onchange_only_totals(self):
        if self.only_totals_per_day:
            self.only_totals = True
