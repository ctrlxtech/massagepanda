$(document).ready(function() {

  // process the form
  $('#passwordChangeForm').validator().on('submit', function(event) {
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
            $('#passwordChangeForm')[0].reset();
        },
        complete: function(data) {
            //alert("complete");
        }
    });
    // stop the form from submitting the normal way and refreshing the page
    event.preventDefault();
  });

  $('#addressForm').validator().on('submit', function(event) {
    if (event.isDefaultPrevented()) {
        $('#address-response-errors').text("Correct the inputs");
        $('#address-response-errors').show();
        return;
    }

    event.preventDefault();
    $('#address-response-errors').hide();
    $('#address-response-errors').text("");
    // get the form data
    // there are many ways to get this data using jQuery (you can use the class or id also)
    var csrfToken = $.cookie('csrftoken');

    var formData = {};
    var serverFieldList = $(this).find('input[type=text], input[type=email]');
    for (var i = 0; i < serverFieldList.length; i++) {
        var $serverField = $(serverFieldList[i]);
        var fieldKey = $serverField.attr('id');
        var fieldValue = $serverField.val();
        formData[fieldKey] = fieldValue;
    }

    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'addNewAddress', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            if (data.status == 'failure') {
                $('#address-response-errors').show();
                $('#address-response-errors').text(data.error);
            } else {
                alert("New Address Added!");
                $('#addressModal').modal('hide');
                $('#addressForm')[0].reset();
                addToAddressList(data);
            }
        },
        complete: function(data) {
            //alert("complete");
        }
    });
  });

  $('#address-section').on('click', 'a[name="editAddressBtn"]', function(event) {
    event.preventDefault();
    $('#addressModal').modal();
  });

  $('#address-section').on('click', 'a[name="deleteAddressBtn"]', function(event) {
    event.preventDefault();
    var csrfToken = $.cookie('csrftoken');

    var formData = {
        'addressId': $(event.target).closest('.edit-div').find('input[name="addressId"]').val(),
    };

    $('#confirm').modal({ backdrop: 'static'})
        .one('click', '#delete', function() {
            deleteAddress(csrfToken, formData, $(event.target).closest('.address-desc'));
    });
  });
  $('#address-section').on('click', 'a[name="setDefaultBtn"]', function(event) {
    event.preventDefault();
    var csrfToken = $.cookie('csrftoken');

    var formData = {
        'addressId': $(event.target).closest('.edit-div').find('input[name="addressId"]').val(),
    };

    setDefaultAddress(csrfToken, formData, $(event.target).closest('.edit-div'));
  });

});

function deleteAddress(csrfToken, formData, section) {
    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'deleteAddress', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            if (data.status == 'failure') {
                alert("Error!");
            } else {
                section.remove();
                alert("Address Deleted!");
            }
        },
        complete: function(data) {
            //alert("complete");
        }
    });
}

function setDefaultAddress(csrfToken, formData, thisDiv) {
    $.ajax({
        type        : 'POST', // define the type of HTTP verb we want to use (POST for our form)
        traditional: true,
        beforeSend: function (request)
        {
            request.setRequestHeader("X-CSRFToken", csrfToken);
        },
        url         : 'setDefaultAddress', // the url where we want to POST
        dataType    : 'json', // what type of data do we expect back from the server
        data: formData,
        encode          : true,
        // using the done promise callback
        success: function(data) {
            if (data.status == 'success') {
                alert("Address set as default!");
                $('span[name="defaultIndicator"]').hide();
                $('a[name="setDefaultBtn"]').show();
                thisDiv.find('span[name="defaultIndicator"]').show();
                thisDiv.find('a[name="setDefaultBtn"]').hide();
            } else {
                alert("Error!");
            }
        },
        error: function(data) {
            alert("Error!");
        }
    });
}

function addToAddressList(data) {
var addressDesc = $('<div></div>').addClass('border address-desc');

addressDesc.append(createDefaultIndicator());
addressDesc.append(createAddressDetail(data));
addressDesc.append(createEditPanel(data.addressId));
addressDesc.append(createDelimiterSection());
$('#address-section').append(addressDesc);
}

function createDelimiterSection() {
var styledHr = $('<hr></hr>').addClass('styled-hr');
var delimiterSec = $('<div></div>');
delimiterSec.append($('<div></div>').addClass('delimiter'));
delimiterSec.append(styledHr);
delimiterSec.append($('<div></div>').addClass('delimiter'));

return delimiterSec;
}

function createDefaultIndicator() {
var indicator = $('<span></span>').attr('name', defaultIndicator).text("Default Address");
indicator.hide();
return indicator;
}

function createAddressDetail(address) {
var detail = $('<div></div>').addClass('address-detail');
detail.text(address.name + ", " + address.address_line1 + " " + address.address_line2 + ", " + address.city + " " + address.state + " " + address.zipcode);
return detail;
}

function createEditPanel(addressId) {
var editDiv = $('<div></div>').addClass('edit-div');
editDiv.append($('<a></a>').attr("name", "setDefaultBtn").text('Set as default'));
editDiv.append($('<a></a>').addClass('delete-link').attr("name", "deleteAddressBtn").text('Delete'));
var inputId = $('<input></input>').attr({
    type: 'hidden',
    value: addressId,
    name: 'addressId'
});
editDiv.append(inputId);
return editDiv;
}
