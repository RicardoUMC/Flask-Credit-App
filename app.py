from flask import Flask, render_template, request, redirect, url_for, jsonify
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

@app.route('/api/creditos', methods=['GET'])
def obtener_creditos():
    creditos = Credito.query.order_by(Credito.fecha_otorgamiento).all()
    datos = []
    for credito in creditos:
        datos.append({
            'cliente': credito.cliente,
            'monto': credito.monto,
            # Los siguientes datos no se utilizan en el frontend, aunque se podrían acceder
            'tasa_interes': credito.tasa_interes,
            'plazo': credito.plazo,
            'fecha_otorgamiento': credito.fecha_otorgamiento
        })
    return jsonify(datos)

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

        return redirect(url_for('index'))
    else:
        return render_template("registro.html")

@app.route('/editar/<int:id>', methods = ['GET', 'POST'])
def editar(id):
    credito = Credito.query.get_or_404(id)
    if request.method == 'POST':
        credito.cliente = request.form['cliente']
        credito.monto = float(request.form['monto'])
        credito.tasa_interes = float(request.form['tasa_interes'])
        credito.plazo = int(request.form['plazo'])
        fecha_otorgamiento = request.form['fecha_otorgamiento']
        credito.fecha_otorgamiento = datetime.strptime(fecha_otorgamiento, '%Y-%m-%d').date()
        
        try:
            db.session.commit()
            return redirect(url_for('index'))
        except:
            return "Hubo un problema al modificar el crédito"

    else:
        return render_template('modificacion.html', credito = credito)

@app.route('/eliminar/<int:id>')
def eliminar(id):
    credito = Credito.query.get_or_404(id)
    try:
        db.session.delete(credito)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Hubo un problema al eliminar el crédito"

@app.route('/')
def index():
    creditos = Credito.query.order_by(Credito.fecha_otorgamiento).all()
    return render_template('index.html', creditos = creditos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug = True, port = 8080)
