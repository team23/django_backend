from django import forms


class NoWidget(forms.HiddenInput):
    '''
    Do not render this field in the template. This is useful if you want to
    grab a that is passed in the POST data but should be a html form field
    itself.

    One usecase is e.g. to get the value of the button that was used to submit
    the form.
    '''

    def render(self, *args, **kwargs):
        return u''
