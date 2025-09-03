from pathlib import Path
import re, json
from urllib.parse import quote

DOCS = Path("docs")

def clean(md: str) -> str:
    md = re.sub(r"```.*?```", " ", md, flags=re.S)   # 코드블록 제거
    md = re.sub(r"`[^`]+`", " ", md)                 # 인라인코드 제거
    md = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", md) # 링크는 텍스트만
    md = re.sub(r"<!\-\-.*?\-\->", " ", md, flags=re.S)  # 주석 제거
    md = re.sub(r"#+\s*", "", md)                    # 헤더 마크 제거
    return re.sub(r"\s+", " ", md).strip()

def title_of(path: Path, fallback=None) -> str:
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if line.strip().startswith("#"):
            return re.sub(r"^#+\s*", "", line).strip()
    return fallback or path.stem

def rel_path_without_ext(path: Path) -> str:
    rel = path.relative_to(DOCS).with_suffix("")     # .md 제거
    return "/" + quote(str(rel.as_posix()))                     # /네트워크/TCP 형태

items = []
for md in DOCS.rglob("*.md"):
    if md.name.lower() == "index.md":
        continue
    txt = md.read_text(encoding="utf-8", errors="ignore")
    items.append({
        "title": title_of(md),
        "path": rel_path_without_ext(md),            # baseurl은 JS에서 붙임
        "content": clean(txt),
    })

(DOCS / "search_index.json").write_text(
    json.dumps(items, ensure_ascii=False, separators=(",", ":")),
    encoding="utf-8"
)
