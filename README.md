# File Organizer Agent

Claude Code 커스텀 명령어로 Downloads 폴더를 자동 정리합니다.

## 기능

Downloads 폴더의 파일들을 4개 카테고리로 자동 분류:

| 폴더 | 내용 |
|------|------|
| **Business** | 사업계획서, 계약서, 법인서류, 재무서류 |
| **Media** | 사진, 영상, 스크린샷, 오디오 |
| **Dev** | 앱 빌드(AAB/APK), 목업, 개발 에셋 |
| **Resources** | 책, 교육자료, 템플릿 |

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

### Media
- `IMG_*`, `SNOW_*`, `KakaoTalk_*` - 사진/영상
- `Screenshot*`, `ScreenRecording_*` - 스크린샷/녹화
- `*.mp4`, `*.MOV`, `*.m4a`, `*.mp3` - 영상/오디오

### Dev
- `*.aab`, `*.apk` - Android 빌드
- `*mockup*`, `apple-iphone-*` - 목업
- `AuthKey*`, `PushKey*` - 인증 키
- `*firebase*.json` - Firebase 설정

### Business
- `*계획서*`, `*계약서*`, `*견적서*` - 사업 문서
- `*Certificate*`, `*사업자등록증*` - 법인 서류
- `Koddy*`, `MARU*`, `YC*` - 스타트업 관련

### Resources
- 책 PDF, 교육자료
- `Notion Icons*`, `Notioly*` - 템플릿

### 자동 삭제
- `*.dmg` - 설치 파일 (확인 후 삭제)

## 커스터마이징

`rules.json` 파일을 수정하여 분류 규칙을 변경할 수 있습니다.

## 라이센스

MIT
