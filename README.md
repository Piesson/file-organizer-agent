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

## 라이센스

MIT
