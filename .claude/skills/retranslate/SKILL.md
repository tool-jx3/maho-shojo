---
name: retranslate
description: 重譯檢驗 - review translated markdown files and suggest better translations for each sentence, learning from past user decisions
user-invocable: true
disable-model-invocation: true
---

# Retranslate - Review and Improve Translations

Use `pdf-translation` and `terminology-management` skills for reference.

## Purpose

Review already-translated `.md` files and propose better translations on a **sentence-by-sentence basis**. This skill:
- Learns from past user decisions via `retranslate-history.json`
- Adapts suggestions to match user's expressed preferences over time
- Promotes recurring preferences into `style-decisions.json` as permanent rules
- Maintains consistency with `glossary.json` terminology

## History File: `retranslate-history.json`

Location: project root (alongside `glossary.json` and `style-decisions.json`)

This file is the **persistent memory** of all retranslation sessions.

### Design Principle: Aggregate, Not Log

Raw per-sentence decisions are **never stored**. They are scaffolding used only within a single session to update aggregated counts.

Once a session ends, only the aggregated statistics survive:
- `candidates{}` — patterns with insufficient evidence (accepted < 3)
- `preferences{}` — confirmed patterns (confidence ≥ 0.75, accepted ≥ 3)
- `file_reviews{}` — per-file audit metadata

This keeps the file **permanently small** regardless of how many sessions have run.

### Schema

```json
{
  "_meta": {
    "description": "重譯歷史紀錄 - 聚合偏好，不儲存原始決策流水帳",
    "updated": "2026-02-24"
  },
  "candidates": {
    "<id>": {
      "description": "描述這條候選偏好",
      "change_type": "naturalness",
      "accepted": 2,
      "rejected": 0,
      "examples": [
        { "before": "擲 2d6", "after": "投擲 2d6" }
      ]
    }
  },
  "preferences": {
    "<id>": {
      "description": "擲骰動詞偏好「投擲」而非「擲」",
      "change_type": "naturalness",
      "pattern": "dice rolling verbs",
      "preferred": "投擲",
      "over": ["擲", "丟"],
      "accepted": 5,
      "rejected": 1,
      "confidence": 0.83,
      "examples": [
        { "before": "擲 2d6", "after": "投擲 2d6" }
      ],
      "promoted_to_style_decisions": false
    }
  },
  "file_reviews": {
    "rules/combat.md": {
      "last_reviewed": "2026-02-24T11:09:21Z",
      "review_count": 2,
      "issues_found": 8,
      "changes_applied": 6,
      "paragraphs_reviewed": 42,
      "last_section_reviewed": "## 傷害與治療",
      "resume_from": null
    }
  }
}
```

### Field Reference

| Field | Values | Description |
|-------|--------|-------------|
| `change_type` | `terminology` / `naturalness` / `clarity` / `accuracy` | Category of the proposed change |
| `accepted` / `rejected` | integer | Cumulative counts across all sessions |
| `confidence` | 0.0–1.0 | `accepted / (accepted + rejected)` |
| `examples` | max 2 items | Representative before/after pairs (oldest replaced by newest) |
| `promoted_to_style_decisions` | boolean | If true, already written to `style-decisions.json` — skip in future suggestions |

---

## Process

### 0. Initialize History

At the start of every session:

1. Check if `retranslate-history.json` exists.
   - If not: create it with empty `_meta`, `candidates`, `preferences`, `file_reviews`.
2. Load `preferences` and `candidates`.
3. Display summary if preferences exist:
   ```
   📚 已載入 3 條學習偏好：
   - 擲骰動詞：偏好「投擲」（信心度 83%，6 次紀錄）
   - 術語括注：偏好加「」標記（信心度 100%，4 次紀錄）→ 已晉升為永久規則
   - 數值用詞：偏好「數值」而非「技能」（信心度 75%，3 次紀錄）
   ```

### 1. Select Target

If no `$ARGUMENTS`:
- List available translated files in `docs/src/content/docs/`
- Show review status from `file_reviews`:
  ```
  📂 可審閱的檔案：
  ┌─────────────────────────────────┬──────────────┬────────┐
  │ 檔案                            │ 上次審閱     │ 次數   │
  ├─────────────────────────────────┼──────────────┼────────┤
  │ rules/combat.md                 │ 2026-02-20   │ 2 次   │
  │ rules/index.md                  │ 未審閱       │ -      │
  │ characters/index.md             │ 未審閱       │ -      │
  └─────────────────────────────────┴──────────────┴────────┘
  ```
