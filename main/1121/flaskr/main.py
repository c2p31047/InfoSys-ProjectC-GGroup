# flaskアプリのオブジェクトをインポート
from flaskr import app
# 現在日時
import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash  # Add this import
import os
import secrets
import sqlite3

app.secret_key = secrets.token_hex(16)

# Sessionの初期化
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

tourokuDATABASE = "touroku_database.db"

# データベース接続のヘルパーファンクション
def get_db():
    return sqlite3.connect(tourokuDATABASE)

# ユーザーテーブルの初期化
def init_db():
    with get_db() as con:
        con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, password TEXT NOT NULL);")

# イベントテーブルの初期化
def init_event_table():
    with get_db() as con:
        con.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, start TEXT NOT NULL, end TEXT NOT NULL, color TEXT NOT NULL);")

# ユーザーテーブルの初期化
init_db()

# イベントテーブルの初期化
init_event_table()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with get_db() as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            email = cursor.fetchone()

            if email and check_password_hash(email[2], password):
                flash('ログイン成功', 'success')
                session['email'] = email[1] 
                return redirect('/')
            else:
                flash('ログイン失敗。メールアドレスまたはパスワードが正しくありません。', 'error')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        with get_db() as con:
            cursor = con.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            existing_user = cursor.fetchone()

            if existing_user:
                flash('そのメールアドレスは既に使われています。', 'error')
                return redirect(url_for('signup'))

            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            con.commit()

            flash('新しいユーザーが登録されました。', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')

#トップ画面(index.html)にアクセスしたときに実行される
@app.route('/board')#　/　=　WebアプリのトップのURL
def board():
    print('email' in session)  # デバッグメッセージ
    if 'email' in session:
        logged_in_user = session['email']
        con = sqlite3.connect(tourokuDATABASE)
        #infoのテーブルのデータをすべて取得する(fetchallはデータをpythonのリストとして取得する)
        #ORDER BY date ASC で日付順に取得
        db_info = con.execute("SELECT * FROM tourokuDATABASE ORDER BY date ASC").fetchall()
        con.close()
        info = []
        for row in db_info:
            info.append({"date":row[0], "time":row[1],"place":row[2], "name":row[3]})        
        return render_template('board.html', user=logged_in_user, info=info)
    else:
        print('Redirecting to login')  # デバッグメッセージ
        return redirect(url_for('login'))

#formの関数
@app.route('/form')
def form():
    if 'email' in session:
        logged_in_user = session['email']
        return render_template('form.html', user=logged_in_user)
    else:
        return redirect(url_for('login'))
    
#formの関数
@app.route('/')
def index():
    if 'email' in session:
        logged_in_user = session['email']
        return render_template('index.html', user=logged_in_user)
    else:
        return redirect(url_for('login'))

#登録ボタンが押されたときに実行される関数
#registerというpythonの関数にPOSTのリクエストがあったらregisterが呼び出される
@app.route('/touroku-register', methods=["POST"])
def register():
    #POSTで送られてきたinput_boxに入力された値が入っている
    date = request.form["date"]
    time = request.form["time"]
    place = request.form["place"]
    name = request.form["name"]

    #送られてきた値をSQLのINFOTABLEに入れる
    con = sqlite3.connect(tourokuDATABASE)
    con.execute("INSERT INTO tourokuDATABASE VALUES(?,?,?,?)",[date,time,place,name])
    con.commit()
    con.close()
    
    #終わった後に最初の画面に戻す
    return redirect(url_for("index"))

# カレンダーの表示と予約データの取得
@app.route('/calendar')
def calendar():
    if 'email' not in session:
        return redirect(url_for('login'))
    return render_template('calendar.html')

@app.route('/logout')
def logout():
    # セッションからユーザー情報を削除
    session.pop('email', None)
    return redirect(url_for('login'))


@app.route('/get-reservations')
def get_reservations():
    # Retrieve reservation data from your database
    # (Replace this with your actual database query)
    # For now, we'll use dummy data
    return jsonify(reservation_data)

# カレンダーのイベントデータを提供するエンドポイント
@app.route('/events', methods=['GET'])
def events():
    # データベースからイベントデータを取得
    event_data = get_event_data_from_database()
    events = get_all_events()
    return jsonify(event_data)
    return render_template('events.html', events=events)

def get_event_data_from_database():
    # SQLite データベースに接続
    connection = sqlite3.connect('touroku_database.db')
    cursor = connection.cursor()

    # イベントデータの取得クエリ（仮のクエリ）
    query = "SELECT id, title, start, end, color FROM events"
    cursor.execute(query)

    # イベントデータの取得
    event_data = []
    for row in cursor.fetchall():
        event_data.append({
            'id': row[0],
            'title': row[1],
            'start': row[2],
            'end': row[3],
            'color': row[4]
        })

    # データベース接続を閉じる
    connection.close()

    return event_data

# イベント追加ページの表示とイベントのデータベース挿入
@app.route('/add_event', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        title = request.form['title']
        start = request.form['start']
        end = request.form['end']
        color = request.form['color']

        # データベースにイベントデータを挿入
        insert_event_data(title, start, end, color)

        return redirect(url_for('index'))

    return render_template('add_event.html')

@app.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    # イベントIDを使用して特定のイベントを取得する関数（適切な関数名に変更してください）
    event = get_event_by_id(event_id)

    if request.method == 'POST':
        # フォームから送信されたデータを使用してイベントを更新する関数（適切な関数名に変更してください）
        update_event(event_id, request.form)
        return redirect(url_for('events'))

    return render_template('edit_event.html', event=event)


def insert_event_data(title, start, end, color):
    # SQLite データベースに接続
    connection = sqlite3.connect('touroku_database.db')
    cursor = connection.cursor()

    # Check if an event with the same title, start, and end already exists
    query = "SELECT id FROM events WHERE title = ? AND start = ? AND end = ?"
    cursor.execute(query, (title, start, end))
    existing_event_id = cursor.fetchone()

    if existing_event_id:
        # Event already exists, update the existing event
        update_query = "UPDATE events SET color = ? WHERE id = ?"
        cursor.execute(update_query, (color, existing_event_id[0]))
    else:
        # Event doesn't exist, insert a new event
        insert_query = "INSERT INTO events (title, start, end, color) VALUES (?, ?, ?, ?)"
        cursor.execute(insert_query, (title, start, end, color))

    # データベースに変更をコミット
    connection.commit()

    # データベース接続を閉じる
    connection.close()


# Function to get all events from the database
def get_all_events():
    # Connect to the database and retrieve events (replace this with your actual database query)
    connection = sqlite3.connect('touroku_database.db')
    cursor = connection.cursor()

    # Query to get all events
    query = "SELECT id, title, start, end, color FROM events"
    cursor.execute(query)

    # Fetch all events
    events = cursor.fetchall()

    # Close the database connection
    connection.close()

    return events

if __name__ == '__main__':
    app.run(debug=True)