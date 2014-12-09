define('django_backend.formdata', ['jquery'], function ($, undefined) {
  "use strict";

  var supportsFormData = window.FormData;
  //supportsFormData = false;

  return {
    supportsFormData: supportsFormData,

    get: function ($form, method) {
      if (supportsFormData && method === 'post') {
        var formdata = new window.FormData($form[0]);
        return formdata;
      } else {
        return $form.serialize();
      }
    },

    submit: function ($form, opts) {
      var defaults = {
        cache: false,
        method: $form.attr('method') || 'get'
      };

      if (this.supportsFormData) {
        defaults.processData = false;
        defaults.contentType = false;
      }
      defaults.data = this.get($form, defaults.method);

      opts = $.extend({}, defaults, opts || {});

      $.ajax(opts);
    }
  };
});