- Ask user which to review

Scope options:
- Single file: `docs/src/content/docs/rules/basic.md`
- Section: `rules` (all files in section)
- All: `all`

### 2. Load Resources

Read in this order:
1. `retranslate-history.json` → active preferences, candidates
2. `glossary.json` → approved terminology
3. `style-decisions.json` → translation policies
4. **Target file**: current Chinese translation
5. **Original file**: source text via `chapters.json` page mapping (language determined by `style-decisions.json` → `source_language`)
   - Read `chapters.json` → find `pages: [start, end]` for target file
   - Extract matching `<!-- PAGE N -->` blocks from `data/markdown/<name>_pages.md`
   - Fallback: proceed without original if unavailable (show warning)

### 3. Sentence-Level Review

**IMPORTANT: Process files sequentially, one at a time.**

**CRITICAL: Do NOT use the following for file review:**
- ❌ `task` tool with any agent type (explore/task/general-purpose)
- ❌ Parallel tool calls to read/analyze multiple files
- ❌ Any form of concurrent file processing

**REQUIRED: Review files one-by-one using direct tools:**
- ✅ `Read` tool to read file content
- ✅ `Grep` tool for pattern detection
- ✅ `AskUserQuestion` tool for user decisions
- ✅ Process File 1 → complete → File 2 → complete → ...

**Review Mode（由 Strategy 選擇決定）：**
- **Strategy A**：逐段完整審閱 — 依序處理 alignment[] 中的每個段落配對
- **Strategy B/C/D**：目標式審閱 — 僅處理符合篩選條件的段落

For each target file, keep an **in-session tally** (discarded at session end):

```
session_tally = {}   # { "<candidate-id>": { accepted: 0, rejected: 0, examples: [] } }
```

This tally is only used within the current session to update `candidates{}` and `preferences{}` at the end.

#### 3.0 Structural Alignment

Run the alignment script:

```bash
PYTHONIOENCODING=utf-8 uv run python scripts/retranslate_align.py --target <target-file>
```

Parse the JSON output to obtain `alignment[]`, `stats`, and `meta`.

**Verify:**
- `stats.unmatched_sections` > 0 → inspect and manually verify unmatched headings
- Display alignment summary table to user (from stats + alignment context types)

The script handles: source text extraction from `chapters.json` + page markers, heading map construction via reverse glossary lookup, paragraph pairing by sequential order, context detection (Strict/Moderate/Flexible), and low-priority template field detection.

**Output schema key fields per alignment entry:**
- `zh_heading` / `es_heading`: matched headings (`es_heading: null` = unmatched)
- `zh_paragraphs` / `es_paragraphs`: paragraph lists for comparison
- `context`: Strict / Moderate / Flexible
- `low_priority`: true for template/fill-in-the-blank sections
- `zh_lines`: `[start, end]` line numbers in the translated file

**Interpretation notes:**
- `es_heading: null` + `es_paragraphs: []` = no source equivalent found (translator-added content, or glossary gap)
- `low_priority: true` = template fields — still compare but with reduced scrutiny (only flag mistranslated/missing labels)
- `:::note`/`:::tip` content inside asides is marked `context: Flexible` but still paired with source text normally

#### Session Log Directory

Before starting review, create `./retranslate-result/` directory if not exists.

For each review session, create a timestamped log file:
- Path: `./retranslate-result/<file-slug>_<timestamp>.md`
- Example: `./retranslate-result/rules-combat_2026-02-24T11-09-21Z.md`
- Timestamp format: `YYYY-MM-DDTHH-mm-ssZ` (UTC, ISO 8601)
- File slug: replace `/` with `-` (e.g., `rules/combat.md` → `rules-combat`)

Write each suggestion to the log file in real-time (immediately when presenting to user, before they respond).

**Clean section recording**: At the end of the session log (before the summary), record sections that had no issues. This provides evidence that those sections were actually reviewed (not skipped):
```markdown
## 無問題章節
以下章節經逐段比對，未發現需修改之處：
- ## 偶像（La Idol）— 6 段
- ## 偶像（La Idol sheet）— 22 段
- …
```

#### 3.1 Parse Document Structure

1. **Skip**: YAML frontmatter, code blocks, dice notation (2d6, 1d20+3), raw URLs

2. **Review with Context Awareness**:
   - **Strict context**: paragraphs under `##` headers containing "規則", "動作", "機制", "檢定"
   - **Flexible context**: paragraphs in `:::note[]`, `:::tip[]`, blockquotes `>`, poem-like formatting
   - **Moderate context**: everything else (examples, descriptions, tables)

