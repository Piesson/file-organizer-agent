# File Organizer Agent - Claude 규칙

## Downloads 정리 요청 처리 (MANDATORY)

"정리해", "파일 정리", "Downloads 정리", "다운로드 정리" 등 파일 정리 관련 요청 시:

**ALWAYS** `/organize` 스킬 사용
**NEVER** `ls ~/Downloads` 직접 실행 - 파일명에 PI(개인정보)가 포함될 수 있음

### 이유
~/Downloads 파일명에 재정정보/신원서류/보안키 등 민감 PI 포함 가능.
직접 `ls` 실행 시 PI 파일명이 Anthropic API로 전송됨.
`/organize` 스킬은 PI 파일을 로컬에서 먼저 처리하는 3단계 워크플로우 사용.

### 로컬 실행 (스킬 없이 직접 실행)

```bash
python3 ~/Desktop/file-organizer-agent/organizer.py --execute
```
