define(
    'django_backend.instantsubmit',
    [
      'jquery',
      'django_backend.widget'
    ],
    function ($, Widget, undefined) {

  "use strict";

  var InstantSubmit = Widget.subclass({
    constructor: Widget.prototype.constructor,

    init: function () {
      var self = this;

      this.getTriggerElements().on('change', function (e) {
        self.$element.closest('form').submit();
      });
    },

    getTriggerElements: function () {
      if (this.$element.is('form')) {
        return this.$element.find(':input');
      } else {
        return this.$element;
      }
    }
  });

  return InstantSubmit;
});

