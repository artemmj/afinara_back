LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] [%(levelname)8s]: %(message)s',
        },
        'simple': {
            'format': '[{levelname}]: {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console_default': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
            'level': 'DEBUG',
        },
        'console_info': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
            'level': 'DEBUG',
        },
    },
    'loggers': {
        'django_info': {
            'handlers': ['console_default'],
            'level': 'INFO',
        },
        'django_errors': {
            'handlers': ['console_default'],
            'level': 'ERROR',
        },
    },
}
