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
    post: function(url, param, callback, controller, $header, returnDataType, sendDataType){
        if (!returnDataType) 
            returnDataType = 'json';
        if (!sendDataType) 
            sendDataType = 'application/json; charset=UTF-8'
        var csrfToken = $.cookie('csrftoken'); 
        $.ajax({
            type: 'POST',
            url: url,
            data: JSON.stringify(param),
            contentType: sendDataType,
            dataType: returnDataType,
            beforeSend: function(request) {
                request.setRequestHeader("X-CSRFToken", csrfToken);
                if (typeof(controller) === 'object' && typeof(controller.beforeSend) === 'function') {
                    var success = controller.beforeSend();
                    
                    if (success === false) {
                        return false;
                    }
                }
            }
        }).done(function(data){
            if (typeof(callback) === 'function') 
                callback(data);
            
            if (typeof(controller) === 'object' && typeof(controller.afterResponse) === 'function') {
                controller.afterResponse(data, $header);
            }
        }).fail(function(jqXHR, textStatus){
            if (typeof(controller) === 'object' && typeof(controller.afterFail) === 'function') {
                controller.afterFail(jqXHR, textStatus);
            }
            else 
                pandaAjax.fail(jqXHR, textStatus);
        });
        ;
    }
};

var pandaHelpCenterPage = (function(){
    var publicObj = {
        afterResponse: function(data, $header){
            $('#panda_helpCenter').find('a.mp-hrefBlock').click(function(e){
                e.preventDefault();
            });
        }
    };
    return publicObj;
}());

