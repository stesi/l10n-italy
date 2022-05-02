odoo.define('fiscal_epos_print_validation_fix.PaymentScreen', function (require) {
    "use strict";
        var PaymentScreen = require("fiscal_epos_print.PaymentScreen")
            var core = require("web.core");

    var _t = core._t;
const Registries = require("point_of_sale.Registries");
const MyPaymentScreenFix = (PaymentScreen) =>

  class extends PaymentScreen {


 _isOrderValid(isForceValidate) {
var order = this.env.pos.get_order();

if (order){
var orderlines = order.orderlines
var taxes = orderlines.find(function (line) {
                        return line.product.taxes_id.length ==0;
                    })

if (taxes){

 this.showPopup("ErrorPopup", {
                        title: _t("Missing tax on some product"),
                        body: _t(
                            "The tax should be on all product"
                        ),
                    });
                    return false;
}

}

  return super._isOrderValid(isForceValidate);
 }

    }


       Registries.Component.extend(PaymentScreen, MyPaymentScreenFix);
       return PaymentScreen
    })

