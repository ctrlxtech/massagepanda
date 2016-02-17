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
        addSMSTabs(data, isOut, false);
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
        addSMSTabs(data, true, true);
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
        addSMSTabs(data, false, true);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(inWorker, 10000);
    }
  });
})();
