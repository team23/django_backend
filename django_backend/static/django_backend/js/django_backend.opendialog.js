define(
    'django_backend.opendialog',
    [
      'jquery',
      'django_backend.stackedajaxdialog'
    ], function ($, StackedAjaxDialog) {

  "use strict";

  return {
    init: function (pageContext) {
      pageContext.$element.on('click', '[data-dialog=open]', function (e) {

        var dialog = new StackedAjaxDialog(this, {
          url: $(this).attr('href'),
          width: 880,  // dialog width should be similar to normal content width content area
          height: Math.min(800, $(window).height() - 150),
          parentPageContext: pageContext
        });

        dialog.on('success', function (data) {
          console.log('dialog success', dialog.url, data);
          dialog.close();
        });
        dialog.open();

        return false;
      });
    }
  };

});
