function constructSMS(e) {
    type = $(e).siblings('[name="service_type"]').val();
    service_datetime = $(e).siblings('[name="service_datetime"]').val();
    address = $(e).siblings('[name="sa"]').val();
    recipient = $(e).siblings('[name="recipient"]').val();
    alert("Datetime: " + service_datetime + " |Address: " + address + " |Type: " + type + " |Customer Name: " + recipient);
    return false;
}

(function worker() {
  $.ajax({
    url: '{% url 'getOrders' %}', 
    data: {index: curIndex},
    success: function(data) {
        appendOrder(data);
    },
    complete: function() {
      // Schedule the next request when the current one's complete
      setTimeout(worker, 5000);
    }
  });
})();

function appendOrder(data) {
    var results = JSON.parse(data);
    var list = document.getElementById('orderList');
    for (i = 0; i < results.length; i++) {
      addToList(list, 
          results[i].fields['name'],
          results[i].fields['phone'], results[i].fields['email'],
          results[i].fields['shipping_address']);
      curIndex += 1;
    }
}

function addToList(list, amount, name, phone, email, sa) {
    var entry = document.createElement('li');
    var f = document.createElement('form');
    f.setAttribute('method',"post");
    f.setAttribute('action',"{% url 'mcharge'%}");
    
    f.appendChild(createInput("amount", amount));
    f.appendChild(createInput("b_phone", b_phone));
    f.appendChild(createInput("b_email", b_email));
    f.appendChild(createInput("name", name));
    f.appendChild(createInput("phone", phone));
    f.appendChild(createInput("email", email));
    f.appendChild(createInput("sa", sa));
    
    var s = document.createElement("input"); //input element, Submit button
    s.setAttribute('type',"submit");
    s.setAttribute('value',"Submit");

    f.appendChild(s);
   
    list.appendChild(f);
}

function createInput(name, value) {
    var i = document.createElement("input"); //input element, text
    i.setAttribute('type',"text");
    i.setAttribute('value',value);
    i.setAttribute('name',name);
    i.setAttribute('readonly',"true");
    return i;
}
