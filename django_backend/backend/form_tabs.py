from .renderable import Renderable


class BaseFormElement(Renderable):
    def __init__(self, template_name=None, position=0):
        self.position = position
        super(BaseFormElement, self).__init__(template_name=template_name)

    def resolve_help_text(self, context):
        return None

    @property
    def states(self):
        """
        A helper so that you can call in the template::

            {% render tab.states %}
        """
        tab = self

        class RenderableStates(object):
            def render(self, context=None):
                return ' '.join(tab.get_states(context))

        return RenderableStates()

    def get_states(self, context):
        """
        Return a list of states that this element is in. This could be ``error``
        for example if a containing field has an error. Those states can be
        added as css classes to the template. You can then use those to style it
        accordingly.

        Where and whether the css classes are added to the template is up the
        the subclass like tabs, rows, etc.
        """
        return []


class FormTab(BaseFormElement):
    template_name = 'django_backend/formlayout/table.html'

    def __init__(self, name, rows, *args, **kwargs):
        self.name = name
        self._rows = map(self._initialize_row, rows)
        super(FormTab, self).__init__(*args, **kwargs)

    def add_row(self, row):
        self._rows.append(self._initialize_row(row))
        # Make calls chainable.
        return self

    def _initialize_row(self, row):
        if isinstance(row, dict):
            return FormRow(row.get('label', ''), row.get('fields', []))
        # TODO: Add possibility to just add field list directly
        # (row should be created on the fly, using the first field label)
        if isinstance(row, list):
            return FormRow(None, row)

        return row

    def resolve_has_error(self, context):
        """
        Return ``True`` if one of the containing rows contains an form
        validation error.
        """
        return any(
            row.resolve_has_error(context)
            for row in self._rows
            if hasattr(row, 'resolve_has_error'))

    def get_states(self, context):
        states = list(super(FormTab, self).get_states(context))
        if self.resolve_has_error(context):
            states += ['has-error']
        return states

    def get_context_data(self, context, **kwargs):
        kwargs.update({
            'tab': self,
            'tab_rows': self.rows,
        })
        return super(FormTab, self).get_context_data(context, **kwargs)

    @property
    def rows(self):
        return list(sorted(self._rows, cmp=lambda x,y: cmp(x.position, y.position)))

    @property
    def fields(self):
        fields = []
        for row in self.rows:
            fields = fields + row.fields
        return fields


class FormRow(BaseFormElement):
    template_name = 'django_backend/formlayout/tr.html'

    def __init__(self, label, fields, help_text=None, *args, **kwargs):
        self.label = label
        self._fields = map(self._initialize_field, fields)
        self.help_text = help_text
        super(FormRow, self).__init__(*args, **kwargs)

    def add_field(self, field):
        self._fields.append(self._initialize_field(field))
        # Make calls chainable.
        return self

    def _initialize_field(self, field):
        if isinstance(field, basestring):
            return FormField(field)
        return field

    def resolve_has_error(self, context):
        """
        Return ``True`` if one of the containing fields contains an form
        validation error.
        """
        return any(
            field.resolve_has_error(context)
            for field in self._fields
            if hasattr(field, 'resolve_has_error'))

    def get_states(self, context):
        states = list(super(FormRow, self).get_states(context))
        if self.resolve_has_error(context):
            states += ['has-error']
        return states

    def resolve_default_label(self, context):
        if self.label:
            return self.label
        if len(self.fields) == 1:
            return self.fields[0].resolve_label(context)
        return ''

    def resolve_help_text(self, context):
        if self.help_text:
            return self.help_text
        if len(self.fields) == 1:
            return self.fields[0].resolve_help_text(context)
        return ''

    def resolve_required(self, context):
        return any(f.resolve_required(context) for f in self._fields)

    def get_context_data(self, context, **kwargs):
        kwargs.update({
            'row': self,
            'row_label': self.resolve_default_label(context),
            'row_fields': self.fields,
            # I think that's not required anymore.
            #'row_form_fields': [f.resolve_field(context) for f in self.fields],
            'row_help_text': self.resolve_help_text(context),
            'row_required': self.resolve_required(context),
        })
        return kwargs

    @property
    def fields(self):
        return list(sorted(self._fields,
                           cmp=lambda x, y: cmp(x.position, y.position)))

    def field_names(self):
        return [field.field for field in self.fields]


class FormField(BaseFormElement):
    template_name = 'django_backend/formlayout/field.html'

    def __init__(self, field, *args, **kwargs):
        self.field = field
        super(FormField, self).__init__(*args, **kwargs)

    def get_states(self, context):
        states = list(super(FormField, self).get_states(context))
        if self.resolve_has_error(context):
            states += ['has-error']
        return states

    def resolve_has_error(self, context):
        field = self.resolve_field(context)
        if field and hasattr(field, 'errors'):
            return bool(field.errors)
        return False

    def resolve_form(self, context):
        if 'form' in context:
            return context['form']

    def resolve_field(self, context):
        form = self.resolve_form(context)
        if form is None:
            return  # we need the form to exists
        try:
            return form[self.field]
        except KeyError:
            return

    def resolve_label(self, context):
        return self.resolve_field(context).label

    def resolve_help_text(self, context):
        return self.resolve_field(context).help_text

    def resolve_required(self, context):
        return self.resolve_field(context).field.required

    def get_context_data(self, context, **kwargs):
        form_field = self.resolve_field(context)
        kwargs.update({
            'field': self,
            'field_name': self.field,
            'field_form_field': form_field,
        })
        return super(FormField, self).get_context_data(context, **kwargs)

    def render(self, context):
        form_field = self.resolve_field(context)
        if form_field is None:
            return ''
        return super(FormField, self).render(context)
