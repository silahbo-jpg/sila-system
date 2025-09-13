# backend/app/utils/pdf_generator.py
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
import qrcode
from PIL import Image
import os
import tempfile  # Adicionado para gerenciar arquivos temporários

def generate_pdf(filename: str, data: dict) -> str:
    """
    Gera um documento PDF com conteúdo de um dicionário e incorpora um QR code.
    Retorna o caminho completo para o arquivo PDF gerado.
    """
    # Garante que o diretório de PDFs existe
    pdf_dir = os.path.join("static", "pdfs")
    os.makedirs(pdf_dir, exist_ok=True)
    file_path = os.path.join(pdf_dir, filename)

    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    p.setTitle(data.get("type", "Documento Oficial"))

    # Título principal do documento
    p.setFont("Helvetica-Bold", 18)
    p.drawString(72, height - 72, f"{data.get('type', 'Documento').replace('_', ' ').upper()}")
    
    # Conteúdo do documento
    p.setFont("Helvetica", 12)
    y = height - 110
    
    # Adiciona os detalhes do documento ao PDF
    for key, value in data.items():
        if key in ["id", "documentPath"]:
            continue
        line = f"{key.replace('_', ' ').title()}: {value}"
        p.drawString(72, y, line)
        y -= 20
        if y < 72:  # Se a página estiver cheia, adiciona uma nova página
            p.showPage()
            y = height - 72

    # Geração do QR Code
    qr_content = f"http://127.0.0.1:8000/validate/{data.get('type', 'document').lower()}/{data.get('id')}"
    if not data.get('id'):
        qr_content = "http://127.0.0.1:8000/validate/document"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4)
    qr.add_data(qr_content)
    qr.make(fit=True)

    # Cria um arquivo temporário para o QR code
    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as tmp_file:
        # Gera a imagem do QR code
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(tmp_file.name, format='PNG')
        
        # Desenha a imagem no PDF
        qr_size = 1.5 * inch
        p.drawImage(tmp_file.name, width - 72 - qr_size, 72, width=qr_size, height=qr_size)
        
        # Remove o arquivo temporário
        os.unlink(tmp_file.name)

    # Salva o PDF
    p.save()
    
    # Salva o buffer no arquivo final
    with open(file_path, "wb") as f:
        f.write(buffer.getvalue())
    
    # Fecha os buffers
    buffer.close()

    return file_path

