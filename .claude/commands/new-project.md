---
name: new-project
description: 建立新專案 - 從模板建立本地專案
arguments:
  - name: pdf_path
    description: PDF 檔案路徑
    required: true
  - name: project_name
    description: 專案名稱（用於資料夾名稱）
    required: false
---

# Create New Project from Template

從 game-doc-template 模板建立新的遊戲文件專案。

## Prerequisites

- `git` 已設定
- PDF 檔案已準備好

## Process

### 1. Gather Information

使用 AskUserQuestion 工具一次詢問以下問題：

**問題 1: 專案路徑**
- header: "專案路徑"
- question: "要將專案建立在哪個路徑？"
- options:
  - `../` (預設，與模板同層)
  - 自訂路徑

**問題 2: 遊戲標題**
- header: "遊戲標題"
- question: "這個遊戲的繁體中文標題是什麼？"
- 從 PDF 檔名提取原文名稱作為參考
- 讓使用者輸入繁中翻譯

**問題 3: 專案名稱**（若 `$ARGUMENTS` 未提供）
- header: "專案名稱"
- question: "專案資料夾與 repo 名稱？"
- 根據 PDF 檔名建議 slug 格式（lowercase, hyphenated）

Example:
```
PDF: "Blades in the Dark.pdf"
原文標題: Blades in the Dark
繁中標題: 暗夜冷鋒 (由使用者輸入)
建議專案名稱: blades-in-the-dark
```

### 2. Determine Paths

```bash
# Template path (current project)
TEMPLATE_PATH="D:\Code\game-doc-template"

# Target directory (user specified, default: ../)
TARGET_DIR="<user_specified_path>/<project_name>"

# PDF path (from arguments)
PDF_PATH="$ARGUMENTS[0]"

# Game title (user specified)
GAME_TITLE_EN="<extracted_from_pdf>"
GAME_TITLE_ZH="<user_specified>"
```

### 3. Copy Template

```bash
# Copy template to target directory
Copy-Item -Path $TEMPLATE_PATH -Destination $TARGET_DIR -Recurse

# Navigate to new project
cd $TARGET_DIR

# Remove .git directory
Remove-Item -Path .git -Recurse -Force

# Initialize new git repo
git init
git add .
git commit -m "Initial commit from game-doc-template"
```

### 4. Copy PDF

```bash
# Create data directory if not exists
mkdir -p data/pdfs

# Copy PDF to new project
cp "<pdf_path>" data/pdfs/
```

### 5. Update Project Configuration

Edit `docs/astro.config.mjs`:
- Update `SITE_CONFIG.title` with `GAME_TITLE_ZH` (繁中標題)

Edit `CLAUDE.md`:
- Update project description with game name (原文 + 繁中)
- Example: `# blades-in-the-dark\n\nBlades in the Dark（暗夜冷鋒）PDF 遊戲規則翻譯專案。`

### 6. Verify Setup

```bash
# Check structure
Get-ChildItem
Get-ChildItem data\pdfs\
Get-ChildItem docs\

# Verify git status
git status
```

### 7. Next Steps

Inform user:
```
✓ 專案已建立: <project_name>
✓ 遊戲標題: <GAME_TITLE_EN>（<GAME_TITLE_ZH>）
✓ 專案路徑: <TARGET_DIR>
✓ PDF 已複製到: data\pdfs\<filename>

下一步：
1. cd <TARGET_DIR>
2. 執行 /init-doc 開始初始化文件
```

## Example Usage

```
/new-project ~/Downloads/Blades-in-the-Dark.pdf
/new-project ~/Downloads/game.pdf my-game-docs
```

## Error Handling

- If target directory already exists: Ask for confirmation to overwrite or use different name
- If PDF not found: Ask for correct path
- If template directory not accessible: Verify TEMPLATE_PATH
