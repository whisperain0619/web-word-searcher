from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# 경고 무시
logging.getLogger('selenium').setLevel(logging.CRITICAL)

app = Flask(__name__)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}


@app.route('/')
def home():
    """웹 UI"""
    html = """
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>🔍 웹 단어 검색기</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            
            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                max-width: 700px;
                width: 100%;
                padding: 40px;
            }
            
            h1 {
                text-align: center;
                color: #333;
                margin-bottom: 30px;
                font-size: 2.5em;
            }
            
            .form-group {
                margin-bottom: 20px;
            }
            
            label {
                display: block;
                margin-bottom: 8px;
                color: #333;
                font-weight: 600;
                font-size: 1.1em;
            }
            
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 1em;
                transition: border-color 0.3s;
            }
            
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            
            .button-group {
                display: flex;
                gap: 10px;
                margin-top: 20px;
            }
            
            button {
                flex: 1;
                padding: 12px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s;
            }
            
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            
            .btn-secondary {
                background: #f0f0f0;
                color: #333;
            }
            
            .btn-secondary:hover {
                background: #e0e0e0;
            }
            
            .result {
                margin-top: 30px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                border-left: 4px solid #667eea;
                display: none;
            }
            
            .result.show {
                display: block;
            }
            
            .result-item {
                display: flex;
                justify-content: space-between;
                padding: 12px;
                background: white;
                border-radius: 6px;
                margin-bottom: 10px;
                border-left: 3px solid #667eea;
            }
            
            .word {
                font-weight: 600;
                color: #333;
            }
            
            .count {
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 20px;
                font-weight: 600;
            }
            
            .loading {
                text-align: center;
                padding: 20px;
                display: none;
            }
            
            .loading.show {
                display: block;
            }
            
            .spinner {
                border: 4px solid #f3f3f3;
                border-top: 4px solid #667eea;
                border-radius: 50%;
                width: 30px;
                height: 30px;
                animation: spin 1s linear infinite;
                margin: 0 auto 10px;
            }
            
            @keyframes spin {
                0% { transform: rotate(0deg); }
                100% { transform: rotate(360deg); }
            }
            
            .stats {
                display: grid;
                grid-template-columns: 1fr 1fr 1fr;
                gap: 10px;
                margin-top: 20px;
            }
            
            .stat-box {
                background: white;
                padding: 15px;
                border-radius: 8px;
                text-align: center;
                border: 2px solid #667eea;
            }
            
            .stat-label {
                font-size: 0.9em;
                color: #666;
            }
            
            .stat-value {
                font-size: 1.8em;
                font-weight: 600;
                color: #667eea;
                margin-top: 5px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🔍 웹 단어 검색기</h1>
            
            <div class="form-group">
                <label>🔗 웹사이트 URL</label>
                <input type="url" id="urlInput" placeholder="https://example.com">
            </div>
            
            <div class="form-group">
                <label>🔎 찾을 단어 (쉼표로 구분)</label>
                <input type="text" id="wordsInput" placeholder="예: 논리적글쓰기, 미분적분학">
            </div>
            
            <div class="button-group">
                <button class="btn-primary" onclick="searchWords()">🚀 검색하기</button>
                <button class="btn-secondary" onclick="clearForm()">🗑️ 초기화</button>
            </div>
            
            <!-- 로딩 -->
            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p id="loadingText">크롤링 중... (30초 정도 소요) ⏳</p>
            </div>
            
            <!-- 결과 -->
            <div class="result" id="result">
                <h2 style="margin-bottom: 15px; color: #333;">📊 검색 결과</h2>
                
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-label">총 단어 수</div>
                        <div class="stat-value" id="totalWords">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">검색된 단어</div>
                        <div class="stat-value" id="foundCount">0</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-label">일치율</div>
                        <div class="stat-value" id="matchRate">0%</div>
                    </div>
                </div>
                
                <div id="resultList" style="margin-top: 20px;"></div>
            </div>
        </div>
        
        <script>
            function showLoading() {
                document.getElementById('loading').classList.add('show');
                document.getElementById('result').classList.remove('show');
            }
            
            function hideLoading() {
                document.getElementById('loading').classList.remove('show');
            }
            
            async function searchWords() {
                const url = document.getElementById('urlInput').value;
                const wordsInput = document.getElementById('wordsInput').value;
                
                if (!url.trim()) {
                    alert('URL을 입력해주세요!');
                    return;
                }
                
                if (!wordsInput.trim()) {
                    alert('찾을 단어를 입력해주세요!');
                    return;
                }
                
                showLoading();
                
                try {
                    const response = await fetch('/api/search', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({
                            url: url,
                            words: wordsInput.split(',').map(w => w.trim().toLowerCase())
                        })
                    });
                    
                    const data = await response.json();
                    hideLoading();
                    
                    if (data.success) {
                        showResults(data);
                    } else {
                        alert('오류: ' + data.error);
                    }
                } catch (e) {
                    hideLoading();
                    alert('오류 발생: ' + e.message);
                }
            }
            
            function showResults(data) {
                const totalWords = data.total_words;
                const results = data.results;
                
                // 통계
                let foundCount = 0;
                let totalFoundWords = 0;
                
                for (let word in results) {
                    if (results[word] > 0) {
                        foundCount++;
                        totalFoundWords += results[word];
                    }
                }
                
                const matchRate = totalWords > 0 ? Math.round((totalFoundWords / totalWords) * 100) : 0;
                
                document.getElementById('totalWords').textContent = totalWords.toLocaleString();
                document.getElementById('foundCount').textContent = foundCount;
                document.getElementById('matchRate').textContent = matchRate + '%';
                
                // 결과 리스트
                let html = '';
                const sorted = Object.entries(results).sort((a, b) => b[1] - a[1]);
                
                for (let [word, count] of sorted) {
                    const bgColor = count > 0 ? '#e8f5e9' : '#ffebee';
                    const textColor = count > 0 ? '#2e7d32' : '#c62828';
                    
                    html += `
                        <div class="result-item" style="background-color: ${bgColor};">
                            <span class="word" style="color: ${textColor};">"${word}"</span>
                            <span class="count" style="background-color: ${textColor};">${count}개</span>
                        </div>
                    `;
                }
                
                document.getElementById('resultList').innerHTML = html;
                document.getElementById('result').classList.add('show');
            }
            
            function clearForm() {
                document.getElementById('urlInput').value = '';
                document.getElementById('wordsInput').value = '';
                document.getElementById('result').classList.remove('show');
            }
        </script>
    </body>
    </html>
    """
    return html


