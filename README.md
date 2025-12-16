# 🔍 웹 단어 검색기

웹사이트에서 원하는 단어가 몇 개 있는지 찾아주는 Flask 웹 애플리케이션입니다.

**JavaScript로 동적 로드되는 웹사이트도 지원!** (Selenium 사용)

## ✨ 주요 기능

- 🌐 **웹사이트 자동 크롤링** - URL 입력 후 자동 크롤
- 🔍 **단어 개수 세기** - 여러 단어 동시 검색
- 📊 **통계 표시** - 총 단어 수, 검색된 단어, 일치율
- ⚡ **JavaScript 렌더링** - 동적 로딩되는 웹사이트 지원
- 🎨 **깔끔한 UI** - 모던하고 반응형 디자인

## 🚀 설치 방법

### 1. 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/web-word-searcher.git
cd web-word-searcher
```

### 2. 가상환경 생성
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. 라이브러리 설치
```bash
pip install -r requirements.txt
```

## 🎯 사용 방법

### 앱 실행
```bash
python app.py
```

### 브라우저에서 접속
```
http://localhost:5000
```

### 검색하기
1. **URL 입력**: 검색할 웹사이트 주소
2. **단어 입력**: 찾을 단어들 (쉼표로 구분)
   - 예: `python, machine, learning`
3. **🚀 검색하기** 클릭
4. 결과 확인!

## 📋 예시

### 입력
```
🔗 URL: https://en.wikipedia.org/wiki/Python_(programming_language)
🔎 단어: python, programming, language
```

### 결과
```
📊 검색 결과
- python: 127개
- programming: 45개  
- language: 38개
- 총 단어: 2,531개
- 일치율: 8%
```

## 🛠️ 기술 스택

| 기술 | 버전 | 용도 |
|------|------|------|
| **Flask** | 2.3.2 | 웹 프레임워크 |
| **Selenium** | 4.15.2 | 웹 드라이버 (JavaScript 렌더링) |
| **BeautifulSoup4** | 4.12.2 | HTML 파싱 |
| **Requests** | 2.31.0 | HTTP 요청 |

## 📁 프로젝트 구조

```
web-word-searcher/
├── app.py              # 메인 Flask 애플리케이션
├── requirements.txt    # 의존성 목록
├── README.md           # 프로젝트 설명
└── .gitignore         # Git 무시 파일
```

## 🔑 주요 기능 상세

### 1. 동적 웹사이트 지원
- Selenium WebDriver로 JavaScript 렌더링
- 페이지 로드 완료 대기
- 스크롤을 통한 콘텐츠 동적 로드

### 2. 텍스트 추출
- 모든 텍스트 수집 (숨겨진 텍스트 포함)
- 스크립트, 스타일 제거
- 한글/영문 지원

### 3. 단어 검색
- 정확한 단어 카운트
- 대소문자 구분 안 함
- 정규표현식 기반 단어 분리

## ⚙️ 설정

### 시간 조정
`app.py`에서 다음을 수정:
```python
time.sleep(5)  # 로딩 대기 시간 (초)
```

### 스크롤 횟수 조정
```python
for _ in range(3):  # 스크롤 횟수
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
```

## 🐛 트러블슈팅

### ChromeDriver 오류
```bash
pip install webdriver-manager
```

### GPU 경고 메시지
- 무시해도 됩니다
- 경고일 뿐 기능에 영향 없음

### 단어가 안 검색됨
- URL이 올바른지 확인
- 단어 띄어쓰기 확인
- 30초 정도 시간 소요 가능

## 📝 라이선스

MIT License

## 👨‍💻 작성자

개발자 이름

## 🤝 기여

Pull Request는 언제나 환영합니다!

---

**Happy Searching! 🔍✨**
