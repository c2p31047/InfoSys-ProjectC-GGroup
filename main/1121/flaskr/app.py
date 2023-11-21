# app.py

import sqlite3
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # 任意のシークレットキーを設定

DATABASE = "reservations.db"

def get_db():
    return sqlite3.connect(DATABASE)

# その他のコード...

class Reservation:
    def __init__(self, date, time, place, name):
        self.date = date
        self.time = time
        self.place = place
        self.name = name

@app.route('/touroku-register', methods=["POST"])
def register():
    # POSTで送られてきたinput_boxに入力された値が入っている
    date = request.form["date"]
    time = request.form["time"]
    place = request.form["place"]
    name = request.form["name"]

    # 送られてきた値をSQLite3のデータベースに新しい予約として追加
    con = get_db()
    cursor = con.cursor()
    cursor.execute("INSERT INTO reservations (date, time, place, name) VALUES (?, ?, ?, ?)", (date, time, place, name))
    con.commit()
    con.close()

    # 終わった後に最初の画面に戻す
    return redirect(url_for("index"))

# FullCalendarにデータを提供するエンドポイント
@app.route('/events')
def get_events():
    events = Reservation.query.all()
    event_data = []

    for event in events:
        event_data.append({
            'id': event.id,
            'title': event.title,
            'start': event.start_time.isoformat(),
            'end': event.end_time.isoformat(),
        })

    return jsonify(event_data)