import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ConversationHandler,
)
from datetime import datetime

# Стан для ConversationHandler
START_ORDER, ASK_ORDER, ASK_PAYMENT, ASK_LOCATION, CONFIRM_ORDER = range(5)

# Токен
TOKEN = os.environ["BOT_TOKEN"]  # Заміни, або в Replit додай секрет

# Повна наявність товару
PRODUCTS_TEXT = """
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
🔸GRAPEFRUIT 🍊
🔸WILD BERRIES 🥶😏
🔸BERRY LEMONADE🍓🥶🧃
🔸BLUEBERRY 🥶
🔸SPEARMINT🍃
🔸ORANGE LEMONADE🍊🍸
🔸COCONUT MELON🥳🍈
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
🔶Смородина ментол🫐🍃
🔶Чорниця ментол 🍃

🔽Lucky 30𝐦𝐥 𝟓% (готова)🔽
💰 - 280 грн 
🔸BLUEBERRY 🥶

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

🔽Chaser Special Berry 30ml 6.5%🔽
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

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[InlineKeyboardButton("🛒 Зробити замовлення", callback_data="start_order")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привіт! Оберіть дію:", reply_markup=reply_markup)
    return START_ORDER

# Натискання кнопки Зробити замовлення
async def start_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query:
        await query.answer()
        await query.message.reply_text("Ось актуальні товари:\n\n" + PRODUCTS_TEXT)
        await query.message.reply_text("Напишіть, що саме потрібно і кількість:")
    else:
        await update.message.reply_text("Ось актуальні товари:\n\n" + PRODUCTS_TEXT)
        await update.message.reply_text("Напишіть, що саме потрібно і кількість:")
    return ASK_ORDER

# Введення замовлення
async def ask_payment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["order"] = update.message.text
    keyboard = [
        [InlineKeyboardButton("💳 Карта", callback_data="card")],
        [InlineKeyboardButton("💵 Готівка", callback_data="cash")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Оберіть спосіб оплати:", reply_markup=reply_markup)
    return ASK_PAYMENT

# Обробка оплати
async def ask_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    context.user_data["payment"] = query.data

    keyboard = [
        [InlineKeyboardButton("🏫 6Б1", callback_data="6Б1")],
        [InlineKeyboardButton("📍 Інше місце", callback_data="other")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.message.reply_text("Оберіть місце отримання:", reply_markup=reply_markup)
    return ASK_LOCATION

# Обробка локації
async def confirm_order(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "other":
        context.user_data["location"] = "Інше місце (ввести вручну)"
        await query.message.reply_text("Введіть, будь ласка, адресу вручну:")
        return CONFIRM_ORDER
    else:
        context.user_data["location"] = "6Б1"
        return await finish_order(query.message, context)

# Якщо ввели адресу вручну
async def finish_order(message, context):
    order = context.user_data.get("order", "")
    payment = context.user_data.get("payment", "")
    location = context.user_data.get("location", "")

    text = f"📝 НОВЕ ЗАМОВЛЕННЯ:\n\n📦 Замовлення: {order}\n💳 Оплата: {payment}\n📍 Місце: {location}\n🕒 Час: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    # Надіслати замовлення адміну
    admin_chat_id = os.environ["ADMIN_CHAT_ID"]
    await context.bot.send_message(chat_id=admin_chat_id, text=text)

    # Зберегти в файл
    with open("orders.txt", "a") as file:
        file.write(text + "\n\n")

    # Додати кнопку "Зробити нове замовлення"
    keyboard = [[InlineKeyboardButton("🛒 Зробити нове замовлення", callback_data="start_order")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await message.reply_text("✅ Замовлення прийнято! Очікуйте на підтвердження.\n\n🔁 Щоб зробити нове замовлення, натисніть кнопку нижче:", reply_markup=reply_markup)
    return ConversationHandler.END

# Якщо користувач вводить адресу вручну
async def handle_custom_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["location"] = update.message.text
    return await finish_order(update.message, context)

# Обробка текстових повідомлень
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "🛒 Зробити замовлення":
        return await start_order(update, context)
    return ASK_ORDER

# Основний запуск
    if __name__ == "__main__":
        app = Application.builder().token(TOKEN).build()

        app.add_handler(conv_handler)

        print("Бот запущено")
        app.run_polling()

    conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START_ORDER: [CallbackQueryHandler(start_order, pattern="^start_order$")],
        ASK_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_payment)],
        ASK_PAYMENT: [CallbackQueryHandler(ask_location)],
        ASK_LOCATION: [CallbackQueryHandler(confirm_order)],
        CONFIRM_ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_location)],
    },
    fallbacks=[MessageHandler(filters.TEXT, handle_text)],
    per_message=True,  # ✅ Ось додано
)

    app.add_handler(conv_handler)
    app.run_polling()
