from flask import Flask, request, render_template, abort
import json

app = Flask(__name__)

def load_allowed_users():
    try:
        with open("allowed_users.json", "r") as f:
            return set(json.load(f))
    except:
        return set()

@app.route("/")
def home():
    user_id = request.args.get("id")
    allowed_users = load_allowed_users()

    if user_id and user_id.isdigit() and int(user_id) in allowed_users:
        return render_template("index.html")
    else:
        return "<h3>⛔ Доступ запрещён. Запустите через Telegram /start.</h3>"

if __name__ == "__main__":
    app.run(debug=True)
