0.4.2
-----

- Validate selected elements in ``GenericRelationListField`` against the
  allowed content types. That makes sure no unwanted objects end up in the
  list.
- Allow name of generic foreign key field to be set explicitly in
  ``GenericRelationListField``. You can use the ``generic_fk_name`` argument
  for this.
- Adding or changing a new item in a ``GenericRelationListField`` will also
  update the edit link based on the update url in the JSON response.
- JavaScript: The PageContext got the capability to watch the element that
  represents the page context in the DOM. That allows us to close obsolete
  tooltips even if their original trigger got already removed from the page.
- JavaScript: The pagecontext element gets the data-pagecontext attribute to
  make it queryable.
- JavaScript: Bootstrap tooltips are now attached to pagecontext elements
  instead of the body. That will better capsulate them into the pagecontext.

0.4.1
-----

- Make ``GenericRelationListField`` determine the names of the ``object_id``
  and ``content_type`` fields by inspecting the used ``GenericForeignKey``.
  That will raise errors about wrong usage earlier.

- Fix JS for ``GenericRelationListField`` if used nested multiple levels deep.
  A click handler was called in every instance in the modal stack, so the
  behaviour was different depending on the number of modals.

0.4.0
-----

- Fix ``GenericRelationListField``. It's internal API was not used correctly
  and therfore just threw errors.

- Allow ``SelectRelatedField`` to pick up inline backends, searching from
  currently active backend. That makes it easier to use customized nested
  inline backends.

0.3.0
-----

* Adjusted multiple imports:

  - Forms, formfields and widgets should be now always imported from
    ``django_backend.forms``. Example::

    # OLD import, will no longer work
    from django_backend.backend.base.formfields import SelectRelatedField

    # NEW import
    from django_backend.forms import SelectRelatedField

* Add ``ManageRelatedField`` that can inline a list page of a related model
  in the change view.

* Add ``GenericRelationListField`` that can show a reorderable list related
  by a intermediary model with a generic foreign key.

* Use Django's app config to make autoloading of backends predictable.

* Ensuring support for Django 1.6 and 1.8.

* Integrating bootstrap styles for floppyforms widgets.

* Disable caching for backend views.

* Allow subclasses of ``FilterForm`` to define ``filter_queryset_{field_name}``
  methods for easy extendability.

0.1.0
-----

* Initial release.
