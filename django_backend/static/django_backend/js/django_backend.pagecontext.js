define(
    'django_backend.pagecontext',
    [
      'jquery',
      'stapes',
      'django_backend.selectall',
      'django_backend.instantsubmit',
      'django_backend.filterform',
      'django_backend.formset',
      'django_backend.inlinerelated',
      'django_backend.managerelated',
      'django_backend.selectrelated',
      'django_backend.opendialog'
    ], function (
      $,
      Stapes,
      SelectAll,
      InstantSubmit,
      FilterForm,
      FormSet,
      InlineRelated,
      ManageRelated,
      SelectRelated,
      opendialog) {

  "use strict";

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
    },

    init: function ($element) {
      // Set the $element late, that's needed if it's not yet
      // available during creation.
      if ($element !== undefined) {
        this.$element = $element;
      }
      var self = this;

      // Initialize bootstrap widgets.
      this.$element.find('[data-toggle="tooltip"]').tooltip({html: true, container: 'body'});
      this.$element.find('[data-toggle="popover"]').popover({html: true});
      this.$element.find('[data-toggle="dropdown"]').dropdown();

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
      this.$element.find('.manage-related-field').each(function () {
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
    },

    inherit: function (options) {
      return new PageContext(this, options);
    },

    prepareUrl: function (url) {
      var params = {};
      if (this.options.lock) {
        params.lock = this.options.lock;
      }
      if (this.options.objectLock) {
        params.object_lock = this.options.objectLock;
      }
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
