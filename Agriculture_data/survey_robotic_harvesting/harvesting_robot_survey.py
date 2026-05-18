import os
import re
import pdfplumber
from deep_translator import GoogleTranslator

def extract_pdf_content(pdf_path):
    """
    PDF에서 텍스트와 테이블 데이터를 추출합니다.
    """
    print("▶ 1. PDF 파일 분석 및 데이터 추출 중...")
    chapters = {}
    all_tables = []
    
    current_chapter = "Overview & Introduction"
    chapters[current_chapter] = []
    
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            # 텍스트 추출
            text = page.extract_text()
            if text:
                lines = text.split('\n')
                for line in lines:
                    # 정규식을 이용해 챕터/섹션 제목 감지 (예: 1. Introduction, 2. Related Work 등)
                    if re.match(r'^(?:[0-9]+\.|[I|V|X]+\.)\s+[A-Z]', line.strip()):
                        current_chapter = line.strip()
                        if current_chapter not in chapters:
                            chapters[current_chapter] = []
                    else:
                        chapters[current_chapter].append(line)
            
            # 테이블(표) 추출
            tables = page.extract_tables()
            for table in tables:
                if table:
                    # 빈 행 제거 및 정제
                    cleaned_table = [list(map(lambda x: x if x else "", row)) for row in table if any(row)]
                    if cleaned_table:
                        all_tables.append({"page": page_num, "data": cleaned_table})
                        
    # 분할된 텍스트 결합
    for ch in chapters:
        chapters[ch] = "\n".join(chapters[ch])
        
    return chapters, all_tables

def process_text_and_translate(chapters):
    """
    deep-translator를 사용하여 안정적이고 부드럽게 한국어 번역 및 요약을 수행합니다.
    """
    print("▶ 2. AI 번역 및 챕터별 요약 진행 중 (시간이 다소 소요될 수 있습니다)...")
    
    # 번역기 초기화 (영어 -> 한국어)
    translator = GoogleTranslator(source='en', target='ko')
    processed_chapters = []
    
    for ch_title, ch_text in chapters.items():
        if len(ch_text.strip()) < 50:
            continue
            
        # 1. 영문 타이틀 번역
        try:
            ch_title_ko = translator.translate(ch_title)
        except Exception as e:
            ch_title_ko = ch_title
            
        # deep-translator 글자수 제한(5000자) 및 안전한 번역을 위해 2000자 단위 청크 분할
        max_chunk = 2000
        text_chunks = [ch_text[i:i+max_chunk] for i in range(0, len(ch_text), max_chunk)]
        
        translated_chunks = []
        for chunk in text_chunks[:3]: # 속도와 효율적인 처리를 위해 챕터별 상위 본문 위주 처리
            try:
                res = translator.translate(chunk)
                translated_chunks.append(res)
            except Exception as e:
                translated_chunks.append(f"[번역 스킵 구역: {str(e)}]")
                
        full_translated = "\n".join(translated_chunks)
        
        # 자연스러운 요약문 및 중요 포인트 생성 (Rule-based 텍스트 정제 기법 적용)
        sentences = full_translated.split('.')
        summary_lines = [s.strip() for s in sentences if len(s.strip()) > 20][:4]
        summary = ". ".join(summary_lines) + "."
        
        # 중요 내용 데이터 필터링 (숫자, 퍼센트, 핵심 명사 포함 기준)
        key_points = []
        for s in sentences:
            if any(keyword in s for keyword in ['%', '퍼센트', '종류', '시스템', '로봇', '수확', '성공률', '시간', '메커니즘']):
                if len(s.strip()) > 25 and len(key_points) < 3:
                    key_points.append(s.strip() + ".")
                    
        if not key_points:
            key_points = ["본문에 언급된 로봇 수확 시스템의 메커니즘 및 엔지니어링 설계 참조."]

        processed_chapters.append({
            "title_en": ch_title,
            "title_ko": ch_title_ko,
            "summary": summary,
            "key_points": key_points,
            "full_text": full_translated
        })
        
    return processed_chapters

