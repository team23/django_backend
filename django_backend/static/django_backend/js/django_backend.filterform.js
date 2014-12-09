define(
    'django_backend.filterform',
    [
      'jquery',
      'django_backend.widget'
    ],
    function ($, Widget, undefined) {

  "use strict";

  var FilterForm = Widget.subclass({
    constructor: Widget.prototype.constructor,

    init: function () {
      var self = this;

      var $toggler = this.$element.find('.filter-form-toggler');
      if(this.$element.hasClass('toggled-compressed')) {
        $toggler.find('.glyphicon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        this.$element.find('.toggled-content').hide();
      }
      if (this.$element.hasClass('toggled-expanded')) {
        $toggler.find('.glyphicon').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        this.$element.find('.toggled-content').show();
      }

      this.$element.on('click', '.filter-form-toggler', function () {
        self.toggle();
      });
    },

    toggle: function () {
      var $toggler = this.$element.find('.filter-form-toggler');
      if(this.$element.hasClass('toggled-compressed')) {
        this.$element.removeClass('toggled-compressed').addClass('toggled-expanded');
        $toggler.find('.glyphicon').removeClass('glyphicon-chevron-down').addClass('glyphicon-chevron-up');
        this.$element.find('.toggled-content').slideDown();
      } else {
        this.$element.removeClass('toggled-expanded').addClass('toggled-compressed');
        $toggler.find('.glyphicon').removeClass('glyphicon-chevron-up').addClass('glyphicon-chevron-down');
        this.$element.find('.toggled-content').slideUp();
      }
    }
  });

  return FilterForm;

});

