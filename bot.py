import logging
import os
from datetime import datetime
from zoneinfo import ZoneInfo

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler


# ------------ Configuration ------------
ZOOM_LINK = "https://zoom.us/j/1234567890?pwd=example"  # Задайте вашу реальную ссылку на Zoom здесь
NEXT_MEETING_DATETIME = datetime(2025, 8, 15, 19, 0, tzinfo=ZoneInfo("Europe/Moscow"))
CHECKIN_OPTIONS = [
    "Спокойный",
    "Взволнованный",
    "Уставший",
    "Вдохновлённый",
    "Злой",
]


# ------------ Logging ------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ------------ Handlers ------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_first_name = update.effective_user.first_name if update.effective_user else "друг"
    text = (
        f"Привет, {user_first_name}!\n\n"
        "Это бот мужского круга.\n\n"
        "Доступные команды:\n"
        "- /checkin — выбрать текущее состояние\n"
        "- /next — дата и время следующей встречи"
    )
    await update.message.reply_text(text)


async def checkin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton(text=CHECKIN_OPTIONS[0], callback_data=f"checkin:{CHECKIN_OPTIONS[0]}"),
         InlineKeyboardButton(text=CHECKIN_OPTIONS[1], callback_data=f"checkin:{CHECKIN_OPTIONS[1]}")],
        [InlineKeyboardButton(text=CHECKIN_OPTIONS[2], callback_data=f"checkin:{CHECKIN_OPTIONS[2]}"),
         InlineKeyboardButton(text=CHECKIN_OPTIONS[3], callback_data=f"checkin:{CHECKIN_OPTIONS[3]}")],
        [InlineKeyboardButton(text=CHECKIN_OPTIONS[4], callback_data=f"checkin:{CHECKIN_OPTIONS[4]}")],
    ]
    await update.message.reply_text(
        "Выбери своё текущее состояние:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_checkin_choice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if not query:
        return

    await query.answer()

    try:
        # Уберём клавиатуру и покажем выбор
        chosen = query.data.split(":", 1)[1] if query.data else "—"
        await query.edit_message_text(f"Вы выбрали: {chosen}")
    except Exception as edit_error:
        logger.debug("Failed to edit message: %s", edit_error)

    await query.message.reply_text(
        f"Спасибо, что поделился. Вот ссылка на Zoom встречу:\n{ZOOM_LINK}"
    )


def format_next_meeting(dt: datetime) -> str:
    # Чёткий числовой формат, чтобы не зависеть от локали
    return dt.strftime("%d.%m.%Y в %H:%M (по Москве)")


async def next_meeting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    when = format_next_meeting(NEXT_MEETING_DATETIME)
    await update.message.reply_text(f"Следующая встреча: {when}")


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError(
            "Не найден токен бота. Установите переменную окружения TELEGRAM_BOT_TOKEN"
        )

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("checkin", checkin))
    application.add_handler(CommandHandler("next", next_meeting))
    application.add_handler(CallbackQueryHandler(handle_checkin_choice, pattern=r"^checkin:"))

    logger.info("Бот запущен. Ожидаю сообщения…")
    application.run_polling(close_loop=False)


if __name__ == "__main__":
    main()