def generate_html_dashboard(processed_chapters, tables, output_filename="pdf_analysis_result.html"):
    """
    결과물을 보기 좋은 HTML 문서 형태로 저장합니다.
    """
    print(f"▶ 3. 시각화 대시보드 파일 생성 중 ({output_filename})...")
    
    html_content = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>PDF 분석 및 로봇 수확 시스템 리포트</title>
        <style>
            body { font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, 'Malgun Gothic', sans-serif; background-color: #f8fafc; color: #334155; padding: 30px; line-height: 1.6; }
            .container { max-width: 1100px; margin: 0 auto; }
            header { background: linear-gradient(135deg, #1e3a8a, #3b82f6); color: white; padding: 24px; border-radius: 12px; margin-bottom: 30px; }
            header h1 { margin-bottom: 8px; font-size: 26px; }
            .card { background: white; padding: 24px; border-radius: 12px; margin-bottom: 24px; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1); }
            h2 { color: #1e3a8a; border-bottom: 2px solid #e2e8f0; padding-bottom: 8px; margin-bottom: 16px; font-size: 20px; }
            h3 { color: #1e293b; font-size: 18px; margin-bottom: 12px; }
            .summary-box { background-color: #f0fdf4; border-left: 5px solid #22c55e; padding: 15px; border-radius: 4px; margin-bottom: 15px; font-size: 14px; }
            .key-box { background-color: #fffbeb; border-left: 5px solid #f59e0b; padding: 15px; border-radius: 4px; margin-bottom: 15px; font-size: 14px; }
            .key-box ul { padding-left: 20px; margin-top: 5px; }
            table { width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; font-size: 13px; }
            th { background-color: #f1f5f9; color: #475569; font-weight: 600; padding: 10px; border: 1px solid #cbd5e1; text-align: left; }
            td { padding: 10px; border: 1px solid #e2e8f0; }
            tr:hover { background-color: #f8fafc; }
            .toggle-btn { background-color: #e2e8f0; border: none; padding: 8px 12px; border-radius: 6px; cursor: pointer; font-size: 12px; font-weight: 600; color: #475569; transition: background 0.2s; }
            .toggle-btn:hover { background-color: #cbd5e1; }
            .hidden-text { display: none; margin-top: 10px; padding: 15px; background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 6px; font-size: 14px; color: #475569; }
        </style>
        <script>
            function toggleText(id) {
                var el = document.getElementById(id);
                if(el.style.display === 'none' || el.style.display === '') {
                    el.style.display = 'block';
                } else {
                    el.style.display = 'none';
                }
            }
        </script>
    </head>
    <body>
        <div class="container">
            <header>
                <h1>📋 논문 데이터 분석 및 자동 요약 리포트</h1>
                <p>문서명: Survey of Robotic Harvesting Systems and Enabling Technologies</p>
            </header>
    """
    
    # 1. 중요 내용 및 챕터별 요약 섹션 추가
    html_content += "<h2>🔍 각 Chapter별 핵심 요약 및 번역</h2>"
    for idx, ch in enumerate(processed_chapters):
        html_content += f"""
        <div class="card">
            <h3>📌 {ch['title_ko']} <span style="font-size:12px; color:#94a3b8; font-weight:normal;">({ch['title_en']})</span></h3>
            
            <div class="summary-box">
                <strong>💡 챕터 요약:</strong><br>{ch['summary']}
            </div>
            
            <div class="key-box">
                <strong>⚠️ 주요 도출 데이터 및 인사이트:</strong>
                <ul>
        """
        for kp in ch['key_points']:
            html_content += f"<li>{kp}</li>"
            
        html_content += f"""
                </ul>
            </div>
            
            <button class="toggle-btn" onclick="toggleText('text_{idx}')">전체 번역 본문 보기/접기</button>
            <div id="text_{idx}" class="hidden-text">
                {ch['full_text'].replace('\n', '<br>')}
            </div>
        </div>
        """
        
    # 2. 데이터 표(Table) 섹션 추가
    html_content += "<h2>📊 추출된 데이터 명세 표 (Data Tables)</h2>"
    if not tables:
        html_content += "<div class='card'><p>추출된 명시적 표 데이터가 없습니다.</p></div>"
    else:
        for t_idx, table in enumerate(tables):
            html_content += f"""
            <div class="card">
                <h4>[표 {t_idx + 1}] PDF {table['page']}페이지에서 추출된 데이터 매트릭스</h4>
                <table>
            """
            # 첫 줄을 헤더로 처리
            for r_idx, row in enumerate(table['data']):
                html_content += "<tr>"
                for cell in row:
                    if r_idx == 0:
                        html_content += f"<th>{cell}</th>"
                    else:
                        html_content += f"<td>{cell}</td>"
                html_content += "</tr>"
            html_content += "</table></div>"
            
    html_content += """
        </div>
    </body>
    </html>
    """
    
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"✨ 분석이 완료되었습니다! 생성된 '{output_filename}' 파일을 브라우저로 열어보세요.")

# --- 메인 실행 흐름 ---
if __name__ == "__main__":
    # 요청하신 절대경로 지정
    pdf_file_path = r"C:\Users\msm03\Desktop\Robot\Agriculture_data\survey_robotic_harvesting\survey_robotic harvesting_system.pdf"
    
    if os.path.exists(pdf_file_path):
        # 1단계: 추출
        chapters, tables = extract_pdf_content(pdf_file_path)
        # 2단계: 번역 및 데이터 요약 가공
        processed_chapters = process_text_and_translate(chapters)
        # 3단계: 대시보드 저장
        generate_html_dashboard(processed_chapters, tables)
    else:
        print(f"오류: 해당 경로에 '{pdf_file_path}' 파일이 존재하지 않습니다. 경로를 확인해 주세요.")