#!/usr/bin/env python3
"""結構對齊腳本 — 將譯文（zh）與排版後原文（es）進行 section-level 對齊。

來源：docs/src/content/docs/es/ 內的西文 .md
目標：docs/src/content/docs/ 內的中文 .md

兩側皆為正規 Markdown，以標題順序直接配對。
輸出 JSON 到 stdout，包含 alignment[]、stats、meta。
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Imports from sibling modules
# ---------------------------------------------------------------------------

sys.path.insert(0, str(Path(__file__).resolve().parent))

from _term_lib import (  # noqa: E402
    DEFAULT_DOCS_ROOT,
    DEFAULT_GLOSSARY,
    PROJECT_ROOT,
    load_glossary,
    load_json,
    read_file,
)

DEFAULT_CHAPTERS = PROJECT_ROOT / "chapters.json"
DEFAULT_ES_ROOT = DEFAULT_DOCS_ROOT.parent / "docs" / "es"


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        description="Structural alignment between zh translation and es source",
    )
    p.add_argument(
        "--target", required=True,
        help="Translated zh .md file (full path, relative from docs root, or short name)",
    )
    p.add_argument("--chapters", default=str(DEFAULT_CHAPTERS), help="chapters.json path")
    p.add_argument("--glossary", default=str(DEFAULT_GLOSSARY), help="glossary.json path")
    return p.parse_args(argv)


# ---------------------------------------------------------------------------
# Path resolution
# ---------------------------------------------------------------------------


def resolve_target(target: str) -> Path:
    """Resolve target path to the zh .md file."""
    p = Path(target)
    if p.is_absolute() and p.exists():
        return p

    candidate = DEFAULT_DOCS_ROOT / target
    if candidate.exists():
        return candidate

    if not target.endswith(".md"):
        candidate = DEFAULT_DOCS_ROOT / f"{target}.md"
        if candidate.exists():
            return candidate

    for md in DEFAULT_DOCS_ROOT.rglob("*.md"):
        if md.stem == target:
            return md

    candidate = PROJECT_ROOT / target
    if candidate.exists():
        return candidate

    print(f"Error: cannot resolve target '{target}'", file=sys.stderr)
    sys.exit(1)


def resolve_source(target: Path) -> Path:
    """Derive the es source path from the zh target path.

    e.g. docs/src/content/docs/rules/fundamentals.md
      →  docs/src/content/docs/es/rules/fundamentals.md
    """
    try:
        rel = target.relative_to(DEFAULT_DOCS_ROOT)
    except ValueError:
        print(f"Error: target '{target}' is not under docs root", file=sys.stderr)
        sys.exit(1)

    source = DEFAULT_ES_ROOT / rel
    if not source.exists():
        print(f"Error: es source not found: {source}", file=sys.stderr)
        sys.exit(1)
    return source


# ---------------------------------------------------------------------------
# chapters.json lookup (for page metadata only)
# ---------------------------------------------------------------------------


def find_pages(chapters_path: Path, target: Path) -> list[int] | None:
    """Look up [start_page, end_page] from chapters.json for metadata."""
    config = load_json(chapters_path, {})
    chapters = config.get("chapters", {})

    try:
        rel = target.relative_to(DEFAULT_DOCS_ROOT)
        parts = rel.parts
    except ValueError:
        return None

    if len(parts) < 2:
        section_name = parts[0].replace(".md", "") if parts else ""
        filename = section_name
    else:
        section_name = parts[0]
        filename = parts[-1].replace(".md", "")

    section = chapters.get(section_name, {})
    files = section.get("files", {})
    file_cfg = files.get(filename)
    if file_cfg is None:
        return None
    return file_cfg.get("pages")


# ---------------------------------------------------------------------------
# Markdown section parsing (shared for both zh and es)
# ---------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^(#{2,4})\s+(.+)$", re.MULTILINE)
_ASIDE_OPEN_RE = re.compile(r"^:::(note|tip|caution|danger)")
_ASIDE_CLOSE_RE = re.compile(r"^:::\s*$")


class Section:
    __slots__ = ("heading", "heading_text", "level", "paragraphs",
                 "start_line", "end_line", "inside_aside")

    def __init__(
        self,
        heading: str,
        heading_text: str,
        level: int,
        paragraphs: list[str],
        start_line: int,
        end_line: int,
        inside_aside: bool,
    ):
        self.heading = heading            # e.g. "## 基礎概論"
        self.heading_text = heading_text  # e.g. "基礎概論"
        self.level = level
        self.paragraphs = paragraphs
        self.start_line = start_line
        self.end_line = end_line
        self.inside_aside = inside_aside


def parse_sections(text: str) -> list[Section]:
    """Parse a Markdown file into sections split by H2/H3/H4 headings."""
    lines = text.split("\n")
    total_lines = len(lines)

    # Skip frontmatter
    fm_end = 0
    if lines and lines[0].strip() == "---":
        for i in range(1, len(lines)):
            if lines[i].strip() == "---":
                fm_end = i + 1
                break

    heading_positions: list[tuple[int, int, str]] = []
    for i in range(fm_end, total_lines):
        m = _HEADING_RE.match(lines[i])
        if m:
            heading_positions.append((i, len(m.group(1)), m.group(2).strip()))

    if not heading_positions:
        content = "\n".join(lines[fm_end:])
        paras = _split_paragraphs(content)
        return [Section("", "", 0, paras, fm_end + 1, total_lines, False)]

    sections: list[Section] = []
    for idx, (line_idx, level, heading_text) in enumerate(heading_positions):
        end_idx = heading_positions[idx + 1][0] if idx + 1 < len(heading_positions) else total_lines

        # Compute aside depth at heading
        aside_depth = 0
        for i in range(fm_end, line_idx):
            if _ASIDE_OPEN_RE.match(lines[i]):
                aside_depth += 1
            elif _ASIDE_CLOSE_RE.match(lines[i]) and aside_depth > 0:
                aside_depth -= 1

        content = "\n".join(lines[line_idx + 1 : end_idx])
        paras = _split_paragraphs(content)

        sections.append(Section(
            heading=f"{'#' * level} {heading_text}",
            heading_text=heading_text,
            level=level,
            paragraphs=paras,
            start_line=line_idx + 1,  # 1-indexed
            end_line=end_idx,
            inside_aside=aside_depth > 0,
        ))

    return sections


def _split_paragraphs(text: str) -> list[str]:
    """Split text into paragraphs by blank lines."""
    raw = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in raw if p.strip()]


# ---------------------------------------------------------------------------
# Context detection
# ---------------------------------------------------------------------------

_STRICT_KEYWORDS = re.compile(r"動作|基礎|進階|成長|規則|機制|檢定")
_DICE_RE = re.compile(r"\d*d\d+", re.IGNORECASE)
_STAT_TABLE_RE = re.compile(r"挑戰.*保護.*思慮.*情感.*奉獻")


def detect_context(section: Section, file_path: str) -> str:
    """Determine context type: Strict / Moderate / Flexible."""
    content = "\n".join(section.paragraphs)

    if section.inside_aside:
        return "Flexible"

    if _STRICT_KEYWORDS.search(section.heading_text):
        return "Strict"

    if _DICE_RE.search(content) or _STAT_TABLE_RE.search(content):
        return "Strict"

    if section.level >= 3 and any(kw in section.heading_text for kw in ["成長", "進階動作"]):
        return "Strict"

    if "rules/" in file_path:
        return "Moderate"

    return "Moderate"


# ---------------------------------------------------------------------------
# Low-priority detection
# ---------------------------------------------------------------------------

_TEMPLATE_LABELS = re.compile(
    r"(姓名|年齡|生活型態|稱號|主題|色彩|護符|星座|血型|最珍貴的寶物|"
    r"黑暗等級|黑暗點數|戀愛等級|友情點數|戀愛點數)[\s：:]*$",
    re.MULTILINE,
)

_LOW_PRI_HEADINGS = {"個人資料", "變身", "黑暗", "戀愛", "友情"}


def detect_low_priority(section: Section) -> bool:
    """Check if section is template/fill-in-the-blank fields."""
    if section.heading_text in _LOW_PRI_HEADINGS:
        return True

    content = "\n".join(section.paragraphs)
    label_count = len(_TEMPLATE_LABELS.findall(content))
    line_count = len([line for line in content.split("\n") if line.strip()])
    if line_count > 0 and label_count / line_count > 0.5:
        return True

    return False


# ---------------------------------------------------------------------------
# Alignment builder
# ---------------------------------------------------------------------------


def build_alignment(
    zh_sections: list[Section],
    es_sections: list[Section],
    file_path: str,
) -> list[dict]:
    """Pair zh and es sections by sequential heading position."""
    alignment: list[dict] = []
    n_zh = len(zh_sections)
    n_es = len(es_sections)

    for idx in range(max(n_zh, n_es)):
        zh = zh_sections[idx] if idx < n_zh else None
        es = es_sections[idx] if idx < n_es else None

        if zh is not None:
            ctx = detect_context(zh, file_path)
            low_pri = detect_low_priority(zh)
            entry: dict = {
                "index": idx,
                "zh_heading": zh.heading,
                "es_heading": es.heading if es else None,
                "context": ctx,
                "zh_paragraphs": zh.paragraphs,
                "es_paragraphs": es.paragraphs if es else [],
                "low_priority": low_pri,
                "zh_lines": [zh.start_line, zh.end_line],
            }
        else:
            # Extra es section with no zh counterpart
            entry = {
                "index": idx,
                "zh_heading": None,
                "es_heading": es.heading if es else None,
                "context": "Moderate",
                "zh_paragraphs": [],
                "es_paragraphs": es.paragraphs if es else [],
                "low_priority": False,
                "zh_lines": [],
            }

        alignment.append(entry)

    return alignment


# ---------------------------------------------------------------------------
# Stats
# ---------------------------------------------------------------------------


def compute_stats(alignment: list[dict]) -> dict:
    total = len(alignment)
    matched = sum(1 for a in alignment if a["es_heading"] is not None and a["zh_heading"] is not None)
    unmatched = total - matched
    zh_paras = sum(len(a["zh_paragraphs"]) for a in alignment)
    es_paras = sum(len(a["es_paragraphs"]) for a in alignment)
    low_pri = sum(1 for a in alignment if a["low_priority"])

    context_counts: dict[str, int] = {}
    for a in alignment:
        ctx = a["context"]
        context_counts[ctx] = context_counts.get(ctx, 0) + 1

    return {
        "total_sections": total,
        "matched_sections": matched,
        "unmatched_sections": unmatched,
        "total_zh_paragraphs": zh_paras,
        "total_es_paragraphs": es_paras,
        "low_priority_sections": low_pri,
        "context_counts": context_counts,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)

    target = resolve_target(args.target)
    source = resolve_source(target)
    chapters_path = Path(args.chapters)

    # Relative path for metadata / context detection
    try:
        rel_path = str(target.relative_to(DEFAULT_DOCS_ROOT)).replace("\\", "/")
    except ValueError:
        rel_path = str(target)

    # Parse both files
    zh_sections = parse_sections(read_file(target))
    es_sections = parse_sections(read_file(source))

    # Build alignment
    alignment = build_alignment(zh_sections, es_sections, rel_path)
    stats = compute_stats(alignment)

    # Page metadata from chapters.json
    pages = find_pages(chapters_path, target)

    output = {
        "meta": {
            "target": f"docs/src/content/docs/{rel_path}",
            "source": f"docs/src/content/docs/es/{rel_path}",
            "pages": pages,
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        },
        "stats": stats,
        "alignment": alignment,
    }

    json.dump(output, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
