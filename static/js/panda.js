var pandaBrowser = {
    mobile: function(){
        if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) 
            return true;
        else 
            return false;
    },
    apple: function(){
        if (/iPhone|iPad|iPod/i.test(navigator.userAgent)) 
            return true;
        else 
            return false;
    },
    android: function(){
        if (/Android/i.test(navigator.userAgent)) {
            //check android is on mobile or tablet.
            var userAgentString = navigator.userAgent.toLowerCase();
            if ((userAgentString.search("android") > -1) && (userAgentString.search("mobile") > -1)) 
                return true;
            else 
                return false;
        }
        else 
            return false;
    },
    phone: function(){
        if (/iPhone|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) 
            return true;
        else 
            if (/Android/i.test(navigator.userAgent)) {
                //check android is on mobile or tablet.
                var userAgentString = navigator.userAgent.toLowerCase();
                if ((userAgentString.search("android") > -1) && (userAgentString.search("mobile") > -1)) 
                    return true;
                else 
                    return false;
            }
            else 
                return false;
    }
    
}

var pandaAjax = {
    fail: function(jqXHR, textStatus, errorThrown){
        console.log("Sorry, Error Occur !");
    },
    get: function(url, param, callback, $header, returnDataType){
        if (!returnDataType) 
            returnDataType = 'text';
        //callback is only use for easy request, for example load html
        var jqxhr = $.get(url, param, undefined, returnDataType);
        jqxhr.done(function(data){
            if (typeof(callback) === 'function') 
                callback(data);
        });
        jqxhr.fail(function(jqXHR, textStatus){
            pandaAjax.fail(jqXHR, textStatus);
        });
        
    },
    post: function(url, param, callback, $header, returnDataType, sendDataType){
        if (!returnDataType) 
            returnDataType = 'json';
        if (!sendDataType) 
            sendDataType = 'application/json; charset=UTF-8';
        var csrfToken = $.cookie('csrftoken');
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(param),
            contentType: sendDataType,
            dataType: returnDataType,
            beforeSend: function(request){
                request.setRequestHeader("X-CSRFToken", csrfToken);
            }
        }).done(function(data){
            if (typeof(callback) === 'function') 
                callback(data);
            
        }).fail(function(jqXHR, textStatus){
            pandaAjax.fail(jqXHR, textStatus);
        });
    }
};

var pandaHelpCenterPage = (function(){
    var publicObj = {
        afterResponse: function(pageId){
            $('#panda_helpCenter').find('a.mp-hrefBlock').click(function(e){
                e.preventDefault();
            });
        }
    };
    return publicObj;
}());

var pandaRegisterPage = (function(){
	 function afterSubmit(data){
        var returnObj = data;
        var $form =  $('#panda_register').find('.mp-registerForm');
        $form.find('input').val('');
		$('#panda_register').find('#mp-registerForm-panelAlert').hide();
		//check login is success or not
		if(returnObj.status = 'success')
		{
			//register success
			var firstName = returnObj.firstName;		
			var $navigation = $('#mp-navbar').find('.mp-navigation>ul');
			var navDropdown = $navigation.children('li.dropdown');
			navDropdown.children('a.dropdown-toggle').html(firstName+'<span class="caret"></span>');
			$navigation.children('li.mp-loginHeader').hide();
			navDropdown.show();
			$('#mp-rightSideNav').find('.mp-mobileLoginfalse').hide();
			$('#mp-rightSideNav').find('.mp-mobileLoginTrue').show();
			$('#mp-rightSideNav').find('.mp-mobileLoginName').text(firstName);
			//go to home page
			localStorage.setItem("pandaLogin", 'true');
			localStorage.setItem("pandaLoginName", firstName);
			 $('#panda_login').find('.mp-loginSuccess').click();
		}
		else{
			//register fail
			var $panelAlert = $('#panda_register').find('#mp-registerForm-panelAlert');
			$panelAlert.text(returnObj.errorMsg);
			$panelAlert.show();
		}
    };
	
    var publicObj = {
        afterResponse: function(pageId){
               $('#panda_register').find('.mp-registerForm').on('submit', function(e){
                var $form = $(this);
             	var serverObj = {};
		        var $serverFieldList = $form.find('input[data-serverField="true"]');
		        for (var i = 0; i < $serverFieldList.length; i++) {
		            var $serverField = $($serverFieldList[i]);
		            var fieldKey = $serverField.attr('name');
		            var fieldValue = $serverField.val();
		            serverObj[fieldKey] = fieldValue;
		        }
				var gender = $('#panda_register').find('input[name="registerGender"]:checked').val();
		        serverObj['registerGender']=gender;
				//TODO need use server side path for panda register!!!
		        var url = '/manager/createCustomerFromJson';
    	        pandaAjax.post(url, serverObj, afterSubmit);
				event.preventDefault()
            });
        }
    };
    return publicObj;
}());

var pandaLoginPage = (function(){
	 function afterSubmit(data){
        var returnObj = data;
        var $form =  $('#panda_login').find('.mp-loginForm');
        $form.find('input').val('');
		$('#panda_login').find('#mp-loginForm-panelAlert').hide();
		//check login is success or not
		if(returnObj.status == 'success')
		{
			//login success
			var firstName = returnObj.firstName;		
			var $navigation = $('#mp-navbar').find('.mp-navigation>ul');
			var navDropdown = $navigation.children('li.dropdown');
			navDropdown.children('a.dropdown-toggle').html(firstName+'<span class="caret"></span>');
			$navigation.children('li.mp-loginHeader').hide();
			navDropdown.show();
			$('#mp-rightSideNav').find('.mp-mobileLoginfalse').hide();
			$('#mp-rightSideNav').find('.mp-mobileLoginTrue').show();
			$('#mp-rightSideNav').find('.mp-mobileLoginName').text(firstName);
			//go to home page
			localStorage.setItem("pandaLogin", 'true');
			localStorage.setItem("pandaLoginName", firstName);
			 $('#panda_login').find('.mp-loginSuccess').click();
		}
		else{
			//login fail
			$('#panda_login').find('#mp-loginForm-panelAlert').show();
		}
    };
	
    var publicObj = {
        afterResponse: function(pageId){
               $('#panda_login').find('.mp-loginForm').on('submit', function(e){
                var $form = $(this);
             	var serverObj = {};
		        var $serverFieldList = $form.find('input[data-serverField="true"]');
		        for (var i = 0; i < $serverFieldList.length; i++) {
		            var $serverField = $($serverFieldList[i]);
		            var fieldKey = $serverField.attr('name');
		            var fieldValue = $serverField.val();
		            serverObj[fieldKey] = fieldValue;
		        }
		        //TODO need use server side path for panda Login!!!
		        var url = '/manager/userLogin';				
		        pandaAjax.post(url, serverObj, afterSubmit);
				event.preventDefault()
            });
        }
    };
    return publicObj;
}());

