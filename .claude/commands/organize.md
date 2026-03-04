---
description: Downloads 폴더를 PI-safe 3단계 워크플로우로 자동 분류 (개인정보 보호)
allowed-tools: Bash, Read, Glob
---

# Downloads 폴더 정리 에이전트 (PI-Safe)

## ⚠️ 개인정보 보호 고지

`~/Downloads` 파일명 중 일부는 재정정보/신원정보/보안키 등 민감 PI를 포함합니다.

| pi_level | 예시 | 처리 방식 |
|----------|------|----------|
| HIGH | 급여명세서, 신분증, Wire-Details, AuthKey | Step 1: 로컬 처리 (API 전송 없음) |
| MEDIUM | 사업계획서, 계약서, DB파일 | Step 1: 로컬 처리 (API 전송 없음) |
| LOW | YC자료, 이력서, 코딩로그 | Step 2: 로컬 처리 |
| NONE | 목업, 에셋, 미디어, 서적 | Step 2: 로컬 처리 |

**이 명령어는 PI 파일을 Claude API로 전달하지 않습니다.**

---

## Step 1: PI 파일 로컬 처리 (Anthropic API 전송 없음)

```bash
python3 ~/Desktop/file-organizer-agent/organizer.py --pi-only --execute
```

HIGH/MEDIUM pi_level 파일 처리 완료.
이 파일명은 Claude가 보지 않습니다.

---

## Step 2: 나머지 패턴 매칭 파일 처리 (Anthropic API 전송 없음)

```bash
python3 ~/Desktop/file-organizer-agent/organizer.py --non-pi --execute
```

LOW/NONE pi_level 파일 처리 완료.
rules.json 패턴으로 명확히 분류 가능한 파일 모두 처리됩니다.

---

## Step 3: 미분류 파일 확인 및 선택적 Claude 분류

```bash
python3 ~/Desktop/file-organizer-agent/organizer.py --report
```

패턴 매칭 안 된 파일 목록을 표시합니다.
이 시점에 `~/Downloads`에는 PI 파일이 없습니다.

미분류 파일이 있고 Claude 분류가 필요하다면:
```bash
ls ~/Downloads | grep -vE "^(Business|Media|Dev|Resources)$"
```

파일명을 확인하고 적절한 subfolder로 이동하거나 rules.json 패턴을 추가합니다.

---

## 일상적 사용 (Step 1+2 통합)

매일 Downloads 정리는 이것만으로 충분합니다:

```bash
python3 ~/Desktop/file-organizer-agent/organizer.py --execute
```

Step 3 (Claude 분류)는 새 파일 유형이 생겼을 때 선택적으로 사용합니다.

---

## Dry-run 미리보기

실행 전 확인:
```bash
python3 ~/Desktop/file-organizer-agent/organizer.py
```

PI 파일만 확인:
```bash
python3 ~/Desktop/file-organizer-agent/organizer.py --pi-only
```

---

## 주의사항

- 파일 이동 전 항상 dry-run으로 확인
- 중복 파일은 모두 유지 (suffix 추가: `파일_1.pdf`)
- 이동 로그: `~/.local/share/file-organizer/organize.log`
- `*.dmg` 파일은 자동 처리 대상 아님 (수동 삭제)
