import bcrypt

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
