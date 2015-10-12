$(window).load(function(){
    number = $('#number').val();
    outWorker(number);
    inWorker(number);
});

function outWorker(number) {
  var csrfToken = $.cookie('csrftoken');
  console.log("number: " + number);
  $.ajax({
    method: 'POST',
    url: 'getOutLogsByNum',
    data: {
        number: number,
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
    }
  });
}

function inWorker(number) {
  var csrfToken = $.cookie('csrftoken');
  console.log("number: " + number);
  $.ajax({
    method: 'POST',
    url: 'getInLogsByNum',
    data: {
        number: number,
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
    }
  });
}
