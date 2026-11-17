import os
from pathlib import Path
from dotenv import load_dotenv
BASE_DIR=Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR/".env")
SECRET_KEY=os.getenv("DJANGO_SECRET_KEY","dev-only-change-me")
DEBUG=os.getenv("DEBUG","True").lower()=="true"
ALLOWED_HOSTS=os.getenv("ALLOWED_HOSTS","127.0.0.1,localhost").split(",")
INSTALLED_APPS=["django.contrib.admin","django.contrib.auth","django.contrib.contenttypes","django.contrib.sessions","django.contrib.messages","django.contrib.staticfiles","core"]
MIDDLEWARE=["django.middleware.security.SecurityMiddleware","whitenoise.middleware.WhiteNoiseMiddleware","django.contrib.sessions.middleware.SessionMiddleware","django.middleware.common.CommonMiddleware","django.middleware.csrf.CsrfViewMiddleware","django.contrib.auth.middleware.AuthenticationMiddleware","django.contrib.messages.middleware.MessageMiddleware","django.middleware.clickjacking.XFrameOptionsMiddleware"]
ROOT_URLCONF="config.urls"
TEMPLATES=[{"BACKEND":"django.template.backends.django.DjangoTemplates","DIRS":[BASE_DIR/"templates"],"APP_DIRS":True,"OPTIONS":{"context_processors":["django.template.context_processors.debug","django.template.context_processors.request","django.contrib.auth.context_processors.auth","django.contrib.messages.context_processors.messages","core.context_processors.module_menu"]}}]
WSGI_APPLICATION="config.wsgi.application"
ASGI_APPLICATION="config.asgi.application"
DATABASES={"default":{"ENGINE":os.getenv("DB_ENGINE","django.db.backends.sqlite3"),"NAME":os.getenv("DB_NAME",str(BASE_DIR/"db.sqlite3")),"USER":os.getenv("DB_USER",""),"PASSWORD":os.getenv("DB_PASSWORD",""),"HOST":os.getenv("DB_HOST",""),"PORT":os.getenv("DB_PORT","")}}
AUTH_PASSWORD_VALIDATORS=[{"NAME":"django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},{"NAME":"django.contrib.auth.password_validation.MinimumLengthValidator"},{"NAME":"django.contrib.auth.password_validation.CommonPasswordValidator"},{"NAME":"django.contrib.auth.password_validation.NumericPasswordValidator"}]
LANGUAGE_CODE="en-us"; TIME_ZONE=os.getenv("TIME_ZONE","Asia/Kolkata"); USE_I18N=True; USE_TZ=True
STATIC_URL="static/"; STATIC_ROOT=BASE_DIR/"staticfiles"; STATICFILES_DIRS=[BASE_DIR/"static"]
MEDIA_URL="media/"; MEDIA_ROOT=BASE_DIR/"media"
DEFAULT_AUTO_FIELD="django.db.models.BigAutoField"
LOGIN_URL="login"; LOGIN_REDIRECT_URL="dashboard"; LOGOUT_REDIRECT_URL="login"
EMAIL_BACKEND="django.core.mail.backends.console.EmailBackend"
AI_API_KEY=os.getenv("AI_API_KEY",""); AI_API_BASE=os.getenv("AI_API_BASE","https://api.openai.com/v1"); AI_MODEL=os.getenv("AI_MODEL","gpt-4o-mini")
