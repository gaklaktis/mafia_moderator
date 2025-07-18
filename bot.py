from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import json
import subprocess  # ← Добавьте этот импорт
import os         # ← Добавьте этот импорт

ADMIN_ID = 7355212004  # ← сюда вставь свой Telegram ID

def load_allowed():
    with open("allowed.json", "r") as f:
        return set(json.load(f))

def save_allowed(allowed):
    with open("allowed.json", "w") as f:
        json.dump(list(allowed), f)

async def git_push(user_id: int):  # ← Новая функция для git операций
    try:
        repo_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(repo_dir)
        subprocess.run(["git", "add", "allowed.json"], check=True)
        subprocess.run(["git", "commit", "-m", f"Update access for {user_id}"], check=True)
        subprocess.run(["git", "push"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Git error: {e}")
        return False

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
    webapp_url = f"https://mafia-moderator.onrender.com/webview"
    
    keyboard = [[
        InlineKeyboardButton("Открыть таблицу", web_app=WebAppInfo(url=webapp_url))
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Добро пожаловать!", reply_markup=reply_markup)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 7355212004:  # ← Используем константу ADMIN_ID
        await update.message.reply_text("⛔ Только админ может это делать.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Используй: /grant <user_id>")
        return

    try:
        user_id = int(context.args[0])
        allowed = load_allowed()
        allowed.add(user_id)
        save_allowed(allowed)
        
        # ▼▼▼ Вставленный код для git push ▼▼▼
        if await git_push(user_id):
            await update.message.reply_text(f"✅ Доступ выдан для {user_id} и сохранён в GitHub")
        else:
            await update.message.reply_text(f"✅ Доступ выдан для {user_id}, но не удалось обновить GitHub")
        # ▲▲▲ Конец вставки ▲▲▲
            
    except ValueError:
        await update.message.reply_text("❌ Неверный ID. Укажите числовой ID пользователя")

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != 7355212004:  # ← Используем константу ADMIN_ID
        await update.message.reply_text("⛔ Только админ может это делать.")
        return

    if not context.args:
        await update.message.reply_text("⚠️ Используй: /revoke <user_id>")
        return

    try:
        user_id = int(context.args[0])
        allowed = load_allowed()
        allowed.discard(user_id)
        save_allowed(allowed)
        
        # ▼▼▼ Вставленный код для git push ▼▼▼
        if await git_push(user_id):
            await update.message.reply_text(f"🚫 Доступ отозван у {user_id} и сохранён в GitHub")
        else:
            await update.message.reply_text(f"🚫 Доступ отозван у {user_id}, но не удалось обновить GitHub")
        # ▲▲▲ Конец вставки ▲▲▲
            
    except ValueError:
        await update.message.reply_text("❌ Неверный ID. Укажите числовой ID пользователя")

app = ApplicationBuilder().token("7398262284:AAE0MPai4JPZC1XkdDI14Mrc68Ke1buYEtY").build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("grant", grant))
app.add_handler(CommandHandler("revoke", revoke))

app.run_polling()