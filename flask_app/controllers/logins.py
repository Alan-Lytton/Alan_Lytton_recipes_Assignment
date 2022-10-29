from flask import render_template, redirect, request, session
from flask_app.models.login import Login  #change this import line based on your extra .py file for generating OOP instances
from flask_bcrypt import Bcrypt
from flask_app import app

bcrypt = Bcrypt(app)

@app.route("/")     # lines 6 through 11 can be changed depending on what we need controller to do.
def home():
    return render_template("log_reg.html")

@app.route('/destroy-session')
def destroy():
    session.clear()
    return redirect('/')

@app.route("/create_user", methods = ['POST'])
def f_register():
    if not Login.validate_reg(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'fname': request.form['fname'],
        'lname': request.form['lname'],
        'email': request.form['email'],
        'password': pw_hash
    }
    data2 = {
        'user_id': Login.register_user(data)
    }
    session['user_id'] = Login.get_one_reg(data2)
    return redirect('/recipes')

@app.route('/login', methods = ['POST'])
def f_login():
    if not Login.validate_login(request.form):
        return redirect('/')
    data = {
        'email': request.form['email']
    }
    user_id = Login.get_one_login(data)
    session['user_id'] = user_id
    print(session['user_id'])
    return redirect('/recipes')