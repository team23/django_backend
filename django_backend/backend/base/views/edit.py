from django.db import models
from django.http import HttpResponseRedirect
from django_backend.backend.views import BackendSingleObjectMixin


class BackendDismissViewMixin(BackendSingleObjectMixin):
    def handle_dismiss(self):
        dismiss = bool(self.request.POST.get('dismiss', False))
        if dismiss:
            return self.dismiss(self.request)

    def get_dismiss_url(self):
        raise NotImplementedError('Should be defined by the subclass')

    def dismiss(self, request, *args, **kwargs):
        return HttpResponseRedirect(self.get_dismiss_url())


class BackendFormViewMixin(BackendDismissViewMixin):
    success_url_name = None

    def post(self, request, *args, **kwargs):
        self.get_object()

        response = self.handle_dismiss()
        if response:
            return response

        form_class = self.get_form_class()
        form = self.get_form(form_class)

        if form.is_valid():
            return self.form_valid(form=form)
        else:
            return self.form_invalid(form=form)

    def get_initial_from_request(self, request):
        """
        Allow users to provide initial data to the form via GET parameters.

        If you have the URL
        ``/backend/1/en/user/add/?first_name=John&is_staff=0``, then the
        initial dictionary passed to the form will be::

            {
                "first_name": "John",
                "is_staff": "0"
            }

        ``ManyToManyFields`` are special-cased. For those you can give a
        comma-separated list of ids. Like:
        ``/backend/1/en/user/add/?groups=1,5,asdf,,32&permissions=``. It will
        become::

            {
                "groups": ["1", "5", "asdf", "", "32"],
                "permissions": [""]
            }
        """

        # Prepare the dict of initial data from the request.
        # We have to special-case M2Ms as a list of comma-separated PKs.
        initial = dict(request.GET.items())
        for k in initial:
            try:
                f = self.backend.model._meta.get_field(k)
            except models.FieldDoesNotExist:
                continue
            if isinstance(f, models.ManyToManyField):
                initial[k] = initial[k].split(",")
        return initial

    def get_initial(self):
        initial = super(BackendFormViewMixin, self).get_initial()
        initial.update(self.get_initial_from_request(self.request))
        initial.update(self.backend.get_form_initial(self.object))
        return initial

    def get_form(self, form_class=None):
        self.form = super(BackendFormViewMixin, self).get_form(form_class)
        self.form_tabs = self.get_form_tabs()
        return self.form

    def get_form_tabs(self):
        return self.backend.get_form_tabs(self.form)

    def get_context_data(self, **kwargs):
        kwargs['form_tabs'] = self.form_tabs
        kwargs['readonly_fields'] = self.backend.get_readonly_fields(
            self.form,
            self.object)
        return super(BackendFormViewMixin, self).get_context_data(**kwargs)
