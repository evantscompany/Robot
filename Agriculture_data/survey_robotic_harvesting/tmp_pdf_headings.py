from pathlib import Path
import pdfplumber

pdf_path = Path(r"C:\Users\msm03\Desktop\Robot\Agriculture_data\survey_robotic_harvesting\survey_robotic harvesting_system.pdf")
print('exists', pdf_path.exists(), 'size', pdf_path.stat().st_size if pdf_path.exists() else None)
with pdfplumber.open(pdf_path) as pdf:
    for i, page in enumerate(pdf.pages, start=1):
        text = page.extract_text() or ''
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        headings = [line for line in lines if line.startswith('Section') or line.startswith('1 ') or line.startswith('2 ') or line.startswith('3 ') or line.isupper() or line.startswith('Table') or line.startswith('Figure') or 'Contents' in line or 'Introduction' in line or 'Conclusion' in line or 'Related' in line or 'Robotic' in line]
        if headings:
            print(f"\n--- page {i} headings ---")
            for line in headings[:15]:
                print(line)
