#!/usr/bin/env python3
from pathlib import Path
import re
import unicodedata

DOCS_DIR = Path("docs")
INDEX_PATH = DOCS_DIR / "index.md"

# ---------- 유틸 ----------

def normalize_name(name: str) -> str:
    """표시용: 숫자 프리픽스 제거(01_, 1., 1- 등), 앞뒤 공백 제거."""
    n = re.sub(r"^\s*(\d+[_\.\-\s]+)", "", name)
    return n.strip()

def sort_key(p: Path):
    """정렬용: 폴더/파일 이름에서 숫자 프리픽스 추출해 정렬 안정화."""
    s = p.name
    m = re.match(r"^\s*(\d+)", s)
    num = int(m.group(1)) if m else 10**9
    # 한글/영문 혼합 정렬 안정화를 위해 NFKD 정규화
    ascii_key = unicodedata.normalize("NFKD", s).lower()
    return (p.is_file() * 1, num, ascii_key)

def is_hidden_or_tmp(p: Path) -> bool:
    """임시/숨김 제외: _로 시작, .으로 시작, ~백업, .swp 등."""
    n = p.name
    return n.startswith(".") or n.startswith("_") or n.endswith("~") or n.endswith(".swp")

def find_title(md_path: Path) -> str:
    """첫 H1/H2를 제목으로, 없으면 파일명 기반."""
    try:
        for line in md_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            t = line.strip()
            if t.startswith("#"):
                return re.sub(r"^#+\s*", "", t).strip()
    except Exception:
        pass
    return normalize_name(md_path.stem)

def rel_link(md_path: Path) -> str:
    """
    링크는 Jekyll 기본(= .md -> .html 변환)을 가정하여 확장자 생략을 권장.
    예: docs/network/TCP.md -> network/TCP
    """
    rel = md_path.relative_to(DOCS_DIR)
    return str(rel.with_suffix(""))

# ---------- 트리 빌드 ----------

def list_children(dir_path: Path):
    items = []
    for p in sorted(dir_path.iterdir(), key=sort_key):
        if is_hidden_or_tmp(p):
            continue
        # /docs 내부만, symlink는 무시(원한다면 허용 가능)
        if p.is_dir() or (p.is_file() and p.suffix.lower() == ".md"):
            items.append(p)
    return items

def build_tree(dir_path: Path, depth: int = 0):
    """
    폴더 트리를 재귀적으로 순회하여 (folders, files, readme) 구조 반환.
    readme.md는 폴더 소개 문서로 특별 취급.
    """
    nodes = {"path": dir_path, "depth": depth, "folders": [], "files": [], "readme": None}
    for child in list_children(dir_path):
        if child.is_dir():
            nodes["folders"].append(build_tree(child, depth + 1))
        else:
            if child.name.lower() == "readme.md":
                nodes["readme"] = child
            elif child.name.lower() != "index.md":
                nodes["files"].append(child)
    return nodes

# ---------- 렌더러 ----------

def header_for_depth(depth: int) -> str:
    """
    depth=0 : 문서 전체 타이틀(#)
    depth>=1 : 폴더 헤더(##, ###, #### ...)
    """
    if depth <= 0:
        return "#"
    level = min(depth + 1, 6)  # 최대 ###### 로 제한
    return "#" * level

def render_folder(node) -> list[str]:
    lines = []
    path: Path = node["path"]
    depth: int = node["depth"]
    name = normalize_name(path.name) if depth > 0 else "스터디 내용 정리"

    # 폴더 헤더
    lines.append(f"{header_for_depth(depth)} {name}")
    if depth == 0:
        lines.append("> 이 파일은 GitHub Actions로 자동 생성/갱신됩니다. 직접 수정하지 마세요.")
    # 폴더 README 링크(있으면)
    if node["readme"] is not None:
        title = find_title(node["readme"])
        href = rel_link(node["readme"])
        lines.append(f"- 📄 [{title}]({href})")

    # 파일 목록 (중첩 리스트)
    for f in node["files"]:
        title = find_title(f)
        href = rel_link(f)
        lines.append(f"- [{title}]({href})")

    # 하위 폴더 재귀
    for sub in node["folders"]:
        lines.append("")  # 섹션 간 여백
        lines.extend(render_folder(sub))
    return lines

def build_index_md():
    tree = build_tree(DOCS_DIR, depth=0)
    lines = render_folder(tree)
    lines.append("")  # EOF 개행
    return "\n".join(lines)

# ---------- 엔트리 ----------

def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    content = build_index_md()
    prev = INDEX_PATH.read_text(encoding="utf-8", errors="ignore") if INDEX_PATH.exists() else ""
    if prev.strip() != content.strip():
        INDEX_PATH.write_text(content, encoding="utf-8")

if __name__ == "__main__":
    main()
