"""
Django settings for Kluck_config project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
from kluck_env import env_settings as env
from datetime import timedelta
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.Django_SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# 온라인 서버에 배포 할때만 사용
# ALLOWED_HOSTS = ['43.201.60.229']
# 온라인 서버에서 Nginx, gunicorn 사용시에 사용
# ALLOWED_HOSTS = [
#     'kluck-dev2.ap-northeast-2.elasticbeanstalk.com',
#     'kluck.playfillit.com',
#     '172.31.12.235',
#     '43.201.60.229',
# ]
# 개발 중에는 아래 내용을 사용  - EB서버의 gunicorn에서 ALLOWED_HOSTS에러가 발생하고 있으니 *로 변경하고 후에 원인을 찾기로 함.
ALLOWED_HOSTS = ['*']

# Application definition

SYSTEM_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
]

CUSTOM_APPS = [
    # Rest Framework
    'rest_framework',
    # JWT Token
    'rest_framework_simplejwt',
    # 스웨거API
    'drf_spectacular',
    # scheduler
    'django_apscheduler',
    # django-crontab
    "django_crontab",
    # 각종 설정값 테이블
    'admin_settings',
    # 관리자 User의 커스텀 테이블
    'admins',
    # 프롬프트 명령 테이블
    'gpt_prompts',
    # 운세 데이터 테이블
    'luck_messages',
    # 푸시 알림 테이블
    'kluck_notifications',
]

INSTALLED_APPS = SYSTEM_APPS + CUSTOM_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # "django_apscheduler.middleware.DjangoJobExecMiddleware",
]

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
    'GET',
    'POST',
)


ROOT_URLCONF = "Kluck_config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Kluck_config.wsgi.application"

# Auth_user를 커스텀 지정.
# AUTH_USER_MODEL = 'admins.Admin'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': env.MYSQL_DBNAME,
        'USER': env.MYSQL_USERNAME,
        'PASSWORD': env.MYSQL_PASSWD,
        'HOST': env.MYSQL_HOST,  # 또는 MySQL 서버의 IP 주소
        'PORT': env.MYSQL_PORT,  # MySQL의 기본 포트 번호
        'OPTIONS':{
            'charset': 'utf8mb4'
        }
    }
}

# 테이블 생성과 관리자 로그인 관련 SQL확인을 위한 설정
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'console': {
#             'class': 'logging.StreamHandler',
#         },
#     },
#     'loggers': {
#         'django.db.backends': {
#             'level': 'DEBUG',
#             'handlers': ['console'],
#         },
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Swagger settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework_simplejwt.authentication.JWTAuthentication',],
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated',],
}

# JWT Token설정
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': env.Django_TOKEN_KEY,
    'VERIFYING_KEY': None,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'K-Luck Project API',
    'DESCRIPTION': '오늘의 운세를 통한 개인화 메시지 발송 기능 개발 프로젝트',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,  # 스키마 엔드포인트를 포함하지 않도록 설정
}   # '/api/schema/' 숨김처리


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Email settings
# 이메일 백엔드 설정: Django에서 이메일을 보내는 데 사용할 백엔드 지정
# SMTP 이메일 백엔드를 사용하여 SMTP 서버를 통해 이메일을 전송합니다.
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' # 개발 환경용
# SMTP 서버 주소 설정: Gmail의 SMTP 서버 주소 사용
EMAIL_HOST = "smtp.gmail.com"
# SMTP 서버 포트 설정: Gmail의 TLS 암호화를 사용하는 경우 587 포트 사용
EMAIL_PORT = 587
# TLS(Tansport Layer Security, 전송 계층 보안) 암호화 사용 여부 설정: 이메일 통신에 TLS 암호화를 사용하여 보안 강화
EMAIL_USE_TLS = True
# SMTP 인증에 사용할 이메일 주소 설정: 환경 변수 설정의 이메일 주소 사용
EMAIL_HOST_USER = env.EMAIL_HOST_USER
# SMTP 인증에 사용할 비밀번호 설정: 환경 변수 설정의 비밀번호 사용
EMAIL_HOST_PASSWORD = env.EMAIL_HOST_PASSWORD


# django-crontab Setting
# Django 프로젝트의 루트 디렉토리 경로
# CRON_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CRONJOBS = [
    # ('* * * * *', 'kluck_notifications.cron.hi', f'>> {os.path.join(BASE_DIR, "logs/hi_cron.log")} 2>&1'),
    ('* * * * *', 'kluck_notifications.cron.push_cron_job', f'>> {os.path.join(BASE_DIR, "logs/push_cron.log")} 2>&1'), # 매 분마다 실행 -> push_scheduler
    ('0 0 * * *', 'kluck_notifications.cron.remove_inactive_tokens', f'>> {os.path.join(BASE_DIR, "logs/device_token_cron.log")} 2>&1'), # 매일 0시 0분 실행 -> inactive
]