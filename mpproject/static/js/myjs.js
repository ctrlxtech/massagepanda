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
