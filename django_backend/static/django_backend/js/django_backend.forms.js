define('django_backend.forms', ['jquery'], function ($, undefined) {
  "use strict";

  var ENTER_KEY = 13;

  return {
    handleDefaultButtons: function () {
        $('html').on('keypress', 'form input', function (e) {
            if (e.which == ENTER_KEY) {
                var form = $(this).parents('form:first');
                var defaultButton = form.find('[type=submit].default');
                if (defaultButton.length) {
                    defaultButton.click();
                    return false;
                }
            }
        });
    },

    init: function () {
      this.handleDefaultButtons();
    }
  };
});
