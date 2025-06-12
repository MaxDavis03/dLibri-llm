import re
import subprocess
from pathlib import Path
import fitz  # PyMuPDF
import time

INPUT_FOLDER = Path("input-files")
OUTPUT_FOLDER = Path("output-files")

# -------------------------
# Utils
# -------------------------
def make_safe_filename(name: str) -> str:
    """Sanitize a filename by removing unsafe characters."""
    name = name.split('\n')[0]  # Only the first line
    name = re.sub(r'[\\/*?:"<>|]', "", name)  # Remove forbidden characters
    return name.strip()

# -------------------------
# File Processing
# -------------------------
def extract_full_text(pdf_path: Path) -> str:
    try:
        doc = fitz.open(pdf_path)
        return "\n".join(page.get_text() for page in doc).strip()
    except Exception as e:
        return f"[ERROR] {e}"

def convert_to_pdf(input_path: Path) -> Path:
    """Convert supported file types to PDF using LibreOffice."""
    supported = [".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".txt"]
    if input_path.suffix.lower() in supported:
        try:
            subprocess.run([
                "libreoffice", "--headless", "--convert-to", "pdf", "--outdir", str(input_path.parent), str(input_path)
            ], check=True)
            return input_path.with_suffix(".pdf")
        except subprocess.CalledProcessError:
            print(f"[ERROR] Failed to convert {input_path.name} to PDF.")
            return None
    elif input_path.suffix.lower() == ".pdf":
        return input_path
    else:
        print(f"[SKIPPED] Unsupported file type: {input_path.name}")
        return None

def classify_with_llm(text: str) -> str:
    prompt = f"""
You are a librarian assistant. Based on the following document, assign it a Dewey Decimal Classification and a short descriptive title.

Respond ONLY in the format:
<DDD Dewey Category> - <Short Title>

Example:
005 Computer Science - Generative AI and LLMs

Document content:
{text[:3000]}
"""
    try:
        result = subprocess.run(
            ["ollama", "run", "mistral"],
            input=prompt.encode(),
            capture_output=True,
            timeout=600
        )
        return result.stdout.decode().strip()
    except Exception as e:
        return f"[ERROR] LLM failed: {e}"

def rename_pdf_file(pdf_path: Path) -> Path:
    text = extract_full_text(pdf_path)
    if text.startswith("[ERROR]"):
        print(text)
        return None

    suggestion = classify_with_llm(text)
    if suggestion.startswith("[ERROR]"):
        print(suggestion)
        return None

    new_filename = make_safe_filename(suggestion) + ".pdf"
    output_path = OUTPUT_FOLDER / new_filename

    try:
        OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)
        pdf_path.rename(output_path)
        print(f"Renamed to: {output_path.name}")
        return output_path
    except Exception as e:
        print(f"Rename failed: {e}")
        return None

def process_all_files():
    for file in INPUT_FOLDER.rglob("*.*"):
        pdf_path = convert_to_pdf(file)
        if pdf_path:
            print(f"Processing file: {pdf_path.name}")
            start_time = time.time()
            rename_pdf_file(pdf_path)
            end_time = time.time()
            print(f"Processed {pdf_path.name} in {end_time - start_time:.2f} seconds\n")

if __name__ == "__main__":
    if not INPUT_FOLDER.exists():
        print(f"Folder '{INPUT_FOLDER}' not found.")
    else:
        process_all_files()
