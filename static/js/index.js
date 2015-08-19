window.addEventListener("DOMContentLoaded", function () {
  var serviceType = document.getElementById("type");
  serviceType.addEventListener("change", function(e) {
    var option = document.getElementById("oneHalfHours");
    if ($("#type").val() != 5) {
      option.style.display = "block";
    } else {
      option.style.display = "none";
    }
  });

  var submitBtn = document.getElementById("submitHref");
  submitBtn.addEventListener("click", function () {
    updateServiceId();
    var form = document.getElementById("serviceSearch");
    form.submit();
  });
});

function updateServiceId() {
  var e = document.getElementById("length");
  var length = e.options[e.selectedIndex].value;
  e = document.getElementById("type");
  var type = e.options[e.selectedIndex].value;
  var serviceId = document.getElementById("serviceId");
    if (type == 1) {
        if (length == 1) {
          serviceId.value = 1;
        } else if (length == 2) {
          serviceId.value = 2;
        }
    } else if (type == 2) {
      if (length == 1) {
          serviceId.value = 3;
      } else if (length == 2) {
          serviceId.value = 4;
      }
    } else if (type == 3) {
      if (length == 1) {
          serviceId.value = 5;
      } else if (length == 2) {
          serviceId.value = 6;
      }
    } else if (type == 4) {
      if (length == 1) {
          serviceId.value = 7;
      } else if (length == 2) {
          serviceId.value = 8;
      }
    } else if (type == 5) {
          serviceId.value = 9;
    } else {
          serviceId.value = 1;
    }
}
