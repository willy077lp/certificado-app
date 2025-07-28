
from flask import Flask, render_template, request, send_file
from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import qrcode
import io

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generar", methods=["POST"])
def generar():
    nombre = request.form["nombre"]
    ci = request.form["ci"]

    texto_qr = f"{nombre} - C.I.: {ci} - FEDERACIÓN REGIONAL DE TRABAJADORES DE EDUCACIÓN URBANA DE UYUNI (F.RE.T.E.U.-U) - FEDERACIÓN REGIONAL DE TRABAJADORES DE EDUCACIÓN URBANA DE VILLAZÓN (F.R.T.E.U.V.)"

    qr_img = qrcode.make(texto_qr)
    qr_buffer = io.BytesIO()
    qr_img.save(qr_buffer, format='PNG')
    qr_buffer.seek(0)
    qr_image = ImageReader(qr_buffer)

    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 18)
    can.drawCentredString(390, 320, nombre)
    can.drawImage(qr_image, x=675, y=85, width=80, height=80)
    can.save()
    packet.seek(0)

    plantilla_path = "plantilla.pdf"
    original = PdfReader(plantilla_path)
    new_layer = PdfReader(packet)
    page = original.pages[0]
    page.merge_page(new_layer.pages[0])

    output = PdfWriter()
    output.add_page(page)

    output_path = f"{nombre.replace(' ', '_')}_certificado.pdf"
    with open(output_path, "wb") as f:
        output.write(f)

    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
