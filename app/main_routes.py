from flask import Blueprint, render_template

main_bp = Blueprint('main', _name_)

@main_bp.route('/')
def home():
    return render_template('welcome.html')

@main_bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_bp.route('/about')
def about():
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')