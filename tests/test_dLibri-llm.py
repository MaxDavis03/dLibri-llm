import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock
from dLibri_llm.py import make_safe_filename, extract_full_text, classify_with_llm, rename_pdf_file

# ------------------------
# Test make_safe_filename
# ------------------------
def test_make_safe_filename():
    raw = "005: CS/AI - Intro*to|LLMs"
    expected = "005 CSAI - IntrotoLLMs"
    assert make_safe_filename(raw) == expected

# ------------------------
# Test extract_full_text
# ------------------------
@pytest.fixture
def sample_pdf(tmp_path):
    # Create a sample 1-page PDF
    pdf_path = tmp_path / "test.pdf"
    import fitz
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((100, 100), "This is a test PDF document.")
    doc.save(str(pdf_path))
    return pdf_path

def test_extract_full_text(sample_pdf):
    text = extract_full_text(sample_pdf)
    assert "test PDF document" in text

# ------------------------
# Test classify_with_llm
# ------------------------
@patch("dlibrillm_modular.subprocess.run")
def test_classify_with_llm(mock_run):
    mock_run.return_value = MagicMock(stdout=b"005 Computer Science - Sample Title")
    text = "Some text about programming and AI."
    result = classify_with_llm(text)
    assert result.startswith("005")

# ------------------------
# Test rename_pdf_file
# ------------------------
@patch("dlibrillm_modular.classify_with_llm")
def test_rename_pdf_file(mock_classify, tmp_path):
    # Create PDF
    import fitz
    pdf_path = tmp_path / "original.pdf"
    doc = fitz.open()
    doc.new_page().insert_text((50, 50), "AI and machine learning content")
    doc.save(str(pdf_path))

    # Mock classifier
    mock_classify.return_value = "005 Computer Science - ML Basics"

    # Override output folder
    from dlibrillm_modular import OUTPUT_FOLDER
    OUTPUT_FOLDER.mkdir(parents=True, exist_ok=True)

    # Run rename
    new_path = rename_pdf_file(pdf_path)
    assert new_path.exists()
    assert new_path.name.startswith("005")
