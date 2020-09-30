# Internationalization

Standard i18n using django's gettext, static strings are marked with the
translation function, and database strings (such as movement categories
descriptions) are translated through a serializer method field

When a new string is added there is a catch. You have to recompile the .po
file and then add any additional changes needed. After that, check with a
diff tool to reverse any changes not intended, since django will comment every
manually added entry, thus invalidating all the entries needed for the
serializer method fields.

### Activation

To enable i18n the important bits on the settings.py file are:

* Import gettext

    
    from django.utils.translation import gettext_lazy as _

* Add the configuration variables, for example:

    
    LOCALE_PATHS = [
        os.path.join(BASE_DIR, 'locale'),
    ]
    
    LANGUAGE_CODE = 'en-us'

    LANGUAGES = [
        ('es', _('Spanish')),
        ('en', _('English')),
    ]
    
    TIME_ZONE = 'UTC'
    
    USE_I18N = True
    
    USE_L10N = True
    
Then, to use it, create the _locale_ folder and make the file for the languages

    django-admin makemessages -l es
    
After that, edit the file and compile

    django-admin compilemessages
