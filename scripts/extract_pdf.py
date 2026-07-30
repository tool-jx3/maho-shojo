#!/usr/bin/env python3
"""
PDF 提取工具
將 PDF 轉換為 Markdown，支援文字與圖片提取

使用方式：
    python scripts/extract_pdf.py <pdf_file>
    python scripts/extract_pdf.py data/rulebook.pdf

輸出：
    data/markdown/<檔名>.md               - markitdown 提取版本
    data/markdown/<檔名>_pages.md         - 含頁碼標記版本（用於章節拆分）
    data/markdown/<檔名>_formatted.md     - 含格式版本（標題/粗體/斜體/表格/列表）
    data/markdown/images/<檔名>/          - 提取的圖片
"""

import sys
from pathlib import Path

try:
    from markitdown import MarkItDown
except ImportError:
    MarkItDown = None

try:
    import pymupdf
except ImportError:
    pymupdf = None

try:
    import pymupdf4llm
except ImportError:
    pymupdf4llm = None


def extract_with_markitdown(pdf_path: Path, output_dir: Path) -> Path | None:
    """使用 markitdown 提取 PDF 內容（較好的格式保留）"""
    if MarkItDown is None:
        print("⚠️  markitdown 未安裝，跳過")
        return None

    md = MarkItDown()
    result = md.convert(str(pdf_path))

    output_file = output_dir / f"{pdf_path.stem}.md"
    output_file.write_text(result.text_content, encoding="utf-8")

    print(f"✓ 已提取: {output_file}")
    return output_file


def extract_with_pages(pdf_path: Path, output_dir: Path) -> Path | None:
    """使用 pymupdf 提取 PDF 內容（保留頁碼標記，用於章節拆分）"""
    if pymupdf is None:
        print("⚠️  pymupdf 未安裝，跳過")
        return None

    doc = pymupdf.open(str(pdf_path))

    content_parts = []
    for page_num, page in enumerate(doc, 1):
        text = page.get_text("text")
        content_parts.append(f"\n\n<!-- PAGE {page_num} -->\n\n{text}")

    output_file = output_dir / f"{pdf_path.stem}_pages.md"
    output_file.write_text("".join(content_parts), encoding="utf-8")

    print(f"✓ 已提取（含頁碼）: {output_file}")
    return output_file


def extract_with_formatting(pdf_path: Path, output_dir: Path) -> Path | None:
    """使用 pymupdf4llm 提取 PDF 內容（保留頁碼、標題層級、粗體/斜體/等寬、列表、表格）"""
    if pymupdf4llm is None:
        print("⚠️  pymupdf4llm 未安裝，跳過")
        return None

    def hdr_info(span, page=None):
        """依字體大小映射標題層級（8.5pt 為內文基準）"""
        size = span["size"]
        if size >= 26:
            return "# "
        if size >= 20:
            return "## "
        if size >= 18:
            return "### "
        if size >= 13:
            return "#### "
        if size >= 11:
            return "##### "
        if size >= 9:
            return "###### "
        return ""

    pages = pymupdf4llm.to_markdown(
        doc=str(pdf_path),
        page_chunks=True,
        hdr_info=hdr_info,
    )

    content_parts = []
    for chunk in pages:
        page_num = chunk["metadata"]["page"] + 1
        text = chunk["text"]
        content_parts.append(f"\n\n<!-- PAGE {page_num} -->\n\n{text}")

    output_file = output_dir / f"{pdf_path.stem}_formatted.md"
    output_file.write_text("".join(content_parts).strip(), encoding="utf-8")

    print(f"✓ 已提取（含格式）: {output_file}")
    return output_file


def extract_images(pdf_path: Path, output_dir: Path) -> list[Path]:
    """提取 PDF 中的圖片"""
    if pymupdf is None:
        print("⚠️  pymupdf 未安裝，無法提取圖片")
        return []

    doc = pymupdf.open(str(pdf_path))
    images_dir = output_dir / "images" / pdf_path.stem
    images_dir.mkdir(parents=True, exist_ok=True)

    saved_images = []
    for page_num, page in enumerate(doc, 1):
        for img_index, img in enumerate(page.get_images()):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            image_path = images_dir / f"page{page_num:03d}_img{img_index:02d}.{image_ext}"
            image_path.write_bytes(image_bytes)
            saved_images.append(image_path)

    print(f"✓ 已提取 {len(saved_images)} 張圖片到 {images_dir}")
    return saved_images


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_path = Path(sys.argv[1])

    if not pdf_path.exists():
        print(f"❌ 找不到檔案: {pdf_path}")
        sys.exit(1)

    # 設定輸出目錄
    project_root = Path(__file__).parent.parent
    output_dir = project_root / "data" / "markdown"
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n📄 處理: {pdf_path.name}")
    print("-" * 50)

    # 使用 markitdown 提取
    # extract_with_markitdown(pdf_path, output_dir)

    # 使用 pymupdf 提取（含頁碼）
    # extract_with_pages(pdf_path, output_dir)

    # 使用 pymupdf4llm 提取（含格式）
    extract_with_formatting(pdf_path, output_dir)

    # 提取圖片
    # extract_images(pdf_path, output_dir)

    print("-" * 50)
    print("✅ 完成！")
    print(f"\n下一步：使用 split_chapters.py 拆分章節")


if __name__ == "__main__":
    main()
