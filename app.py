from flask import Flask, request, render_template
import json
import urllib.parse

app = Flask(__name__)

def load_allowed():
    try:
        with open("allowed.json", "r") as f:
            data = json.load(f)
            return set(data) if isinstance(data, list) else {data}
    except:
        return set()

def parse_user_id(init_data):
    # распарсить строку initData
    data = urllib.parse.parse_qs(init_data)
    user_json = data.get("user", [None])[0]
    if user_json:
        user = json.loads(user_json)
        return user.get("id")
    return None

@app.route('/webapp')
def webapp():
    init_data = request.args.get('tgWebAppData')
    if not init_data:
        return "❌ Доступ запрещён. Запустите через Telegram /start."

    user_id = parse_user_id(init_data)
    if not user_id or user_id not in load_allowed():
        return "❌ Доступ запрещён. Запустите через Telegram /start."

    return render_template("index.html")
