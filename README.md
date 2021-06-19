# Info
Django Telegram Bot Skeleton.

Based on: https://github.com/ohld/django-telegram-bot/

# Установка
Проект настроен для деплоя через Dokku. Берем VPS, ставим dokku, создаем приложение там, postgres, redis, git.
Создаем необходимые переменные окружения:

BUILDPACK_URL:            https://github.com/heroku/heroku-buildpack-python.git#v191

DISABLE_COLLECTSTATIC:    1

DJANGO_DEBUG:             False

DOKKU_LETSENCRYPT_EMAIL:  email@gmail.com

MEDIA_DOMAIN:             https://my_site.com

WEB_DOMAIN:               https://my_site.com

TELEGRAM_TOKEN:           tg_token_from_bot_father

Говорит TG, что будем webhook-ом работать через запрос: 

https://api.telegram.org/bot[ТУТ_ТОКЕН]/setWebhook?url=[ТУТ_URL_WEBHOOK]/super_secter_webhook/

Пушим проект в dokku и готово. Детальнее тут: https://github.com/ohld/django-telegram-bot/wiki/Production-Deployment-using-Dokku
