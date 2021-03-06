import socket
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent
ENV_FILE_PATH = BASE_DIR / '.env'

env = environ.Env()
environ.Env.read_env(env_file=str(ENV_FILE_PATH))


SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG', default=False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.postgres',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'debug_toolbar',
    'django_extensions',

    'accounts.apps.AccountsConfig',
    'home.apps.HomeConfig',
    'language_tests.apps.LanguageTestsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'test_your_language.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'test_your_language.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': env.str('DB_ENGINE'),
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': env.str('DB_HOST'),
        'PORT': env.int('DB_PORT'),
    }
}

LOGIN_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.AllowAllUsersModelBackend',
)

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = env.str('LANGUAGE_CODE')

TIME_ZONE = env.str('TZ')

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_DIR = BASE_DIR / 'static'
STATICFILES_DIRS = [STATIC_DIR, ]


ip = socket.gethostbyname(socket.gethostname())
INTERNAL_IPS = ['127.0.0.1', ip[:-1] + '1', ]


CELERY_BROKER_URL = env.str('CELERY_BROKER_URL')
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = env.str('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json', ]
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = env.str('TZ')


EMAIL_BACKEND = env.str('EMAIL_BACKEND')
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_PORT = env.int('EMAIL_PORT')
EMAIL_USE_SSL = True


ACTIVATION_LINK_LIFETIME = env.int(
    'ACTIVATION_LINK_LIFETIME',
    default=(60 * 60 * 24)  # 24 h.
)
