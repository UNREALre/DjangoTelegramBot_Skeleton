import logging
import telegram

from functools import wraps
from dtb.settings import ENABLE_DECORATOR_LOGGING, TELEGRAM_TOKEN
from django.utils import timezone
from tgbot.models import UserActionLog, User
from telegram import MessageEntity

logger = logging.getLogger('default')


def send_typing_action(func):
    """Sends typing action while processing func command."""

    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=telegram.ChatAction.TYPING)
        return func(update, context,  *args, **kwargs)

    return command_func


def handler_logging(action_name=None):
    """ Turn on this decorator via ENABLE_DECORATOR_LOGGING variable in dtb.settings """
    def decor(func):
        def handler(update, context, *args, **kwargs):
            user, _ = User.get_user_and_created(update, context)
            action = f"{func.__module__}.{func.__name__}" if not action_name else action_name
            try:
                text = update.message['text'] if update.message else ''
            except AttributeError:
                text = ''
            UserActionLog.objects.create(user_id=user.user_id, action=action, text=text, created_at=timezone.now())
            return func(update, context, *args, **kwargs)
        return handler if ENABLE_DECORATOR_LOGGING else func
    return decor


def send_message(user_id, text, parse_mode=None, reply_markup=None, reply_to_message_id=None,
                 disable_web_page_preview=None, entities=None, tg_token=TELEGRAM_TOKEN):
    bot = telegram.Bot(tg_token)
    try:
        if entities:
            entities = [
                MessageEntity(type=entity['type'],
                              offset=entity['offset'],
                              length=entity['length']
                )
                for entity in entities
            ]

        m = bot.send_message(
            chat_id=user_id,
            text=text,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            reply_to_message_id=reply_to_message_id,
            disable_web_page_preview=disable_web_page_preview,
            entities=entities,
        )
    except telegram.error.Unauthorized:
        print(f"Can't send message to {user_id}. Reason: Bot was stopped.")
        User.objects.filter(user_id=user_id).update(is_blocked_bot=True)
        success = False
    except Exception as e:
        print(f"Can't send message to {user_id}. Reason: {e}")
        success = False
    else:
        success = True
        User.objects.filter(user_id=user_id).update(is_blocked_bot=False)
    return success
