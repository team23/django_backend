require.config({
    baseUrl: window.CONFIG.STATIC_URL + 'django_backend/js'
});

// Wrap "lame" javascript modules, so they can be used by requirejs

define('modernizr', [], function () {
    return window.Modernizr;
});

define('stapes', [], function () {
    return window.Stapes;
});

define('jquery', [], function () {
    return window.jQuery;
});

define('jquery-ui', ['jquery'], function (jQuery) {
    return jQuery; // jquery ui is no extra lib, but now we can use it like it was
});
