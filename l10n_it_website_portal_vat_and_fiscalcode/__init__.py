from . import controllers

from odoo import api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


def _pre_init_check_module(cr):
    env = api.Environment(cr, SUPERUSER_ID, {})
    module = env['ir.module.module'].search([('name', '=', 'l10n_it_website_portal_fiscalcode')])
    if module and module.state in ['installed', 'to upgrade', 'to remove']:
        raise ValidationError(_("Please uninstall 'l10n_it_website_portal_fiscalcode' before install last one"))
