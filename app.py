from flask import Flask, render_template, request, make_response, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from PIL import Image
from funtion.supa import datos

app = Flask(__name__)

@app.before_request
def cargar_datos():
    global items
    items = datos("https://ymhtktsffxmaajexzney.supabase.co/rest/v1/Productos?select=*","eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InltaHRrdHNmZnhtYWFqZXh6bmV5Iiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY4NDA0NDcyNCwiZXhwIjoxOTk5NjIwNzI0fQ.aw9AKo_rs39WTNGjorSexD79k-Izt5cmUdDCnBcVXfM")

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/catalogo/<int:item_id>')
def detalle_item(item_id):
    # Encuentra el item correspondiente en la lista de items
    item = None
    for i in items:
        if i['id'] == item_id:
            item = i
            break

    # Renderiza el template de detalle de item y pasa el item como argumento
    return render_template('detalle_item.html', item=item)

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf():
    nombre = request.form['nombre']
    precio = request.form['precio']
    descripcion = request.form['descripcion']
    imagen_url = request.form['imagen_url']

    item = {
        'Nombreproducto': nombre,
        'Precio': precio,
        'Descripcion': descripcion,
        'URLim': imagen_url
    }

    response = generate_pdf(item)
    response.headers['Content-Disposition'] = 'attachment; filename=detalle_item.pdf'
    return response

@app.route('/contacto', methods=['GET', 'POST'])
def contacto():
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        mensaje = request.form.get('mensaje')

        # Generar el archivo PDF
        response = generate_pdf({'nombre': nombre, 'email': email, 'mensaje': mensaje})
        response.headers['Content-Disposition'] = 'attachment; filename=contacto.pdf'
        return response

    return render_template('contacto.html')

@app.route('/catalogo')
def catalog():
    return render_template('catalogo.html', items=items)

@app.route('/recibo/<int:item_id>', methods=['GET', 'POST'])
def recibo(item_id):
    # Encuentra el item correspondiente en la lista de items
    item = None
    for i in items:
        if i['id'] == item_id:
            item = i
            break

    if request.method == 'GET':
        return render_template('recibo.html', item=item)

    # Renderiza el template del recibo y pasa el item como argumento
    return render_template('recibo.html', item=item)

def generate_pdf(item):
    # Crear un objeto BytesIO para almacenar el PDF generado en memoria
    buffer = BytesIO()

    # Crear el objeto PDF con ReportLab
    p = canvas.Canvas(buffer, pagesize=letter)

    # Agregar contenido al PDF
    p.setFont("Helvetica", 12)
    p.drawString(50, 750, "Nombre del producto: {}".format(item['Nombreproducto']))
    p.drawString(50, 730, "Precio: {}".format(item['Precio']))

    # Agrega más detalles del producto según tus necesidades

    p.drawString(50, 700, "Total: $XX.XX")

    # Guardar el PDF en el objeto BytesIO
    p.showPage()
    p.save()

    # Mover el puntero del objeto BytesIO al inicio del archivo
    buffer.seek(0)

    # Crear una respuesta HTTP con el PDF generado
    response = make_response(buffer.getvalue())
    response.headers['Content-Type'] = 'application/pdf'

    return response

if __name__ == '__main__':
    app.run(debug=True)
