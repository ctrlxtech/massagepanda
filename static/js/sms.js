$(document).ready(function() {
    $('#selectall1').click(function(event) {  //on click
        if(this.checked) { // check select status
            $('.checkbox1').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"              
            });
        }else{
            $('.checkbox1').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                      
            });        
        }
    });
    $('#selectall2').click(function(event) {  //on click
        if(this.checked) { // check select status
            $('.checkbox2').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"              
            });
        }else{
            $('.checkbox2').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                      
            });        
        }
    }); 
    $('#selectall3').click(function(event) {  //on click
        if(this.checked) { // check select status
            $('.checkbox3').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"              
            });
        }else{
            $('.checkbox3').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                      
            });        
        }
    });

    $('#selectall4').click(function(event) {  //on click
        if(this.checked) { // check select status
            $('.checkbox4').each(function() { //loop through each checkbox
                this.checked = true;  //select all checkboxes with class "checkbox1"              
            });
        }else{
            $('.checkbox4').each(function() { //loop through each checkbox
                this.checked = false; //deselect all checkboxes with class "checkbox1"                      
            });        
        }
    });

 // process the form
    $('#SMSForm').submit(function(event) {
        $('#send').prop('disabled', true);
        document.getElementById("myDiv").innerHTML = "";
        // get the form data
        // there are many ways to get this data using jQuery (you can use the class or id also)
        var nums = new Array();
        $('input[name=needToSend]:checked').each(function() { nums.push($(this).val()) });
        var formData = {
            'needToSend'        : nums,
            'num'               : $('input[name=num]').val(),
            'message'          : $('textarea[name=message]').val(),
        };
        var csrftoken = getCookie('csrftoken'); 
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            traditional: true,
            beforeSend: function (request)
            {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url         : 'send', // the url where we want to POST
            dataType    : 'json', // what type of data do we expect back from the server
            data: formData,
            encode          : true,
            // using the done promise callback
            success: function(data) {
                var count = data['message-count'];
                for (i = 0; i < count; i++) {
                    if (data.messages[i].status == 0) {
                        document.getElementById("myDiv").innerHTML+="Succeeded in texting to " + data.messages[i].to + "<br>";
                    } else {
                        document.getElementById("myDiv").innerHTML+="Failed in texting to " + data.messages[i].to + "[" + data.messages[i]['error-text'] + "]<br>";
                    }
                }
            },
            complete: function(data) {
                //alert("complete");
                document.getElementById("myDiv").innerHTML+=data.responseText + "<br>";
                $('#send').prop('disabled', false);
            }
        });
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });

    $('#getcontactlistform').submit(function(event) {
        emptyList("queryList");
        var gender = new Array();
        $('input[name=gender]:checked').each(function() { gender.push($(this).val()) });
        var formData = {
            'gender'              : gender,
            'areacode'               : $('select[name=areacode]').val(),
        };
        var csrftoken = getCookie('csrftoken'); 
        $.ajax({
            type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
            traditional: true,
            beforeSend: function (request)
            {
                request.setRequestHeader("X-CSRFToken", csrftoken);
            },
            url         : 'getContactList', // the url where we want to POST
            dataType    : 'json', // what type of data do we expect back from the server
            data: formData,
            encode          : true,
            // using the done promise callback
            success: function(data) {
                for (i = 0; i < data.length; i++) {
                    addToList("queryList", 4, data[i].fields.first_name, data[i].fields.last_name, data[i].fields.phone_number)
                }
            }
        });
        // stop the form from submitting the normal way and refreshing the page
        event.preventDefault();
    });
});

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

