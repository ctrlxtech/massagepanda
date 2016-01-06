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
    } else {
      return false;
    }
  });

});
