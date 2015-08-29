$(document).ready(function() {

$('#myModal').on('hidden.bs.modal', function (e) {
    $('#response-errors').hide();
    $('#response-errors').text("");

  $(this)
    .find("input,textarea,select")
       .val('')
       .end()
    .find("input[type=checkbox], input[type=radio]")
       .prop("checked", "")
       .end();
})

  // process the form
  $('#passwordChangeForm').submit(function(event) {
    $('#response-errors').hide();
    $('#response-errors').text("");
    // get the form data
    // there are many ways to get this data using jQuery (you can use the class or id also)
    var csrfToken = $.cookie('csrftoken');

    var formData = {
        'oldPassword'               : $('#oldPassword').val(),
        'newPassword'               : $('#newPassword').val()
    };
    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'changePassword', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            if (data.status == 'failure') {
                $('#response-errors').show();
                $('#response-errors').text(data.error);
            } else {
                alert("Password Changed!");
                $('#myModal').modal('hide');
            }
        },
        complete: function(data) {
            //alert("complete");
        }
    });
    // stop the form from submitting the normal way and refreshing the page
    event.preventDefault();
  });
});
