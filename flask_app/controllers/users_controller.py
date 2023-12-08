from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.users_model import User #importing the class here
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/clear')
    data = {
        "id": session['user_id']
    }
    return render_template("dashboard.html" , users = User.get_user_by_id(data))

@app.route('/register', methods = ['POST'])
def register():
    if not User.validate_users(request.form):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    data = {
    "first_name": request.form['first_name'],
    "last_name": request.form['last_name'],
    "email": request.form['email'],
    "password": pw_hash
    }
    user_id = User.save_users(data)
    session['user_id'] = user_id
    return redirect('/dashboard')

@app.route('/login', methods = ['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    specific_user = User.get_emails(data)
    if not specific_user:
        flash("Invalid Email", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(specific_user.password, request.form['password']):
        flash("Invalid Password", "login")
        return redirect('/')
    session['user_id'] = specific_user.id
    return redirect('/dashboard')

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect('/')