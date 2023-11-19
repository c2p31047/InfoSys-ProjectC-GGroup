import sqlite3

tourokuDATABASE = "touroku_database.db"
startDATABASE = "start_database.db"

#登録データベースを作る関数
def create_info_table():
    #コネクションオブジェクト（データベースへのアクセス）
    con = sqlite3.connect(tourokuDATABASE)
    #テーブル作成SQL
    con.execute("CREATE TABLE IF NOT EXISTS tourokuDATABASE (date,time,place,name)")
    con.commit()       
    con.close()

def create_start_table():
    con = sqlite3.connect(startDATABASE)
    con.execute("CREATE TABLE IF NOT EXISTS startDATABASE (username,mail,password)")
    con.commit()       
    con.close()