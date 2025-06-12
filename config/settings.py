import os
from pathlib import Path
from dotenv import load_dotenv
# import dj_database_url  # 2025-06-12: 테스트를 위해 임시 주석 처리 (모듈 없음 에러 해결)

load_dotenv()  # .env 파일 불러오기

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1,localhost,.onrender.com').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.naver',
    'rest_framework',
    'apps.transactions',
    'apps.analysis',
    'apps.notifications',
    'apps.accounts',
    'apps.users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'config.wsgi.application'

# 2025-06-12: 테스트를 위해 SQLite로 임시 변경 (PostgreSQL 연결 불가로 인함)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 원래 설정 (테스트 후 복원용) - 2025-06-12: 운영 환경에서는 다시 활성화 필요
# DATABASES = {
#     'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
# }

# 2025-06-12: 개발 환경에서 이메일을 콘솔로 출력 (SMTP 연결 오류 해결)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# allauth 설정 추가 - 2025-06-12: 이메일 인증 관련 설정
ACCOUNT_EMAIL_VERIFICATION = 'none'  # 이메일 인증 비활성화 (개발용)
ACCOUNT_AUTHENTICATION_METHOD = 'email'  # 이메일로 인증
ACCOUNT_EMAIL_REQUIRED = True  # 이메일 필수
ACCOUNT_USERNAME_REQUIRED = False  # 사용자명 불필요

# 2025-06-12: 로그인 후 리다이렉트 URL 설정
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# 2025-06-12: 소셜 로그인 설정
SOCIALACCOUNT_PROVIDERS = {
    'naver': {
        'APP': {
            'client_id': os.getenv('NAVER_CLIENT_ID', ''),
            'secret': os.getenv('NAVER_CLIENT_SECRET', ''),
        },
        'SCOPE': ['email', 'nickname'],
        'AUTH_PARAMS': {},
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
    }
}

SOCIALACCOUNT_LOGIN_ON_GET = True  # GET 요청으로도 소셜 로그인 가능
SOCIALACCOUNT_AUTO_SIGNUP = True  # 자동 회원가입
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'  # 소셜 로그인 시 이메일 인증 비활성화

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'ko-kr'
TIME_ZONE = 'Asia/Seoul'
USE_I18N = True
USE_TZ = True


STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'users.User'

ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# 2025-06-12: deprecated 설정 제거됨 (위에서 새로운 방식으로 설정)

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

SITE_ID = 1
