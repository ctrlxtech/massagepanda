$(document).ready(function() {
    Stripe.setPublishableKey($('#stripePublishKey').val());
});

function doCheckout(form) {
  $("#payment-errors").text("");
  $("#mp-checkoutAlertDanger").hide();

  var formData = $("#payment-form").serialize();
  var csrfToken = $.cookie('csrftoken');
  $.parseHTML(formData);
  $.ajax({
      type        : 'POST',
      beforeSend: function (request)
      {
          request.setRequestHeader("X-CSRFToken", csrfToken);
      },
      url         : 'uncaptureCharge',
      data: formData,
      success: function(data) {
          if (data.status == 'succeeded') {

             if ($('input[name="stripeToken"]').length == 0) {
                form.append($('<input type="hidden" name="stripeToken" />').val(data.id));
             } else {
                $('input[name="stripeToken"]').val(data.id)
             }
             // and re-submit
             form.get(0).submit();
          } else {
             $("#payment-errors").text(data.error);
             $("#mp-checkoutAlertDanger").show();
             $('.btn-success').prop('disabled', false);
          }
      },
      complete: function(data) {
          //alert("complete");
      }
  })
}

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
        doCheckout($form);
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
