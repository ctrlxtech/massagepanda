function pandaPhoneInit() {
    var menuLeft = document.getElementById('mp-leftSideNav'),
        menuRight = document.getElementById('mp-rightSideNav'),
        showLeftPush = document.getElementById('mp-showLeftPush'),
        showRightPush = document.getElementById('mp-showRightPush'),
        navBar = document.getElementById('mp-navbar'),
        mainContent = document.getElementById('mp-mainContent'),
        footer = document.getElementById('mp-footer');
    showLeftPush.onclick = function() {
        if ($('#mp-rightSideNav').hasClass('cbp-spmenu-open')) {
            classie.toggle(menuRight, 'cbp-spmenu-open');
        }
        classie.toggle(this, 'active');
        classie.toggle(navBar, 'cbp-spmenu-push-toright');
        classie.toggle(mainContent, 'cbp-spmenu-push-toright');
        classie.toggle(footer, 'cbp-spmenu-push-toright');
        classie.toggle(menuLeft, 'cbp-spmenu-open');

    };
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
    $('#mp-leftSideNav').on('click', function() {
        $('#mp-showLeftPush').trigger('click');
    });
    $('#mp-rightSideNav').on('click', function() {
        $('#mp-showRightPush').trigger('click');
    });

}
