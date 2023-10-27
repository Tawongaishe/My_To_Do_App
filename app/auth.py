from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from .models import Users, db
import re

auth = Blueprint('auth', __name__)

def load_user(user_id):
    return Users.query.get(int(user_id))

@auth.route('/', methods=['GET', 'POST'])
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email format using a regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address format.', 'error')
            return redirect(url_for('auth.signup'))

        # Check if the email already exists in the database
        existing_user = Users.query.filter_by(email=email).first()
        if existing_user:
            flash('Email address already registered.', 'error')
            return redirect(url_for('auth.login'))

        # Validate password length
        if len(password) < 5:
            flash('Password must be at least 5 characters long.', 'error')
            return redirect(url_for('auth.signup'))

        new_user = Users(email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created!', 'success')
        login_user(new_user)
        return redirect(url_for('web.home'))

    return render_template('signup.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Validate email format using a regular expression
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address format.', 'error')
            return redirect(url_for('auth.login'))

        user = Users.query.filter_by(email=email).first()
        if not user:
            flash('You do not yet have an account. Please sign up', 'error')
            flash('', 'clear')
            return redirect(url_for('auth.signup'))

        if len(password) < 5:
            flash('Password must be at least 5 characters long.', 'error')
            return redirect(url_for('auth.login'))

        if user and user.password == password:
            login_user(user)
            flash('Logged in successfully', 'success')
            flash('', 'clear')
            return redirect(url_for('web.home'))
        else:
            flash('Login failed. Please check your credentials.', 'error')
            flash('', 'clear')

    return render_template('login.html')



@auth.route('/logout')
@login_required
def logout():
    """
    Logs out the current user and redirects to the login page.

    Returns:
        A redirect response to the login page.
    """
    logout_user()  # Log out the current user
    flash('Logged out successfully', 'success')
    flash('', 'clear')
    return redirect(url_for('auth.login'))