var checkoutPage = (function(){
    //private function
    function afterSubmit(data){
		//sever return obj: example : {status : true}
        var returnObj = data;
        var $form = $('#payment-form');
        $form.find('button').prop('disabled', false);
        if (returnObj.status) {
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
        
        
    }
    
    //private function
    function submitForm($form){
        var serverObj = {};
        var $serverFieldList = $form.find('input[data-serverField="true"]');
        for (var i = 0; i < $serverFieldList.length; i++) {
            var $serverField = $($serverFieldList[i]);
            var fieldKey = $serverField.attr('name');
            var fieldValue = $serverField.val();
            serverObj[fieldKey] = fieldValue;
        }
        //TODO need use server side path !!!
        var url = '/manager/placeOrder';
        //$form.get(0).submit();
        pandaAjax.post(url,serverObj,afterSubmit);
    }
    
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
    }
    
    var publicObj = {
        beforeShow: function(parent){
            var $this = $(this);
            var $parent = $(parent);
            var $massageDetailsPanel = $parent.closest('.mp-massageDetails-panel');
            var title = $massageDetailsPanel.find('div.mp-massageDetails-title').text();
            var date = $massageDetailsPanel.find('input[name="massageDetailsDate"]').val();
            var time = $massageDetailsPanel.find('input[name="massageDetailsTime"]').val();
            var gender = $massageDetailsPanel.find('input[name="genderPreferred"]').val();
            var quantity = $massageDetailsPanel.find('input[name="quantity"]').val();
            var coupon = $massageDetailsPanel.find('input[name="coupon"]').val();
            var feeType = $massageDetailsPanel.find('input[name="detailsFeeType"]').val();
            var amount = parseInt($massageDetailsPanel.find('div.mp-detailsAmount').text());
            var totalAmount = amount * parseInt(quantity);
            //setup hidden form
            var $pamentForm = $('#payment-form');
            $pamentForm.find('input[name="amount"]').val(totalAmount);
            $pamentForm.find('input[name="feeType"]').val(feeType);
            $pamentForm.find('input[name="serviceDate"]').val(date);
            $pamentForm.find('input[name="serviceTime"]').val(time);
            $pamentForm.find('input[name="serviceGenderPreferred"]').val(gender);
            $pamentForm.find('input[name="serviceQuantity"]').val(quantity);
            $pamentForm.find('input[name="serviceCoupon"]').val(coupon);
            $pamentForm.find('button').prop('disabled', false);
            $pamentForm.find('div.alert-danger').css('display', 'none');
            $pamentForm.find('span.checkoutAlertDanger').text('');
            //setup summary
            var $summary = $this.find('div.mp-checkout-summary');
            $summary.find('span.mp-summary-amount').text('(Subtotal : $' + totalAmount + ')')
            var $liList = $summary.find('ul li');
            var index = 0;
            $liList.eq(index++).text(title);
            $liList.eq(index++).text('Quantity : ' + quantity);
            $liList.eq(index++).text('Date : ' + date);
            $liList.eq(index++).text('Time : ' + time);
            $liList.eq(index++).text('Gender Preferred : ' + gender);
            $liList.eq(index++).text('Coupon : ' + coupon);
            
        },
        afterResponse: function(data, $header){
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
            
            $('.mp-returnInfo').popover();
            
            $('.mp-useBilling').on('change', function(){
                var checkbox = $(this).find('input[type="checkbox"]');
                if (checkbox.prop("checked")) 
                    useBilling();
            })
        },
        validate: function($this){
            var $massageDetailsForm = $this.closest('.mp-massageDetails-form');
            var date = $massageDetailsForm.find('input[name="massageDetailsDate"]').val();
            var time = $massageDetailsForm.find('input[name="massageDetailsTime"]').val();
            var gender = $massageDetailsForm.find('input[name="genderPreferred"]').val();
            var quantity = $massageDetailsForm.find('input[name="quantity"]').val();
            quantity = parseInt(quantity);
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
            if (!quantity) {
                $panelAlert.text('Please enter quantity !');
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
        $parentDiv.find('button').html(value + '<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true">')
        e.preventDefault();
    };
    //private function
    function setupTimeDropdown($timeList){
        var $timeTemp = $('<li class="mp-item"> <a></a></li><li class="divider"></li>');
        var timeArray = ['9:00am', '9:15am', '9:30am', '9:45am', '10:00am', '10:15am', '10:30am', '10:45am', '11:00am', '11:15am', '11:30am', '11:45am', '12:00pm', '12:15pm', '12:30pm', '12:45pm', '1:00pm', '1:15pm', '1:30pm', '1:45pm', '2:00pm', '2:15pm', '2:30pm', '2:45pm', '3:00pm', '3:15pm', '3:30pm', '3:45pm', '4:00pm', '4:15pm', '4:30pm', '4:45pm', '5:00pm', '5:15pm', '5:30pm', '5:45pm', '6:00pm', '6:15pm', '6:30pm', '6:45pm', '7:00pm', '7:15pm', '7:30pm', '7:45pm', '8:00pm', '8:15pm', '8:30pm', '8:45pm', '9:00pm'];
        for (var i = 0; i < 49; i++) {
            var time = timeArray[i];
            var $cloneTimeTemp = $timeTemp.clone();
            $cloneTimeTemp.find('a').text(time);
            $timeList.append($cloneTimeTemp);
        }
        $timeList.on("click", "a", processSelection);
    };
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
            $massageDetailsPanel.find('p.mp-massageDetails-description').hide();
            $massageDetailsPanel.find('p[data-massageType="' + massageType + '"]').show();
            $this.find('.mp-massageDetails-image').attr('src', massageImage);
            $this.find('.mp-massageDetails-title').text(massageName + ' ' + massagePrice);
            $this.find('li.mp-currentDetailsPage').text(massageName + ' ' + massagePrice);
            $massageDetailsPanel.find('div.mp-detailsAmount').text(massagePrice.replace(/[^\d.-]/g, ''));
            $massageDetailsPanel.find('input[name="detailsFeeType"]').val(massageFeeType);
            $this.find('button.massageDetailsTime').html('Select Time<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>');
            $this.find('button.genderPreferred').html('Gender Preferred<span class="glyphicon glyphicon-triangle-bottom" aria-hidden="true"></span>');
        },
        afterResponse: function(data, $header){
            var pageId = $header.attr(headerAttr.mpPageId);
            var $this = $('#' + pageId);
            $this.find("#massageDetails_datepicker").datepicker({
                minDate: new Date()
            });
            $this.find("#massageDetails_spinner").spinner({
                spin: function(event, ui){
                    if (ui.value > 100) {
                        $(this).spinner("value", 0);
                        return false;
                    }
                    else 
                        if (ui.value < 0) {
                            $(this).spinner("value", 0);
                            return false;
                        }
                }
            });
            setupTimeDropdown($this.find('#massageDetails_timeList'));
            var $genderPreferredList = $this.find('#massageDetails_genderPreferredList');
            $genderPreferredList.on("click", "a", processSelection);
        }
        
    };
    
    return publicObj;
    
}());




var defualtSetting = {
    appBaseURL: '../static/html/',
    initActivePage: 'panda_home',
    loadedPageArray: [],
    pageState: 0
};

var pandaPageObj = {};

