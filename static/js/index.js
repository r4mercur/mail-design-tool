$(document).ready(function() {
    // Menu actions
    $('#login-btn').click(function() {
        window.location.href = "/login";
    });

    $('#logout-btn').click(function() {
        window.location.href = "/logout";
    });

    $('#signup-btn').click(function () {
        window.location.href = "/register";
    });

    // Set active menu item
    var currentPath = window.location.pathname;
    $('#main-menu a').each(function() {
        var href = $(this).attr('href');
        if (currentPath === href) {
            $(this).removeClass('secondary-color');
            $(this).addClass('highlight-color');
        }

        // check if mail is the current path and then set the speficic mail menu item active
        if (currentPath.includes('/mail')) {
            $('#templates').removeClass('secondary-color');
            $('#templates').addClass('highlight-color');
        }
    });

    // Custom button actions
    $('#mail-create').click(function() {
        window.location.href = "/mail/create";
    });
});