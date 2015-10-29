function pandaPhoneInit() {
    var menuLeft = document.getElementById('mp-leftSideNav'),
        menuRight = document.getElementById('mp-rightSideNav'),
        showLeftPush = document.getElementById('mp-showLeftPush'),
        showRightPush = document.getElementById('mp-showRightPush'),
        navBar = document.getElementById('mp-navbar'),
        mainContent = document.getElementById('mp-mainContent'),
        footer = document.getElementById('mp-footer');
		pagewrapper = document.getElementById('page-wrapper');
		viewport = document.getElementById('site-viewport');
		
	var menuShowed = false;
    /*showLeftPush.onclick = function() {
        if ($('#mp-rightSideNav').hasClass('cbp-spmenu-open')) {
            classie.toggle(menuRight, 'cbp-spmenu-open');
        }
        classie.toggle(this, 'active');
        classie.toggle(navBar, 'cbp-spmenu-push-toright');
        classie.toggle(mainContent, 'cbp-spmenu-push-toright');
        classie.toggle(footer, 'cbp-spmenu-push-toright');
        classie.toggle(menuLeft, 'cbp-spmenu-open');

    };*/
	//pagewrapper.addEventListener("webkitAnimationEnd", AnimationEnd);
			
	showLeftPush.onclick = function() {
		if (menuShowed == false){
			menuLeft.style.display = 'block';
			navBar.style.webkitTransform = 'translate3d(60%, 0px, 0px)';
			pagewrapper.style.webkitTransform = 'translate3d(60%, 0px, 0px)';
			viewport.style.overflow = 'hidden';
			menuShowed = true;
		}
		else{
			navBar.style.webkitTransform = 'translate3d(0%, 0px, 0px)';
			pagewrapper.style.webkitTransform = 'translate3d(0%, 0px, 0px)';
			viewport.style.overflow = 'visible';
			menuShowed = false;
		}
	}
	
	$(pagewrapper).on("webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend",function(event) {
		if (menuShowed == false){
			menuLeft.style.display = 'none';
		}
		else{
			menuLeft.style.display = 'block';
		}
	});
/*
    showRightPush.onclick = function() {
        if ($('#mp-leftSideNav').hasClass('cbp-spmenu-open')) {
            classie.toggle(navBar, 'cbp-spmenu-push-toright');
            classie.toggle(mainContent, 'cbp-spmenu-push-toright');
            classie.toggle(footer, 'cbp-spmenu-push-toright');
            classie.toggle(menuLeft, 'cbp-spmenu-open');
        }
        classie.toggle(this, 'active');
        classie.toggle(menuRight, 'cbp-spmenu-open');

    };
    $('#mp-rightSideNav').on('click', function() {
        $('#mp-showRightPush').trigger('click');
    });


    $('#mp-leftSideNav').on('click', function() {
        $('#mp-showLeftPush').trigger('click');
    });
	*/

}

/*function AnimationEnd() {
	var menuLeft = document.getElementById('mp-leftSideNav');
	if (menuLeft.style.display === 'block'){
		menuLeft.style.display = 'none';
	}
}*/

