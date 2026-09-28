#!/usr/bin/env python3
"""Convert the v1.1 preprint DOCX to PDF via Microsoft Word COM."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "Structural_Identifiability_Epistemic_Value_Active_Inference_v1.1.docx"
PDF = ROOT / "Structural_Identifiability_Epistemic_Value_Active_Inference_v1.1.pdf"


def convert() -> None:
    if not DOCX.exists():
        raise SystemExit(f"missing {DOCX}")
    import win32com.client

    word = win32com.client.Dispatch("Word.Application")
    word.Visible = False
    try:
        doc = word.Documents.Open(str(DOCX.resolve()))
        # 17 = wdFormatPDF
        doc.SaveAs(str(PDF.resolve()), FileFormat=17)
        doc.Close(False)
    finally:
        word.Quit()
    print("wrote", PDF, "bytes", PDF.stat().st_size)


if __name__ == "__main__":
    convert()
