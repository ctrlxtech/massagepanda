$(document).ready(function() {
    Stripe.setPublishableKey($('#stripePublishKey').val());
});

var stripeResponseHandler = function(status, response) {
    var $form = $('#payment-form');
    if (response.error) {
        // Show the errors on the form
        $form.find('.payment-errors').text(response.error.message);
        $form.find('.mp-checkoutAlertDanger').css('display', 'block');
        $form.find('button').prop('disabled', false);
    } else {
        $form.find('.mp-checkoutAlertDanger').css('display', 'none');
        // token contains id, last4, and card type
        var token = response.id;
        // Insert the token into the form so it gets submitted to the server
        $form.append($('<input type="hidden" name="stripeToken" />').val(token));
        // and re-submit
        $form.get(0).submit();
    }
};

var addPaymentHandler = function(status, response) {
    var $form = $('#new-payment-form');
    if (response.error) {
        // Show the errors on the form
        $form.find('.payment-errors').text(response.error.message);
        $form.find('.mp-checkoutAlertDanger').css('display', 'block');
        $form.find('button').prop('disabled', false);
    } else {
        $form.find('.mp-checkoutAlertDanger').css('display', 'none');
        // token contains id, last4, and card type
        var token = response.id;
        // Insert the token into the form so it gets submitted to the server
        $form.append($('<input type="hidden" name="stripeToken" />').val(token));
        // and re-submit
        addNewPayment();
    }
};
