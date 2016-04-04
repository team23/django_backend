define('django_backend.framedcontent', ['jquery', 'django_backend.formdata', 'django_backend.partialcontentloader', 'django_backend.widget'], function ($, formdata, PartialContentLoader, Widget, undefined) {
  "use strict";
  
  var FramedContent = Widget.subclass({
    defaults: $.extend({}, Widget.prototype.defaults, {
      url: null
    }),

    constructor: function (element, options) {
      FramedContent.parent.constructor.apply(this, arguments);
      // We will keep track of the currently active URL if the user followed a
      // link.
      this.url = this.options.url;
    },

    init: function () {
        this.load(this.options.url);
    },

    gotNewContent: function ($content, data) {
      this.$element.empty();
      this.$element.append($content);
    },

    gotNewAction: function (action, data) {
      this.load(this.options.url);
    },

    prepareContent: function ($content) {
      $content = $('<div class="framed-content" />').append($content);
      return $content;
    },

    attachEventHandlers: function ($content) {
      var self = this;

      $content.on('click', 'a', function (e) {
        var $a = $(this);
        var href = $a.attr('href');
        // Do not handle the click if it's a hash.
        if (href.match(/^#/)) {
            return true;
        }
        // Do not handle new window links
        if ($a.attr('target') == '_blank') {
            return true;
        }
        e.preventDefault();
        self.onClickLink($a);
        return false;
      });

      $content.on('submit', 'form', function (e) {
        self.onSubmit($(this));
        return false;
      });

      $content.on('click', 'button', function (e) {
        var $button = $(this);
        var $form = $button.closest('form');
        if ($form.length && $button.attr('type') == 'submit') {
          $form.append($('<input>').attr('type', 'hidden')
            .attr('name', $button.attr('name'))
            .attr('value', $button.attr('value')));
        }
      });
    },

    load: function (url) {
      this.url = url;
      $.ajax(this.url, {
        cache: false,
        dataType: 'json',
        success: this.handleDataResponse.bind(this)
      });
    },

    onClickLink: function ($a) {
      var url = $a.attr('href');
      this.load(url);
    },

    onClickLinkSuccess: function (data) {
        this.handleDataResponse(data);
    },

    onSubmit: function ($form) {
      var self = this;
      formdata.submit($form, {
        url: $form.attr('action') || this.url,
        success: function (data) {
          self.handleDataResponse(data);
        }
      });
      this.emit('submit');
    },
  });

  $.extend(FramedContent.prototype, PartialContentLoader.prototype);

  return FramedContent;
});

