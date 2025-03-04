from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creditos.db'
db = SQLAlchemy(app)

class Credito(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cliente = db.Column(db.String(100), nullable = False)
    monto = db.Column(db.Float, nullable = False)
    tasa_interes = db.Column(db.Float, nullable = False)
    plazo = db.Column(db.Integer, nullable = False)
    fecha_otorgamiento = db.Column(db.String(10), nullable = False)

    def __repr__(self):
        return '<Credito %r>' % self.id

with app.app_context():
    db.create_all()

@app.route('/registrar', methods=['GET', 'POST'])
def registrar():
    if request.method == "POST":
        cliente = request.form['cliente']
        monto = float(request.form['monto'])
        tasa_interes = float(request.form['tasa_interes'])
        plazo = int(request.form['plazo'])
        fecha_otorgamiento = request.form['fecha_otorgamiento']
        fecha_otorgamiento = datetime.strptime(fecha_otorgamiento, '%Y-%m-%d').date()

        nuevo_credito = Credito(
            cliente = cliente,
            monto = monto,
            tasa_interes = tasa_interes,
            plazo = plazo,
            fecha_otorgamiento = str(fecha_otorgamiento)
        )

        db.session.add(nuevo_credito)
        db.session.commit()

        return redirect('/')
    else:
        return render_template("registro.html")

@app.route('/')
def index():
    creditos = Credito.query.order_by(Credito.fecha_otorgamiento).all()
    return render_template('index.html', creditos = creditos)

if __name__ == '__main__':
    app.run(debug = True, port = 8080)
