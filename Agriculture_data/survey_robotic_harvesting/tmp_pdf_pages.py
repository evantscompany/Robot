from pathlib import Path
import pdfplumber
pdf_path = Path(r"C:\Users\msm03\Desktop\Robot\Agriculture_data\survey_robotic_harvesting\survey_robotic harvesting_system.pdf")
with pdfplumber.open(pdf_path) as pdf:
    for page_num in [2,3,4,5,8,20,26,28,29]:
        if page_num <= len(pdf.pages):
            page = pdf.pages[page_num-1]
            print(f"\n=== page {page_num} ===")
            text = page.extract_text() or ''
            print(text[:5000])
