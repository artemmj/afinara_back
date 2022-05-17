CONSTANCE_BACKEND = 'constance.backends.database.DatabaseBackend'

CONSTANCE_CONFIG = {
    'email_about_order': ('info@afinara.ru', 'Куда послать email с информацией о заказе.'),
    'email_feedback': ('info@afinara.ru', 'Куда послать email с фидбеком.'),
    'map_site': ('/', 'Карта сайта'),
}

CONSTANCE_CONFIG_FIELDSETS = {
    'Emails': ('email_about_order', 'email_feedback'),
    'Other': ('map_site',)
}
