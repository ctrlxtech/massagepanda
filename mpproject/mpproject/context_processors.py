from django.conf import settings # import the settings file

def prod(context):
    return {'prod': not settings.DEBUG}
