from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)
DATA_FILE = "data.json"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/update_balance", methods=["POST"])
def update_balance():
    data = request.json
    user_id = str(data["user_id"])
    win = int(data["win"])

    db = load_data()
    if user_id not in db:
        db[user_id] = {"balance": 1000}

    db[user_id]["balance"] += win
    save_data(db)

    return jsonify({"balance": db[user_id]["balance"]})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
