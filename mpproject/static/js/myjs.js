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

function addToAdminList(id, first_name, last_name, phone_number, src) {
    var adminList = document.getElementById('adminList');
    var entry = document.createElement('li');
    addCheckBox(id, entry, 1);
    entry.appendChild(document.createTextNode(first_name + " " + last_name + ", " + phone_number));
//    addImage(id, adminList, src);
    adminList.appendChild(entry);
}

function addToMaleList(id, first_name, last_name, phone_number, src) {
    var mList = document.getElementById('mList');
    var entry = document.createElement('li');
    addCheckBox(id, entry, 2);
    entry.appendChild(document.createTextNode(first_name + " " + last_name + ", " + phone_number));
//    addImage(id, mList, src);
    mList.appendChild(entry);
}


function addToFemaleList(id, first_name, last_name, phone_number, src) {
    var fList = document.getElementById('fList');
    var entry = document.createElement('li');
    addCheckBox(id, entry, 3);
    entry.appendChild(document.createTextNode(first_name + " " + last_name + ", " + phone_number));
    fList.appendChild(entry);
//    addImage(id, fList, src);
}

function addCheckBox(id, list, index) {
    var input = document.createElement("input");
    input.type = "checkbox";
    input.name = "needToSend";
    input.value = id;
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

