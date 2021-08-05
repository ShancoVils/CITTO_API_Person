
# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'person_manager_db',
        'USER' : 'postgres',
        'PASSWORD' : 'sikurity1399',
        'HOST' : '127.0.0.1',
        'PORT' : '5432',
    }
}

#Email settings

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.mail.ru"
EMAIL_HOST_USER = 'pernens@mail.ru'
EMAIL_HOST_PASSWORD ='shaurma1599'
EMAIL_PORT = 2525
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
DEFAULT_FROM_EMAIL = 'pernens@mail.ru'


ALLOWED_HOSTS = []