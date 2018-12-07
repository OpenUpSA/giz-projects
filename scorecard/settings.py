"""
Django settings for GIZ-projects project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

TESTING = False

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DJANGO_DEBUG', 'true') == 'true'

PRELOAD_CUBES = os.environ.get('PRELOAD_CUBES', 'false') == 'true'

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
    SECRET_KEY = '-r&cjf5&l80y&(q_fiidd$-u7&o$=gv)s84=2^a2$o^&9aco0o'
else:
    SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')

DATA_GOOGLE_ANALYTICS_ID = 'UA-48399585-37'
SCORECARD_GOOGLE_ANALYTICS_ID = 'UA-48399585-40'

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'import_export',
    'scorecard',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.contenttypes',
    'django.contrib.humanize',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'django_extensions',
    'corsheaders',

)

MAPIT = {
    'url': 'https://mapit.code4sa.org',
    'generation': '2',
}

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'scorecard.middleware.RedirectsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'scorecard.urls'

WSGI_APPLICATION = 'scorecard.wsgi.application'


# Database
os.environ['PGOPTIONS'] = '-c statement_timeout=' + os.environ.get('DB_STMT_TIMEOUT', '30000')

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
import dj_database_url
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgres://giz:giz@localhost:5432/giz_projects')

db_config = dj_database_url.parse(DATABASE_URL)
db_config['ATOMIC_REQUESTS'] = True
db_config['AUTOCOMMIT'] = True
DATABASES = {
    'default': db_config,
}

# Caches
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
            'LOCATION': '/var/tmp/django_cache',
        }
    }

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-za'
TIME_ZONE = 'Africa/Johannesburg'
USE_I18N = False
USE_L10N = True
USE_TZ = True
USE_THOUSAND_SEPARATOR = True
FORMAT_MODULE_PATH = 'scorecard.formats'


# CORS
CORS_ORIGIN_ALLOW_ALL = True


# Templates

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                "django.contrib.messages.context_processors.messages",
                "scorecard.context_processors.google_analytics",
            ]
        }
    },
]

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

ASSETS_DEBUG = DEBUG
ASSETS_URL_EXPIRE = False

# assets must be placed in the 'static' dir of your Django app

# where the compiled assets go
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# the URL for assets
STATIC_URL = '/static/'

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "pipeline.finders.PipelineFinder",
)
MATERIALISED_VIEWS_BASE = os.path.join(BASE_DIR, 'scorecard/materialised/')

PYSCSS_LOAD_PATHS = [
    os.path.join(BASE_DIR, 'scorecard', 'static'),
    os.path.join(BASE_DIR, 'scorecard', 'static', 'stylesheets'),
    os.path.join(BASE_DIR, 'scorecard', 'static', 'bower_components'),
    os.path.join(BASE_DIR, 'census', 'static'),
]
PIPELINE = {
    'PIPELINE_ENABLED' : False,
    'STYLESHEETS': {
        'scorecard': {
            'source_filenames': (
                'stylesheets/vendor/leaflet-0.6.4.css',
                'stylesheets/vendor/leaflet.label.css',
                'stylesheets/bootstrap.min.css',
                'bower_components/fontawesome/css/font-awesome.css',
                'stylesheets/icomoon.css',
                'stylesheets/scorecard.scss',
                'bower_components/bootstrap-sass/assets/stylesheets/_bootstrap.scss',
            ),
            'output_filename': 'scorecard.css'
        },
    },
    'JAVASCRIPT': {
        'scorecard': {
            'source_filenames': (
                'js/dist/jquery.min.js',
                'js/dist/d3.min.js',
                'js/dist/underscore.js',
                'js/vendor/d3-format.min.js',
                'js/vendor/bootstrap-3.3.2/affix.js',
                'js/vendor/bootstrap-3.3.2/scrollspy.js',
                'js/vendor/bootstrap-3.3.2/transition.js',
                'js/vendor/bootstrap-3.3.2/collapse.js',
                'js/vendor/bootstrap-3.3.2/modal.js',
                'js/vendor/typeahead-0.11.1.js',
                'js/vendor/spin.min.js',
                'js/vendor/leaflet-0.6.4.js',
                'js/vendor/leaflet.label.js',
                'js/charts.js',
                'js/place-finder.js',
                'js/maps.js',
                'js/scorecard.js',
            ),
            'output_filename': 'scorecard.js'
        }
    },
    'CSS_COMPRESSOR': None,
    'JS_COMPRESSOR': None,
    'DISABLE_WRAPPER': True,

    'COMPILERS': (
        'scorecard.pipeline.PyScssCompiler',
    ),
}

# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'scorecard.pipeline.GzipManifestPipelineStorage'


# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '%(asctime)s %(levelname)s %(module)s %(process)d %(thread)d %(message)s'
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR'
    },
    'loggers': {
        'scorecard': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        },
        'sqlalchemy.engine': {
            'level': 'INFO' if DEBUG else 'WARN',
        },
        'django': {
            'level': 'DEBUG' if DEBUG else 'INFO',
        }
    }
}

FIXTURE_DIRS = (
   'scorecard/fixtures/',
)