var pageStateObj = {}

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
            if (pandaPageObj[pageId].mpShow) 
                continue;
            
            // only	process header has mpPageId.
            if (pageId) {
                if (defualtSetting.loadedPageArray.indexOf(pageId) == -1) {
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
        if ($header.attr(headerAttr.mpPageType) === 'default' || forceLoad === 'true') {
            var getURL = defualtSetting.appBaseURL + mpNewPageId + '.html';
            pandaAjax.get(getURL, undefined, function(data){
                console.log(mpNewPageId + ' page load success ! ');
                pandaPageObj[mpNewPageId].mpLoaded = true;
                defualtSetting.loadedPageArray.push(mpNewPageId);
                $('#mp-mainContent').append(data);
                //call afterResponse
                if (typeof(mpController) === 'object' && typeof(mpController.afterResponse) === 'function') {
                    mpController.afterResponse(data, $header);
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
            
            if (headerValidArr.indexOf(tempPageId) == -1) {
                headerValidArr.push(tempPageId);
                realHeaderArr.push($header);
            }
            
            if (typeof($header.attr(headerAttr.mpPageType)) === 'undefined') 
                $header.attr(headerAttr.mpPageType, 'default');
            
            
            if (typeof(pandaPageObj[tempPageId]) === 'undefined') {
                pandaPageObj[tempPageId] = {
                    mpLoaded: false,
                    mpShow: false,
                    mpShowing: false,
                }
            }
        };
        //setup click event
        $pageHeaders.off('click');
        $pageHeaders.on('click', function(e){
            var $this = $(this);
            var clickPageId = $this.attr(headerAttr.mpPageId);
            var newPageControllerName = $this.attr(headerAttr.mpController);
            if (window[newPageControllerName]) {
                var newPageController = window[newPageControllerName];
                if (typeof(newPageController) === 'object' && typeof(newPageController.validate) === 'function') {
                    var result = newPageController.validate($this);
                    if (!result) 
                        return false;
                }
            }
            var isAjax = $this.attr(headerAttr.mpAjax);
            if (isAjax !== 'false') {
            
                if (pandaPageObj[clickPageId].mpLoaded) {
                    //TODO add animation
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
    changePage: function($this){
        var newPageId = $this.attr(headerAttr.mpPageId);
        var activePageId = localStorage.getItem("mp-activePage");
        if (activePageId !== newPageId) {
            pandaPageObj[activePageId].mpShowing = false;
            $('#' + activePageId).hide(function(){
            
            });
            var newPageControllerName = $this.attr(headerAttr.mpController);
            if (window[newPageControllerName]) {
                var newPageController = window[newPageControllerName];
                if (typeof(newPageController) === 'object' && typeof(newPageController.beforeShow) === 'function') {
                    newPageController.beforeShow.apply($('#' + newPageId), $this);
                }
            }
            pandaPageObj[newPageId].mpShowing = true;
            localStorage.setItem('mp-activePage', newPageId);
            $('#' + newPageId).show(0, function(){
                window.scrollTo(0, 0);
                // Change our States
                defualtSetting.pageState = defualtSetting.pageState + 1;
                pageStateObj[defualtSetting.pageState] = newPageId;
                //setup child page
                if (!pandaPageObj[newPageId].mpShow) {
                    pandaPageObj[newPageId].mpShow = true;
                    pageController.setup($this.attr(headerAttr.mpPageId));
                }
                if ($this.attr(headerAttr.mpPageStateType) !== 'replace') {
                    History.pushState({
                        state: defualtSetting.pageState
                    }, undefined, "?state=" + defualtSetting.pageState);
                }
                else {
                    History.replaceState({
                        state: defualtSetting.pageState
                    }, undefined, "?state=" + defualtSetting.pageState);
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
        var activePageId = localStorage.getItem("mp-activePage");
        if (activePageId !== newPageId) {
            $('#' + activePageId).hide(function(){
                pandaPageObj[activePageId].mpShowing = false;
            });
            
            $('#' + newPageId).show(0, function(){
                window.scrollTo(0, 0);
                pandaPageObj[newPageId].mpShowing = true;
                localStorage.setItem('mp-activePage', newPageId);
            });
        }
    }
}

var pandaInit = function(){
    localStorage.setItem('mp-activePage', defualtSetting.initActivePage);
    defualtSetting.loadedPageArray.push(defualtSetting.initActivePage);
    pandaPageObj[defualtSetting.initActivePage] = {
        mpLoaded: true,
        mpShow: true,
        mpShowing: true
    };
    
    History.Adapter.bind(window, 'statechange', function(){ // Note: We are using statechange instead of popstate
        var pageState = History.getState(); // Note: We are using History.getState() instead of event.state
        var newState = pageState.data.state;
        if (newState) {
            var newPageId = pageStateObj[newState];
            if (!pandaPageObj[newPageId].mpShowing) 
                pageBackForward.change(newState);
        }
        else {
            var activePageId = localStorage.getItem("mp-activePage");
            if (activePageId !== defualtSetting.initActivePage) {
                $('#' + activePageId).hide(function(){
                    pandaPageObj[activePageId].mpShowing = false;
                });
                $('#' + defualtSetting.initActivePage).show(0, function(){
                    pandaPageObj[defualtSetting.initActivePage].mpShowing = true;
                    localStorage.setItem('mp-activePage', defualtSetting.initActivePage);
                });
            }
        }
    });
}

$(function(){
    history.pushState("", document.title, window.location.pathname);
    pandaInit();
    pageController.setup();
    
})
