from flask import Flask, render_template, request, redirect, session, send_file
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from datetime import datetime
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

        cliente = request.form["cliente"]
        endereco = request.form["endereco"]
        equipamento = request.form["equipamento"]
        tamanho = request.form["tamanho"]
        cor = request.form["cor"]
        descricao = request.form["descricao"]
        valor = request.form["valor"]
        pagamento = request.form["pagamento"]
        previsao = request.form["previsao"]

        foto = request.files["foto"]

        pdf_path = "orcamento.pdf"
        c = canvas.Canvas(pdf_path, pagesize=A4)
        largura, altura = A4

        # 🔹 LOGO FIXA
        if os.path.exists("static/logo.png"):
            logo = ImageReader("static/logo.png")
            c.drawImage(logo, 0, altura - 130, width=largura, height=110)

        # 🔹 TÍTULO
        c.setFont("Helvetica-Bold", 18)
        c.drawCentredString(largura / 2, altura - 160, "Proposta Comercial")

        # 🔹 DADOS
        y = altura - 200
        c.setFont("Helvetica", 12)

        c.drawString(50, y, f"Cliente: {cliente}")
        y -= 25
        c.drawString(50, y, f"Endereço: {endereco}")
        y -= 25
        c.drawString(50, y, f"Tipo de equipamento: {equipamento}")
        y -= 25
        c.drawString(50, y, f"Tamanho: {tamanho}")
        y -= 25
        c.drawString(50, y, f"Cor: {cor}")
        y -= 25
        c.drawString(50, y, f"Descrição: {descricao}")
        y -= 35

        # 🔹 VALOR DESTACADO
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, f"Valor: R$ {valor}")
        y -= 40

        # 🔹 FOTO DO PRODUTO (ÁREA FIXA)
        if foto and foto.filename != "":
            try:
                from PIL import Image, ImageOps

                imagem = Image.open(foto.stream)

                # Corrige rotação automática do celular
                imagem = ImageOps.exif_transpose(imagem)

                imagem = imagem.convert("RGB")

                # Redimensiona mantendo proporção
                max_largura = 300
                max_altura = 200
                imagem.thumbnail((max_largura, max_altura))

                temp_path = "temp_foto.jpg"
                imagem.save(temp_path)

                img = ImageReader(temp_path)

                # POSIÇÃO FIXA (não depende do texto)
                pos_x = 50
                pos_y = 250  # altura fixa da imagem

                c.drawImage(img, pos_x, pos_y,
                            width=imagem.width,
                            height=imagem.height)

                os.remove(temp_path)

            except Exception as e:
                print("Erro ao processar imagem:", e)

        # 🔹 CONDIÇÕES
        c.setFont("Helvetica", 12)
        c.drawString(50, y, f"Condições de pagamento: {pagamento}")
        y -= 25
        c.drawString(50, y, f"Previsão de instalação: {previsao}")

        # 🔹 ASSINATURA
        y -= 60
        c.line(50, y, 250, y)
        c.drawString(50, y - 15, "Assinatura do responsável")

        c.save()
        return send_file(pdf_path, as_attachment=True)

    return render_template("orcamento.html")

if __name__ == "__main__":
    app.run()
