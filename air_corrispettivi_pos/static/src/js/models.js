odoo.define('air_corrispettivi_pos.corrispettivi', function (require) {
"use strict";

    var models = require('point_of_sale.models');
    var rpc = require('web.rpc')
    var db = require('point_of_sale.DB')
    models.PosModel = models.PosModel.extend({

        get_client:  function () {
            var order = this.get_order();
            var cliente= null;
            var self =this;
            var partner_id=this.get_public_user();
            //Promise esegue la funzione asincrona
            var x =Promise.resolve(partner_id).then(function (results) { partner_id= results

            console.log('3');
            if (order) {
               cliente= order.get_client();
               if (cliente !== null){

                return cliente
               }
            }

            if  (cliente == null) {

                cliente = self.env.pos.db.get_partner_by_id(partner_id);
                order.attributes['client']= cliente;
                order.client=cliente;
                return cliente;
           }



        });},
        get_public_user:function() {
        // Funzione asincrona
            return  rpc.query({
                    model: 'account.move',
                    method: 'api_public_user'
                    }).then(function (result) {
                     console.log(result);
                     return result;
                     })

         },
    });

//    models.Order= models.PosModel.extend({

});


