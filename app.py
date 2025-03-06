from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///creditos.db'
db = SQLAlchemy(app)

# The class `Credito` represents a credit entity with attributes such as id, cliente, monto,
# tasa_interes, plazo, and fecha_otorgamiento.
class Credito(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    cliente = db.Column(db.String(100), nullable = False)
    monto = db.Column(db.Float, nullable = False)
    tasa_interes = db.Column(db.Float, nullable = False)
    plazo = db.Column(db.Integer, nullable = False)
    fecha_otorgamiento = db.Column(db.String(10), nullable = False)

@app.route('/api/creditos', methods=['GET'])
def obtener_creditos():
    """
    The function `obtener_creditos` retrieves credit information from a database and returns it in JSON
    format.
    
    Returns:
      The function `obtener_creditos()` is returning a JSON response containing information about
    credits. The information includes the client's name, the credit amount, and other details such as
    interest rate, term, and date of approval. This data is fetched from the database using SQLAlchemy's
    `query` method and then converted into a JSON format using `jsonify`.
    """
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
    """
    The `registrar` function handles the registration of a new credit entry in a database based on user
    input.
    
    Returns:
      If the request method is "POST", the function is returning a redirect to the 'index' route. If the
    request method is not "POST", the function is returning the rendered template "registro.html".
    """
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
    """
    The `editar` function in Python is used to update credit information in a database based on user
    input through a form.
    
    Args:
      id: The `id` parameter in the `editar` function is used to identify the specific credit record
    that needs to be edited. This function retrieves the credit record with the given `id` from the
    database using `Credito.query.get_or_404(id)`.
    
    Returns:
      If the request method is 'POST' and the credit information is successfully updated in the
    database, the function will return a redirect to the 'index' route. If there is an exception during
    the database commit, it will return the message "Hubo un problema al modificar el crédito". If the
    request method is not 'POST', it will render the 'modificacion.html' template with the credit
    """
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
    """
    This Python function deletes a credit record from a database and redirects to the index page,
    handling any potential errors.
    
    Args:
      id: The `eliminar` function takes an `id` as a parameter. This `id` is used to retrieve a specific
    credit record from the database using `Credito.query.get_or_404(id)`. The function then attempts to
    delete this record from the database using `db.session.delete(cred
    
    Returns:
      If the deletion of the credit is successful, the function will return a redirect to the 'index'
    route. If there is a problem during the deletion process, it will return the message "Hubo un
    problema al eliminar el crédito".
    """
    credito = Credito.query.get_or_404(id)
    try:
        db.session.delete(credito)
        db.session.commit()
        return redirect(url_for('index'))
    except:
        return "Hubo un problema al eliminar el crédito"

@app.route('/')
def index():
    """
    The `index` function retrieves all credit records from the database and renders them in the
    `index.html` template.
    
    Returns:
      The `index()` function is returning a rendered template called 'index.html' along with a list of
    credits sorted by the 'fecha_otorgamiento' attribute. The list of credits is passed to the template
    as a variable named 'creditos'.
    """
    creditos = Credito.query.order_by(Credito.fecha_otorgamiento).all()
    return render_template('index.html', creditos = creditos)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug = True, port = 8080)
