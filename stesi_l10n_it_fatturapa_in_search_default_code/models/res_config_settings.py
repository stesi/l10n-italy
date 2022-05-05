

from odoo import fields, models


class AccountConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"
    fatturapa_in_search_by_default_code = fields.Boolean(
        string="Search product by global default code in fatturapa_in",
        config_parameter="l10n_it_fatturapa_in.search_default_code",
    )
