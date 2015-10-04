require(
    [
        'jquery',
        'django_backend.forms',
        'django_backend.pagecontext'
    ],
    function ($, forms, PageContext) {

  "use strict";

  $(document).ready(function () {
    // Initialize root page context.
    var $pageContent = $('.container');
    var pageContext = new PageContext(undefined, {});

    pageContext.init($pageContent);

    forms.init();
  });

});