@app.route('/api/search', methods=['POST'])
def search_words():
    """웹에서 단어 검색 (Selenium으로 강화된 크롤링)"""
    driver = None
    try:
        data = request.get_json()
        url = data.get('url', '').strip()
        words = data.get('words', [])
        
        if not url:
            return jsonify({'error': 'URL을 입력해주세요'}), 400
        
        if not words:
            return jsonify({'error': '단어를 입력해주세요'}), 400
        
        # URL 준비
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Selenium 설정 (헤드리스, 최적화)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--start-maximized')
        options.add_argument(f'user-agent={HEADERS["User-Agent"]}')
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        driver = webdriver.Chrome(options=options)
        
        # 페이지 로드
        driver.get(url)
        
        # JavaScript 실행 완료 대기 (최대 15초)
        try:
            WebDriverWait(driver, 15).until(
                lambda driver: driver.execute_script('return document.readyState') == 'complete'
            )
        except:
            pass
        
        # 추가 대기 (동적 콘텐츠 로드)
        time.sleep(5)
        
        # 페이지 아래로 여러 번 스크롤 (더 많은 콘텐츠 로드)
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)
        
        # HTML 가져오기 (완전히 렌더링된 상태)
        html_content = driver.page_source
        
        # BeautifulSoup으로 파싱
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # 스크립트, 스타일 제거
        for script in soup(['script', 'style', 'meta', 'link']):
            script.decompose()
        
        # 모든 텍스트 가져오기 (숨겨진 텍스트, 속성 텍스트도 포함)
        text = soup.get_text(separator=' ', strip=True).lower()
        
        # 단어로 분리 (한글 포함)
        all_words = re.findall(r'[a-zA-Z0-9가-힣ㄱ-ㅎㅏ-ㅣ]+', text)
        
        # 단어 개수
        total_words = len(all_words)
        
        # 각 단어 카운트
        results = {}
        for word in words:
            if word:
                count = all_words.count(word)
                results[word] = count
        
        return jsonify({
            'success': True,
            'total_words': total_words,
            'results': results,
            'url': url
        })
    
    except Exception as e:
        return jsonify({'error': f'크롤링 오류: {str(e)}'}), 400
    
    finally:
        if driver:
            try:
                driver.quit()
            except:
                pass


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
