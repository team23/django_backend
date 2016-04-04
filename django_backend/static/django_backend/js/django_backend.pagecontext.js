define(
    'django_backend.pagecontext',
    [
      'jquery',
      'stapes',
      'django_backend.selectall',
      'django_backend.instantsubmit',
      'django_backend.filterform',
      'django_backend.forms',
      'django_backend.formset',
      'django_backend.inlinerelated',
      'django_backend.managerelated',
      'django_backend.selectrelated',
      'django_backend.relationlistfield',
      'django_backend.opendialog'
    ], function (
      $,
      Stapes,
      SelectAll,
      InstantSubmit,
      FilterForm,
      forms,
      FormSet,
      InlineRelated,
      ManageRelated,
      SelectRelated,
      RelationListField,
      opendialog) {

  "use strict";


  function isInDom($element) {
    // Fastes way to check if an element is still in the DOM.
    // See here for details: http://jsperf.com/jquery-element-in-dom/2
    return $.contains(document.documentElement, $element[0]);
  }


  var PageContext = Stapes.subclass({
    defaults: {},

    constructor: function (parent, options) {

      // The PageContext is responsible for everything inside this element.
      this.$element = null;
      this.parent = parent;

      this.options = $.extend(
        {},
        this.defaults,
        // Inherit options from the parent as well.
        parent ? parent.options : {},
        options);

      this._watchers = [];
      this._watchDelay = 200;
      this._watchInterval = null;
    },

    /*
     * Add a new watcher for this page context. The watchers are supposed to
     * health check parts of the page context.
     */
    addWatcher: function (watcher) {
      this._watchers.push(watcher);
    },

    startWatcher: function () {
      if (this._watchInterval === null) {
        this._watchInterval = setInterval(this.watch.bind(this), this._watchDelay);
      }
    },

    stopWatcher: function () {
      clearInterval(this._watchInterval);
      this._watchInterval = null;
    },

    /*
     * Walks through all watchers and calls them once.
     *
     * It will stop the watch interval if this page context is no longer in
     * the DOM.
     */
    watch: function () {
      this._watchers.forEach(function (watcher) {
        watcher(this.$element);
      }.bind(this));

      if (!isInDom(this.$element)) {
        this.stopWatcher();
      }
    },

    /*
     * Takes care of checking if a tooltip trigger is still in the DOM. If
     * it's not the case, we close the according tooltip. Reason is that
     * otherwise an open tooltip will stay there forever if the trigger element
     * gets removed, for example by closing a modal (with ESC) that contains
     * the element.
     */
    watchTooltip: function ($element) {
      var $tooltips = $element.find('[data-toggle="tooltip"]');
      $tooltips.each(function () {
        var $tooltip = $(this);
        if (!isInDom($tooltip)) {
          $tooltip.tooltip('destroy');
        }
      });
    },

    init: function ($element) {
      // Set the $element late, that's needed if it's not yet
      // available during creation.
      if ($element !== undefined) {
        this.$element = $element;
      }
      var self = this;

      this.$element.attr('data-pagecontext', '');

      // Initialize bootstrap widgets.
      this.$element.find('[data-toggle="tooltip"]').tooltip({
        html: true,
        container: '[data-pagecontext]',
      });
      this.addWatcher(this.watchTooltip.bind(this));

      this.$element.find('[data-toggle="popover"]').popover({html: true});
      this.$element.find('[data-toggle="dropdown"]').dropdown();

      // Initialize forms.
      forms.init(this.$element);

      // Initialize the filter forms.
      this.$element.find('.filter-form').each(function () {
          var widget = new FilterForm(this);
          widget.init();
      });

      // Initialize the formsets.
      this.$element.find('.formset').each(function () {
          var formSet = new FormSet(this);
          formSet.init();
          // Make sure to initialize new context around added forms.
          formSet.on('add_form', function (data, e) {
            self.inherit().init(data.$element);
          });
      });

      // Initialize inline related.
      this.$element.find('[data-inline-related]').each(function () {
        var inlineRelated = new InlineRelated(this, {
          pageContext: self
        });
        inlineRelated.init();
      });

      // Initialize select related fields.
      this.$element.find('[data-manage-related]').each(function () {
        var manageRelated = new ManageRelated(this, {
          pageContext: self
        });
        manageRelated.init();
      });

      // Initialize select related fields.
      this.$element.find('.select-related-field').each(function () {
        var selectRelated = new SelectRelated(this, {
          pageContext: self
        });
        selectRelated.init();
      });

      // Initialize select related fields.
      this.$element.find('.relation-list-field').each(function () {
        var relationListField = new RelationListField(this, {
          pageContext: self
        });
        relationListField.init();
      });

      // Initialize select all checkbox.
      this.$element.find('[data-select-all]').each(function () {
          var selectAll = new SelectAll(this, {
            boundary: self.$element
          });
          selectAll.init();
      });

      // Initialize instant submit fields.
      this.$element.find('.instant-submit').each(function () {
          var instantSubmit = new InstantSubmit(this, {pageContext: self});
          instantSubmit.init();
      });

      opendialog.init(this);

      this.startWatcher();
    },

    inherit: function (options) {
      return new PageContext(this, options);
    },

    prepareUrl: function (url) {
      var params = {};
      if (params) {
        if (url.match(/\?/))
          url = url + '&' + $.param(params);
        else
          url = url + '?' + $.param(params);
      }
      return url;
    }
  });

  // Shortcut to initialize an element more easily.
  PageContext.init = function ($element) {
    var pageContext = new PageContext();
    pageContext.init($element);
  };

  return PageContext;

});
