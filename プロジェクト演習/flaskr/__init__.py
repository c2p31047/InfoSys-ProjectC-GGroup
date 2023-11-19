#初期化処理
from flask import Flask
app = Flask(__name__)
import flaskr.main

from flaskr import db
#空のテーブルが作られる
db.create_info_table()
db.create_start_table()

