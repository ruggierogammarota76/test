from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User, Booking
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:postgres@db:5432/meetings')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')

db.init_app(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return redirect(url_for('bookings'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('bookings'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/bookings')
@login_required
def bookings():
    bookings = Booking.query.order_by(Booking.start_time).all()
    return render_template('bookings.html', bookings=bookings)

@app.route('/book', methods=['POST'])
@login_required
def book():
    title = request.form['title']
    start = request.form['start']
    end = request.form['end']
    b = Booking(title=title, start_time=start, end_time=end, user_id=current_user.id)
    db.session.add(b)
    db.session.commit()
    return redirect(url_for('bookings'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
