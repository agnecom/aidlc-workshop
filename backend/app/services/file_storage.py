from __future__ import annotations
import os
import uuid

from app.config import settings

ALLOWED_EXTENSIONS = {"jpg", "jpeg", "png", "gif", "webp"}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB


class FileStorage:
    @staticmethod
    def save(file_content: bytes, filename: str) -> str:
        ext = filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
        if ext not in ALLOWED_EXTENSIONS:
            raise ValueError(f"Allowed extensions: {ALLOWED_EXTENSIONS}")
        if len(file_content) > MAX_FILE_SIZE:
            raise ValueError("File size exceeds 5MB limit")
        new_filename = f"{uuid.uuid4()}_{filename}"
        path = os.path.join(settings.upload_dir, new_filename)
        os.makedirs(settings.upload_dir, exist_ok=True)
        with open(path, "wb") as f:
            f.write(file_content)
        return f"/uploads/{new_filename}"

    @staticmethod
    def delete(image_url: str):
        if not image_url:
            return
        filename = image_url.split("/uploads/")[-1]
        path = os.path.join(settings.upload_dir, filename)
        if os.path.exists(path):
            os.remove(path)
