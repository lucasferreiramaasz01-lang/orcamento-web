from flask import Flask, render_template, request, redirect, session, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

app = Flask(__name__)
app.secret_key = "chave_super_secreta_123"

USUARIO = "lucas"
SENHA = "123456"

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["usuario"] == USUARIO and request.form["senha"] == SENHA:
            session["logado"] = True
            return redirect("/orcamento")
    return render_template("login.html")

@app.route("/orcamento", methods=["GET", "POST"])
def orcamento():
    if not session.get("logado"):
        return redirect("/")

    if request.method == "POST":
        nome = request.form["cliente"]
        endereco = request.form["endereco"]
        valor = request.form["valor"]

        pdf_path = "orcamento.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        largura, altura = A4

        # Logo fixa
        if os.path.exists("static/logo.png"):
            logo = ImageReader("static/logo.png")
            c.drawImage(logo, 0, altura - 120, width=largura, height=100)

        c.setFont("Helvetica-Bold", 18)
        c.drawString(50, altura - 160, "Proposta Comercial")

        c.setFont("Helvetica", 12)
        c.drawString(50, altura - 200, f"Cliente: {nome}")
        c.drawString(50, altura - 220, f"Endereço: {endereco}")
        c.drawString(50, altura - 240, f"Valor: R$ {valor}")

        c.save()
        return send_file(pdf_path, as_attachment=True)

    return render_template("orcamento.html")

if __name__ == "__main__":
    app.run()
