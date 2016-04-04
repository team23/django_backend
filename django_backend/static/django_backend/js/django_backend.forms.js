define('django_backend.forms', ['jquery'], function ($, undefined) {
  "use strict";

  var ENTER_KEY = 13;

  return {
    handleDefaultButtons: function ($target) {
        $target.on('keypress', 'form input', function (e) {
            if (e.which == ENTER_KEY) {
                var $form = $(this).parents('form:first');
                var $defaultButton = $form.find('[type=submit].default');
                if ($defaultButton.length) {
                    $defaultButton.click();
                    return false;
                }
            }
        });
    },

    /*
     * We want to prevent multiple submitts for the same form. We therefore
     * intercept the submit event and remember if it has already been called.
     * If so, we prevent the second submit event to propagate to other
     * handlers and stop the browser to handle it as well.
     *
     * We also disable the submit buttons when clicking them the first time.
     * This will show the user that a second click will have no effect.
     *
     * Disabling a button has the effect, that the name/value pair of the
     * clicked button will not be submitted with the form. We therefore need
     * to fake this browser behaviour by adding a hidden input field with the
     * same name/value values.
     */
    disableMultipleSubmits: function ($target) {
      $target.on('submit', 'form', function (e) {
        var $form = $(this);
        if ($form.data('isSubmitted')) {
          e.preventDefault();
          e.stopImmediatePropagation();
          return false;
        } else {
          $form.data('isSubmitted', true);
          $form.find('button, input[type=submit]').each(function () {
            var $this = $(this);
            // We can identify the clicked button by ':focus'.
            if ($this.is(':focus') && $this.is('[name]')) {
              var $hidden = $('<input type="hidden" />');
              $hidden.attr('name', $this.attr('name'));
              $hidden.attr('value', $this.attr('value'));
              $this.after($hidden);
            }

            this.disabled = true;
          });
        }
      });
    },

    init: function ($target) {
      this.handleDefaultButtons($target);
      this.disableMultipleSubmits($target);
    }
  };
});
