odoo.define('stesi_l10n_it_posfiscalcode_fix.screens', function(require){
    'use strict';

//    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const ClientListScreen = require('point_of_sale.ClientDetailsEdit');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');

    const POSSaveClientOverride = ClientListScreen => class extends ClientListScreen {
        async saveChanges(event) {
            var fiscalcode = $('.fiscalcode').val();
            await this.env.pos.load_new_partners();
            this.state.selectedClient = this.env.pos.db.get_partner_by_id(partnerId);
            this.state.detailIsShown = false;
            this.render();
        }
    };
    Registries.Component.extend(ClientListScreen, POSSaveClientOverride);
    return ClientListScreen;
});
