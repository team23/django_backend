define(
    'django_backend.stackedajaxdialog',
    [
      'jquery',
      'django_backend.ajaxdialog'
    ], function ($, AjaxDialog, undefined) {

  "use strict";

  var StackedAjaxDialog = AjaxDialog.subclass({
    constructor: function () {
      StackedAjaxDialog.parent.constructor.apply(this, arguments);
      this.pageContext = this.options.parentPageContext.inherit();
    },

    handleResponse: function (data) {
      StackedAjaxDialog.parent.handleResponse.call(this, data);
      var contextOptions = {};
      var parentPageContext = this.options.parentPageContext;
      this.pageContext = parentPageContext.inherit(contextOptions);
    },

    prepareContent: function (content) {
      var $content = StackedAjaxDialog.parent.prepareContent.call(this, content);

      this.pageContext.init($content);

      return $content;
    },

    load: function (url, success) {
      url = this.pageContext.prepareUrl(url);
      StackedAjaxDialog.parent.load.call(this, url, success);
    }
  });

  return StackedAjaxDialog;

});
