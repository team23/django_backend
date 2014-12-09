from django_assets import Bundle, register


backend_js = Bundle(
    # Modernizr
    'django_backend/libs/modernizr/modernizr.js',

    # jQuery
    'django_backend/libs/jquery/dist/jquery.min.js',
    'django_backend/libs/jquery-ui/ui/minified/jquery-ui.min.js',
    'django_backend/js/jquery.django-csrf.js',

    # Bootstrap
    'django_backend/libs/bootstrap-sass/dist/js/bootstrap.min.js',
    'django_backend/libs/bootstrap-tab-history/vendor/assets/javascripts/bootstrap-tab-history.js',

    # Stapes
    'django_backend/libs/stapes/stapes.min.js',

    # RequireJS
    'django_backend/libs/requirejs/require.js',
    'django_backend/js/require-init.js',

    # Backend
    'django_backend/js/django_backend.widget.js',
    'django_backend/js/django_backend.dialog.js',
    'django_backend/js/django_backend.ajaxdialog.js',
    'django_backend/js/django_backend.selectall.js',
    'django_backend/js/django_backend.instantsubmit.js',
    'django_backend/js/django_backend.pagecontext.js',
    'django_backend/js/django_backend.filterform.js',
    'django_backend/js/django_backend.forms.js',
    'django_backend/js/django_backend.formset.js',
    'django_backend/js/django_backend.stackedajaxdialog.js',
    'django_backend/js/django_backend.opendialog.js',
    'django_backend/js/django_backend.selectrelated.js',
    'django_backend/js/django_backend.inlinerelated.js',
    # 'django_backend/js/main.js',
    'django_backend/js/init.js',

    filters='jsmin',
    output='django_backend/assets/backend.js')
register('backend.js', backend_js)


backend_css = Bundle(
    'django_backend/css/jquery-ui.css',
    'django_backend/css/django_backend.css',

    filters='cssmin',
    output='django_backend/assets/backend.css')
register('backend.css', backend_css)
