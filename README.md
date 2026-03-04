# File Organizer Agent

Claude Code 커스텀 명령어로 Downloads 폴더를 자동 정리합니다.

## 기능

Downloads 폴더의 파일들을 4개 카테고리, 20+ 하위폴더로 자동 분류:

| 폴더 | 내용 |
|------|------|
| **Business** | 사업계획서, 계약서, 법인서류, 재무서류 |
| **Media** | 사진, 영상, 스크린샷, 오디오 |
| **Dev** | 앱 빌드(AAB/APK), 목업, 개발 에셋 |
| **Resources** | 책, 교육자료, AI 연구자료, 강연자료 |

## 폴더 구조

```
~/Downloads/
├── Business/
│   ├── Koddy_Inc/
│   │   ├── 법인설립/     ← Certificate, CSC, IRS, Delaware 서류
│   │   ├── 재무/         ← Invoice, 세금계산서, Wire Details
│   │   └── 계약서/       ← MARU SF, 임대차, 멤버십
│   ├── 예창패/
│   │   ├── 2025/         ← 제출서류, 재제출서류, 최종서류 포함
│   │   └── 2026/
│   ├── 창업중심대학/
│   ├── YC/
│   ├── 개인서류/         ← 경력증명서, 급여명세서, 신분증
│   └── 채용/
├── Dev/
│   ├── 코딩로그/         ← *__코딩로그_*.pdf
│   ├── 목업/             ← apple-iphone-*, AppScreens-*
│   ├── 에셋/             ← SVG, 로고, 아이콘
│   ├── 배포/             ← *.aab, *.apk
│   ├── 인증키/           ← AuthKey, PushKey, Firebase JSON
│   └── 데이터/           ← *.db, *.csv, *.xml
├── Resources/
│   ├── Books/
│   │   ├── AI-Tech/      ← AI/개발 서적
│   │   ├── Business/     ← 비즈니스 서적
│   │   └── General/      ← 일반 서적
│   ├── AI/               ← AI 연구자료, 사진
│   ├── 강연자료/         ← 강연 PDF
│   └── 한국어/           ← 한국어 교재
└── Media/
    ├── AI생성이미지/     ← Gemini, ChatGPT 생성 이미지
    ├── 개인사진/         ← 개인/지인 사진
    ├── 스크린샷/         ← Screenshot*, ScreenRecording_*
    ├── 동영상/           ← *.mp4, *.MOV, *.gif
    ├── 음성/             ← *.mp3, *.m4a
    └── 기타이미지/       ← 분류 어려운 이미지
```

## 설치

```bash
git clone https://github.com/YOUR_USERNAME/file-organizer-agent.git
cd file-organizer-agent
chmod +x install.sh
./install.sh
```

## 사용법

Claude Code에서:
```
/organize
```

## 분류 규칙

### 경계 케이스 우선순위
| 파일 | 분류 | 근거 |
|------|------|------|
| `*__코딩로그_*.pdf` | Dev/코딩로그 | 개발 산출물 |
| `김경빈*.jpg` (증명사진) | Business/개인서류 | 서류 목적 |
| `Hinton/Kurzweil *.jpg` | Resources/AI | 연구 자료 |
| `Gemini_Generated_Image*` | Media/AI생성이미지 | AI 생성 |
| `*.aab`, `*.apk` | Dev/배포 | 앱 빌드 |
| `AuthKey*`, `*.p8`, `*.p12` | Dev/인증키 | 보안 키 |
| `*창업중심대학*` | Business/창업중심대학 | 사업 운영 |
| `*예비창업패키지*` | Business/예창패/20XX | 사업 운영 |

### Media/스크린샷
- `Screenshot*`, `ScreenRecording_*`

### Media/동영상
- `*.mp4`, `*.MP4`, `*.MOV`, `*.gif`

### Media/음성
- `*.mp3`, `*.m4a`

### 자동 삭제
- `*.dmg` - 설치 파일 (확인 후 삭제)

## 커스터마이징

`rules.json` 파일을 수정하여 분류 규칙을 변경할 수 있습니다.

## 개인정보 보호 모델

### 왜 PI-Safe인가?

파일명 자체가 개인정보(PI)인 경우가 있습니다:

| 위험도 | 파일명 예시 | 포함 정보 |
|--------|------------|----------|
| HIGH | `급여명세서 1.pdf`, `소득확인증명서.pdf` | 재정 현황 |
| HIGH | `신분증.png`, `재학증명서.pdf` | 신원 서류 |
| HIGH | `AuthKey_77D7KC8DN2.p8` | 보안 자격증명 |
| HIGH | `koddy-inc_Wire-Details-Checking-9390.pdf` | 은행 계좌 정보 |

기존 `/organize` 명령어는 `ls ~/Downloads` 전체를 Claude API로 전송했습니다.
이제 PI 파일을 먼저 로컬 처리하여 API로 전달되지 않게 합니다.

### 3단계 워크플로우

```
┌─────────────────────────────────────────────────┐
│  STEP 1: PI 파일 로컬 처리 (API 전송 ZERO)         │
│  python3 organizer.py --pi-only --execute        │
│  → HIGH/MEDIUM 파일 처리 (재무, 서류, 인증키)      │
└─────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────┐
│  STEP 2: 나머지 파일 로컬 처리 (API 전송 ZERO)      │
│  python3 organizer.py --non-pi --execute         │
│  → LOW/NONE 파일 처리 (YC, 이력서, 미디어, 서적)   │
└─────────────────────────────────────────────────┘
           ↓
┌─────────────────────────────────────────────────┐
│  STEP 3: 미분류 파일 선택적 Claude 분류             │
│  python3 organizer.py --report                   │
│  → 패턴 미매칭 파일 목록 + PI 추정 수준 표시         │
│  → 이 시점 Downloads에 PI 파일명 없음               │
└─────────────────────────────────────────────────┘
```

**일상 정리**: Step 1+2 통합 실행으로 충분합니다:
```bash
python3 organizer.py --execute
```

### pi_level 체계

| pi_level | 서브폴더 예시 | Claude API 전송 |
|----------|-------------|----------------|
| HIGH | 개인서류, Koddy_Inc/재무, 인증키 | ❌ 전송 안 함 |
| MEDIUM | 예창패, 창업중심대학, Dev/데이터 | ❌ 전송 안 함 |
| LOW | YC, 채용, Dev/코딩로그 | ❌ 전송 안 함 |
| NONE | 목업, 에셋, 미디어, 서적 | ✅ Step 3에서만 가능 |

### organizer.py CLI

```bash
python3 organizer.py                      # dry-run 전체
python3 organizer.py --execute            # 전체 실행
python3 organizer.py --pi-only            # PI (HIGH+MEDIUM) dry-run
python3 organizer.py --pi-only --execute  # PI (HIGH+MEDIUM) 실행
python3 organizer.py --non-pi --execute   # 비PI (LOW+NONE) 실행
python3 organizer.py --report             # 미분류 파일 목록 출력
```

이동 로그: `~/.local/share/file-organizer/organize.log`

## 라이센스

MIT
