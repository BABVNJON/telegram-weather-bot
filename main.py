import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

API_KEY = 'a46668592865810ea33d86dde0b41011'  # ← твой API-ключ
BOT_TOKEN = '7906543159:AAEPNwNKe-cacyE9Qq_iXQySIHt2enaoj3o'        # ← сюда вставь токен от BotFather

# Получение погоды
def get_weather(city):
    url = f'https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={API_KEY}&units=metric&lang=ru'
    response = requests.get(url)

    if response.status_code != 200:
        return "❌ Город не найден. Попробуй другой."

    data = response.json()
    current = data['list'][0]
    result = f"🌍 Погода в {city.title()}:\n"
    result += f"Сейчас: {current['main']['temp']}°C, {current['weather'][0]['description']}\n\n"

    result += "📅 Прогноз на 5 дней:\n"
    added_days = set()

    for item in data['list']:
        date = item['dt_txt'].split(' ')[0]
        if date not in added_days and len(added_days) < 5:
            temp = item['main']['temp']
            desc = item['weather'][0]['description']
            result += f"{date}: {temp}°C, {desc}\n"
            added_days.add(date)

    return result

# Обработка сообщений
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text
    weather_info = get_weather(city)
    await update.message.reply_text(weather_info)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Напиши название города, и я пришлю тебе прогноз погоды на 5 дней.")

# Основной запуск
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен. Ожидает сообщения...")
    app.run_polling()

if __name__ == "__main__":
    main()
