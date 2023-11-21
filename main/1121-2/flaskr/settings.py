# settings.py

from flask import Flask
import os

class Config:
    # データベースのURI（SQLiteを使用する場合）
    SQLALCHEMY_DATABASE_URI = 'sqlite:///your_database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # デバッグモード
    DEBUG = True

    # FullCalendarなどのフロントエンドライブラリの静的ファイルのパス
    STATIC_FOLDER = 'static'

    # テンプレートのフォルダ
    TEMPLATE_FOLDER = 'templates'

    # セッションの設定
    SESSION_TYPE = 'filesystem'

    # その他のアプリケーション固有の設定
    # ...

# ファクトリ関数を使って設定を読み込む
def create_app():
    app = Flask(__name__)

    # 上記の Config クラスから設定を読み込む
    app.config.from_object(Config)

    return app
