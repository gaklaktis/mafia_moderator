from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json

ADMIN_ID = 123456789  # ← сюда вставь свой Telegram ID

def load_allowed():
    with open("allowed.json", "r") as f:
        return set(json.load(f))

def save_allowed(allowed):
    with open("allowed.json", "w") as f:
        json.dump(list(allowed), f)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print(f"User {user_id} tried to access")  # Логирование
    
    allowed = load_allowed()
    if not allowed:  # Если файл пуст/не существует
        print("Warning: allowed.json is empty or not found!")
        await update.message.reply_text("⚠️ Системная ошибка. Администратору: проверьте allowed.json")
        return

    if user_id not in allowed:
        await update.message.reply_text(f"⛔ Доступ запрещён (ваш ID: {user_id}). Обратитесь к администратору.")
        return

    # Добавляем случайный параметр, чтобы избежать кеширования
    import random
    webapp_url = f"https://mafia-moderator.onrender.com/webapp?r={random.randint(1,10000)}"
    
    keyboard = [[
        InlineKeyboardButton("Открыть таблицу", web_app=WebAppInfo(url=webapp_url))
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать!", reply_markup=reply_markup)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 7355212004:
        await update.message.reply_text("⛔ Только админ может это делать.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Используй: /grant <user_id>")
        return

    user_id = int(context.args[0])
    allowed = load_allowed()
    allowed.add(user_id)
    save_allowed(allowed)
    await update.message.reply_text(f"✅ Доступ выдан для {user_id}")

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 7355212004:
        await update.message.reply_text("⛔ Только админ может это делать.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Используй: /revoke <user_id>")
        return

    user_id = int(context.args[0])
    allowed = load_allowed()
    allowed.discard(user_id)
    save_allowed(allowed)
    await update.message.reply_text(f"🚫 Доступ отозван у {user_id}")

app = ApplicationBuilder().token("7398262284:AAE0MPai4JPZC1XkdDI14Mrc68Ke1buYEtY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("grant", grant))
app.add_handler(CommandHandler("revoke", revoke))

app.run_polling()