var pandaLogoutPage = (function(){
	 var publicObj = {
        beforeShow: function(parent){
            var $this = $(this);
            var $parent = $(parent);
			var $navigation = $('#mp-navbar').find('.mp-navigation>ul');
			var navDropdown = $navigation.children('li.dropdown');
			navDropdown.children('a.dropdown-toggle').empty();
			navDropdown.hide();
			$navigation.children('li.mp-loginHeader').show();
			$('#mp-rightSideNav').find('.mp-mobileLoginfalse').show();
			$('#mp-rightSideNav').find('.mp-mobileLoginTrue').hide();
			$('#mp-rightSideNav').find('.mp-mobileLoginName').text('');
			//go to home page
			localStorage.setItem("pandaLogin", 'false');
			localStorage.setItem("pandaLoginName", '');
        }
    };
    return publicObj;
}());

var pandaContactUsPage = (function(){
	 function afterSubmit(data){
        //sever return obj: example : {status : true}
        var returnObj = data;
        var $form =  $('#panda_contactUs').find('.mp-contactUsForm');
        $form.find('input').val('');
		 $form.find('textarea').val('');
    };
	
    var publicObj = {
        afterResponse: function(pageId){
               $('#panda_contactUs').find('.mp-contactUsForm').on('submit', function(e){
                var $form = $(this);
             	var serverObj = {};
		        var $serverFieldList = $form.find('input[data-serverField="true"]');
		        for (var i = 0; i < $serverFieldList.length; i++) {
		            var $serverField = $($serverFieldList[i]);
		            var fieldKey = $serverField.attr('name');
		            var fieldValue = $serverField.val();
		            serverObj[fieldKey] = fieldValue;
		        }
		        //TODO need use server side path for panda contactUS!!!
		        var url = '';
		        pandaAjax.post(url, serverObj, afterSubmit);
				event.preventDefault()
            });
        }
    };
    return publicObj;
}());

var pandaUtil = {
	getParameterByName : function (name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
        results = regex.exec(location.search);
     return results === null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
   },
   getDateString : function(dateObj){            	
				var dd = dateObj.getDate();
				var mm = dateObj.getMonth()+1; //January is 0!
				var yyyy = dateObj.getFullYear();				
				if(dd<10) {
				    dd='0'+dd
				} 				
				if(mm<10) {
				    mm='0'+mm
				} 
				var dateString = mm+'/'+dd+'/'+yyyy;
			return	dateString;
   }
}

