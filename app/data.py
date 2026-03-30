from langchain_community.document_loaders import TextLoader, PyPDFLoader
from pathlib import Path
import hashlib
from typing import List, Dict
from PIL import Image
import pytesseract

class DocumentLoader:
    def __init__(self, path: str):
        self.path = Path(path)

    def load(self) -> List[Dict[str, any]]:
        docs = []
        for file in self.path.rglob("*"):
            if not file.is_file():
                continue
            try:
                content = self._read_file(file)
                if not content:
                    continue
                doc_hash = hashlib.md5(content.encode("utf-8")).hexdigest()
                docs.append({
                    "id": str(file),
                    "content": content,
                    "hash": doc_hash,
                    "metadata": {
                        "file_name": str(file),
                        "file_type": file.suffix,
                        "path": str(file)
                    }
                })
            except Exception as e:
                print(f"Error: {e}")
        return docs

    def _read_file(self, file: Path) -> str:
        suffix = file.suffix.lower()

        if suffix in [".txt", ".md"]:
            return TextLoader(str(file), encoding="utf-8").load()[0].page_content

        if suffix == ".pdf":
            return PyPDFLoader(file).load()[0].page_content

        if suffix in [".png", ".jpg"]:
            image = Image.open(file)
            text = pytesseract.image_to_string(image)
            return text.strip()

        else:
            return ""