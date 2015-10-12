var curInIndex = 0; 
var curOutIndex = 0;

function addSMS(results, isOutSMS, needUpdateIndex) {
    var mList = document.getElementById('SMSList');
    
    var index = 0;
    var children = mList.children;
    for (i = 0; i < results.length; i++) {
        while (index < children.length && (!children[index].querySelector('input[name="timestamp"]') || children[index].querySelector('input[name="timestamp"]').value > results[i].timestamp)) {
            index++;
        }
        var position = children[index];
        if (isOutSMS) {
            addToList(mList, position, results[i].receiver, results[i].first_name, results[i].last_name, results[i].timestamp, results[i].messageBody, "rightLi");
        } else {
            addToList(mList, position, results[i].sender, results[i].first_name, results[i].last_name, results[i].timestamp, results[i].messageBody, "leftLi");
        }
    }

    var csrfToken = $.cookie('csrftoken');
    // init editable
    $('[name="replyMessage"]').editable({
        url: 'send',
        title: 'Reply SMS',
        rows: 10,
        value: "",
        placement: "bottom",
        display: false,
        placeholder: "Your reply here...",
        params: function(params) {
            params.num = $(this).text();
            params.message = params.value;
            return params;
        },
        ajaxOptions: {
            dataType: 'json',
            traditional: true,
            beforeSend: function(request)
            {
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        },
        success: function(response, newValue) {
            console.log("reply success");
            console.log(response);
            var count = response['message-count'];
            toNum = "";
            for (i = 0; i < count; i++) {
                if (response.messages[i].status == 0) {
                    if (toNum != response.messages[i].to) {
                        toNum = response.messages[i].to;
                        alert("Succeeded in texting to " + toNum);
                    }
                } else {
                    alert("Failed in texting to " + response.messages[i].to + "[" + response.messages[i]['error-text'] + "]");
                }
            }
        },
        error: function(response, newValue) {
            console.log("reply error");
            if(response.status === 500) {
                return 'Service unavailable. Please try later.';
            } else {
                return response.responseText;
            }
        }
    });

    if (needUpdateIndex && results.length > 0) {
        if (isOutSMS) {
            curOutIndex = results[0].id;
        } else {
            curInIndex = results[0].id;
        }
    }
}

function addToList(list, position, phone_number, first_name, last_name, timestamp, message_body, class_name) {
    var entry = document.createElement('li');
    entry.className = class_name;
    entry.appendChild(buildPopupAnchor(phone_number));
    entry.appendChild(document.createTextNode("(" + first_name + " " + last_name + ") [" + timestamp + "]:"));
    var br = document.createElement("br");
    entry.appendChild(br);
    var p = document.createElement('p');
    p.appendChild(document.createTextNode(message_body));
    entry.appendChild(p);

    var hiddenTimestamp = document.createElement("input");
    hiddenTimestamp.setAttribute("type", "hidden");
    hiddenTimestamp.setAttribute("name", "timestamp");
    hiddenTimestamp.setAttribute("value", timestamp);
    entry.appendChild(hiddenTimestamp);
    
    list.insertBefore(entry, position);
    var div = document.createElement('div');
    div.className = "delimitDiv";
    list.insertBefore(div, position);
}

function buildPopupAnchor(text) {
    var a = document.createElement('a');
    a.href = "#";
    a.setAttribute("name", "replyMessage");
    a.setAttribute("data-type", "textarea");
    a.setAttribute("data-pk", "1");
    var linkText = document.createTextNode(text);
    a.appendChild(linkText);
    return a;
}

$(window).load(function(){
    $('#searchInList').keyup(function() {
        filterInList(this);
    });

    function filterInList(element) {
        var value = $(element).val();
        $("#SMSList > li").each(function () {
            if ($(this).text().indexOf(value) > -1) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    }
});

