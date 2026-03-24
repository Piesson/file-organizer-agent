#!/usr/bin/env python3
"""
PI-Safe File Organizer
~/Downloads 폴더를 로컬에서 안전하게 정리합니다.

PI (개인정보) 파일을 먼저 처리하여 Claude API로 전송되지 않게 합니다.

사용법:
  python3 organizer.py                      # dry-run 전체
  python3 organizer.py --execute            # 전체 실행
  python3 organizer.py --pi-only            # PI (HIGH+MEDIUM) dry-run
  python3 organizer.py --pi-only --execute  # PI (HIGH+MEDIUM) 실행
  python3 organizer.py --non-pi --execute   # 비PI (LOW+NONE) 실행
  python3 organizer.py --report             # 미분류 파일 목록 출력
"""

import argparse
import fnmatch
import json
import logging
import shutil
import sys
import unicodedata
from pathlib import Path

RULES_JSON = Path(__file__).parent / "rules.json"
LOG_DIR = Path.home() / ".local" / "share" / "file-organizer"
LOG_FILE = LOG_DIR / "organize.log"

# 파일명에서 PI HIGH로 추정할 키워드
PI_HIGH_KEYWORDS = [
    "소득", "급여", "신분증", "재학", "휴학", "졸업", "경력",
    "Wire", "backup-codes", "AuthKey", "firebase", ".p12", ".p8",
    "계좌", "세금계산서", "임대차", "수료증", "Certificate",
    "Incorporation", "IRS", "Delaware", "FranchiseTax", "Invoice",
]

PI_MEDIUM_KEYWORDS = [
    "사업계획서", "계획서", "계약서", "Contract", "창업", "사업자",
]

SKIP_FILES = {".DS_Store", ".localized"}

PI_ICON = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🟢", "NONE": "⚪"}


def setup_log_file():
    """로그 파일 핸들러 반환 (stdout 미포함)."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger("organizer")
    logger.setLevel(logging.INFO)
    if not logger.handlers:
        handler = logging.FileHandler(LOG_FILE)
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
    return logger


def load_rules():
    with open(RULES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def get_target_folder(rules):
    path_str = rules["settings"]["targetFolder"].replace("~", str(Path.home()))
    return Path(path_str)


def build_subfolder_list(rules, target_folder):
    """
    반환: [(target_path, patterns, pi_level, cat_name, subfolder_rel), ...]
    순서: Business → Dev → Resources → Media (우선순위 순)
    """
    entries = []
    for cat_name in ["Business", "Dev", "Resources", "Media", "기타"]:
        cat = rules["categories"].get(cat_name)
        if not cat:
            continue
        for subfolder_rel, value in cat.get("subfolders", {}).items():
            if isinstance(value, dict):
                patterns = value.get("patterns", [])
                pi_level = value.get("pi_level", "NONE")
            else:
                # 레거시 배열 형식 지원
                patterns = value
                pi_level = "NONE"

            if not patterns:
                continue

            target_path = target_folder / cat_name / subfolder_rel
            entries.append((target_path, patterns, pi_level, cat_name, subfolder_rel))
    return entries


def get_files_in_downloads(target_folder):
    """~/Downloads 최상위 파일 목록 (폴더, 숨김파일 제외)."""
    if not target_folder.exists():
        print(f"❌ 폴더를 찾을 수 없음: {target_folder}")
        sys.exit(1)

    files = []
    for item in sorted(target_folder.iterdir(), key=lambda f: f.name):
        if item.is_dir():
            continue
        if item.name.startswith("."):
            continue
        if item.name in SKIP_FILES:
            continue
        files.append(item)
    return files


def match_file(filename, entries):
    """첫 번째 매칭 엔트리 반환. macOS NFD 파일명을 NFC로 정규화 후 매칭."""
    normalized = unicodedata.normalize("NFC", filename)
    for target_path, patterns, pi_level, cat_name, subfolder_rel in entries:
        for pattern in patterns:
            if fnmatch.fnmatch(normalized, pattern):
                return target_path, pi_level, cat_name, subfolder_rel
    return None, None, None, None


def should_process(pi_level, mode):
    """mode에 따라 처리 여부 반환."""
    if mode == "all":
        return True
    elif mode == "pi_only":
        return pi_level in ("HIGH", "MEDIUM")
    elif mode == "non_pi":
        return pi_level in ("LOW", "NONE")
    return True


def estimate_pi_level(filename):
    """미매칭 파일의 PI 수준 추정."""
    name_lower = filename.lower()
    for kw in PI_HIGH_KEYWORDS:
        if kw.lower() in name_lower:
            return "HIGH"
    for kw in PI_MEDIUM_KEYWORDS:
        if kw.lower() in name_lower:
            return "MEDIUM"
    return "UNKNOWN"


def move_file(src, dest_dir, logger):
    """파일 이동 (중복 시 suffix 추가)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / src.name

    if dest.exists():
        stem = src.stem
        suffix = src.suffix
        counter = 1
        while dest.exists():
            dest = dest_dir / f"{stem}_{counter}{suffix}"
            counter += 1

    shutil.move(str(src), str(dest))
    logger.info(f"MOVED {src.name} → {dest_dir}")
    return dest


