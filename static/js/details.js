window.addEventListener("DOMContentLoaded", function () {

  $('#datepicker').val('');
  $('#timepicker').val('');
  $('#genderPreferred').val('');
  $('#massage1').val('');
  $('#massage2').val('');

  $(function() {
    $("#datepicker").datepicker({
      minDate: new Date(),

      onSelect: function(dateText, inst) {
        massageDetailsTimeForList();
      }
    });
  });
  setupTimeDropdown($("#massageDetails_timeList"));
  var genderPreferredList = $('#massageDetails_genderPreferredList');
  genderPreferredList.on("click", "a", genderSelection);
  var massage1List = $('#massageDetails_massage1List');
  massage1List.on("click", "a", processSelection);
  var massage2List = $('#massageDetails_massage2List');
  massage2List.on("click", "a", processSelection);

$('#zipcode').keydown(function(e) {
    date = $(this).val();
    if ((e.keyCode >= 65 && e.keyCode <= 90) || (e.keyCode >= 106 && e.keyCode <= 111) || (e.keyCode >= 186 && e.keyCode <= 222)) {
      e.preventDefault();
      return;
    }
    date = $(this).val();
    if (date.length == 5 && ((e.keyCode >= 48 && e.keyCode <= 57) || (e.keyCode >= 96 && e.keyCode <= 105))) {
      e.preventDefault();
      return;
    }
});

});

//private function
function genderSelection(e){
    var value = $(this).text();
    var gender = 0;
    switch(value) {
        case "Either":
            gender = 0;
            break;
        case "Female Preferred":
            gender = 1;
            break;
        case "Male Preferred":
            gender = 2;
            break;
        default:
            break;
    }
            
    $('#genderPreferred').val(gender);
    console.log($('#genderPreferred').val());
    var $parentDiv = $(this).closest('div.mp-massageDetails-input');
    $parentDiv.find('button').html(value + '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true">');
    e.preventDefault();
};

//private function
function processSelection(e){
    var value = $(this).text();
    var $parentDiv = $(this).closest('div.mp-massageDetails-input');
    $parentDiv.find('input').val(value);
    console.log($parentDiv.find('input').val());
    $parentDiv.find('button').html(value + '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true">');
    e.preventDefault();
};

var pandaUtil = {
        getParameterByName: function(name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),

                results = regex.exec(location.search);
            return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        },
        getDateString: function(dateObj) {
            var dd = dateObj.getDate();
            var mm = dateObj.getMonth() + 1; //January is 0!
            var yyyy = dateObj.getFullYear();
            if (dd < 10) {
                dd = '0' + dd
            }
            if (mm < 10) {
                mm = '0' + mm
            }
            var dateString = mm + '/' + dd + '/' + yyyy;
            return dateString;
        }
    }
    
var timeArray = ['9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am', '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm', '3:00pm', '3:30pm', '4:00pm', '4:30pm', '5:00pm', '5:30pm', '6:00pm', '6:30pm', '7:00pm', '7:30pm', '8:00pm', '8:30pm', '9:00pm', '9:30pm', '10:00pm'];

    //private function
function setupTimeDropdown($timeList) {
    $timeList.empty();
    for (var i = 0; i < 27; i++) {
        var time = timeArray[i];
        var timeTempString = '<li class="mp-item"><a>' + time + '</a></li><li class="divider"></li>';
        $timeList.append(timeTempString);
    }
    $timeList.append('<li class="mp-item noServiceAvaliable" style="display:none"><a>Sorry, we are closed..</a></li>');
    $timeList.on("click", "a", processSelection);
};

function massageDetailsTimeForList() {
    var page = $("#panda_massageDetails");
    var time = page.find('button.massageDetailsTime');
    var $parentInputDiv = time.closest('.mp-massageDetails-input');
    var $massageDetailsForm = time.closest('.mp-massageDetails-form');
    var $timeList = $parentInputDiv.find('#massageDetails_timeList');
    if ($parentInputDiv.hasClass('open')) {
        $timeList.find('li').removeClass('timeListHide');
        $timeList.find('li.noServiceAvaliable').hide();
    } else {
        var date = $massageDetailsForm.find('input[name="massageDetailsDate"]').val();

        var today = new Date();
        var todayDateString = pandaUtil.getDateString(today);
        if (todayDateString === date) {
            var currentHours = today.getHours();
            var currentMins = today.getMinutes();
            currentMins = Math.ceil(currentMins / 30) * 30;
            if (currentMins === 60) {
                currentMins = '00';
                currentHours = currentHours + 1;
            }
            //special case if over 10pm,then no service
            if (currentHours >= 22) {
                $timeList.find('li').not('.noServiceAvaliable').addClass('timeListHide');
                $timeList.find('li.noServiceAvaliable').show();
                $('input[type=submit]').prop('disabled', true);
                $('#timepicker').val("");
                return;
            }
            var currentSuffix = (currentHours >= 12) ? 'pm' : 'am';
            currentHours = ((currentHours + 11) % 12 + 1);
            var currentTimeString = currentHours + ':' + currentMins + currentSuffix;
            if (timeArray.indexOf(currentTimeString) > -1) {
                var timeStringIndex = timeArray.indexOf(currentTimeString) * 2;
                $timeList.find('li:lt(' + timeStringIndex + ')').addClass('timeListHide');
            }
        } else {
            $('input[type=submit]').prop('disabled', false);
            $timeList.find('li').removeClass('timeListHide');
            $timeList.find('li.noServiceAvaliable').hide();
        }
    }
}

function validate() { 
  var $massageDetailsForm = $('#mp-massageDetails-form');
  var date = $('#datepicker').val();
  var time = $('#timepicker').val();
  var gender = $('#genderPreferred').val();
  var zipcode = $('#zipcode').val();
  var $panelAlert = $('#mp-massageDetails-panelAlert');
  $panelAlert.css('display', 'none');
  if (!date) {
      $panelAlert.text('Please select date !');
      $panelAlert.css('display', 'block');
      return false;
  };
  if (!time) {
      $panelAlert.text('Please select time !');
      $panelAlert.css('display', 'block');
      return false;
  };
  if (!gender) {
      $panelAlert.text('Please select you preferred gender !');
      $panelAlert.css('display', 'block');
      return false;
  };
  if (!zipcode || (zipcode.length != 5)) {
      $panelAlert.text('Please provide your correct zipcode!');
      $panelAlert.css('display', 'block');
      return false;
  };
}
