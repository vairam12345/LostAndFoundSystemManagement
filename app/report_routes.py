from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.db import mysql
import os
from werkzeug.utils import secure_filename

report_bp = Blueprint('report', _name_)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

@report_bp.route('/upload', methods=['GET', 'POST'])
def upload_report():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join('app/static/uploads', filename)
            file.save(filepath)

            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO reports (title, description, image) VALUES (%s, %s, %s)", (title, description, filename))
            mysql.connection.commit()
            cur.close()

            flash("Report submitted successfully!", "success")
            return redirect(url_for('main.dashboard'))
    return render_template('upload_report.html')

@report_bp.route('/view_reports')
def view_reports():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM reports")
    reports = cur.fetchall()
    cur.close()
    return render_template('view_reports.html', reports=reports)