def run_organize(execute, mode, source=None):
    """파일 정리 실행."""
    rules = load_rules()
    target_folder = get_target_folder(rules)
    source_folder = Path(source).expanduser() if source else target_folder
    entries = build_subfolder_list(rules, target_folder)
    files = get_files_in_downloads(source_folder)

    logger = setup_log_file() if execute else None

    moved = 0
    skipped = 0
    unmatched_count = 0

    mode_label = {
        "all": "전체",
        "pi_only": "PI (HIGH+MEDIUM)",
        "non_pi": "비PI (LOW+NONE)",
    }[mode]
    action = "실행" if execute else "DRY-RUN"

    print(f"\n{'='*58}")
    print(f"  PI-Safe File Organizer [{action}] - {mode_label}")
    print(f"{'='*58}\n")

    for f in files:
        target_path, pi_level, cat_name, subfolder_rel = match_file(f.name, entries)

        if target_path is None:
            unmatched_count += 1
            continue

        if not should_process(pi_level, mode):
            skipped += 1
            continue

        icon = PI_ICON.get(pi_level, "❓")
        rel_dest = f"{cat_name}/{subfolder_rel}"

        if execute:
            move_file(f, target_path, logger)

        print(f"  {icon} [{pi_level:6}] {f.name}")
        print(f"          → {rel_dest}/")
        moved += 1

    print(f"\n{'='*58}")
    print(f"  {'완료' if execute else '예정'}: {moved}개 {'이동' if execute else '이동 예정'}")
    print(f"  스킵 ({mode_label} 외): {skipped}개")
    print(f"  미분류: {unmatched_count}개  (--report 로 확인)")
    if not execute:
        flag = "--pi-only " if mode == "pi_only" else "--non-pi " if mode == "non_pi" else ""
        print(f"\n  실제 실행: python3 organizer.py {flag}--execute")
    print(f"{'='*58}\n")

    if execute and logger:
        logger.info(f"완료: 이동={moved}, 스킵={skipped}, 미분류={unmatched_count} [{mode_label}]")


def run_report(source=None):
    """미분류 파일 목록 보고."""
    rules = load_rules()
    target_folder = get_target_folder(rules)
    source_folder = Path(source).expanduser() if source else target_folder
    entries = build_subfolder_list(rules, target_folder)
    files = get_files_in_downloads(source_folder)

    unmatched = []
    for f in files:
        target_path, _, _, _ = match_file(f.name, entries)
        if target_path is None:
            unmatched.append(f)

    print(f"\n{'='*58}")
    print(f"  미분류 파일 리포트")
    print(f"{'='*58}\n")

    if not unmatched:
        print("  ✅ 미분류 파일 없음 - 모든 파일이 패턴에 매칭됨\n")
        print(f"{'='*58}\n")
        return

    estimated = [(f, estimate_pi_level(f.name)) for f in unmatched]
    high_risk = [(f, est) for f, est in estimated if est == "HIGH"]
    others = [(f, est) for f, est in estimated if est != "HIGH"]

    if high_risk:
        print(f"  ⚠️  PI 추정 HIGH ({len(high_risk)}개) - 수동 처리 권장:")
        print(f"  {'─'*52}")
        for f, _ in high_risk:
            print(f"    🔴 {f.name}")
        print()

    if others:
        print(f"  📁 Claude 분류 가능 ({len(others)}개) - PI 위험 낮음:")
        print(f"  {'─'*52}")
        for f, est in others:
            icon = "📊" if est == "MEDIUM" else "✅"
            print(f"    {icon} {f.name}  [{est}]")
        print()

    print(f"  총 {len(unmatched)}개 미분류")
    print(f"\n  💡 Claude 분류: PI HIGH 파일 먼저 정리 후 /organize 실행")
    print(f"{'='*58}\n")


def main():
    parser = argparse.ArgumentParser(
        description="PI-Safe File Organizer - ~/Downloads 정리",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""사용 예시:
  python3 organizer.py                      # dry-run 전체
  python3 organizer.py --execute            # 전체 실행
  python3 organizer.py --pi-only            # PI (HIGH+MEDIUM) dry-run
  python3 organizer.py --pi-only --execute  # PI (HIGH+MEDIUM) 실행
  python3 organizer.py --non-pi --execute   # 비PI (LOW+NONE) 실행
  python3 organizer.py --report             # 미분류 파일 목록""",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="실제 파일 이동 (기본: dry-run)",
    )
    parser.add_argument(
        "--source",
        type=str,
        default=None,
        help="정리할 소스 폴더 (기본: ~/Downloads)",
    )

    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument(
        "--pi-only",
        action="store_true",
        help="PI HIGH/MEDIUM 파일만 처리",
    )
    mode_group.add_argument(
        "--non-pi",
        action="store_true",
        help="비PI (LOW/NONE) 파일만 처리",
    )
    mode_group.add_argument(
        "--report",
        action="store_true",
        help="미분류 파일 목록 출력",
    )

    args = parser.parse_args()

    if args.report:
        run_report(source=args.source)
        return

    if args.pi_only:
        mode = "pi_only"
    elif args.non_pi:
        mode = "non_pi"
    else:
        mode = "all"

    run_organize(execute=args.execute, mode=mode, source=args.source)


if __name__ == "__main__":
    main()
