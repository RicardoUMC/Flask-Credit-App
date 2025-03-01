import sqlite3
from flask impor Flask, render_tamble, request, redirect, url_for

app = Flask(__name__)

@app.route('/register', methods=['GET', 'POST'])