var checkoutPage = (function(){
    //private function
    function afterSubmit(data){
        //sever return obj: example : {status : true}
        var returnObj = data;
        var $form = $('#payment-form');
        $form.find('button').prop('disabled', false);
        if (returnObj.status == 'success') {
            //request success !
            $form.find('input').val('');
            var $summary = $('#payment-form').find('div.mp-checkout-summary');
            $summary.find('li').text('');
            $summary.find('span.mp-summary-amount').text('');
            $('#panda_checkout').find('.mp-checkoutSuccess').click();
        }
        else {
            //request fail!
            var errorMsg = returnObj.errorMsg;
            var $pamentError = $form.find('.payment-errors');
            $form.find('.mp-checkoutAlertDanger').css('display', 'block');
            $pamentError.text(errorMsg);
        }
    };
    
    //private function
    function submitForm($form){
        var serverObj = {};
        var $serverFieldList = $form.find('[data-serverField="true"]');
        for (var i = 0; i < $serverFieldList.length; i++) {
            var $serverField = $($serverFieldList[i]);
            var fieldKey = $serverField.attr('name');
            var fieldValue = $serverField.val();
            serverObj[fieldKey] = fieldValue;
        }
        if (!serverObj['service_id']) {
            serverObj['service_id'] = 1;
        }

        //TODO need use server side path !!!
        var url = '/manager/placeOrder';
        pandaAjax.post(url, serverObj, afterSubmit);
    };
    
    //private function
    function stripeResponseHandler(status, response){
        var $form = $('#payment-form');
        if (response.error) {
            // Show the errors on the form
            var $pamentError = $form.find('.payment-errors');
            $form.find('.mp-checkoutAlertDanger').css('display', 'block');
            $pamentError.text(response.error.message);
            $form.find('button').prop('disabled', false);
        }
        else {
            // token contains id, last4, and card type
            var token = response.id;
            // Insert the token into the form so it gets submitted to the server
            $form.find('input[name="stripeToken"]').val(token);
            // and re-submit
            submitForm($form);
        }
    };
    
    function useBilling(){
        var $paymentForm = $('#payment-form');
        var b_name = $paymentForm.find('input[name="name"]').val();
        $paymentForm.find('input[name="full-name"]').val(b_name);
        
        var b_al1 = $paymentForm.find('input[name="address-line1"]').val();
        $paymentForm.find('input[name="al1"]').val(b_al1);
        
        var b_al2 = $paymentForm.find('input[name="address-line2"]').val();
        $paymentForm.find('input[name="al2"]').val(b_al2);
        
        var b_city = $paymentForm.find('input[name="address-city"]').val();
        $paymentForm.find('input[name="city"]').val(b_city);
        
        var b_state = $paymentForm.find('input[name="address-state"]').val();
        $paymentForm.find('input[name="state"]').val(b_state);
        
        var b_zip = $paymentForm.find('input[name="address-zip"]').val();
        $paymentForm.find('input[name="zipcode"]').val(b_zip);
    };
    
    function massageDetailPageAsParent($this, $parent){
        var $massageDetailsPanel = $parent.closest('.mp-massageDetails-panel');
        var title = $massageDetailsPanel.find('div.mp-massageDetails-title').text();
        var date = $massageDetailsPanel.find('input[name="massageDetailsDate"]').val();
        var time = $massageDetailsPanel.find('input[name="massageDetailsTime"]').val();
        var gender = $massageDetailsPanel.find('input[name="genderPreferred"]').val();
		var $needTable = $massageDetailsPanel.find('input[name="needTable"]');
		var parkingInfo = $massageDetailsPanel.find('textarea[name="parkingInfo"]').val();
      //  var coupon = $massageDetailsPanel.find('input[name="coupon"]').val();
        var feeType = $massageDetailsPanel.find('input[name="detailsFeeType"]').val();
        var amount = parseInt($massageDetailsPanel.find('input[name="detailsAmount"]').val());
        var totalAmount = amount;
        //setup hidden form
        var $pamentForm = $('#payment-form');
        $pamentForm.find('input[name="amount"]').val(totalAmount);
        $pamentForm.find('input[name="feeType"]').val(feeType);
        $pamentForm.find('input[name="serviceDate"]').val(date);
        $pamentForm.find('input[name="serviceTime"]').val(time);
        $pamentForm.find('input[name="serviceGenderPreferred"]').val(gender);
		$pamentForm.find('textarea[name="serviceParkingInfo"]').val(parkingInfo);
		var referCode = localStorage.getItem("referCode");
		if(referCode)
		{
		   $pamentForm.find('input[name="referCode"]').val(referCode);	
		};
			
		if ($needTable.is(":checked"))
		{
             $pamentForm.find('input[name="serviceNeedTable"]').val('yes');
	    }
		else
		{
			$pamentForm.find('input[name="serviceNeedTable"]').val('no');
		};
       // $pamentForm.find('input[name="serviceCoupon"]').val(coupon);
        $pamentForm.find('button').prop('disabled', false);
        $pamentForm.find('button').removeClass('disabled');
        $pamentForm.find('div.alert-danger').css('display', 'none');
        $pamentForm.find('span.checkoutAlertDanger').text('');
        //setup summary
        var $summary = $this.find('div.mp-checkout-summary');
        $summary.find('span.mp-summary-amount').text('(Subtotal : $' + totalAmount + ')');
        var liListString = '<li class="list-group-item  mp-summary-title"></li>' +
        '<li class="list-group-item  mp-summary-quantity"></li>' +
        '<li class="list-group-item  mp-summary-date"></li>' +
        '<li class="list-group-item  mp-summary-time"></li>' +
        '<li class="list-group-item  mp-summary-genderPrefer"></li>' ;
       // '<li class="list-group-item  mp-summary-coupon"></li>';
        $summary.find('ul').html(liListString);
        var $liList = $summary.find('ul li');
        var index = 0;
        $liList.eq(index++).text(title);
        $liList.eq(index++).text('Quantity : 1');
        $liList.eq(index++).text('Date : ' + date);
        $liList.eq(index++).text('Time : ' + time);
        $liList.eq(index++).text('Gender Preferred : ' + gender);
      //  $liList.eq(index++).text('Coupon : ' + coupon);
    };
    
    function massageGiftPageAsParent($this, $parent){
        var $massageDetailsPanel = $parent.closest('.mp-massageDetails-panel');
        var title = $massageDetailsPanel.find('div.mp-massageDetails-title').text();
        var massageType = $massageDetailsPanel.find('input[name="massageDetailsType"]').val();
        var massageLength = $massageDetailsPanel.find('input[name="massageDetailsLength"]').val();
       // var coupon = $massageDetailsPanel.find('input[name="coupon"]').val();
        var feeType = $massageDetailsPanel.find('input[name="detailsFeeType"]').val();
        var amount = parseInt($massageDetailsPanel.find('input[name="detailsAmount"]').val());
        var totalAmount = amount;
        
        //setup hidden form
        var $pamentForm = $('#payment-form');
        $pamentForm.find('input[name="amount"]').val(totalAmount);
        $pamentForm.find('input[name="feeType"]').val(feeType);
       // $pamentForm.find('input[name="serviceCoupon"]').val(coupon);
        $pamentForm.find('input[name="serviceMassageType"]').val(massageType);
        $pamentForm.find('input[name="serviceMassageLength"]').val(massageLength);
	    var referCode = localStorage.getItem("referCode");
		if(referCode)
		{
		   $pamentForm.find('input[name="referCode"]').val(referCode);	
		};
        $pamentForm.find('button').prop('disabled', false);
        $pamentForm.find('button').removeClass('disabled');
        $pamentForm.find('div.alert-danger').css('display', 'none');
        $pamentForm.find('span.checkoutAlertDanger').text('');      
	
        //setup summary
        var $summary = $this.find('div.mp-checkout-summary');
        $summary.find('span.mp-summary-amount').text('(Subtotal : $' + totalAmount + ')');
        var liListString = '<li class="list-group-item  mp-summary-title"></li>' +
        '<li class="list-group-item  mp-summary-quantity"></li>' +
        '<li class="list-group-item  mp-summary-massageType"></li>' +
        '<li class="list-group-item  mp-summary-massageLength"></li>';
       // '<li class="list-group-item  mp-summary-coupon"></li>';
        $summary.find('ul').html(liListString);
        var $liList = $summary.find('ul li');
        var index = 0;
        $liList.eq(index++).text(title);
        $liList.eq(index++).text('Quantity : 1');
        $liList.eq(index++).text('Massage Type : ' + massageType);
        $liList.eq(index++).text('Massage Length : ' + massageLength);
       // $liList.eq(index++).text('Coupon : ' + coupon);
    };
    
    var publicObj = {
        beforeShow: function(parent){
            var $this = $(this);
            var $parent = $(parent);
			 var $pamentForm = $('#payment-form').find('.form-group').removeClass('has-error');
            var fromPageId = $parent.find('div.mp-pageId').text().trim();
            if (fromPageId === 'panda_massageDetails') 
                massageDetailPageAsParent($this, $parent);
            if (fromPageId === 'panda_gift') 
                massageGiftPageAsParent($this, $parent);
        },
        afterResponse: function(pageId){
            $('#payment-form').validator().on('submit', function(e){
                var $form = $(this);
                $form.find('.mp-checkoutAlertDanger').css('display', 'none');
                $form.find('span.payment-errors').text('');
                if (e.isDefaultPrevented()) {
                    $form.find('button[type="submit"]').prop('disabled', false);
                    $form.find('button[type="submit"]').removeClass('disabled');
                }
                else {
                    // everything looks good!
                    // Disable the submit button to prevent repeated clicks
                    $form.find('button').prop('disabled', true);
                    Stripe.setPublishableKey('pk_test_704p8Gz1ev0sCJJK5sc4b9cF');
                    Stripe.card.createToken($form, stripeResponseHandler);
                    // Prevent the form from submitting with the default action
                    return false;
                }
            });
            
            $('#panda_checkout').find('.mp-shippingInfo').on('click', function(e){
                var $returnPolicy = $('#panda_checkout').find('.mp-returnPolicy');
                if ($returnPolicy.attr('aria-describedby')) {
                    $returnPolicy.popover('hide');
					return false;
                }
            });
            $('#panda_checkout').find('.mp-returnPolicy').on('click',  function(e){
                 var $shippingInfo = $('#panda_checkout').find('.mp-shippingInfo');
                if ($shippingInfo.attr('aria-describedby')) {
                    $shippingInfo.popover('hide');
					return false;
                }
            });
            $('#panda_checkout').click(function(e){
                var $realElement = $(e.target);
                if ($realElement.hasClass('popover') || $realElement.hasClass('mp-returnInfo')) 
                    return false;
                var $openPopover = $('div[id^="popover"]');
                if ($openPopover.length > 0) {
                    var $returnInfo = $(this).find('div.mp-returnInfoDiv');
                    $openPopover.each(function(){
                        var popoverId = $(this).attr('id');
                        $returnInfo.find('span[aria-describedby="' + popoverId + '"]').click();
                        
                    });
                }
            });
            $('.mp-returnInfo').popover();
            $('.mp-checkout-mobileTab').find('button.mp-toOrder').addClass('active');
            $('.mp-toOrder').click(function(){
                $('.mp-checkout-mobileTab').find('button.mp-toShipping').removeClass('active');
                $('.mp-checkout-mobileTab').find('button.mp-toOrder').addClass('active');
                var $sectionRight = $('#payment-form').find('.mp-checkoutSection-right');
                var $sectionLeft = $('#payment-form').find('.mp-checkoutSection-left');
                if ($sectionRight.hasClass('mp-smallScreenHide')) {
                    $sectionLeft.addClass('mp-smallScreenHide');
                    $sectionRight.removeClass('mp-smallScreenHide');
                };
                
                window.scrollTo(0, 0);
            });
            $('.mp-toShipping').click(function(){
                $('.mp-checkout-mobileTab').find('button.mp-toShipping').addClass('active');
                $('.mp-checkout-mobileTab').find('button.mp-toOrder').removeClass('active');
                var $sectionRight = $('#payment-form').find('.mp-checkoutSection-right');
                var $sectionLeft = $('#payment-form').find('.mp-checkoutSection-left');
                if ($sectionLeft.hasClass('mp-smallScreenHide')) {
                    $sectionLeft.removeClass('mp-smallScreenHide');
                    $sectionRight.addClass('mp-smallScreenHide');
                };
                
                window.scrollTo(0, 0);
            });
            // do not need this because there is no billing address            
            //            $('.mp-useBilling').on('change', function(){
            //                var checkbox = $(this).find('input[type="checkbox"]');
            //               if (checkbox.prop("checked")) 
            //                    useBilling();
            //            })
        }
    };
    return publicObj;
}());

