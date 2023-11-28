import bcrypt
import re
from pdf2image import convert_from_bytes
from io import BytesIO
from fastapi import UploadFile

from typing import Dict, Any


class Utility:
    def formatResponse(
        success: bool, status: int, message: str, data: Any
    ) -> Dict[str, any]:
        return {
            "success": success,
            "status": status,
            "message": message,
            "data": data,
        }

    def encrypt(text: str):
        return bcrypt.hashpw(text.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def decrypt(text: str, hashed: str):
        return bcrypt.checkpw(text.encode("utf-8"), hashed.encode("utf-8"))

    def checkEmail(email: str) -> bool:
        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+", email):
            return True

        else:
            return False

    def pdfToImage(file: UploadFile) -> UploadFile:
        imageFile = convert_from_bytes(file.file.read(), fmt="png")[0]

        imageByte = BytesIO()
        imageFile.save(imageByte, format="PNG", optimize=True, quality=50)

        return UploadFile(
            filename=file.filename.replace(".pdf", ".png"),
            file=imageByte.getvalue(),
            headers="image/png",
        )
