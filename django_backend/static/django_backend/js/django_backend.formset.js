define(
    'django_backend.formset',
    [
      'jquery',
      'django_backend.widget'
    ],
    function ($, Widget, undefined) {

  "use strict";

  var FormSet = Widget.subclass({
    constructor: Widget.prototype.constructor,

    init: function () {
      var self = this;
      this.initFormDelete();
      this.initAddAnother();
      this.initSortable();

      // Bind on DOM element to get notified if someone else adds a form.
      this.$element.on('update_form', function () {
        self.updatePosition();
      });
      this.$element.on('add_form', function () {
        self.updatePosition();
      });
    },

    handleDeleteForm: function ($a, e) {
      var $form = $a.closest('.formset-form');
      var $deleteInput = $form.find('input[name$=-DELETE]:first');

      $deleteInput.val("1");
      $form.addClass('delete');
    },

    handleUndoDeleteForm: function ($a, e) {
      var $form = $a.closest('.formset-form');
      var $deleteInput = $form.find('input[name$=-DELETE]:first');

      $deleteInput.val("");
      $form.removeClass('delete');
    },

    initFormDelete: function () {
      var self = this;
      this.$element.on('click', '.form-delete', function (event) {
        self.handleDeleteForm($(this), event);
        return false;
      });
      this.$element.on('click', '.form-undo-delete', function (event) {
        self.handleUndoDeleteForm($(this), event);
        return false;
      });
    },

    initAddAnother: function () {
      var self = this;

      this.$element.on('click', '.add-form', function (e) {
        return self.addAnotherHandler($(this), e);
      });
    },

    getTemplate: function () {
      return this.$element.find('.formset-form.template:first');
    },

    getNewForm: function (formFieldPrefix) {
      var $form = this.getTemplate().clone().removeClass('template');

      var replacePrefix = function (index, attrValue) {
        return attrValue.replace(/__prefix__/, formFieldPrefix);
      };

      $form.find('label').each(function () {
        $(this).attr('for', replacePrefix);
      });

      $form.find(':input').each(function () {
        $(this).attr('name', replacePrefix);
        $(this).attr('id', replacePrefix);
      });

      return $form;
    },

    insertForm: function ($form, $a) {
      // Insert into DOM.
      var $lastForm = this.$element.find('.formset-form:not(.template):last');
      if ($lastForm.length > 0) {
        $lastForm.after($form);
      } else {
        // Add form after template if no other form is present yet.
        this.getTemplate().after($form);
      }
    },

    addAnotherHandler: function ($a, e) {
      var self = this;
      var $formset = self.$element,
          formsetPrefix = $formset.attr('data-formset-prefix'),
          $totalFormsInput = $formset.find(
            '[name=' + formsetPrefix + '-TOTAL_FORMS]'),
          formFieldPrefix = $totalFormsInput.val();

      var $form = self.getNewForm(formFieldPrefix);

      $totalFormsInput.val(function (index, i) {
        return parseInt(i) + 1;
      });

      self.emit('add_form_ready', {
        $form: $form,
        $a: $a,
        $totalFormsInput: $totalFormsInput,
        formFieldPrefix: formFieldPrefix
      });

      self.insertForm($form, $a);

      // Focus first input.
      $form.find(':input:visible:first').focus();

      self.emit('add_form', {$element: $form});

      self.initSortable();

      return false;
    },

    initSortable: function () {
      var self = this;
      var orderField = this.$element.attr('data-order-field');
      if (orderField) {
        this.$element.sortable({
          axis: 'y',
          tolerance: 'pointer',
          items: this.getSortableItems(),
          handle: this.getSortableHandle(),
          update: function () {
            self.emit('update_form');
          }
        });
      } else {
        this.$element.addClass('no-sortable');
      }
    },

    getSortableHandle: function () {
      return '.move';
    },

    getSortableItems: function () {
      return '> .formset-form:not(.template)';
    },
    
    updatePosition: function () {
      var orderField = this.$element.attr('data-order-field');
      var position = 0;
      this.$element.find('.formset-form:not(.template)').each(function () {
          position += 1;
          $(this).find(':input[name$=-' + orderField + ']').val(position);
      });
    }
  });

  return FormSet;

});