var massageGiftPage = (function(){
    // beforeShow and afterShow will call every time when page showup
    // afterResponse only execute once when page load. afterResponse execute before beforeShow.
    //private function
    function processSelection(e){
        var value = $(this).text();
        var $parentDiv = $(this).closest('div.mp-massageDetails-input');
        $parentDiv.find('input').val(value);
        $parentDiv.find('button').html(value + '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true">');
        var $massageDetailsPanel = $(this).closest('.mp-massageDetails-panel');
        var massageLength = $massageDetailsPanel.find('input[name="massageDetailsLength"]').val();
        var massageType = $massageDetailsPanel.find('input[name="massageDetailsType"]').val();
        var massageMoney = '';
        if (massageLength && massageType) {
            if (massageType === 'Individual') {
                if (massageLength === '1hour') {
                    massageMoney = '$79';
                    $massageDetailsPanel.find('input[name="detailsFeeType"]').val(1);
                }
                else 
                    if (massageLength === '1.5hour') {
                        massageMoney = '$109';
                        $massageDetailsPanel.find('input[name="detailsFeeType"]').val(3);
                    }
            }
            else 
                if (massageType === 'Couple') {
                    if (massageLength === '1hour') {
                        massageMoney = '$149';
                        $massageDetailsPanel.find('input[name="detailsFeeType"]').val(5);
                    }
                    else 
                        if (massageLength === '1.5hour') {
                            massageMoney = '$199';
                            $massageDetailsPanel.find('input[name="detailsFeeType"]').val(7);
                        }
                }
            
            $massageDetailsPanel.find('input[name="detailsAmount"]').val(massageMoney.replace(/[^\d.-]/g, ''));
            var detailsAmount = parseInt($massageDetailsPanel.find('input[name="detailsAmount"]').val());
            // TODO: what is the difference between detailsAmount and massageMoney
            if (1) {
                var totalAmount = detailsAmount;
                $massageDetailsPanel.find('div.mp-massageDetails-titlePrice').text('Subtotal : ' + '$' + totalAmount);
            }
            else 
                $massageDetailsPanel.find('div.mp-massageDetails-titlePrice').text('Subtotal : ' + massageMoney);
        }
        
        
        e.preventDefault();
    };
    
    var publicObj = {
        beforeShow: function(parent){
            var $this = $(this);
            $this.find('input').val('');
            var $massageDetailsPanel = $this.find('.mp-massageDetails-panel');
            $massageDetailsPanel.find('.mp-massageDetails-titlePrice').text('$79.00 - $199.00');
            $massageDetailsPanel.find('#mp-massageDetails-panelAlert').hide();
            $massageDetailsPanel.find('button.mp-massageTypeSelection').html('Massage Type<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>');
            $massageDetailsPanel.find('button.mp-massageLengthSelection').html('Massage Length<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>');
        },
        afterResponse: function(pageId){
            var $this = $('#' + pageId);
            // TODO: comment out for now
            /*
            $this.find('input[name="quantity"]').change(function(){
                var $massageDetailsPanel = $(this).closest('.mp-massageDetails-panel');
                var detailsAmount = parseInt($massageDetailsPanel.find('input[name="detailsAmount"]').val());
                if (detailsAmount) {
                    if ($(this).val()) {
                        var totalAmount = parseInt($(this).val()) * detailsAmount;
                        $massageDetailsPanel.find('div.mp-massageDetails-titlePrice').text('Subtotal : ' + '$' + totalAmount);
                    }
                    else 
                        $massageDetailsPanel.find('div.mp-massageDetails-titlePrice').text('Subtotal : ' + '$' + detailsAmount);
                    
                }
            });
            */
            var $massageDetailsSelectionList = $this.find('.mp-massageDetailsSelectionList');
            $massageDetailsSelectionList.on("click", "a", processSelection);
        },
        checkoutPageValidate: function($this){
            var $massageDetailsForm = $this.closest('.mp-massageDetails-form');
            var massageLength = $massageDetailsForm.find('input[name="massageDetailsLength"]').val();
            var massageType = $massageDetailsForm.find('input[name="massageDetailsType"]').val();
            var $panelAlert = $massageDetailsForm.find('#mp-massageDetails-panelAlert');
            $panelAlert.css('display', 'none');
            if (!massageType) {
                $panelAlert.text('Please select massage type !');
                $panelAlert.css('display', 'block');
                return false;
            };
            if (!massageLength) {
                $panelAlert.text('Please select massage length !');
                $panelAlert.css('display', 'block');
                return false;
            };
            return true;
        }
        
    };
    
    return publicObj;
}());

