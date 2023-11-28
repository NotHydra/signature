import bcrypt
import re
from gridfs import GridOut
from pdf2image import convert_from_bytes
from io import BytesIO
from fastapi import UploadFile
from PIL import Image

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

    def imageToPDF(file: GridOut) -> BytesIO:
        imageFile = Image.open(BytesIO(file.read()))
        pdfFile = BytesIO()

        imageFile.save(pdfFile, "PDF")

        pdfFile.seek(0)

        return BytesIO(pdfFile.getvalue())

    def replaceMultiple(text: str, targetArray: list[str], value: str) -> str:
        for targetObject in targetArray:
            text = text.replace(targetObject, value)

        return text
