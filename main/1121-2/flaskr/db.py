import sqlite3

import datetime #現在日時
current_date = datetime.date.today() 

tourokuDATABASE = "touroku_database.db"
#登録データベースを作る関数
def create_info_table():
    #コネクションオブジェクト（データベースへのアクセス）
    con = sqlite3.connect(tourokuDATABASE)
    #テーブル作成SQL
    con.execute("CREATE TABLE IF NOT EXISTS tourokuDATABASE (date,time,place,name)")
    con.commit()       
    con.close()

_DATABASE = "choice.db"
def create_place_table():
    con = sqlite3.connect(place_choice_DATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS place_choice_DATABASE (new_place)")
    con.commit()       
    con.close()