var massageDetailsPage = (function(){
    //private function
    function processSelection(e){
        var value = $(this).text();
        var $parentDiv = $(this).closest('div.mp-massageDetails-input');
        $parentDiv.find('input').val(value);
        $parentDiv.find('button').html(value + '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true">');
        e.preventDefault();
    };
    //private function
    function setupTimeDropdown($timeList){
        $timeList.empty();
        var timeArray = ['9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am', '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm', '3:00pm', '3:30pm', '4:00pm', '4:30pm', '5:00pm', '5:30pm', '6:00pm', '6:30pm', '7:00pm', '7:30pm', '8:00pm', '8:30pm','9:00pm'];
        for (var i = 0; i < 25; i++) {
            var time = timeArray[i];
			 var timeTempString = '<li class="mp-item"><a>'+time+'</a></li><li class="divider"></li>';           
            $timeList.append(timeTempString);
        }
		$timeList.append('<li class="mp-item noServiceAvaliable" style="display:none"><a>No Services</a></li>');
        $timeList.on("click", "a", processSelection);
    };
	//private function
	function processTableSelection(e){
		if($(this).hasClass('timeTableDisable'))
		 return false;
		var value = $(this).text();
	    var $parentDiv = $(this).closest('div.mp-massageDetails-input');
		$parentDiv.find('input').val(value);
        $parentDiv.find('button').html(value + '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true">');
        $parentDiv.find('div.mp-timeTableDiv').fadeOut();
		e.preventDefault();
	}
	//private function keep for reference
	function setupTimeTable($timeTable){		
		var timeArray = ['','9:00am', '9:15am', '9:30am', '9:45am', '10:00am', '10:15am', '10:30am', '10:45am', '11:00am', '11:15am', '11:30am', '11:45am', '12:00pm', '12:15pm', '12:30pm', '12:45pm', '1:00pm', '1:15pm', '1:30pm', '1:45pm', '2:00pm', '2:15pm', '2:30pm', '2:45pm', '3:00pm', '3:15pm', '3:30pm', '3:45pm', '4:00pm', '4:15pm', '4:30pm', '4:45pm', '5:00pm', '5:15pm', '5:30pm', '5:45pm', '6:00pm', '6:15pm', '6:30pm', '6:45pm', '7:00pm', '7:15pm', '7:30pm', '7:45pm', '8:00pm', '8:15pm', '8:30pm', '8:45pm', '9:00pm'];
		for(var i= 1 ; i <48 ; i = i+4){
			var tableRowString = '<tr><td>'+timeArray[i]+'</td><td>'+timeArray[i+1]+'</td><td>'+timeArray[i+2]+'</td><td>'+timeArray[i+3]+'</td></tr>';
			$timeTable.append(tableRowString);
		}
		 $timeTable.on("click", "td", processTableSelection);
	}
	//private function
	function massageDetailsTimeForList($this){
		var $parentInputDiv = $this.closest('.mp-massageDetails-input');
		var $massageDetailsForm = $this.closest('.mp-massageDetails-form');	
		var $timeList = $parentInputDiv.find('#massageDetails_timeList');	
		if($parentInputDiv.hasClass('open'))
		{
			$timeList.find('li').removeClass('timeListHide');
			$timeList.find('li.noServiceAvaliable').hide();
		}
		else
		{
			var date = $massageDetailsForm.find('input[name="massageDetailsDate"]').val();				 
			var today = new Date();
			var todayDateString = pandaUtil.getDateString(today);
			if (todayDateString === date) {
				 var timeArray = ['9:00am', '9:30am', '10:00am', '10:30am', '11:00am', '11:30am', '12:00pm', '12:30pm', '1:00pm', '1:30pm', '2:00pm', '2:30pm', '3:00pm', '3:30pm', '4:00pm', '4:30pm', '5:00pm', '5:30pm', '6:00pm', '6:30pm', '7:00pm', '7:30pm', '8:00pm', '8:30pm','9:00pm'];
				 var currentHours = today.getHours()+1;
				  var currentMins = today.getMinutes();
				  currentMins = Math.ceil(currentMins/30)*30;	
				   if (currentMins === 60) {
				   	currentMins = '00';
				   	currentHours = currentHours + 1;
				   }
				   				 //special case if over 10,then no service
				 if(currentHours>22)
				 {
				 	$timeList.find('li').not('.noServiceAvaliable').addClass('timeListHide');
					$timeList.find('li.noServiceAvaliable').show();
					return ;
				 }
				   	var currentSuffix = (currentHours >= 12)? 'pm' : 'am';
					currentHours = ((currentHours + 11) % 12 + 1);
					var currentTimeString = currentHours +':'+currentMins+currentSuffix;
			        if(timeArray.indexOf(currentTimeString)>-1)
					{
						var timeStringIndex = timeArray.indexOf(currentTimeString)*2;
						$timeList.find('li:lt('+timeStringIndex+')').addClass('timeListHide');
						
					}
			}
		}
	}
	//private function keep for reference
	function massageDetailsTimeForTable($this){
		var $massageDetailsForm = $this.closest('.mp-massageDetails-form');
				var $timeTable = $this.next();
				if($timeTable.css('display')==='none')
				{				   
				   var date = $massageDetailsForm.find('input[name="massageDetailsDate"]').val();				 
				   var today = new Date();
				   var todayDateString = pandaUtil.getDateString(today);
			      if (todayDateString === date) {
				  		var timeArray = ['9:00am', '9:15am', '9:30am', '9:45am', '10:00am', '10:15am', '10:30am', '10:45am', '11:00am', '11:15am', '11:30am', '11:45am', '12:00pm', '12:15pm', '12:30pm', '12:45pm', '1:00pm', '1:15pm', '1:30pm', '1:45pm', '2:00pm', '2:15pm', '2:30pm', '2:45pm', '3:00pm', '3:15pm', '3:30pm', '3:45pm', '4:00pm', '4:15pm', '4:30pm', '4:45pm', '5:00pm', '5:15pm', '5:30pm', '5:45pm', '6:00pm', '6:15pm', '6:30pm', '6:45pm', '7:00pm', '7:15pm', '7:30pm', '7:45pm', '8:00pm', '8:15pm', '8:30pm', '8:45pm', '9:00pm'];
						var currentHours = today.getHours()+1;
						var currentMins = today.getMinutes();
						currentMins = Math.ceil(currentMins/15)*15;	
						if(currentMins===60)
						{
							currentMins = '00';
							currentHours = currentHours+1;
						}				
						var currentSuffix = (currentHours >= 12)? 'pm' : 'am';
						currentHours = ((currentHours + 11) % 12 + 1);
						var currentTimeString = currentHours +':'+currentMins+currentSuffix;
			            if(timeArray.indexOf(currentTimeString)>-1)
						{
							var timeStringIndex = timeArray.indexOf(currentTimeString);
							var rowNum = Math.ceil((timeStringIndex+1)/4);
							var columnNum = (timeStringIndex)%4;
							$timeTable.find('tr:lt('+rowNum+')').find('td').addClass('timeTableDisable');
							$timeTable.find('tr:eq('+(rowNum-1)+')').find('td:gt('+(columnNum-1)+')').removeClass('timeTableDisable');
						}
				   }	
					 $timeTable.fadeIn();
				}	 
				else
				{					
					  $timeTable.fadeOut();
					    $massageDetailsForm.find('#massageDetails_timeTable').find('td').removeClass('timeTableDisable');
				}	
	}
    // beforeShow and afterShow will call every time when page showup
    // afterResponse only execute once when page load. afterResponse execute before beforeShow.
    var publicObj = {
        beforeShow: function(parent){
            var $this = $(this);
            var $parent = $(parent);
            $this.find('input').val('');
            var massageName = $parent.find('.mp-massageTypePreview-name').text();
            var massagePrice = $parent.find('.mp-massageTypePreview-price').text();
            var massageType = $parent.find('input[name="panda-massageType"]').val();
            var massageFeeType = $parent.find('input[name="panda-massageFeeType"]').val();
            var massageImage = $parent.find('.mp-massageTypePreview-image').attr('src');
            var $massageDetailsPanel = $this.find('.mp-massageDetails-panel');
            $massageDetailsPanel.find('#mp-massageDetails-panelAlert').hide();
            $massageDetailsPanel.find('p.mp-massageDetails-description').hide();
            $massageDetailsPanel.find('p[data-massageType="' + massageType + '"]').show();
            $this.find('.mp-massageDetails-image').attr('src', massageImage);
            $this.find('.mp-massageDetails-title').text(massageName + ' ' + massagePrice);
            $this.find('li.mp-currentDetailsPage').text(massageName + ' ' + massagePrice);
            $massageDetailsPanel.find('input[name="detailsAmount"]').val(massagePrice.replace(/[^\d.-]/g, ''));
            $massageDetailsPanel.find('input[name="detailsFeeType"]').val(massageFeeType);
            $massageDetailsPanel.find('input[name="needTable"]').prop( "checked", true );
			$this.find('button.massageDetailsTime').html('Select Time<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>');
            $this.find('button.genderPreferred').html('Gender Preferred<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>');
        },
        afterResponse: function(pageId){
            var $this = $('#' + pageId);
            var $datePicker = $this.find("input.mp-massageDetails-DatePicker");
            if ($datePicker.hasClass('hasDatepicker')) {
                // $datePicker.datepicker("destroy");
                $datePicker.removeClass("hasDatepicker").removeAttr('id');
            }
            $datePicker.datepicker({
                minDate: new Date()
            });
			//setupTimeTable($this.find('#massageDetails_timeTable'));
             setupTimeDropdown($this.find('#massageDetails_timeList'));
			$this.find('button.massageDetailsTime').off('click');
			$this.find('button.massageDetailsTime').on('click',function(e){
				 var $this = $(this);
				 // this is for dropdown table. keep the code for reference
				 //massageDetailsTimeForTable($this);
				 massageDetailsTimeForList($this);
				 
			});

            var $genderPreferredList = $this.find('#massageDetails_genderPreferredList');
            $genderPreferredList.on("click", "a", processSelection);
        },
        checkoutPageValidate: function($this){
            var $massageDetailsForm = $this.closest('.mp-massageDetails-form');
            var date = $massageDetailsForm.find('input[name="massageDetailsDate"]').val();
            var time = $massageDetailsForm.find('input[name="massageDetailsTime"]').val();
            var gender = $massageDetailsForm.find('input[name="genderPreferred"]').val();
            var $panelAlert = $massageDetailsForm.find('#mp-massageDetails-panelAlert');
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
                $panelAlert.text('Please select genderPreferred !');
                $panelAlert.css('display', 'block');
                return false;
            };
			var today = new Date();
			var pickMonth = date.split('/')[0];
			pickMonth=parseInt(pickMonth)-1;
			var pickDay = date.split('/')[1];
			var pickYear = date.split('/')[2];
			var pickDate = new Date(pickYear,pickMonth,pickDay,23,59);
			if(pickDate<today)
			{
				$panelAlert.text('Date can not be  in the past !');
                $panelAlert.css('display', 'block');
                return false;
			}
			//if user select today, we need check whether it is hour after
			var todayDateString = pandaUtil.getDateString(today);
			if(todayDateString === date)
			{
				var day = today.getDate();
				var month = today.getMonth(); //January is 0!
				var year = today.getFullYear();
				var pureTime = time.replace(/am|pm/gi,'');
				var hour = pureTime.split(':')[0];
				var min = pureTime.split(':')[1];
				var selectTimeObj;
				if ( time.indexOf("am") > -1 )
				{					
					selectTimeObj = new Date(year,month,day,hour,min);
				}	
				else 
				{
					if(parseInt(hour)<12)
					{
						hour=parseInt(hour)+12;
					}
					selectTimeObj = new Date(year,month,day,hour,min);
				}
				var ONE_HOUR = 60 * 60 * 1000; 
			    if((selectTimeObj.getTime()-today.getTime())<ONE_HOUR)
				{
					$panelAlert.text('Time should be one hour later from now !');
                	$panelAlert.css('display', 'block');
                	return false;
				}
			}
            return true;
        }
        
    };
    
    return publicObj;
    
}());




