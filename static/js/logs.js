var curInIndex = 0; 
var curOutIndex = 0;
var dateToGet = new Date();
dateToGet.setDate(dateToGet.getDate() - 2);
var timestampToGet = getFormattedDate(dateToGet);

function getFormattedDate(dateObj) {
    var dd = dateObj.getDate();
    var mm = dateObj.getMonth()+1; //January is 0!

    var yyyy = dateObj.getFullYear();
    dd = addZero(dd);
    mm = addZero(mm);
    var HH = dateObj.getHours();
    HH = addZero(HH);
    var MM = dateObj.getMinutes();
    MM = addZero(MM);
    var SS = dateObj.getSeconds();
    SS = addZero(SS);
    return yyyy+"-"+mm+"-"+dd+" "+HH+":"+MM+":"+SS;
}

function addZero(value) {
    if (value < 10){
        value = "0" + value;
    }
    return value;
}

function showMore() {
    oldDate = new Date(dateToGet);
    dateToGet.setDate(dateToGet.getDate() - 2);
    getOldLogs('getOldOutLogs', getFormattedDate(dateToGet), getFormattedDate(oldDate), true);
    getOldLogs('getOldInLogs', getFormattedDate(dateToGet), getFormattedDate(oldDate), false);
    return false;
}

function getOldLogs(url, newTimestamp, oldTimestamp, isOut) {
  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: url,
    data: {
        newTimestamp: newTimestamp,
        oldTimestamp: oldTimestamp
    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        addSMS(data, isOut, false);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
    }
  });
}

(function outWorker() {
  console.log("outIndex: " + curOutIndex);
  console.log("timestamp: " + timestampToGet);
  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: 'getNewOutLogs', 
    data: {
        index: curOutIndex,
        timestamp: timestampToGet
    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        addSMS(data, true, true);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(outWorker, 10000);
    }
  });
})();

(function inWorker() {
  console.log("inIndex: " + curInIndex);
  console.log("timestamp: " + timestampToGet);
  var csrfToken = $.cookie('csrftoken');
  $.ajax({
    method: 'POST',
    url: 'getNewInLogs', 
    data: {
        index: curInIndex,
        timestamp: timestampToGet
    },
    beforeSend: function(request)
    {
        request.setRequestHeader("X-CSRFToken", csrfToken);
    },
    success: function(data) {
        addSMS(data, false, true);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(inWorker, 10000);
    }
  });
})();

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

