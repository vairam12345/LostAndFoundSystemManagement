from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.db import mysql
from app import bcrypt

auth_bp = Blueprint('auth', _name_)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cur.close()
        flash("Registration successful! Please log in.", "success")
        return redirect(url_for('auth.login'))
    return render_template('register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cur.fetchone()
        cur.close()

        if user and bcrypt.check_password_hash(user[3], password):
            session['logged_in'] = True
            session['username'] = user[1]
            return redirect(url_for('main.dashboard'))
        else:
            flash("Invalid credentials. Please try again.", "danger")
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.home'))