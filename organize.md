---
description: Downloads 폴더를 Business, Media, Dev, Resources 4개 카테고리로 자동 분류
allowed-tools: Bash, Read, Glob, TodoWrite
---

# Downloads 폴더 정리 에이전트

## 개요
~/Downloads 폴더의 파일들을 4개 카테고리로 자동 분류합니다.

## 분류 규칙

### 1. Media (미디어)
개인 사진, 영상, 스크린샷, 오디오 파일
- `IMG_*` - iPhone 사진
- `SNOW_*` - SNOW 앱 영상
- `KakaoTalk_*` - 카카오톡 사진/영상
- `Screenshot*` - 스크린샷
- `ScreenRecording_*` - 화면 녹화
- `*.MOV`, `*.mp4`, `*.MP4` - 영상
- `*.m4a`, `*.mp3` - 오디오
- `*.jpeg`, `*.jpg`, `*.JPG`, `*.png`, `*.PNG`, `*.gif` - 이미지
- `Gemini_Generated_Image*` - AI 생성 이미지

### 2. Dev (개발)
앱 빌드, 목업, 개발 관련 에셋
- `*.aab`, `*.apk` - Android 빌드
- `*mockup*`, `apple-iphone-*` - 목업
- `AppScreens-*` - 앱 스크린 렌더
- `AuthKey*`, `PushKey*` - 인증 키
- `*firebase*.json` - Firebase 설정
- `*.xml`, `*.json` (설정 파일)
- `*.svg` - 벡터 이미지
- 로고, 아이콘 관련 파일

### 3. Business (사업/창업)
사업 문서, 계약서, 재무 서류
- `*계획서*`, `*사업계획서*` - 사업계획서
- `*계약서*`, `*Contract*` - 계약서
- `*견적서*`, `*Invoice*` - 견적서
- `*세금계산서*`, `*급여명세서*` - 재무
- `*Certificate*`, `*사업자등록증*` - 법인 서류
- `MARU*`, `Koddy*`, `Koddies*`, `YC*` - 스타트업 관련
- `*Resume*`, `*이력서*` - 이력서
- 린스타트업, 창업 관련 문서

### 4. Resources (자료)
책, 교육자료, 참고문서
- 책 PDF (ALMANACK, Mom Test 등)
- `*교육*`, `*강연*` - 교육자료
- `Notion Icons`, `Notioly` - 템플릿/아이콘
- 기타 학습 자료

### 삭제 대상
- `*.dmg` - 설치 파일 (이미 설치 완료된 것으로 간주)

## 실행 절차

1. **폴더 확인/생성**
```bash
mkdir -p ~/Downloads/{Business,Media,Dev,Resources}
```

2. **현재 상태 확인**
```bash
ls ~/Downloads | grep -vE "^(Business|Media|Dev|Resources)$"
```

3. **DMG 파일 삭제** (사용자 확인 후)

4. **카테고리별 파일 이동**
   - Media: IMG_*, SNOW_*, KakaoTalk_*, Screenshot*, 영상, 오디오
   - Dev: *.aab, *.apk, mockup, firebase, 인증키
   - Business: 계획서, 계약서, 법인서류, 재무서류
   - Resources: 책, 교육자료, 템플릿

5. **미분류 파일 확인 및 수동 처리**

6. **결과 보고**
```bash
echo "Business: $(ls ~/Downloads/Business | wc -l)개"
echo "Media: $(ls ~/Downloads/Media | wc -l)개"
echo "Dev: $(ls ~/Downloads/Dev | wc -l)개"
echo "Resources: $(ls ~/Downloads/Resources | wc -l)개"
```

## 주의사항
- 파일 이동 전 항상 현재 상태를 확인
- 중복 파일은 모두 유지 (사용자 선호)
- 한글 파일명 처리 시 따옴표 사용
- 권한 문제 발생 시 `chmod` 사용
