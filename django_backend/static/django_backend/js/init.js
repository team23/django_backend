require(
    [
        'jquery',
        'django_backend.pagecontext'
    ],
    function ($, PageContext) {

  "use strict";

  $(document).ready(function () {
    // Initialize root page context.
    var $pageContent = $('.container');
    var pageContext = new PageContext(undefined, {});

    pageContext.init($pageContent);
  });

});