var defualtSetting = {
    appBaseURL: '../static/html/',
    initActivePage: 'panda_home'
};

var pandaPageObj = {};

var pageStateObj = {
    pageState: 0
};

var headerAttr = {
    mpController: 'data-mpController',
    mpPageId: 'data-mpPageId',
    mpAjax: 'data-mpAjax', //true(default) or false
    mpPageType: 'data-mpPageType', //default(default) or other 
    mpPageStateType: 'data-pageStateType'
};

var pageController = {
    init: function($pageHeaders){
    
        var $header;
        for (var i = 0; i < $pageHeaders.length; i++) {
            $header = $($pageHeaders[i]);
            var pageId = $header.attr(headerAttr.mpPageId);
            //check page has been loaded or not
            if (!pageId) 
                continue;
            if (pandaPageObj[pageId].mpLoaded) 
                continue;
            
            // only	process header has mpPageId.
            if (pageId) {
                if ($('#'+pageId).length === 0 && $header.attr(headerAttr.mpPageType) === 'preLoad') {
                    //page has not been load for sure
                    pageController.load($header);
                }
                
            }
            
        }
    },
    load: function($header, callBack, forceLoad){
        var mpControllerName = $header.attr(headerAttr.mpController);
        var mpNewPageId = $header.attr(headerAttr.mpPageId);
        if (!mpNewPageId) 
            return;
        //page already been loaded
        if ($('#mp-mainContent').find('#' + mpNewPageId).length > 0) 
            return;
        var mpController;
        if (window[mpControllerName]) 
            mpController = window[mpControllerName];
        //only load pageType is default
        if ($header.attr(headerAttr.mpPageType) === 'preLoad' || forceLoad === 'true') {
            var getURL = defualtSetting.appBaseURL + mpNewPageId + '.html';
            pandaAjax.get(getURL, undefined, function(data){
                console.log(mpNewPageId + ' page load success ! ');
                pandaPageObj[mpNewPageId].mpLoaded = true;
                $('#mp-mainContent').append(data);
                
				//setup child page
                pageController.setup(mpNewPageId);
               //call afterResponse
			    if (typeof(mpController) === 'object' && typeof(mpController.afterResponse) === 'function') {
                    mpController.afterResponse(mpNewPageId);
                }
                //this callBack only use for framework. 
                if (typeof(callBack) === 'function') 
                    callBack.apply($header);
            }, $header);
        }
        
    },
    setup: function(pageId){
        var $pageHeaders;
        if (pageId) 
            $pageHeaders = $('#' + pageId).find('.mp-pageHeader');
        else 
            $pageHeaders = $('.mp-pageHeader');
        //setup default attr
        var $header;
        var headerValidArr = [];
        var realHeaderArr = [];
        for (var i = 0; i < $pageHeaders.length; i++) {
            $header = $($pageHeaders[i]);
            
            var tempPageId = $header.attr(headerAttr.mpPageId);
            
            if (!tempPageId) 
                continue;
           
            if (headerValidArr.indexOf(tempPageId) == -1 &&  $('#'+tempPageId).length ===0) {
                headerValidArr.push(tempPageId);
                realHeaderArr.push($header);
            }
            //use other to do lazy loading .use default to do init loading
            if (typeof($header.attr(headerAttr.mpPageType)) === 'undefined') 
                $header.attr(headerAttr.mpPageType, 'default');
            
            
            if (typeof(pandaPageObj[tempPageId]) === 'undefined') {
                pandaPageObj[tempPageId] = {
                    mpLoaded: false,
                    mpRefresh: false
                }
            }
        };
        //setup click event
        $pageHeaders.off('click');
        $pageHeaders.on('click', function(e){
            var $this = $(this);
            var clickPageId = $this.attr(headerAttr.mpPageId);
            var activePageId = sessionStorage.getItem("mp-activePage");
            var oldPageControllerName = $('#' + activePageId).attr(headerAttr.mpController);
            var newPageControllerName = $this.attr(headerAttr.mpController);
            var newPageValidateMethodName = newPageControllerName + 'Validate';
            if (window[oldPageControllerName]) {
                var oldPageController = window[oldPageControllerName];
                if (typeof(oldPageController) === 'object' && typeof(oldPageController[newPageValidateMethodName]) === 'function') {
                    var result = oldPageController[newPageValidateMethodName]($this);
                    if (!result) 
                        return false;
                }
            }
            var isAjax = $this.attr(headerAttr.mpAjax);
            if (isAjax !== 'false') {
				var clickPageNum = $('#'+clickPageId).length;
                if (pandaPageObj[clickPageId].mpLoaded && clickPageNum==1) {
                    pageController.changePage($this);
                }
                else {
                    var callBack = function(){
                        pageController.changePage($(this));
                    }
                    pageController.load($this, callBack, 'true');
                }
                e.preventDefault();
            }
        });
        //call init
        pageController.init(realHeaderArr);
    },
    changePage: function($this,replaceState){
        var newPageId = $this.attr(headerAttr.mpPageId);
        var activePageId = sessionStorage.getItem("mp-activePage");
        if (activePageId !== newPageId) {
			if(activePageId)
			{
				 $('#' + activePageId).hide(function(){          
           		 });
			}         
            var newPageControllerName = $this.attr(headerAttr.mpController);
            if (window[newPageControllerName]) {
                var newPageController = window[newPageControllerName];
				  //after refresh need to call afterResponse again
                if (pandaPageObj[newPageId].mpRefresh) {
                    if (typeof(newPageController) === 'object' && typeof(newPageController.afterResponse) === 'function') {
                        newPageController.afterResponse(newPageId);
                    }
                    pandaPageObj[newPageId].mpRefresh = false;
                }
                if (typeof(newPageController) === 'object' && typeof(newPageController.beforeShow) === 'function') {
                    newPageController.beforeShow.apply($('#' + newPageId), $this);
                }
            };
            sessionStorage.setItem('mp-activePage', newPageId);
            $('#' + newPageId).show(0, function(){
                window.scrollTo(0, 0);
                // Change our States
                pageStateObj.pageState = pageStateObj.pageState + 1;
                pageStateObj[pageStateObj.pageState] = newPageId;
            
                if ($this.attr(headerAttr.mpPageStateType) === 'replace' || replaceState) {
                    History.replaceState({
                        state: pageStateObj.pageState
                    }, undefined, "?tab=" + pageStateObj[pageStateObj.pageState]);
                }
                else {
					History.pushState({
                        state: pageStateObj.pageState
                    }, undefined, "?tab=" + pageStateObj[pageStateObj.pageState]);
                }
                
                
                if (window[newPageControllerName]) {
                    var newPageController = window[newPageControllerName];
                    if (typeof(newPageController) === 'object' && typeof(newPageController.afterShow) === 'function') {
                        newPageController.afterShow.apply($('#' + newPageId), $this);
                    }
                }
                
                
            });
            
        }
    }
}


