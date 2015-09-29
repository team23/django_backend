define('django_backend.partialcontentloader', ['jquery'], function ($) {
    "use strict";

    function PartialContentLoader() {

    }

    PartialContentLoader.prototype.handleDataResponse = function (data) {
      if (data.status !== 'ok') {
        console.error('Error response: ', data);
        return;
      }

      this.emit('load', data);

      if (data.html) {
        this.pageContext = this.options.parentPageContext.inherit();
        var $content = this.initContent(data.html);
        this.gotNewContent($content, data);
      }
    };

    PartialContentLoader.prototype.getNewPageContext = function (options) {
        return this.options.parentPageContext.inherit(options);

    };

    PartialContentLoader.prototype.initContent = function (content) {
        var $content = $(content);
        if (this.prepareContent) {
            $content = this.prepareContent($content);
        }
        var pageContext = this.getNewPageContext();
        pageContext.init($content);
        return $content;
    };

    return PartialContentLoader;

});
