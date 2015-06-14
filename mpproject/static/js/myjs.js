$(document).ready(function () {
checkOptions();
$("select").change(checkOptions);
$("input[name=Quantity]").change(checkOptions);

function checkOptions() {
  var yesFound = false;
  $("select").each(function(index, element) {
    if ( $(element).val() == "" ) {
      yesFound = true;
    }
  });

  if ( $("input[name=Quantity]").val() == "0" ) {
      yesFound = true;
  }

  if (yesFound) {
    $("button[type=Submit]").attr("disabled","disabled");
    $("a[role=button]").css("pointer-events","none");
  } else {
    $("button[type=Submit]").removeAttr("disabled");
    $("a[role=button]").css("pointer-events", "");
  };
}
});

function emptyList(list_name) {
    var list = document.getElementById(list_name);
    var li = list.getElementsByTagName("li");
    var len = li.length;
    for (i = 0; i < len; i++) {
        list.removeChild(li[0]);
    }
}

function addToList(list_name, checkbox_id, first_name, last_name, phone_number) {
    var list = document.getElementById(list_name);
    var entry = document.createElement('li');
    addCheckBox(phone_number, entry, checkbox_id);
    entry.appendChild(document.createTextNode(first_name + " " + last_name + ", " + phone_number));
    list.appendChild(entry);
}

function addCheckBox(phone_number, list, index) {
    var input = document.createElement("input");
    input.type = "checkbox";
    input.name = "needToSend";
    input.value = phone_number;
    input.className = "checkbox" + index; // set the CSS class
    list.appendChild(input); // put it into the DOM
}

function addImage(id, list, src) {
    var img = document.createElement("img");
    img.src = src;
    img.style.width = '200px';
    img.style.height = '200px';
    list.appendChild(img); // put it into the DOM
}

