define(
    'django_backend.selectall',
    [
      'jquery',
      'django_backend.widget'
    ],
    function ($, Widget, undefined) {

  "use strict";

  var SelectAll = Widget.subclass({
    constructor: Widget.prototype.constructor,

    init: function () {
      var self = this;
      if (this.options.boundary) {
        this.$boundary = $(this.options.boundary);
      } else {
        this.$boundary = this.$element.closest('form');
      }

      this.$element.on('change', function (e) {
        self.toggleCheckboxes($(this).prop('checked'));
      });

      this.$boundary.on('change', this.getCheckboxSelector(), function (e) {
        self.$element.prop('checked', self.areAllChecked());
      });
    },

    toggleCheckboxes: function (checked) {
      this.getCheckboxes().prop('checked', checked);
    },

    /*
     * Returns true if all checkboxes are checked.
     */
    areAllChecked: function () {
      var $checkboxes = this.getCheckboxes();
      if ($checkboxes.length === 0) {
        return false;
      }
      return $checkboxes.length === $checkboxes.filter(':checked').length;
    },

    getCheckboxSelector: function () {
      return this.$element.attr('data-select-all');
    },

    getCheckboxes: function () {
      return this.$boundary.find(this.getCheckboxSelector());
    }
  });

  return SelectAll;
});

