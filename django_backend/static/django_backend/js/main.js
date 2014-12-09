(function ($) {
    $(document).ready(function () {
        var initTooltips = function () {
            $('[data-toggle="tooltip"]').tooltip();
        };

        /*
         * Show previously selected tab on page load.
         */
        var linkToTabInit = function () {
            // Javascript to enable link to tab
            var hash = document.location.hash;
            var prefix = "tab/";

            if (hash && hash.match(prefix)) {
                $('.nav-tabs a[href='+hash.replace(prefix, "")+']').tab('show');
            } 

            // Change hash when tab is shown.
            $(document).on('shown.bs.tab', '.nav-tabs', function (e) {
                window.location.hash = e.target.hash.replace("#", "#" + prefix);
            });

            // Keep hash for specific links.
            $(document).on('click', 'a.keep-tab', function (e) {
                var hash = document.location.hash;
                if (hash.match(prefix)) {
                    e.target.hash = hash;
                }
            });
        };

        $(document).on('tooltip-added', initTooltips);
        initTooltips();
        linkToTabInit();
    });
})(jQuery);
