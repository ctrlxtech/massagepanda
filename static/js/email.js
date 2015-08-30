function resizeIframe(obj) {
  obj.style.height = obj.contentWindow.document.body.scrollHeight + 'px';
}

function updateEmail() {
  $('#to').val($('#order option:selected').attr("email"));
}

$(document).ready(function() {

  // process the form
  $('#feedbackEmailForm').submit(function(event) {
    document.getElementById("myDiv").innerHTML = "";
    // get the form data
    // there are many ways to get this data using jQuery (you can use the class or id also)
    var csrfToken = $.cookie('csrftoken');
    var orderIds = new Array();
    $('input[name=orderId]:checked').each(function() {
      orderIds.push($(this).val())
    });

    var formData = {
        'orderIds'               : orderIds,
    };
    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'sendFeedbackEmails', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            document.getElementById("myDiv").innerHTML+=data.responseText + "<br>";
        },
        complete: function(data) {
            //alert("complete");
            document.getElementById("myDiv").innerHTML+=data.responseText + "<br>";
        }
    });
    // stop the form from submitting the normal way and refreshing the page
    event.preventDefault();
  });

  $('#order').change(function() {
    updateEmail();
  });
  
  updateEmail();

  $('#select-all-orders').click(function(event) {  //on click
      if(this.checked) { // check select status
          $('.orderCheckbox').each(function() { //loop through each checkbox
              this.checked = true;  //select all checkboxes with class "checkbox1"
          });
      }else{
          $('.orderCheckbox').each(function() { //loop through each checkbox
              this.checked = false; //deselect all checkboxes with class "checkbox1"
          });
      }
  });
});

