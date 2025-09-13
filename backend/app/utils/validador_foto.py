from PIL import Image
import io

def validar_foto(image_bytes: bytes) -> bool:
    try:
        image = Image.open(io.BytesIO(image_bytes))
        width, height = image.size
        if width < 300 or height < 300:
            return False
        if image.format not in ["JPEG", "PNG"]:
            return False
        return True
    except Exception:
        return False

