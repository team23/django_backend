define('django_backend.dialog', ['jquery', 'stapes', 'django_backend.widget', 'django_backend.partialcontentloader'], function ($, Stapes, Widget, PartialContentLoader, undefined) {
  "use strict";

  /**
   * The dialog's $element attribute is the element that is clicked to open
   * the dialog. In most cases this will be a link.
   */

  var Dialog = Widget.subclass({
    defaults: {
      title: null,
      content: '',
      width: 800,
      height: 'auto'
    },
    eventNamespace: 'dialog',

    constructor: function (element, options) {
      options = $.extend({}, options, {
        id: 'dialog-' + Stapes._.makeUuid()
      });

      Dialog.parent.constructor.call(this, element, options);
      this.$dialog = $('<div id="' + this.options.id + '" />');
    },

    isOpen: function () {
      return $.contains(document, this.$dialog[0]);
    },

    /**
     * This method gets a raw string and should return a jQuery element. It is
     * called before the content is attached to the DOM. Use it to setup
     * necessary event handlers for the content etc.
     *
     * We wrap the content into a div to make it possible to apply a
     * $content.find('...') that will find top level elements. Otherwise you
     * would need to write this to find all forms:
     *
     *   $content.filter('form').add($content.find('form'));
     *
     * This method should only take care of representational stuff. Event
     * handling should be done in `attachEventHandlers`.
     *
     */
    prepareContent: function ($content) {
      $content = $('<div class="dialog-content" />').append($content);
      return $content
    },

    /*
     * Event handlers should not be registered in `prepareContent` as we want
     * more control in subclasses if we want to register the new event handlers
     * before or after the existing ones.
     */
    attachEventHandlers: function ($content) {

    },

    prepareDialog: function (title, $content) {
      this.$dialog.attr('title', title);

      this.$dialog.empty();
      this.$dialog.append($content);
    },

    create: function (title, $content) {
      var self = this;

      this.prepareDialog(title, $content);
      this.emit('load');

      var body_width = $('body').width();
      this.dialog_width = body_width*0.9;
      if (!this.dialog_width || this.dialog_width > this.options.width)
        this.dialog_width = this.options.width;

      $('body').append(this.$dialog);
      this.$dialog.dialog({
        resizable: false,
        width: this.dialog_width,
        height: this.options.height,
        modal: true,
        close: function (event, ui) {
          self.destroy();
        }
      });

      this._reinit_for_responsive();
      this.$dialog.find('img').bind('load', function(){
        self._reinit_for_responsive();
      });
      $(window).bind('previewChanged.gallery.stemmer', function(e){
        self._reinit_for_responsive();
      });

      Dialog.parent.create.call(this);
    },

    _reinit_for_responsive: function() {
      var self = this;

      var body_width = $('body').width();
      var body_height = window.innerHeight;
      var $parent = this.$dialog.parent();
      var $titelbar = $parent.find('.ui-dialog-titlebar');

      this.dialog_max_height = body_height*0.9;

      var border_tb_width = parseInt($parent.css('border-top-width')) + parseInt($parent.css('border-bottom-width'));
      $parent.css('max-height', this.dialog_max_height);
      $parent.css('top', (body_height-$parent.height()-border_tb_width)/2);
      $parent.css('position', 'fixed');
      this.$dialog.css('max-height', (this.dialog_max_height - $titelbar.height()) - (parseInt($titelbar.css('padding-top')) + parseInt($titelbar.css('padding-bottom'))));

      if ($parent.height() >= this.dialog_max_height) {
        $parent.css('height', this.dialog_max_height);
        $parent.css('top', (body_height-$parent.height()-border_tb_width)/2);
        this.$dialog.css('height', (this.dialog_max_height - $titelbar.height()) - (parseInt($titelbar.css('padding-top')) + parseInt($titelbar.css('padding-bottom'))));
      }

      $(window).on('resize', function (e) {
        body_width = $('body').width();
        body_height = window.innerHeight;

        var dialog_width = body_width*0.9;
        if (dialog_width) {
          if (dialog_width > self.options.width)
            dialog_width = self.options.width;
          if (dialog_width != self.dialog_width) {
            self.dialog_width = dialog_width;
            $parent.width(self.dialog_width);
          }
          var border_lr_width = parseInt($parent.css('border-left-width')) + parseInt($parent.css('border-right-width'));
          $parent.css('left', (body_width-dialog_width-border_lr_width)/2);
        }

        var dialog_max_height = body_height*0.9;
        if (dialog_max_height) {
          if (dialog_max_height != self.dialog_max_height) {
            self.dialog_max_height = dialog_max_height;
            var border_tb_width = parseInt($parent.css('border-top-width')) + parseInt($parent.css('border-bottom-width'));
            $parent.css('max-height', self.dialog_max_height);
            $parent.css('top', (body_height - $parent.height() - border_tb_width) / 2);
            self.$dialog.css('max-height', (self.dialog_max_height - $titelbar.height()) - (parseInt($titelbar.css('padding-top')) + parseInt($titelbar.css('padding-bottom'))));

            $parent.css('height', 'auto');
            self.$dialog.css('height', 'auto');
            if ($parent.height() >= self.dialog_max_height) {
              $parent.css('height', self.dialog_max_height);
              $parent.css('top', (body_height-$parent.height()-border_tb_width)/2);
              self.$dialog.css('height', (self.dialog_max_height - $titelbar.height()) - (parseInt($titelbar.css('padding-top')) + parseInt($titelbar.css('padding-bottom'))));
            }
          }
        }
      });
    },

    destroy: function () {
      this.$dialog.dialog('destroy');
      this.$dialog.detach();
      Dialog.parent.destroy.call(this);
    },

    open: function () {
      var $content = this.initContent(this.options.content);
      this.create(
        this.options.title,
        $content);
      this.emit('open');
    },

    close: function () {
      this.destroy();
      this.emit('close');
    }
  });

  $.extend(Dialog.prototype, PartialContentLoader.prototype);

  return Dialog;
});