3. **Context Detection Heuristics**:
   - File path contains `rules/` → default to **Moderate**
   - Line contains "例如", "範例", "Example" → **Moderate**
   - Line in YAML frontmatter `description:` → **Flexible** (promotional)
   - Paragraph after "---" divider at file start → **Flexible** (back cover)
   - Header text contains "動作", "基礎", "進階" → **Strict**
   - `####` sub-headings under `### 基礎成長` / `### 進階成長` (or equivalent advancement/mechanic sections) → **Strict** (these describe concrete game rules even without keywords)
   - **Character sheet data sections** (archetype playbooks): paragraphs under `## <原型名稱>` headings that contain dice syntax (`2d6`, `1d20`), numeric stat tables, Light Costume tables (`光之裝束`), advancement lists (`成長`), or move descriptions with mechanical effects → **Strict** (these are game data, not prose)
   - `rules/` path + paragraph outside `:::note`/`:::tip`/`>` → at least **Moderate**, upgrade to **Strict** if describing procedures or restrictions

When in doubt, treat as **Moderate** (balance between strict and flexible).

#### 3.2 Context-Aware Glossary Application

**IMPORTANT: Apply glossary terms according to context priority:**

| Context Type | Glossary Priority | Rationale |
|--------------|-------------------|-----------|
| **Rules text** (mechanics, procedures) | 🔴 **Strict** | Consistency critical for gameplay |
| **Examples** (gameplay scenarios) | 🟡 **Moderate** | Balance clarity + natural dialogue |
| **Flavor text** (quotes, poems, songs) | 🟢 **Flexible** | Preserve literary/poetic intent |
| **Back cover** (promotional copy) | 🟢 **Flexible** | Marketing tone > strict terminology |
| **Character dialogue** | 🟡 **Moderate** | Consider character voice |

**When glossary conflicts with context:**
1. **Strict context** → Always use glossary term, flag if awkward
2. **Moderate context** → Prefer glossary, but allow natural phrasing
3. **Flexible context** → Preserve original intent, note glossary exists

**Example:**
```
❌ 封底文案：「正義的勇者」→「正義騎士」
   理由：詩意宣傳文案，保留原文感
   
✅ 規則說明：「正義的勇者」→「正義騎士」
   理由：遊戲機制術語，必須一致
```

When presenting a glossary-based suggestion in **flexible context**, add a note:
```
📍 Line 25 [Flavor text - 封底文案]
目前譯文: "正義的勇者"
Glossary: "正義騎士" (Campeonas de la Justicia)
問題: [terminology] 與 glossary 不符，但此為宣傳文案

建議: 保留詩意或套用 glossary？[保留 / 套用]
```

#### 3.2.1 Glossary Notes Validation

While reviewing each section, **cross-check glossary `notes` fields** against the actual source context:

1. When encountering a glossary term in the translated text, verify that the term's `notes` field in `glossary.json` correctly describes its usage context (e.g., correct archetype attribution, correct game mechanic category)
2. **Common errors to catch**:
   - Wrong archetype attribution (e.g., notes say "參謀" but term belongs to "聖母")
   - Outdated context description after glossary restructuring
   - Missing notes for terms that need disambiguation
3. **If a notes error is found**: correct it silently via direct edit to `glossary.json` — no user prompt needed for notes-only fixes. Record the correction in the session log under a `## Glossary 更新` section.

#### 3.2.2 Homonymous Source Terms (同名異義)

