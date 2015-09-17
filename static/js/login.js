$(document).ready(function() {
  $('#resetChangeForm').validator().on('submit', function(event) {
    if (event.isDefaultPrevented()) {
        $('#response-errors').text("Correct the inputs");
        $('#response-errors').show();
        return;
    }
    $('#response-errors').hide();
    $('#response-errors').text("");
    // get the form data
    // there are many ways to get this data using jQuery (you can use the class or id also)
    var csrfToken = $.cookie('csrftoken');

    var formData = {
        'email'               : $('#email').val(),
    };

    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'resetPassword', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            if (data.status == 'failure') {
                $('#response-errors').show();
                $('#response-errors').text(data.error);
            } else {
                alert(data.message);
                $('#myModal').modal('hide');
            }
            $('#resetChangeForm')[0].reset();
        },
        complete: function(data) {
            //alert(data);
        }
    });
    // stop the form from submitting the normal way and refreshing the page
    event.preventDefault();
  });
});
