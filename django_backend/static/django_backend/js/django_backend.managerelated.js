define(
    'django_backend.managerelated',
    [
      'jquery',
      'stapes',
      'django_backend.stackedajaxdialog'
    ],
    function ($, Stapes, StackedAjaxDialog, undefined) {

  "use strict";

  var ManageRelated = Stapes.subclass({
    defaults: {},

    constructor: function (element, options) {
      this.$element = $(element);
      this.options = $.extend({}, this.defaults, options);
    },

    init: function () {
      var self = this;

      var $preview = this.getPreviewElement();
      if ($preview.is(':empty')) {
        $preview.html($preview.attr('data-default'));
      }

      this.getTriggerElements().on('click', function (e) {
        var dialog = new StackedAjaxDialog(this, {
          url: $(this).attr('href'),
          width: 880,  // dialog width should be similar to normal content width content area
          height: Math.min(800, $(window).height() - 150),
          parentPageContext: self.options.pageContext
        });

        dialog.on('load', function (data) {
          if (data.action == 'dismiss' || data.action == 'select' || data.action == 'delete') {
            dialog.close();
          }
        });

        dialog.on('destroy', function () {
            self.updatePreview();
        });

        dialog.open();
        return false;
      });
    },

    getPreviewElement: function () {
      return this.$element.find('.preview:first');
    },

    getTriggerElements: function () {
      return this.$element.find('[data-dialog=manage-related]');
    },

    updatePreview: function () {
      var self = this;
      var url = this.getTriggerElements().attr('href');
      $.getJSON(url, function (data) {
        var $preview = self.getPreviewElement();
        if (data.preview) {
          $preview.html(data.preview);
        } else {
          $preview.html($preview.attr('data-default'));
        }
      });
    }
  });

  return ManageRelated;

});
