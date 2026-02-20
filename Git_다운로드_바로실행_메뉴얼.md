# Git 다운로드 후 바로 실행 가이드

## 1) 저장소 받기 (git clone)
```bash
git clone https://github.com/sheryloe/Hackerton.git
cd Hackerton
```

## 2) 가장 쉬운 실행 (권장)
Windows에서 아래 파일 더블클릭:
- `start_threadpilot_ui.bat`

또는 명령어로 실행:
```bash
start_threadpilot_ui.bat
```

동작 내용:
- `dist/threadpilot.exe`가 있으면 EXE로 바로 UI 실행
- EXE가 없으면 자동으로 `.venv` 생성 + 기본 의존성 설치 + UI 실행

## 3) 처음부터 기본 설치를 전부 하고 싶다면
```bash
setup_default.bat
```

동작 내용:
- `.venv` 생성
- `pip` 업그레이드
- `requirements.txt` 전체 설치
- `pyinstaller` 설치
- `dist/threadpilot.exe` 빌드
- UI 자동 실행

## 4) UI 접속
실행되면 브라우저에서 아래 주소를 사용:
- `http://127.0.0.1:8000/`

## 5) UI 사용 순서
1. `Health Check`
2. 요구사항 파일 입력 후 `Bootstrap 실행` (예: `요구사항.md`)
3. PR ID 입력 후 `Review 실행`

## 6) 문제 해결
- Python 미설치: Python 3.10+ 설치 후 다시 실행
- 포트 충돌: 다른 프로그램 종료 후 재시도
- Live LLM 사용 시: API Key 환경변수 설정 필요
