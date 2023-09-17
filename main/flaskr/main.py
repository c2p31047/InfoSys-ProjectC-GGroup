#flaskアプリのオブジェクトをインポート
from flaskr import app
#現在日時
import datetime 
current_date = datetime.date.today() 
from flask import render_template,request,redirect,url_for
import sqlite3
tourokuDATABASE = "touroku_database.db"

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



