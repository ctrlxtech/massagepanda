$(document).ready(function() {
  $('#new-payment-form').validator().on('submit', function(event) {
    if (event.isDefaultPrevented()) {
      $('#response-errors').text("Correct the inputs");
      $('#payment-alert').show();
      return;
    }

    populateExpYearAndMonth();
    var $form = $(this);
    // Disable the submit button to prevent repeated clicks
    $form.find('button').prop('disabled', true);
    Stripe.card.createToken($form, addPaymentHandler);
    // Prevent the form from submitting with the default action
    return false;
  });

  $('#payment-table').on('click', 'a[name="deletePaymentBtn"]', function(event) {
    event.preventDefault();
    var csrfToken = $.cookie('csrftoken');
    var cardId = $(event.target).closest('.wsite-multicol-col').find('input[name="card-id"]').val();
    var formData = {
        'cardId': cardId
    };

    $('#confirm').modal({ backdrop: 'static'})
        .one('click', '#delete', function() {
            deletePayment(csrfToken, formData, $(event.target).closest('.wsite-multicol-tr'));
    });
  });

});

function addNewPayment() {
  $('#payment-alert').hide();
  $('#response-errors').text("");

  var csrfToken = $.cookie('csrftoken');
  var formData = {
      'stripeToken': $('input[name="stripeToken"]').val()
  };

  $.ajax({
      type        : 'POST',
      traditional: true,
      beforeSend: function (request)
      {
          request.setRequestHeader("X-CSRFToken", csrfToken);
      },
      url         : 'addNewPayment',
      dataType    : 'json',
      data: formData,
      encode          : true,
      success: function(data) {
          if (data.status == 'failure') {
              $('#payment-alert').show();
              $('#response-errors').text(data.newPayment);
          } else {
              alert("New Payment Added!");
              $('#newPaymentModal').modal('hide');
              $('#new-payment-form')[0].reset();
              //addToPaymentList(data);
          }
      },
      complete: function(data) {
          //alert("complete");
      }
  });
}

function deletePayment(csrfToken, formData, section) {
    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'deletePayment', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            if (data.status == 'failure') {
                alert("Error!");
            } else {
                section.remove();
                alert("Card Deleted!");
            }
        },
        complete: function(data) {
            //alert("complete");
        }
    });
}

