from pathlib import Path
from django.core.exceptions import ImproperlyConfigured
import os
import json
from datetime import timedelta

########################################################### 기본 설정
# 베이스 경로 (세팅 파일 위치 바뀔 시 확인)
BASE_DIR = Path(__file__).resolve().parent.parent

# 개발 디버깅 시 True 서버 업로드시 False
DEBUG = True

# 접근 호스트네임 ex) 도메인으로만 접속 가능하게 할 시 "도메인네임"
ALLOWED_HOSTS = ["*"]

# 루트 url
ROOT_URLCONF = 'config.urls'
# 로그인 성공후 이동하는 URL
LOGIN_REDIRECT_URL = '/swagger/'
# 로그아웃시 이동하는 URL
LOGOUT_REDIRECT_URL = '/swagger/'

LANGUAGE_CODE = 'ko-kr'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_TZ = False

WSGI_APPLICATION = 'config.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# 업로드 필드 수 제한
DATA_UPLOAD_MAX_NUMBER_FIELDS = 100
# 업로드 파일 수 제한
DATA_UPLOAD_MAX_NUMBER_FILES = 50
# 업로드 데이터 용량 제한 ( MB * 1024 * 1024 )
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024
# 업로드 파일 용량 제한 ( MB * 1024 * 1024 )
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024

########################################################### 시크릿 키
secret_file = os.path.join(BASE_DIR, 'secrets.json')
with open(secret_file) as f:
    secrets = json.loads(f.read())


def get_secret(setting):
    try:
        return secrets[setting]
    except KeyError:
        error_msg = "Set the {} environment variable".format(setting)
        raise ImproperlyConfigured(error_msg)


SECRET_KEY = get_secret("SECRET_KEY")

########################################################### 자원 (template, static, media, db)
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],  # Add this line
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

# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # collectstatic 시 경로
STATIC_ROOT = BASE_DIR / 'static/'
STATIC_URL = '/static/'
STATICFILES_DIRS = []

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': BASE_DIR / 'db.sqlite3',
    # },
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '8125',
        'USER': 'nowon',
        'PASSWORD': 'skdndhs12@',
        'HOST': '222.96.199.9',
        'PORT': '5404'
    }
}

########################################################### 모듈
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_yasg',
    'gongo',
    'bbs',
    'common',
    'scrapper',
]

AUTH_USER_MODEL = 'common.User'

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

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

########################################################### CORS
# CORS_ALLOWED_ORIGINS = [
#     'http://localhost:8000',
# ]
CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'rnjsxodyd231@naver.com'  # 발신자 Gmail 계정
EMAIL_HOST_PASSWORD = 'fnehfvm159!'  # 발신자 Gmail 계정의 비밀번호

CSRF_COOKIE_HTTPONLY = False

########################################################### DRF
REST_FRAMEWORK = {
    # 권한
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    # 'DEFAULT_RENDERER_CLASSES': [
    #     'rest_framework.renderers.JSONRenderer',
    #     'rest_framework.renderers.BrowsableAPIRenderer'
    # ],
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination', # 페이지 네이션
    # 'PAGE_SIZE': 10,

    # 'DEFAULT_FILTER_BACKENDS': [  # 필터
    #     'rest_framework.filters.SearchFilter',
    #     'rest_framework.filters.OrderingFilter',
    # ],
    # 'DEFAULT_THROTTLE_CLASSES': [   # 쓰로틀 조절
    #     'rest_framework.throttling.AnonRateThrottle',
    #     'rest_framework.throttling.UserRateThrottle',
    # ],
    # 'DEFAULT_THROTTLE_RATES': {
    #     'anon': '100/day',
    #     'user': '1000/day',
    # }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(seconds=30),  # 액세스 토큰 유효기간 설정
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),  # 리프레시 토큰 유효기간 설정
    # 'REFRESH_TOKEN_LIFETIME': timedelta(seconds=10),  # 리프레시 토큰 유효기간 설정
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
}

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',  # OpenAPI 2.0에서는 'http' 대신 'apiKey'를 사용합니다.
            'name': 'Authorization',
            'in': 'header'
        },
    },
}

########################################################### 로그
# 로깅 경로 폴더 만들기
logging_path = os.path.join(BASE_DIR, 'logs')
os.makedirs(logging_path, exist_ok=True)
# 로깅 설정
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'django.server': {
            '()': 'django.utils.log.ServerFormatter',
            'format': '[{server_time}] {message}',
            'style': '{',
        },
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
        'django.server': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'django.server',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'INFO',
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/logs.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'standard',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'mail_admins', 'file'],
            'level': 'INFO',
        },
        'django.server': {
            'handlers': ['django.server'],
            'level': 'INFO',
            'propagate': False,
        },
    }
}