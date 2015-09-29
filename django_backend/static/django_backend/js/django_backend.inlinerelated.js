define(
    'django_backend.inlinerelated',
    [
      'jquery',
      'stapes',
      'django_backend.ajaxdialog'
    ],
    function ($, Stapes, AjaxDialog, undefined) {

  "use strict";

  var InlineRelated = Stapes.subclass({
    defaults: {},

    constructor: function (element, options) {
      this.$element = $(element);
      this.options = $.extend({}, this.defaults, options);
    },

    init: function () {
      this.bindAddHandler();
      this.bindUpdateHandler();
      this.bindDeleteHandler();
    },

    bindAddHandler: function () {
      var self = this;
      this.$element.on('click', '[data-inline-related-add]', function (e) {
        e.preventDefault();

        var dialog = new AjaxDialog(this, {
          url: $(this).attr('href'),
          width: 880,  // dialog width should be similar to normal content width content area
          height: Math.min(800, $(window).height() - 150),
          parentPageContext: self.options.pageContext
        });

        dialog.on('load', function (data) {
          console.log('GOT inline related', data);
          if (data.action == 'select') {
            self.addObject(data.inline_related);
            dialog.close();
          }
          if (data.action == 'dismiss') {
            dialog.close();
          }
        });

        dialog.open();
        return false;
      });
    },

    bindUpdateHandler: function () {
      var self = this;
      this.$element.on('click', '[data-inline-related-update]', function (e) {
        e.preventDefault();

        var id = $(this).closest('[data-id]').attr('data-id');

        var dialog = new StackedAjaxDialog(this, {
          url: $(this).attr('href'),
          width: 880,  // dialog width should be similar to normal content width content area
          height: Math.min(800, $(window).height() - 150),
          parentPageContext: self.options.pageContext
        });

        dialog.on('load', function (data) {
          if (data.action == 'select') {
            self.updateObject(id, data.inline_related);
            dialog.close();
          }
          if (data.action == 'dismiss') {
            dialog.close();
          }
        });

        dialog.open();
        return false;
      });
    },

    bindDeleteHandler: function () {
      var self = this;
      this.$element.on('click', '[data-inline-related-delete]', function (e) {
        e.preventDefault();

        var id = $(this).closest('[data-id]').attr('data-id');

        var dialog = new StackedAjaxDialog(this, {
          url: $(this).attr('href'),
          width: 880,  // dialog width should be similar to normal content width content area
          height: Math.min(800, $(window).height() - 150),
          parentPageContext: self.options.pageContext
        });

        dialog.on('load', function (data) {
          if (data.action == 'delete') {
            self.deleteObject(id);
            dialog.close();
          }
          if (data.action == 'dismiss') {
            dialog.close();
          }
        });

        dialog.open();
        return false;
      });
    },

    addObject: function (preview) {
        this.$element.find('[data-inline-related-list]').append(preview);
    },

    updateObject: function (id, preview) {
        this.$element.find('[data-id="' + id + '"]').replaceWith(preview);
    },

    deleteObject: function (id) {
        this.$element.find('[data-id="' + id + '"]').remove();
    }
  });

  return InlineRelated;

});
