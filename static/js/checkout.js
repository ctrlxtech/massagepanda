$( window ).load(function() {

  $('#payment-form').on('submit', function(event) {
    var isValid = true;
    $('#payment-form *').filter(':input[required]').each(function(){
        var value = $(this).val();
        if (!value) {
          isValid = false;
          $('#mp-checkoutAlertDanger').text('Please fill out all the fileds');
          $('#mp-checkoutAlertDanger').css('display', 'block');
        }
    });
    
    if ($('input:text[name="al1"]').val().indexOf(",") > -1) {
        isValid = false;
        $('#mp-checkoutAlertDanger').text('Please do not use \",\" in your address');
        $('#mp-checkoutAlertDanger').css('display', 'block');
    }
    
    if (isValid) {
      $('#mp-checkoutAlertDanger').css('display', 'none');
      var $form = $(this);
      if ($("#new-payment-div").css('display') == "none") {
        doCheckout($form);
      } else{
        populateExpYearAndMonth();
        // Disable the submit button to prevent repeated clicks
        $form.find('button').prop('disabled', true);
        Stripe.card.createToken($form, stripeResponseHandler);
        // Prevent the form from submitting with the default action
      }
    }
    return false;
  });

var shippingInfo = $('#panda_checkout').find('.mp-shippingInfo');
shippingInfo.popover();

var returnPolicy = $('#panda_checkout').find('.mp-returnPolicy');
returnPolicy.popover();
$('.mp-toOrder').click(function(){
    $('.mp-checkout-mobileTab').find('button.mp-toShipping').removeClass('active');
    $('.mp-checkout-mobileTab').find('button.mp-toOrder').addClass('active');
    var $sectionRight = $('#payment-form').find('.mp-checkoutSection-right');
    var $sectionLeft = $('#payment-form').find('.mp-checkoutSection-left');
    if ($sectionRight.hasClass('mp-smallScreenHide')) {
        $sectionLeft.addClass('mp-smallScreenHide');
        $sectionRight.removeClass('mp-smallScreenHide');
    };

    window.scrollTo(0, 0);
});
$('.mp-toShipping').click(function(){
    $('.mp-checkout-mobileTab').find('button.mp-toShipping').addClass('active');
    $('.mp-checkout-mobileTab').find('button.mp-toOrder').removeClass('active');
    var $sectionRight = $('#payment-form').find('.mp-checkoutSection-right');
    var $sectionLeft = $('#payment-form').find('.mp-checkoutSection-left');
    if ($sectionLeft.hasClass('mp-smallScreenHide')) {
        $sectionLeft.removeClass('mp-smallScreenHide');
        $sectionRight.addClass('mp-smallScreenHide');
    };

    window.scrollTo(0, 0);
});

var previousRd = $('.mp-checkout-shipping-address input[type="radio"]:checked');

$('input:radio[name="savedAddress"]').change(function(event){
  if (this.checked && this.value == 'new-address-selector') {
    previousRd = $(this);
    $("#new-address-div").show();
    $("#new-address-div").find('input').attr('required', true);
  } else {
    $("#new-address-div").hide();
    $("#new-address-div").find('input').attr('required', false);

    if ($('input:text[name="zipcode"]').val() != $(this).attr("zipcode")) {
        $("#addressConflictAlert").modal('show');
        if (previousRd.val()) {
          previousRd.prop("checked", true);
          if (previousRd.val() == "new-address-selector") {
            $("#new-address-div").show();
            $("#new-address-div").find('input').attr('required', true);
          }
        } else {
          this.checked = false;
        }
    } else {
        previousRd = $(this);
    }
  }
});
if ($("#new-address-div").css('display') == "none") {
    $("#new-address-div").find('input').attr('required', false);
}

$('input:radio[name="savedPayment"]').change(function(){
  if (this.checked && this.value == 'new-payment-selector') {
    $("#new-payment-div").show();
    $("#new-payment-div").find('input').attr('required', true);
  } else {
    $("#new-payment-div").hide();
    $("#new-payment-div").find('input').attr('required', false);
  }
});
if ($("#new-payment-div").css('display') == "none") {
    $("#new-payment-div").find('input').attr('required', false);
}

$('input:text[name="serviceCoupon"]').on('input', function(){
  if (this.value == '') {
    $('#apply-coupon-text').show();
    $('#apply-coupon').hide();
  } else {
	$('#apply-coupon-text').hide();
	$('#apply-coupon').show();
  }
});

$('#apply-coupon').click(function(){
  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: 'applyCoupon',
    data: {
        couponCode: $('input:text[name="serviceCoupon"]').val(),
        serviceId: $('input:hidden[name="serviceId"]').val(),
        needTable: $('input:hidden[name="needTable"]').val(),
        zipcode: $('input:text[name="zipcode"]').val()
    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        if (data.status == 'success') {
          $('#mp-coupon-panelAlert').hide()
          $('#wsite-com-checkout-payment-total-price').find('.wsite-price').text(data.newPrice)
          $('input:hidden[name="couponCode"]').val(data.couponCode)
          showCoupon(data);
        } else {
          $('#mp-coupon-panelAlert').text(data.error)
          $('#mp-coupon-panelAlert').show()
        }
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      $('input:text[name="serviceCoupon"]').val("")
      $('#apply-coupon-text').show();
      $('#apply-coupon').hide();
    }
  });
  return false;
});

$('#delete-coupon').click(function(){
  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: 'deleteCoupon',
    data: {
        serviceId: $('input:hidden[name="serviceId"]').val(),
        needTable: $('input:hidden[name="needTable"]').val(),
        zipcode: $('input:text[name="zipcode"]').val()

    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        if (data.status == 'success') {
          $('#mp-coupon-panelAlert').hide()
          $('#wsite-com-checkout-payment-total-price').find('.wsite-price').text(data.serviceFee)
          hideCoupon(data);
        } else {
          $('#mp-coupon-panelAlert').text(data.error)
          $('#mp-coupon-panelAlert').show()
        }
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      $('input:text[name="serviceCoupon"]').val("")
      $('#apply-coupon-text').show();
      $('#apply-coupon').hide();
    }
  });
  return false;
});
});

function showCoupon(data) {
  $('#wsite-applied-coupon-code').text(data.couponCode);
  $('#wsite-applied-coupon').show();
  $('#mp-coupon-input').hide();
  $('#wsite-discount-price').text(data.markDown);
  $('#wsite-discount-row').show();
}

function hideCoupon(data) {
  $('#wsite-applied-coupon').hide();
  $('#mp-coupon-input').show();
  $('#wsite-discount-row').hide();
}
