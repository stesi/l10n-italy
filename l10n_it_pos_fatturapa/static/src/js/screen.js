odoo.define("l10n_it_pos_fatturapa.screens", function(require) {
    "use strict";


    const ClientListScreen = require('point_of_sale.ClientListScreen');
    const Registries = require('point_of_sale.Registries');
    var { Gui } = require('point_of_sale.Gui');
    var models = require('point_of_sale.models');

    const POSSaveClientOverride = ClientListScreen =>
        class extends ClientListScreen {
            async saveChanges(event) {
                var pec_add =$('.pec_destinatario').val();
                var electronic_invoice_subjected=$('.electronic_invoice_subjected').val();
                var electronic_invoice_obliged_subject=$('.electronic_invoice_obliged_subject').val();
                var codice_destinatario=$('.codice_destinatario').val();


                console.log('pec add has been settedss');
                console.log(pec_add);
                if (pec_add == true) {
                    console.log('pec add has been setted');
                }
                if ((pec_add || codice_destinatario) && (!electronic_invoice_subjected || !electronic_invoice_obliged_subject)){
                     await this.showPopup('ErrorPopup', {
                            title: this.env._t('Error'),
                            body: this.env._t('To set "Pec address/Addresses code" you must set "Enable electronic invoicing" and "Obliged Subject" to True'),
                     });
                     return;
                }
                let partnerId = await this.rpc({
                    model: 'res.partner',
                    method: 'create_from_ui',
                    args: [event.detail.processedChanges],
                });
                await this.env.pos.load_new_partners();
                this.state.selectedClient = this.env.pos.db.get_partner_by_id(partnerId);
                this.state.detailIsShown = false;
                this.render();
            }
        };
        Registries.Component.extend(ClientListScreen, POSSaveClientOverride);
        return ClientListScreen;
});

