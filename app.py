from flask import Flask, request, render_template
import json
import urllib.parse

app = Flask(__name__)
@app.route('/static/audio/<path:filename>')
def serve_audio(filename):
    return send_from_directory('static/audio', filename)

def load_allowed():
    try:
        with open("allowed.json", "r") as f:
            data = json.load(f)
            print(f"DEBUG: Loaded allowed.json -> {data}")  # Лог
            return set(data) if isinstance(data, list) else {data}
    except Exception as e:
        print(f"ERROR reading allowed.json: {e}")  # Лог ошибки
        return set()

def parse_user_id(init_data):
    try:
        # Новый метод парсинга для Telegram WebApp
        from urllib.parse import parse_qs
        params = parse_qs(init_data)
        if 'user' not in params:
            return None
            
        user = json.loads(params['user'][0])
        return user.get('id')
    except Exception as e:
        print(f"Error parsing init_data: {str(e)}")
        return None

@app.route('/webapp')
def webapp():
    init_data = request.args.get('tgWebAppData')
    print(f"Received init_data: {init_data}")  # Логирование

    if not init_data:
        return "❌ Ошибка: не получены данные от Telegram. Запустите через кнопку в боте."

    user_id = parse_user_id(init_data)
    if not user_id:
        return "❌ Ошибка авторизации: не удалось определить пользователя."

    allowed = load_allowed()
    if user_id not in allowed:
        return f"❌ Доступ запрещён (ваш ID: {user_id}). Обратитесь к администратору."

    return render_template("index_partial.html")  # основной HTML

@app.route("/webview")
def webview():
    return render_template("index.html")
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)