from pathlib import Path
import pdfplumber

pdf_path = Path(r"C:\Users\msm03\Desktop\Robot\Agriculture_data\survey_robotic_harvesting\survey_robotic harvesting_system.pdf")
print('exists', pdf_path.exists(), 'size', pdf_path.stat().st_size if pdf_path.exists() else None)
with pdfplumber.open(pdf_path) as pdf:
    print('pages', len(pdf.pages))
    for i in range(min(3, len(pdf.pages))):
        text = pdf.pages[i].extract_text()
        print('\n--- page', i+1, '---')
        if text:
            print(text[:3000])
        else:
            print('<no text>')
