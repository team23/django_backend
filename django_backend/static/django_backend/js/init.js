require(
    [
        'jquery',
        'django_backend.forms',
        'django_backend.pagecontext'
    ],
    function ($, forms, PageContext) {

  "use strict";

  $(document).ready(function () {

    var CONFIG = window.CONFIG;

    // Initialize root page context.
    var $pageContent = $('.container');
    var pageContext = new PageContext(undefined, {
      lock: CONFIG.lock,
      objectLock: CONFIG.objectLock
    });

    pageContext.init($pageContent);

    forms.init();
  });

});
