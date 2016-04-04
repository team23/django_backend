0.6.0
-----

- Disable form buttons after submit so that user cannot double click a form
  submit button. That should prevent (most) doubled submits. Server side
  validation still needs to be in place though.
- Call the ``attachEventHandlers`` after ``prepareContent`` method in
  ``PartialContentLoader``. That makes extending it easier.
- Previously we found ourselve in confusing situation when multiple modals
  where open and in the top one you clicked the delete button. This opened the
  delete confirmation. If the user then clicked "dismiss" in the confirmation,
  the modal was closed. This was confusing as it was not clear that the top
  modal was closed but the now displaying underlying modal has different data
  in it. In this case a re-displaying the update view would make more sense.

  So we added a way for a modal to go the previous URL (like the browsers go
  back button). If the users triggers now a dismiss action, the modal will go
  one view back in most cases. If there is no previous URL recorded, the modal
  will close. This happens for example if you deep link to the delete view with
  a modal.
- Relation list items now will also have a drag handle and remove icon if the
  relation object cannot be displayed (for example if the content type id is
  not valid). We need to have the remove icon visible, otherwise an object with
  ian nvalid content type cannot be deleted by the user which makes it
  impossible for the user to save the object with the invalid relation.

0.5.0
-----

- The widgets ``GenericRelationListWidget`` and ``M2MListWidget`` feature a
  drop down to add new elements. The list used to link to the relation's
  ``create`` view. We found this to be not useful for all cases, since you
  might want to select existing items.

  We changed the view to be now the ``select`` by default. In general you can
  add new items from the select view then as well with the add button. If you
  don't want to allow selecting new items for one specific backend, you can
  always overwrite the ``select`` view and replace it with for example a
  create view instance.
- Close dropdown when clicking link in *add new* menu in relation list
  widgets.

0.4.3
-----

- Improve styling of bootstrap row template. We integrated a ?-icon for the
  help text and removed whitespace between the label and the ":" after the
  field name.

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
