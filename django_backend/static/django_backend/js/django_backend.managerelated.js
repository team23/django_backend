define(
    'django_backend.managerelated',
    [
      'jquery',
      'stapes',
      'django_backend.framedcontent',
      'django_backend.ajaxdialog'
    ],
    function ($, Stapes, FramedContent, AjaxDialog, undefined) {

  "use strict";

  var ManageRelatedContent = FramedContent.subclass({
    constructor: function (element, options) {
        ManageRelatedContent.parent.constructor.apply(this, arguments);
    },

    prepareContent: function ($content) {
      $content = ManageRelatedContent.parent.prepareContent.call(this, $content);
      $content.find('h1').remove();
      return $content;
    },

    onClickLink: function ($a) {
      var url = $a.attr('href');

      var originalPath = this.options.url.split(/\?/)[0].trim();
      var newPath = url.split(/\?/)[0].trim();

      // If we stick to the same url (maybe with different parameters) we
      // reload the framed content. This might be the case for pagination links
      // or sorting links.
      //
      // If it's changing the path we assume it's some change of the nesting
      // like "edit this" or "add that" so we open a modal.
      if (originalPath === newPath) {
        this.load(url);
      } else {
        var dialog = new AjaxDialog($a, {
            url: url,
            width: 880,  // dialog width should be similar to normal content width content area
            height: Math.min(800, $(window).height() - 150),
            parentPageContext: this.options.parentPageContext.inherit()
          });

        dialog.on('load', function (data) {
          if (data.action) {
            dialog.close();
            this.load(this.options.url);
          }
        }.bind(this));

        dialog.open();
      }
      return false;
    }
  });

  var ManageRelated = Stapes.subclass({
    defaults: {},

    constructor: function (element, options) {
      this.$element = $(element);
      this.options = $.extend({}, this.defaults, options);
      this.pageContext = this.options.pageContext;
    },

    init: function () {
      var self = this;

      this.url = this.$element.attr('data-manage-related');

      this.framedContent = new ManageRelatedContent(this.$element, {
          url: this.url,
          parentPageContext: this.options.pageContext
      });
      this.framedContent.init();

      return;
    }
  });

  return ManageRelated;

});
