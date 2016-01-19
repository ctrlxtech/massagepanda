$( window ).load(function() {

  $('.mp-registerForm').on('submit', function(event) {
    var isValid = true;
    $('.mp-registerForm *').filter(':input[required]').each(function(){
        var value = $(this).val();
        if (!value) {
          isValid = false;
          $('#mp-registerForm-panelAlert').text('Please fill out all the fileds');
          $('#mp-registerForm-panelAlert').css('display', 'block');
        }
    });
    if (isValid) {
      $('#mp-registerForm-panelAlert').css('display', 'none');

      var formData = $(this).serialize();
      var csrfToken = $.cookie('csrftoken');
      $.parseHTML(formData);
      $.ajax({
        type        : 'POST',
        beforeSend: function (request)
        {
          request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'createCustomer',
        data: formData,
        success: function(data) {
          if (data.status != 'success') {
             $("#mp-registerForm-panelAlert").text(data.error);
             $('#mp-registerForm-panelAlert').css('display', 'block');
          }
        },
        complete: function(data) {
          //alert("complete");
        }
      })
    }
    return false;

  });

$('#send-code').click(function(){
  if (!$('input:text[name="phone"]').val()) {
    $('#mp-registerForm-panelAlert').text('Please provide your phone number');
    $('#mp-registerForm-panelAlert').css('display', 'block');
    return false;
  }

  $('#mp-registerForm-panelAlert').css('display', 'none');
  phone = $('input:text[name="phone"]').val().replace(/\D/g,'');
  if (phone.length == 10) {
      phone = "1" + phone;
  }

  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: 'getPhoneVerifyCode',
    data: {
        phone: phone,
    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        if (data.status == '0') {
          $('#verifyRequest').val(data.request_id);
          alert("Code has been sent to your phone");
        } else {
          $('#mp-registerForm-panelAlert').text(data.error_text);
          $('#mp-registerForm-panelAlert').css('display', 'block');
        } 
        $('#send-code').text("Resend");
    },
    complete: function() {
    }
  });
  return false;
});

$('#verify-phone').click(function(){
  if (!$('input:text[name="verifyCode"]').val()) {
    $('#mp-registerForm-panelAlert').text('Please provide the verify code you just received');
    $('#mp-registerForm-panelAlert').css('display', 'block');
    return false;
  }

  $('#mp-registerForm-panelAlert').css('display', 'none');
  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: 'verifyPhone',
    data: {
        verifyRequest: $('#verifyRequest').val(),
        verifyCode: $('input:text[name="verifyCode"]').val(),
    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        console.log(data)
        if (data.status == '0') {
            $('#validationSuccess').css('display', 'inline-block');
            $('#verify-phone').css('display', 'none');
        } else {
          $('#mp-registerForm-panelAlert').text(data.error_text);
          $('#mp-registerForm-panelAlert').css('display', 'block');
        } 
    },
    complete: function() {
    }
  });
  return false;
});


});
