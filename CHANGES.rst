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
