import secrets
from flask import Flask, render_template, request, redirect, url_for, flash, get_flashed_messages
from flask_login import LoginManager, login_required, login_user, logout_user

from blueprints import mail_blueprint
from models import db, migrate
from models.user import User
from config import Config

login_manager = LoginManager()
login_manager.login_view = 'login'


def create_app() -> Flask:
    application = Flask(__name__)
    application.config.from_object(Config)

    application.secret_key = secrets.token_hex(16)
    print(f'Secret key: {application.secret_key}')

    # Register blueprints
    application.register_blueprint(mail_blueprint, url_prefix='/mail')

    db.init_app(application)
    migrate.init_app(application, db)

    login_manager.init_app(application)

    with application.app_context():
        db.create_all()

    return application


app = create_app()


@login_manager.user_loader
def load_user(user_id: int):
    return User.query.get(user_id)


@app.route('/')
@login_required
def index():
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        user = User(email=email, username=username)
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('User registered successfully', 'success')

        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Logged in successfully', 'success')
            return redirect(url_for('index'))

        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    get_flashed_messages(with_categories=True)
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
