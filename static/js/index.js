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

  var searchService = document.getElementById("searchService");
  searchService.addEventListener("click", function () {
    this.href = "https://" + {{ request.get_host }} + "/store/"
    updateHref(this);
  });
});

function updateHref(anchor) {
  var e = document.getElementById("length");
  var length = e.options[e.selectedIndex].value;
  e = document.getElementById("type");
  var type = e.options[e.selectedIndex].value;
  var serviceId = document.getElementById("serviceId");
    if (type == 1) {
        if (length == 1) {
          anchor.href += "In-Home_Swedish_Massage_for_1_Hour";
        } else if (length == 2) {
          anchor.href += "In-Home_Swedish_Massage_for_1.5_Hours";
        }
    } else if (type == 2) {
      if (length == 1) {
          anchor.href += "In-Home_Deep_Tissue_Massage_for_1_Hour";
      } else if (length == 2) {
          anchor.href += "In-Home_Deep_Tissue_Massage_for_1.5_Hours";
      }
    } else if (type == 3) {
      if (length == 1) {
          anchor.href += "In-Home_Couples_Massage_for_1_Hour";
      } else if (length == 2) {
          anchor.href += "In-Home_Couples_Massage_for_1.5_Hours";
      }
    } else if (type == 4) {
      if (length == 1) {
          anchor.href += "In-Home_Sports_Massage_for_1_Hour";
      } else if (length == 2) {
          anchor.href += "In-Home_Sports_Massage_for_1.5_Hours";
      }
    } else if (type == 5) {
          anchor.href += "In-Home_Shiatsu_Massage_for_1_Hour";
    } else {
          anchor.href += "In-Home_Swedish_Massage_for_1_Hour";
    }
}
function updateServiceId() {
  var e = document.getElementById("length");
  var length = e.options[e.selectedIndex].value;
  e = document.getElementById("type");
  var type = e.options[e.selectedIndex].value;
  var serviceId = document.getElementById("serviceId");
    if (type == 1) {
        if (length == 1) {
          serviceId.value = "3849f7d6591511e595db0208bb76cfe3";
        } else if (length == 2) {
          serviceId.value = "c6401a16591511e595db0208bb76cfe3";
        }
    } else if (type == 2) {
      if (length == 1) {
          serviceId.value = "d0b2f518591511e595db0208bb76cfe3";
      } else if (length == 2) {
          serviceId.value = "d8702762591511e595db0208bb76cfe3";
      }
    } else if (type == 3) {
      if (length == 1) {
          serviceId.value = "ffe89482591511e595db0208bb76cfe3";
      } else if (length == 2) {
          serviceId.value = "062691c8591611e595db0208bb76cfe3";
      }
    } else if (type == 4) {
      if (length == 1) {
          serviceId.value = "19e44bce591611e595db0208bb76cfe3";
      } else if (length == 2) {
          serviceId.value = "1f9aa66c591611e595db0208bb76cfe3";
      }
    } else if (type == 5) {
          serviceId.value = "297b2a1c591611e595db0208bb76cfe3";
    } else {
          serviceId.value = "3849f7d6591511e595db0208bb76cfe3";
    }
}