When the same source-language term refers to **different game elements** (e.g., "Escudo de Luz" is both the Guardian's signature ability and a Healer sacred power effect):

1. **Check glossary** for existing disambiguation entries (e.g., `Escudo de Luz (Sanadora)`)
2. **If translator already disambiguated** (e.g., 「光之盾」 vs 「光之護盾」) but glossary has no matching entry:
   - Present as a `[g] glossary` decision (see Step 3.4) — keep translation, add glossary entry with `(<context>)` suffix
3. **If translator did NOT disambiguate** (both rendered identically):
   - Propose disambiguation with distinct Chinese terms
   - Explain which game element each refers to
4. **Glossary entry format** for disambiguation: `"<Source Term> (<Archetype/Context>)"` → distinct `zh` value

#### 3.3 Check Against History Before Proposing

Before generating a suggestion, check `preferences` and `candidates`:

- **Matches a preference (`promoted_to_style_decisions: true`)** → skip silently (already a permanent rule)
- **Matches a preference (`promoted: false`)** → pre-fill suggestion, label `🔁 依慣例`; user just confirms
- **Matches a candidate** → generate suggestion normally; note it as a recurring pattern
- **No match** → generate fresh suggestion

Pre-fill display:
```
🔁 依慣例（信心度 83%）
目前譯文: "當你擲 2d6 時..."
套用偏好: "當你投擲 2d6 時..."
是否套用？[Y/n]
```

#### 3.4 Propose Improvements

When a sentence can be improved:

**Step 1: Write to log file first**

Append to `./retranslate-result/<session-file>.md`:

```markdown
## Line 42

**原文 (Page 15):**
> When you attack an enemy, roll 2d6.

**目前譯文:**
> 當你攻擊敵人時，擲 2d6。

**建議譯文:**
> 當你攻擊敵人時，投擲 2d6。

**問題類型:** naturalness  
**說明:** 動詞「擲」可改為更自然的「投擲」

**決策:** _(pending)_

---
```

**Step 2: Present to user via `AskUserQuestion`**

Format the question text with context, then use structured options:

```
question: "Line 42：[naturalness] 動詞「擲」→「投擲」
原文: When you attack an enemy, roll 2d6.
目前: 當你攻擊敵人時，擲 2d6。
建議: 當你攻擊敵人時，投擲 2d6。"

options:
  - [y] 接受   — 套用建議譯文
  - [n] 保留   — 維持目前譯文
  - [g] glossary — 保留譯文，新增/更新 glossary 條目
  - [e] 自訂   — 提供其他譯法（使用者透過 Other 輸入）
```

Use `[g]` when the translation is correct but glossary needs a new disambiguation entry or notes correction (see Step 3.2.1).

The `[s] 跳過` case is handled by user selecting "Other" and typing "skip", or simply by the agent advancing without tally update when the user dismisses.

#### 3.5 Update Session Tally and Log (Not the File)

After each user response:

**First: Update the log file**

Replace `**決策:** _(pending)_` with:
- `y` → `**決策:** ✅ 接受`
- `n` → `**決策:** ❌ 保留`
- `g` → `**決策:** 📖 glossary 更新: "<description of glossary change>"`
- `e` → `**決策:** ✏️ 自訂: "<user's custom text>"`
- `s` → `**決策:** ⏭️ 跳過`

**Then: Update session tally (in-memory only)**

- `y` (accepted) → `session_tally[id].accepted += 1`; save example if < 2 stored
- `n` (rejected) → `session_tally[id].rejected += 1`; optionally ask brief reason
- `g` (glossary) → no tally update; add/update glossary entry directly (see Step 5)
- `e` (custom) → `session_tally[id].accepted += 1`; save custom result as example
- `s` (skip) → no tally update

**When NOT to update tally:**
- `change_type == "terminology"` AND the issue is a one-off glossary mismatch (wrong term used for a specific glossary entry) → do NOT create a tally entry. These are corrected in-place and will not recur, so they are not meaningful as learnable patterns.
- `[g] glossary` decisions → no tally update. These are glossary maintenance actions, not translation pattern learning.
- Only create tally entries for **recurring stylistic patterns** (naturalness, clarity, consistency) that may appear across multiple files.

### 4. Apply Revisions

After completing a file, apply all accepted/custom changes using the `edit` tool, in line-number order.

### 5. Run Terminology Check

```bash
PYTHONIOENCODING=utf-8 uv run --with jsonschema python scripts/term_read.py
```

> **Windows note**: Without `PYTHONIOENCODING=utf-8`, the script may crash on non-ASCII source terms (e.g., Spanish characters) due to `cp950` encoding.

If new terms found, invoke `terminology-management` skill.

**Glossary edit boundary — when to edit directly vs. delegate:**

| Action | Method | Rationale |
|--------|--------|-----------|
| Fix `notes` field (typo, wrong archetype) | Direct edit to `glossary.json` | Metadata-only, no term change |
| Add disambiguation entry (e.g., `Escudo de Luz (Sanadora)`) | Direct edit to `glossary.json` | New entry with known zh/notes, no decision needed |
| Change a term's `zh` value | `terminology-management` skill | Affects all files; needs consistency check |
| Add a brand-new unmanaged term | `terminology-management` skill | Requires evidence calculation and user decision |

### 6. Update `file_reviews` (End of Each File)

After completing each file review, update the file's metadata:

```json
"rules/combat.md": {
  "last_reviewed": "2026-02-24T11:09:21Z",
  "review_count": 3,
  "issues_found": 8,
  "changes_applied": 6,
  "paragraphs_reviewed": 42,
  "last_section_reviewed": "## 傷害與治療",
  "resume_from": null
}
```

**Field definitions:**
- `last_reviewed`: ISO 8601 timestamp in UTC (format: `YYYY-MM-DDTHH:MM:SSZ`)
- `review_count`: Total number of times this file has been reviewed (increment by 1)
- `issues_found`: Number of suggestions presented to user in this session
- `changes_applied`: Number of suggestions accepted/custom-edited by user in this session

- `paragraphs_reviewed`: Total paragraphs reviewed in Strategy A (cumulative across sessions; 0 for other strategies)
- `last_section_reviewed`: Heading of the last section reviewed (for resume display; `null` if not applicable)
- `resume_from`: Index into `alignment[]` for next resume point; `null` = review complete

Only `review_count` and `paragraphs_reviewed` increment across sessions. `issues_found` and `changes_applied` reflect current session only.

### 7. Flush Session Tally (End of Session)

After all files reviewed, merge `session_tally` into `retranslate-history.json`:

#### Merge Logic

For each `id` in `session_tally`:

1. **Exists in `preferences{}`** → add counts, recalculate `confidence`, rotate examples (keep max 2)
2. **Exists in `candidates{}`** → add counts; if now `accepted >= 3` AND `confidence >= 0.75`:
   - Move from `candidates{}` to `preferences{}`
   - Show promotion prompt:
     ```
     📈 候選偏好已達門檻：「投擲 vs 擲」（信心度 80%，3 次紀錄）
     是否確認為學習偏好？[Y/n]
     ```
3. **New pattern** → add to `candidates{}`

#### Discard Session Tally

`session_tally` is an in-memory structure only. It is **never written to disk**.

### 8. Promote Preferences to `style-decisions.json`

If a preference reaches `confidence >= 0.90` AND `accepted >= 5`:

```
📌 偏好「投擲 vs 擲」已有充分證據（信心度 90%，5 次紀錄）。
是否寫入 style-decisions.json 作為永久規則？[Y/n]
```

If yes:
- Write to `style-decisions.json`
- Set `promoted_to_style_decisions: true` in the preference entry
- This preference will no longer generate suggestions (silently skipped)

### 9. Prune Stale Candidates (Optional, On Request)

Run `/retranslate --prune` to clean up stale candidates:
- Remove candidates with `accepted + rejected <= 1` and last session > 30 days ago
- Ask user to confirm before deletion

### 10. Session Summary

At the end of the session, write a summary section to the **last file's log** or create a separate `session-summary_<timestamp>.md`:

```markdown
---

# 審閱摘要

- **審閱時間:** 2026-02-24T11:09:21Z
- **建議項目:** 8 項
- **接受:** 6 項
- **拒絕:** 2 項
- **自訂:** 0 項
- **跳過:** 0 項

## 偏好更新
- 更新：「投擲」偏好（信心度 75% → 83%）
- 晉升：術語括注 → style-decisions.json ✓
```

Then show to user:

```
## 重譯完成

### 審閱統計
- 檔案：rules/combat.md
- 建議：8 項 ／ 接受：6 ／ 拒絕：2
- 📝 紀錄已存至：./retranslate-result/rules-combat_2026-02-24T11-09-21Z.md

### 偏好更新
- 更新：「投擲」偏好（信心度 75% → 83%）
- 晉升：術語括注 → style-decisions.json ✓

### 下一步
- 繼續審閱：rules/index.md（未審閱）
```

---

## Review Strategies

Ask user to choose at session start:

| Strategy | Actual Process | Best for |
|----------|----------------|----------|
| **A: Full Review** | 逐段完整審閱 — 每段與西文原文逐一比對 | 首次深度審閱、關鍵規則文件 |
| **B: Targeted** | 術語 (glossary) + 清晰度 only, skip style/naturalness | 大型文件快速 QA |
| **C: History-Driven** | 僅套用已學 preferences，不提新建議 | 大批量套用既有規則 |
| **D: Terminology-Only** | 僅 `term_read.py` + glossary cross-check | 翻譯後即時驗證 |

### Strategy A: Full Review（逐段完整審閱）

A true paragraph-by-paragraph review comparing every translated paragraph against its Spanish source.

**Expectation Setting（Strategy A 選定後、Phase 1 開始前向使用者顯示）：**
- 每段都會與西文原文逐一比對，無問題的段落會靜默略過
- 僅有建議時才打斷使用者
- 支援中途切換至 Strategy B/C/D
- 支援 `[q]` 中斷 + `/retranslate --resume` 續審

#### Phase 1: Structural Alignment

1. Run `retranslate_align.py` to build `alignment[]`
2. Display alignment summary to user, including a per-section table:
   ```
   📊 對齊摘要：
   - 章節數：8
   - 段落配對數：42
   - 無對應原文（跳過）：3 段（Starlight 組件）
   - 潛在遺漏：1 段

   | # | 章節 | 段落數 | 語境 |
   |---|------|--------|------|
   | 1 | 基本動作（Acciones Básicas） | 12 | Strict |
   | 2 | 範例（Ejemplo） | 5 | Moderate |
   | … | … | … | … |
   ```
   The context type column reflects the **dominant** context detected for each section per Step 3.1 heuristics.
3. **Conditional confirmation** — only ask user to choose if alignment reveals concerns:
   - Potential omissions > 0, OR total paragraphs > 200 → ask:
     - `[c]` 繼續逐段審閱
     - `[b]` 改用 Strategy B（目標式）
     - `[d]` 改用 Strategy C（歷史驅動）
   - Otherwise → proceed directly to Phase 2 (user already chose Strategy A)

#### Phase 2: Sequential Section-by-Section Review

Process each entry in `alignment[]` sequentially:

1. **Check resume checkpoint**: if `resume_from` exists in `file_reviews`, skip entries with `index < resume_from`
2. **Display current section heading** as navigation landmark:
   ```
   ── 章節 3/8：基本動作（Acciones Básicas）──
   ```
3. **For each paragraph pair** `(zh_para, es_para)`:
   - Apply **Step 3.1** (parse document structure, determine context type)
   - Apply **Step 3.2** (context-aware glossary check)
   - Apply **Step 3.3** (check against history)
   - Analyze translation quality: accuracy, terminology compliance, naturalness
   - **Issues found** → execute **Step 3.4** to present suggestion and wait for user decision
   - **No issues** → advance silently
4. **After each section completes**: save `resume_from = next_index` to `file_reviews`
5. **User enters `[q]`**: interrupt, save progress, display resume info:
   ```
   💾 進度已儲存：章節 3/8（基本動作）
   下次執行 /retranslate --resume 可從此處繼續
   ```

#### Phase 3: Completion

1. Clear `resume_from` (set to `null`) — review is complete
2. Update `paragraphs_reviewed` with total paragraphs reviewed
3. Update `last_section_reviewed` with final section heading
4. Proceed to **Step 4** (apply revisions)

### Strategy B: Targeted

Focus ONLY on:
- ✅ Glossary term mismatches
- ✅ Obvious clarity issues (e.g., missing negation)
- ❌ Skip: naturalness, style preferences, word choice

Use when: time-limited, or file already reviewed before

### Strategy C: History-Driven

Apply ONLY existing preferences with `confidence >= 0.75`:
- No new suggestions generated
- Batch-apply known patterns
- Ask user once per pattern type

Use when: bulk-updating many files with learned rules

### Strategy D: Terminology-Only

1. Run `term_read.py` to find undefined terms
2. Cross-check all glossary entries appear correctly
3. No translation quality review

Use when: just translated, want quick term validation

---

## Quality Thresholds

Only propose changes when:
- ✅ Improvement is clear and measurable
- ✅ Aligns with `glossary.json` / `style-decisions.json` **in appropriate context**
- ✅ Original meaning is preserved or clarified
- ✅ Not already a promoted permanent rule
- ❌ Not pure personal preference with no justification
- ❌ Not glossary-forcing in flavor text without user consent

**Context-Specific Quality Bar:**

| Change Type | Strict Context | Flexible Context |
|-------------|----------------|------------------|
| Glossary mismatch | Always propose | Ask user preference |
| Naturalness | Propose if awkward | Propose only if confusing |
| Consistency | Always propose | Propose if pattern exists |
| Accuracy | Always propose | Always propose |

---

## Example Usage

```
/retranslate
/retranslate docs/src/content/docs/rules/basic.md
/retranslate rules
/retranslate all
/retranslate --resume
/retranslate --prune
```

---

## Integration with Other Skills

- **Before**: `/check-consistency` to identify known issues first
- **During**: `terminology-management` for new glossary entries
- **After**: `/check-completeness` to verify structure is intact
- **Persistent memory**: `retranslate-history.json` feeds into future sessions automatically
