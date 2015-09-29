define(
    'django_backend.selectrelated',
    [
      'jquery',
      'stapes',
      'django_backend.ajaxdialog'
    ],
    function ($, Stapes, AjaxDialog, undefined) {

  "use strict";

  var SelectRelated = Stapes.subclass({
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
        var dialog = new AjaxDialog(this, {
          url: $(this).attr('href'),
          width: 880,  // dialog width should be similar to normal content width content area
          height: Math.min(800, $(window).height() - 150),
          parentPageContext: self.options.pageContext
        });

        dialog.on('load', function (data) {
          if (data.action == 'select') {
            self.updateField(data.object_id, data.preview);
            dialog.close();
          }
          if (data.action == 'dismiss') {
            dialog.close();
          }
        });

        dialog.open();
        return false;
      });

      this.$element.find('[data-set-null]').on('click', function (e) {
        self.unset();
        return false;
      });
    },

    getPreviewElement: function () {
      return this.$element.find('.preview:first');
    },

    getTriggerElements: function () {
      return this.$element.find('[data-dialog=select-related]');
    },

    updateField: function (objectId, preview) {
      this.$element.find('input').val(objectId);
      var $preview = this.getPreviewElement();
      if (preview) {
        $preview.html(preview);
      } else {
        $preview.html($preview.attr('data-default'));
      }
      if (objectId === null || objectId === "") {
        this.$element.addClass('is-blank');
      } else {
        this.$element.removeClass('is-blank');
      }
    },

    unset: function () {
      this.updateField(null, '');
    }
  });

  return SelectRelated;

});