var pageBackForward = {
    change: function(newState){
        var newPageId = pageStateObj[newState];
        var activePageId = sessionStorage.getItem("mp-activePage");
        if (activePageId !== newPageId) {
            $('#' + activePageId).hide(function(){
            });
            
            $('#' + newPageId).show(0, function(){
                window.scrollTo(0, 0);
                sessionStorage.setItem('mp-activePage', newPageId);
            });
        }
    },
    afterResponse: function(pageId){
        var newPageControllerName = $('#' + pageId).attr(headerAttr.mpController);
        if (window[newPageControllerName]) {
            var newPageController = window[newPageControllerName];
            if (typeof(newPageController) === 'object' && typeof(newPageController.afterResponse) === 'function') {
                newPageController.afterResponse(pageId);
            }
        }
    }
}

var pandaInit = function(){
	var referCode  = pandaUtil.getParameterByName('referCode');
	if(referCode)
		localStorage.setItem("referCode", referCode);
    var isRefresh = sessionStorage.getItem('pandaRefresh');
    var tabName = pandaUtil.getParameterByName('tab');
	var customizedPageHeader = $('[data-mpPageId="'+tabName+'"]');
	//check if page has been reload
    if (isRefresh) {
        var oldPageElement = sessionStorage.getItem('mp-pageElement');
        $('#mp-mainContent').html(oldPageElement);
        sessionStorage.removeItem('mp-pageElement');
        var oldPandaPageState = JSON.parse(sessionStorage.getItem('mp-pageState'));
        var oldPandaPageObj = JSON.parse(sessionStorage.getItem('mp-pageObj'));
        $.extend(pageStateObj, oldPandaPageState);
        $.extend(pandaPageObj, oldPandaPageObj);
        var lastState = pageStateObj.pageState;
        var lastStatePageId = pageStateObj[lastState];
        //just double check page Id, can be remove later
        var activePageId = sessionStorage.getItem('mp-activePage');
        if (activePageId === lastStatePageId) 
		{
			console.log("pageId is right !!");
		}
		else
		{
			console.log("pageId is wrong !!");
			console.log("activePageId : "+activePageId);	
			console.log("lastStatePageId : "+lastStatePageId);
			//need to recover	
		}

		 pageController.setup();
		 //check if tabName is equals to active page. if not, page is not reload by refresh button
		 //tab name must be manually change by people
		if(tabName!==activePageId)
		{
			//check if tab name is valid. if valid we need to change page.
			if(customizedPageHeader.length>0)
			{
			   var $firstCustomizedPageHeader = customizedPageHeader.first();
			   var mptabPageNum = $('#'+tabName).length;
				if(pandaPageObj[tabName].mpLoaded&&mptabPageNum===1)
				{
					pageController.changePage($firstCustomizedPageHeader,true);
				}
				else
				{
					//need load page
				   var callBack = function(){
	                        pageController.changePage($(this),true);
	                }
	              pageController.load($firstCustomizedPageHeader, callBack, 'true');
				}
			}
			//if tab name is not valid. we need load index page
			else{
				// if last time is not index then we change page
				var homePageDivNum = $('#panda_home').length;
				 var $firstPandaHome = $('[data-mpPageId="panda_home"]').first();
				if(homePageDivNum==1)
				{
				    if(activePageId !== defualtSetting.initActivePage)
					{				
					  pageController.changePage($firstPandaHome,true);
					}
					else
					{
						//if last time is index page we just replace it
						pageStateObj.pageState = pageStateObj.pageState + 1;
		               pageStateObj[pageStateObj.pageState] = activePageId;
				        History.replaceState({
				            state: pageStateObj.pageState
				        }, undefined, "?tab=" + pageStateObj[pageStateObj.pageState]);
					}
				}
				else{						//need load page
				   var callBack = function(){
	                        pageController.changePage($(this),true);
	                }
	              pageController.load($firstPandaHome, callBack, 'true');
				}


			}
		}
    	sessionStorage.setItem('pandaRefresh', false);
    }
    else {		
		if(tabName && customizedPageHeader.length>0 && tabName !== defualtSetting.initActivePage)
		{			
	         pandaPageObj[defualtSetting.initActivePage] = {
	            mpLoaded: true,
	            mpRefresh: false
	         };
	         pageController.setup();
			  var $firstCustomizedPageHeader = customizedPageHeader.first();
			   var callBack = function(){
                        pageController.changePage($(this));
                }
              pageController.load($firstCustomizedPageHeader, callBack, 'true');
		}
		else
		{
			 $('#' + defualtSetting.initActivePage).show();
	         sessionStorage.setItem('mp-activePage', defualtSetting.initActivePage);
	         pandaPageObj[defualtSetting.initActivePage] = {
	            mpLoaded: true,
	            mpRefresh: false
	         };
	         pageController.setup();
		}

    }
    
    History.Adapter.bind(window, 'statechange', function(){ // Note: We are using statechange instead of popstate
        var pageState = History.getState(); // Note: We are using History.getState() instead of event.state
        var newState = pageState.data.state;
        var newPageId = pageStateObj[newState];
        var activePageId = sessionStorage.getItem("mp-activePage");
        //after refresh need to call afterResponse again
        if (pandaPageObj[newPageId].mpRefresh) {
            pageBackForward.afterResponse(newPageId);
            pandaPageObj[newPageId].mpRefresh = false;
        }
        
        if (newState) {
            if (activePageId !== newPageId) {
                pageBackForward.change(newState);
            }
            
        }
        else {
            if (activePageId !== defualtSetting.initActivePage) {
                $('#' + activePageId).hide(function(){
                });
                $('#' + defualtSetting.initActivePage).show(0, function(){
                    sessionStorage.setItem('mp-activePage', defualtSetting.initActivePage);
                });
            }
        }
    });
    
    if (isRefresh) {
        // do not need to do anything. 
		if (tabName !== activePageId) {
	       
		}
		 // override last page
		else{
			pageStateObj.pageState = pageStateObj.pageState + 1;
	        pageStateObj[pageStateObj.pageState] = activePageId;
	        History.replaceState({
	            state: pageStateObj.pageState
	        }, undefined, "?tab=" + pageStateObj[pageStateObj.pageState]);
		}	

        
    }
    else {
        //override home page  
		if(tabName && customizedPageHeader.length>0 && tabName !== defualtSetting.initActivePage)
		{
			//do not need to do anything for now because we need load other page
		}
		else{
			pageStateObj[pageStateObj.pageState] = defualtSetting.initActivePage;
	        History.replaceState({
	            state: pageStateObj.pageState
	        }, undefined, "?tab=" + pageStateObj[pageStateObj.pageState]);
		}

        
    }
    
    
}

