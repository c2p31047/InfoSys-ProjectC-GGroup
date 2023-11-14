# flaskアプリのオブジェクトをインポート
from flaskr import app
# 現在日時
import datetime
from flask import render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash  # Add this import
import sqlite3
app.secret_key = 'your_secret_key'

tourokuDATABASE = "touroku_database.db"

# データベース接続のヘルパーファンクション
def get_db():
    return sqlite3.connect(tourokuDATABASE)

# ユーザーテーブルの初期化
def init_db():
    with get_db() as con:
        con.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, email TEXT NOT NULL, password TEXT NOT NULL);")

# ユーザーテーブルの初期化
init_db()

#トップ画面(index.html)にアクセスしたときに実行される
@app.route('/')#　/　=　WebアプリのトップのURL
def index():
    con = sqlite3.connect(tourokuDATABASE)
    #infoのテーブルのデータをすべて取得する(fetchallはデータをpythonのリストとして取得する)
    #ORDER BY date ASC で日付順に取得
    db_info = con.execute("SELECT * FROM tourokuDATABASE ORDER BY date ASC").fetchall()
    con.close()

    info = []
    for row in db_info:
        info.append({"date":row[0], "time":row[1],"place":row[2], "name":row[3]})
    
    return render_template(
        'index.html',
        info=info
    )

#formの関数
@app.route('/form')
def form():
    return render_template(
        'form.html'
    )

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
                return redirect(url_for('index'))
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

            hashed_password = generate_password_hash(password, method='sha256')
            cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (email, hashed_password))
            con.commit()

            flash('新しいユーザーが登録されました。', 'success')
            return redirect(url_for('login'))

    return render_template('signup.html')