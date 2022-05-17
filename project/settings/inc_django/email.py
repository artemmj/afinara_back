from ..common import env

EMAIL_HOST = env('EMAIL_HOST', str, '')
EMAIL_PORT = env('EMAIL_PORT', str, '')
EMAIL_HOST_USER = env('EMAIL_HOST_USER', str, '')
EMAIL_HOST_PASSWORD = env('EMAIL_HOST_PASSWORD', str, '')
EMAIL_USE_SSL = env('EMAIL_USE_SSL', bool, True)
