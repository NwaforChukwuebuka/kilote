from pathlib import Path
from decouple import config
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-k8@fvf(x+=%^c10@09&8fr2a4(*@wu_50s=p=##a(cyw#at_g2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

LOGIN_URL = '/accounts/login/'  # URL to redirect if user is not logged in
LOGIN_REDIRECT_URL = '/dashboard'  # Where to redirect after successful login

# SOCIAL_AUTH_LOGIN_ERROR_URL = '/login-error/'
# SOCIAL_AUTH_LOGIN_REDIRECT_URL = '/dashboard/'
# SOCIAL_AUTH_LOGIN_URL = '/'

SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY = '77vq2hiaje4mdm'
SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET = 'WPL_AP1.BSEFXq3UaTpCrRNG.36eFFg=='
print("LinkedIn Client ID:", SOCIAL_AUTH_LINKEDIN_OAUTH2_KEY)  # Debugging line
print("LinkedIn Client Secret:", SOCIAL_AUTH_LINKEDIN_OAUTH2_SECRET)  # Debugging line
SOCIAL_AUTH_LINKEDIN_OAUTH2_SCOPE = ['openid', 'w_member_social', 'email', 'profile']
SOCIAL_AUTH_LINKEDIN_OAUTH2_REDIRECT_URI = 'http://localhost:8000/social/auth/complete/linkedin/'  # or http://127.0.0.1:8000/social/auth/complete/linkedin-oauth2/
SOCIAL_AUTH_LINKEDIN_OAUTH2_AUTHORIZATION_URL = 'https://www.linkedin.com/oauth/v2/authorization'
SOCIAL_AUTH_LINKEDIN_OAUTH2_ACCESS_TOKEN_URL = 'https://www.linkedin.com/oauth/v2/accessToken'
SOCIAL_AUTH_LINKEDIN_OAUTH2_USERINFO_URL = 'https://api.linkedin.com/v2/userinfo'
SOCIAL_AUTH_LINKEDIN_OAUTH2_EXTRA_DATA = [
    'sub',
]


AUTHENTICATION_BACKENDS = (
    'social_integration.backends.CustomLinkedinOAuth2',  # Use the actual path to your custom backend
    'django.contrib.auth.backends.ModelBackend',
)
# Application definition
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DATABASE_NAME'),
        'USER': config('DATABASE_USER'),
        'PASSWORD': config('DATABASE_PASSWORD'),
        'HOST': config('DATABASE_HOST'),
        'PORT': config('DATABASE_PORT', default=''),  # Default to empty string if not set
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'core',
    'accounts',
    'social_integration',
    'post_management',
    'analytics',
    'subscription',
    'dashboard',
    'social_django',
]


SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
)



MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'social_django.middleware.SocialAuthExceptionMiddleware',
]

ROOT_URLCONF = 'evin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'evin.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),  # Add this line if you have a global static folder
]
STATIC_ROOT = BASE_DIR / 'staticfiles'



# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
