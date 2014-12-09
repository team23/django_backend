define('django_backend.widget', ['jquery', 'stapes'], function ($, Stapes, undefined) {
  "use strict";

  /**
   * A base class for all ui widgets. It provides a few stub methods to define
   * a common interface that can be used by subclasses.
   */

  var Widget = Stapes.subclass({
    defaults: {},
    eventNamespace: null,

    /**
     * This constructor defines a common signature that all widgets should
     * follow if possible.
     *
     * First element is always a DOM element that this widget is attached to.
     *
     * Second argument is a object that contains configuration. The class may
     * have a ``defaults`` attribute that will hold default options.
     */
    constructor: function (element, options) {
      this.$element = $(element);
      this.options = $.extend({}, this.defaults, options);
    },

    /**
     * The ``create`` method shall attach the ``$element`` to the DOM and
     * trigger the ``create`` event.
     */
    create: function () {
      this.emit('create');
    },

    /**
     * The ``destroy`` method shall be called to cleanup all bound DOM event
     * handlers and remove the ``$element`` from the DOM. After everything is
     * successfully cleanedup, it shall emit the ``destroy`` event.
     */
    destroy: function () {
      this.emit('destroy');
    },

    /**
     * Call jQuery's trigger method for events that are emitted on this class.
     * The jQuery event will have the namespace 'widget' and what ever is in
     * the classes ``eventNamespace`` attribute.
     *
     * So if you call ``this.emit('click');`` it will trigger the jquery event
     * ``'click.widget'``. See http://api.jquery.com/on/ for details on jQuery
     * event namespaces.
     *
     * The widget itself is always passed as ``widget`` property on the data
     * object to the event handler.
     */
    emit: function (types, data) {
      if (data === undefined) {
        data = {};
      }

      // Always attach the widget itself to the data that is passed down to
      // event handlers.
      if (typeof data === 'object' && data.widget === undefined) {
        data.widget = this;
      }

      Widget.parent.emit.call(this, types, data);
      if (this.$element !== undefined && this.$element !== null) {
        // The binding to namespace does not really work.
        /*
        types = types + '.widget';
        if (this.eventNamespace) {
          types = types + '.' + this.eventNamespace;
        }
        */
        this.$element.trigger(types, data);
      }
    }
  });

  return Widget;
});
