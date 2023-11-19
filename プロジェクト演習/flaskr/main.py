#flaskアプリのオブジェクトをインポート
from flaskr import app
from flask import render_template,flash,request,redirect,url_for
import webbrowser
#現在日時
import datetime 
current_date = datetime.date.today() 
import sqlite3
tourokuDATABASE = "touroku_database.db"
startDATABASE = "start_database.db"
import secrets
app.secret_key = secrets.token_hex(16)

#トップ画面(index.html)にアクセスしたときに実行される
@app.route('/')#　/　=　WebアプリのトップのURL
def index():
    return render_template(
        'index.html'
    )

@app.route('/login.html')
def login():
    con = sqlite3.connect(startDATABASE)
    db_start = con.execute("SELECT * FROM startDATABASE").fetchall()
    con.close()

    start = []
    for row in db_start:
        start.append({"username":row[0], "mail":row[1],"password":row[2]})
    
    return render_template(
        'login.html',
        start=start
    )

@app.route('/new_ac.html')
def new_ac():
    return render_template(
        'new_ac.html'
    )

@app.route('/success')
def success():
    return render_template(
        'success.html'
    )

#予約確認画面
@app.route('/keiziban.html')
def keiziban():
    con = sqlite3.connect(tourokuDATABASE)
    #infoのテーブルのデータをリストですべて取得する
    db_info = con.execute("SELECT * FROM tourokuDATABASE ORDER BY date ASC").fetchall()
    con.close()

    info = []
    for row in db_info:
        info.append({"date":row[0], "time":row[1],"place":row[2], "name":row[3]})
    
    return render_template(
        'keiziban.html',
        info=info
    )

@app.route('/form')
def form():
    return render_template(
        'form.html'
    )

@app.route('/tuti.html')
def tuti():
    date = request.args.get('date', '')  # パラメータがない場合にデフォルト値を指定
    time = request.args.get('time', '')
    place = request.args.get('place', '')
    my_name = request.args.get('my_name', '')
    partner_name = request.args.get('partner_name', '')
    return render_template(
        'tuti.html',
        date=date, 
        time=time, 
        place=place,
        partner_name=partner_name,
        my_name=my_name
    )

@app.route('/contact.html')
def contact():
    return render_template(
        'contact.html'
    )

#新規登録
@app.route('/start',methods=["POST"])
def start():
    username = request.form["username"]
    mail = request.form["mail"]
    password = request.form["password"]

    con = sqlite3.connect(startDATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM startDATABASE WHERE username=? AND mail=? AND password=?", (username, mail, password))
    existing_ac = cursor.fetchone()
    if existing_ac:
        flash("すでに登録されています")
        con.close()
        return redirect(url_for('new_ac'))
    #重複がない場合、追加
    cursor.execute("INSERT INTO startDATABASE (username, mail, password) VALUES (?, ?, ?)", (username,mail,password))
    con.commit()
    con.close()
    return redirect(url_for('success'))

#ログイン
@app.route('/login', methods=['POST'])
def login_check():
    username = request.form['username']
    password = request.form['password']

    con = sqlite3.connect(startDATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM startDATABASE WHERE username=? AND password=?", (username,password))
    existing_entry = cursor.fetchone()
    if existing_entry:
         return redirect(url_for('keiziban'))

    message = "登録されていません"
    flash(message)
    return redirect(url_for('login'))
#予約
@app.route('/touroku-register', methods=["POST"])
def register():
    date = request.form["date"]
    time = request.form["time"]
    place = request.form["place"]
    name = request.form["name"]
    #予約がかぶっていないかチェック
    con = sqlite3.connect(tourokuDATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT * FROM tourokuDATABASE WHERE date=? AND time=? AND place=?", (date, time, place))
    existing_entry = cursor.fetchone()
    #予約がかぶっていた場合
    if existing_entry:
        cursor_checkname = con.cursor()
        cursor_checkname.execute("SELECT * FROM tourokuDATABASE WHERE date=? AND time=? AND place=? AND name=?", (date, time, place,name))
        existing_entry_checkname = cursor_checkname.fetchone()
        #予約が自分だった場合
        if existing_entry_checkname:
            flash("すでに予約しています")
            con.close()
            return redirect(url_for('keiziban'))
        #別の人だった場合
        cursor_name = con.cursor()
        cursor_name.execute("SELECT name FROM tourokuDATABASE WHERE date=? AND time=? AND place=?", (date, time, place))
        existing_entry_name = cursor_name.fetchone()
        message=f"{date}の{time}、{place}はすでに{existing_entry_name[0]}が予約しています"
        flash(message)
        con.close()
        return redirect(url_for('tuti',date=date, time=time, place=place, partner_name=existing_entry_name[0],my_name=name))

    #予約がかぶっていなかった場合
    cursor.execute("INSERT INTO tourokuDATABASE (date, time, place, name) VALUES (?, ?, ?, ?)", (date, time, place, name))
    con.commit()
    con.close()
    message = f" {name} さん、{date} の {time} に {place} で予約しました。"
    flash(message)
    return redirect(url_for('keiziban'))

#連絡をとる
@app.route('/submit_mail',methods=["POST"])
def submit_mail():
    my_name = request.form.get('my_name')
    partner_name = request.form.get('partner_name')
    subject = request.form.get('subject')
    body = request.form.get('body')

    con = sqlite3.connect(startDATABASE)
    cursor = con.cursor()
    cursor.execute("SELECT mail FROM startDATABASE WHERE username=? ", (my_name,))
    my_mail = cursor.fetchone()
    cursor.execute("SELECT mail FROM startDATABASE WHERE username=? ", (partner_name,))
    partner_mail = cursor.fetchone()

    if partner_mail:
        to_email = partner_mail[0]  
        from_email = my_mail[0]

        # Gmailをウェブブラウザで開く
        gmail_url = "https://mail.google.com"
        webbrowser.open(f"{gmail_url}?view=cm&to={to_email}&from={from_email}&su={subject}&body={body}")
        message=f"{partner_name}さんにメールを送りました。　予約は完了していません"
        flash(message)
        return redirect(url_for('keiziban'))

    from_email = my_mail[0]
    gmail_url = "https://mail.google.com"
    webbrowser.open(f"{gmail_url}?view=cm&from={from_email}&su={subject}&body={body}")
    message=f"さんにメールを送りました。　予約は完了していません"
    flash(message)
    return redirect(url_for('keiziban'))


