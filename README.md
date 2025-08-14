# Бот мужского круга

Простой Telegram-бот на `python-telegram-bot` (v21), поддерживает команды `/start`, `/checkin`, `/next`.

## Запуск

1. Установите зависимости:

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

2. Задайте токен бота в переменной окружения:

```bash
export TELEGRAM_BOT_TOKEN=ВАШ_ТОКЕН
```

3. (Опционально) Укажите свою ссылку на Zoom и дату следующей встречи в `bot.py`:
- Константа `ZOOM_LINK`
- Константа `NEXT_MEETING_DATETIME`

4. Запустите бота:

```bash
python bot.py
```

## Команды
- `/start` — приветствие и краткая справка
- `/checkin` — выбор состояния из 5 вариантов; после выбора бот отправляет благодарность и ссылку на Zoom
- `/next` — показывает дату и время следующей встречи