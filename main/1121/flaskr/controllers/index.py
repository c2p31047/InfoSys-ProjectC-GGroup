# index.py

from flask import Flask, render_template
from models import db, User, Reservation
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from forms import LoginForm, RegistrationForm
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

app = Flask(__name__)
app.config.from_pyfile('settings.py')  # アプリケーションの設定を読み込み

# データベースの初期化
db.init_app(app)

# Flask-Migrateの初期化
migrate = Migrate(app, db)

# Flask-Loginの初期化
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect('/dashboard')

    return render_template('login.html', form=form)

# ダッシュボードページ（サンプル）
@app.route('/dashboard')
@login_required
def dashboard():
    return f'Hello, {current_user.username}! This is your dashboard.'

# ログアウト
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

# トップページ
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
