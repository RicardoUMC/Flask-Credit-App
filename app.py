from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creditos.db'
db = SQLAlchemy(app)

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    return "todo"

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug = True, port = 8080)
