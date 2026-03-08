import os
from datetime import datetime
from docx import Document
from pypdf import PdfReader


def read_file(filepath: str) -> dict:
    try:
        if not os.path.exists(filepath):
            return {"success": False, "error": "File not found"}

        ext = os.path.splitext(filepath)[1].lower()
        content = ""

        if ext == ".txt":
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        elif ext == ".pdf":
            reader = PdfReader(filepath)
            for page in reader.pages:
                content += page.extract_text()

        elif ext == ".docx":
            doc = Document(filepath)
            for para in doc.paragraphs:
                content += para.text + "\n"

        else:
            return {"success": False, "error": "Unsupported file format"}

        metadata = {
            "filename": os.path.basename(filepath),
            "size": os.path.getsize(filepath),
            "modified": str(datetime.fromtimestamp(os.path.getmtime(filepath)))
        }

        return {"success": True, "content": content, "metadata": metadata}

    except Exception as e:
        return {"success": False, "error": str(e)}


def list_files(directory: str, extension: str = None) -> list:
    try:
        files = []

        for file in os.listdir(directory):

            if extension and not file.endswith(extension):
                continue

            path = os.path.join(directory, file)

            if os.path.isfile(path):
                files.append({
                    "name": file,
                    "size": os.path.getsize(path),
                    "modified": str(datetime.fromtimestamp(os.path.getmtime(path)))
                })

        return files

    except Exception as e:
        return [{"error": str(e)}]


def write_file(filepath: str, content: str) -> dict:
    try:
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return {"success": True, "message": "File written successfully"}

    except Exception as e:
        return {"success": False, "error": str(e)}


def search_in_file(filepath: str, keyword: str) -> dict:
    try:
        data = read_file(filepath)

        if not data["success"]:
            return data

        text = data["content"].lower()
        keyword = keyword.lower()

        matches = []

        if keyword in text:
            index = text.find(keyword)

            start = max(0, index - 40)
            end = index + 40

            matches.append(data["content"][start:end])

        return {
            "success": True,
            "matches": matches
        }

    except Exception as e:
        return {"success": False, "error": str(e)}