from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from sqlalchemy.orm import Session
from . import db
import bcrypt
from flask_login import login_user, login_required, logout_user,current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')   #Here i gonna get the email and password
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first() 
        if user and user.password:
            hashed_password = user.password.encode('utf-8')  # Ensure the stored password is encoded
            if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):  # Check password using bcrypt
                flash('Logged in successfully!')
                login_user(user, remember=True) # Remember that the user is logged
                return redirect(url_for('views.home'))
                
            else:
                flash('Invalid email or password', category='error')
        else:
            flash('Invalid email or password', category='error')

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return render_template("logout.html", user=current_user)

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email is too short', category='error')
        elif len(first_name) < 2:
            flash('First name must be longer than 2 characters', category='error')
        elif password1 != password2:
            flash('Passwords do not match', category='error')
        else:
            hashed_password = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())    #Funcion on bcrypt
            new_user = User(email=email, first_name=first_name, password=hashed_password.decode('utf-8'))    #Here i gonna hash the password
            db.session.add(new_user)    #Here i add the user to the database
            db.session.commit()         #Here i confirm the changes 
            flash('Account created!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up.html", user=current_user)