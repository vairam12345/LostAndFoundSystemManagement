from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from app.db import mysql

app = Flask(_name_)
app.config.from_object('app.config')
bcrypt = Bcrypt(app)
mysql.init_app(app)

from app.auth_routes import auth_bp
from app.main_routes import main_bp
from app.report_routes import report_bp

app.register_blueprint(auth_bp)
app.register_blueprint(main_bp)
app.register_blueprint(report_bp)