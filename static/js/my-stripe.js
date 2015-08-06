// This identifies your website in the createToken call below
Stripe.setPublishableKey('pk_test_704p8Gz1ev0sCJJK5sc4b9cF');

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
jQuery(function($) {
    $('#payment-form').submit(function(e) {
        var $form = $(this);
        // Disable the submit button to prevent repeated clicks
        $form.find('button').prop('disabled', true);
        Stripe.card.createToken($form, stripeResponseHandler);
        // Prevent the form from submitting with the default action
        return false;
    });
});
