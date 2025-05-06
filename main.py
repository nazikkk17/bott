# --- WEB SERVER для Replit ---
from flask import Flask
from threading import Thread

app_web = Flask('')

@app_web.route('/')
def home():
    return "Бот працює"

def run():
    app_web.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

from telegram.ext import Application
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
    ContextTypes
)

(START_ORDER, GET_DETAILS, PAYMENT_TYPE, PICK_LOCATION, CUSTOM_LOCATION) = range(5)

ADMIN_ID = 858968515  # 🔁 Заміни на свій Telegram ID

PRODUCT_LIST = """
🔽𝐄𝐥𝐢𝐱 10 ml 5% (готова)🔽
💰 - 140 грн 
🔸Диня🍈
🔸Смородина мʼята🥶🍃
🔸Суниця🍓
🔸Черешня 🍒
🔸Зелене яблуко🍏 
🔸Груша 👍
🔸Лісові ягоди 🫐🍓
🔸Лісові ягоди лід 🫐🍓🧊
🔸Мʼята 🍃
🔸Блакитна малина мʼята 🫐🍃
🔸Виноград 🍇 
🔸Черешня лід 🍒🧊

🔽Lucky 15𝐦𝐥 𝟓𝟎𝐦𝐠 (готова)🔽
💰 - 160 грн - 1шт, 300грн - 2шт 
🔸WILD BERRIES 🥶😏
🔸BLUEBERRY 🥶
🔸SPEARMINT🍃
🔸ORANGE LEMONADE🍊🍸
🔸COCONUT MELON🥳🍈
🔸Strawberry 🍓
🔸PASSION FRUIT MELON MANGO 🍈🏖

🔽Chaser Special Berry 15ml 5%🔽
💰 - 170 грн
🔸BERRY CANDY🍓🫐🍭
🔸BERRY NEEDLES
🔸BILBERRY MINT🥶🍃
🔸BLACKBERRY🫐
🔸BLUEBERRY LEMON🥶😖
🔸CHERRIES 🍒
🔸CRANBERRY MINT🫐🍃
🔸ENERGY CHERRY⚡️🍒
🔸MYSTERY ONE 🥶🫐🍓
🔸STRAWBERRY JELLY🍓🪼

🔽Chaser For Pods 10ml  5/6.5%🔽
💰 - 140 грн 
🔶Блакитна малина🥶
🔶Виноград 🍇
🔶Вишня 🍒
🔶Вишня ментол🫐🍃

🔽Lucky 30𝐦𝐥 𝟓% (готова)🔽
💰 - 280 грн 
🔸BLUEBERRY 🥶
🔸WILD BERRIES 🥶😏

🔽ELF LIQ 30ml 5%(готова)🔽
💰 - 350 грн 
🔶APPLE PEACH ☠️🥰
🔶PINEAPPLE COLADA 🍍🍹
🔶PINA COLADA 🥳🍹
🔶ELF JACK 
🔶BLUEBERRY ROSE MINT🥶🍃
🔶COOL MINT🍃🥶
🔶STRAWBERRY KIWI🍓🥝
🔶SPEARMINT🍃
🔶BLUEBERRY RASPBERRY POMAGRATE🥶😑
🔶STRAWBERRY RASPBERRY CHERRY ICE 🍓😑🍒🧊
🔶PINK LEMONADE SODA🥤
🔶SOUR WATERMELON GUMMY🍉

🔽𝐄𝐥𝐢𝐱 30 ml 5% (готова)🔽
💰 - 270 грн 
🔶Виноград лід🍇🧊

🔽Chaser Special Berry 
30ml 6.5%🔽
💰 - 300 грн 
🔶BERRY CANDY🍓🫐🍭
🔶CRANBERRY MINT 🫐🍃
🔶BILBERRY MINT🥶🍃
🔶STRAWBERRY JELLY🍓🪼

🆕Chaser mix ULTRA 30ml 50mg🆕
💰 - 300 грн 
🔶БАЗИЛІК МʼЯТА🌿🍃
🔶ГУАВА ПЕРСИК🍈🍑
🔶ПОЛУНИЦЯ БАНАН🍓🍌
🔶ОЖИНОВИЙ ДЖЕМ
🔶БЛАКИТНА МАЛИНА ЛИМОНАД😑🥤

🔽Chaser For Pods 30ml 5/6.5%🔽
💰 - 300 грн 
🔶Блакитна малина🥶
🔶Виноград 🍇
🔶Вишня метол🍒🍃
🔶Вишня 🍒
🔶Смородина ментол🫐🍃
🔶Кавун 🍉
🔶МʼЯТА🍃

🔷Картридж Vaporesso XROS 0.8/0.6 Ом, 2 мл 
💰 - 150 грн (разом з жижою 130грн)
🔷Картридж Vaporesso XROS 0.4Ом, 3 мл 
💰 - 150 грн (разом з жижою 130грн)
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛒 Зробити замовлення", callback_data="start_order")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привіт! Оберіть дію:", reply_markup=reply_markup)
    return START_ORDER

async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(f"🛍️ Наявність товару:\n{PRODUCT_LIST}\n\n✍️ Напишіть, що саме вам потрібно і скільки.")
    return GET_DETAILS

async def get_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["details"] = update.message.text
    keyboard = [["Карта 4441111052928938", "Готівка"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("💳 Оберіть спосіб оплати:", reply_markup=reply_markup)
    return PAYMENT_TYPE

async def choose_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["payment"] = update.message.text
    keyboard = [[KeyboardButton("6Б1"), KeyboardButton("Інше місце")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
    await update.message.reply_text("📍 Оберіть місце отримання:", reply_markup=reply_markup)
    return PICK_LOCATION

async def choose_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text
    if location == "Інше місце":
        await update.message.reply_text("📝 Вкажіть інше місце отримання:")
        return CUSTOM_LOCATION
    else:
        context.user_data["location"] = location
        return await confirm_order(update, context)

async def custom_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    return await confirm_order(update, context)

async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    details = context.user_data["details"]
    payment = context.user_data["payment"]
    location = context.user_data["location"]

    summary = (
        f"✅ НОВЕ ЗАМОВЛЕННЯ!\n\n"
        f"👤 Клієнт: @{user.username or user.first_name}\n"
        f"📦 Товари: {details}\n"
        f"💳 Оплата: {payment}\n"
        f"📍 Отримання: {location}"
    )

    await update.message.reply_text("Замовлення прийнято! Очікуйте на підтвердження.")
    await context.bot.send_message(chat_id=ADMIN_ID, text=summary)

    with open("orders.txt", "a", encoding="utf-8") as f:
        f.write(summary + "\n" + "-" * 40 + "\n")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Замовлення скасовано.")
    return ConversationHandler.END

if __name__ == "__main__":
    keep_alive() #
    app = Application.builder().token("BOT_TOKEN").build()
    import os
    TOKEN = os.environ["BOT_TOKEN"]  # 🔁 Встав свій токен

    app = ApplicationBuilder().token(TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ORDER: [CallbackQueryHandler(start_order, pattern="start_order")],
            GET_DETAILS: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_details)],
            PAYMENT_TYPE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_payment)],
            PICK_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_location)],
            CUSTOM_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, custom_location)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    app.add_handler(conv_handler)
    print("Бот запущено...")
    app.run_polling()