function pandaPhoneInit(){
    var menuLeft = document.getElementById('mp-leftSideNav'),
	menuRight = document.getElementById('mp-rightSideNav'),  
	showLeftPush = document.getElementById('mp-showLeftPush'),
	showRightPush = document.getElementById('mp-showRightPush'),
    navBar = document.getElementById('mp-navbar'),
    mainContent = document.getElementById('mp-mainContent'), 
	footer = document.getElementById('mp-footer');
    showLeftPush.onclick = function(){
		if($('#mp-rightSideNav').hasClass('cbp-spmenu-open'))
		{
		    classie.toggle( menuRight, 'cbp-spmenu-open' );
		}
        classie.toggle(this, 'active');
        classie.toggle(navBar, 'cbp-spmenu-push-toright');
        classie.toggle(mainContent, 'cbp-spmenu-push-toright');
        classie.toggle(footer, 'cbp-spmenu-push-toright');
        classie.toggle(menuLeft, 'cbp-spmenu-open');
	
    };
	showRightPush.onclick = function() {
	    if($('#mp-leftSideNav').hasClass('cbp-spmenu-open'))
		{
			 classie.toggle(navBar, 'cbp-spmenu-push-toright');
            classie.toggle(mainContent, 'cbp-spmenu-push-toright');
           classie.toggle(footer, 'cbp-spmenu-push-toright');
           classie.toggle(menuLeft, 'cbp-spmenu-open');
		}
		classie.toggle(this, 'active');
		classie.toggle( menuRight, 'cbp-spmenu-open' );
	
	};
    $('#mp-leftSideNav').on('click', function(){
        $('#mp-showLeftPush').trigger('click');
    });
	 $('#mp-rightSideNav').on('click', function(){
        $('#mp-showRightPush').trigger('click');
    });
    
}

function pandaLoginSetup(){
	var firstName = localStorage.getItem('pandaLoginName');
	var $navigation = $('#mp-navbar').find('.mp-navigation>ul');
    var navDropdown = $navigation.children('li.dropdown');
	navDropdown.children('a.dropdown-toggle').html(firstName+'<span class="caret"></span>');
	$navigation.children('li.mp-loginHeader').hide();
	navDropdown.show();
	$('#mp-rightSideNav').find('.mp-mobileLoginfalse').hide();
	$('#mp-rightSideNav').find('.mp-mobileLoginTrue').show();
	$('#mp-rightSideNav').find('.mp-mobileLoginName').text(firstName);
}


$(function(){
	if(localStorage.getItem('pandaLogin')=== 'true')
	{
				pandaLoginSetup();
	}
    $(window).on('beforeunload', function(){
        for (var pageId in pandaPageObj) {
            if (pandaPageObj.hasOwnProperty(pageId)) {
                if(pandaPageObj[pageId].mpLoaded)
				{
					pandaPageObj[pageId].mpRefresh = true;
				}
            }
        }	
        sessionStorage.setItem('mp-pageElement', $('#mp-mainContent').html());
        sessionStorage.setItem('mp-pageState', JSON.stringify(pageStateObj));
        sessionStorage.setItem('mp-pageObj', JSON.stringify(pandaPageObj));
        sessionStorage.setItem('pandaRefresh', true);
    });   
    pandaPhoneInit();
    pandaInit();
});
