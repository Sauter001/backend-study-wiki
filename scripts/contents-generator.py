#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
마크다운 파일의 헤더를 기반으로 목차(Table of Contents)를 자동 생성하는 프로그램

사용법: python contents-generator.py <markdown_file_path>
"""

import sys
import re
import os
from typing import List, Tuple

class MarkdownTOCGenerator:
    def __init__(self):
        self.toc_start_marker = "<!-- TOC START -->"
        self.toc_end_marker = "<!-- TOC END -->"
        
    def extract_headers(self, content: str) -> List[Tuple[int, str, str]]:
        """
        마크다운 내용에서 헤더를 추출합니다.
        
        Returns:
            List[Tuple[int, str, str]]: (레벨, 제목, 앵커) 튜플의 리스트
        """
        headers = []
        lines = content.split('\n')
        in_code_block = False
        
        for line in lines:
            stripped = line.strip()

            # code block 시작 끝 감지 (``` or ~~~)
            if re.match(r'^(```|~~~)', stripped):
                in_code_block = not in_code_block
                continue
            if in_code_block:
                continue

            # ATX 스타일 헤더 매칭 (# ## ### 등)
            match = re.match(r'^(#{1,6})\s+(.+?)(?:\s*#*\s*)?$', stripped)
            if match:
                level = len(match.group(1))  # # 개수
                title = match.group(2).strip()
                anchor = self.create_anchor(title)
                headers.append((level, title, anchor))
                
        return headers
    
    def create_anchor(self, title: str) -> str:
        """
        헤더 제목을 GitHub 스타일의 앵커로 변환합니다.
        """
        # 특수문자 제거 및 소문자 변환
        anchor = re.sub(r'[^\w\s가-힣-]', '', title.lower())
        # 공백을 하이픈으로 변경
        anchor = re.sub(r'\s+', '-', anchor.strip())
        # 연속된 하이픈 제거
        anchor = re.sub(r'-+', '-', anchor)
        # 앞뒤 하이픈 제거
        anchor = anchor.strip('-')
        
        return anchor
    
    def generate_toc(self, headers: List[Tuple[int, str, str]]) -> str:
        """
        헤더 리스트로부터 목차를 생성합니다.
        """
        if not headers:
            return ""
            
        toc_lines = [
            self.toc_start_marker,
            "",
            "## 목차",
            ""
        ]
        
        # 최소 레벨을 찾아 상대적 들여쓰기 계산
        min_level = min(header[0] for header in headers)
        
        for level, title, anchor in headers:
            indent = "  " * (level - min_level)  # 2칸씩 들여쓰기
            toc_line = f"{indent}- [{title}](#{anchor})"
            toc_lines.append(toc_line)
        
        toc_lines.extend(["", "---", "", self.toc_end_marker, ""])
        
        return '\n'.join(toc_lines)
    
    def remove_existing_toc(self, content: str) -> str:
        """
        기존 목차를 제거합니다.
        """
        # 정규표현식으로 기존 TOC 섹션 찾기 및 제거
        pattern = rf'{re.escape(self.toc_start_marker)}.*?{re.escape(self.toc_end_marker)}\n?'
        content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # 파일 시작 부분의 빈 줄들 정리
        content = re.sub(r'^\n+', '', content)
        
        return content
    
    def find_title_and_split_content(self, content: str) -> Tuple[str, str]:
        """
        문서 제목(첫 번째 # 헤더)을 찾고 제목과 나머지 내용을 분리합니다.
        
        Returns:
            Tuple[str, str]: (제목 부분, 나머지 내용)
        """
        lines = content.split('\n')
        title_end_idx = -1
        
        # 첫 번째 # 헤더 찾기
        for i, line in enumerate(lines):
            if re.match(r'^#\s+.+', line.strip()):
                title_end_idx = i
                break
        
        if title_end_idx == -1:
            # 제목이 없으면 전체를 나머지 내용으로
            return "", content
        
        # 제목 다음의 빈 줄들까지 포함해서 제목 섹션으로 처리
        title_lines = [lines[title_end_idx]]
        remaining_start_idx = title_end_idx + 1
        
        # 제목 다음의 연속된 빈 줄들을 제목 섹션에 포함
        while (remaining_start_idx < len(lines) and 
               lines[remaining_start_idx].strip() == ""):
            title_lines.append(lines[remaining_start_idx])
            remaining_start_idx += 1
        
        title_section = '\n'.join(title_lines)
        remaining_content = '\n'.join(lines[remaining_start_idx:]) if remaining_start_idx < len(lines) else ""
        
        return title_section, remaining_content

    def process_file(self, file_path: str) -> bool:
        """
        마크다운 파일을 처리하여 목차를 생성/업데이트합니다.
        
        Returns:
            bool: 성공 여부
        """
        try:
            # 파일 읽기
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 기존 목차 제거
            content_without_toc = self.remove_existing_toc(content)
            
            # 제목과 나머지 내용 분리
            title_section, remaining_content = self.find_title_and_split_content(content_without_toc)
            
            # 헤더 추출 (나머지 내용에서만)
            headers = self.extract_headers(remaining_content)
            
            if not headers:
                print("⚠️  헤더를 찾을 수 없습니다. 목차를 생성하지 않습니다.")
                return True
            
            # 목차 생성
            toc = self.generate_toc(headers)
            
            # 새로운 내용 구성: 제목 + 목차 + 나머지 내용
            new_content_parts = []
            
            if title_section.strip():
                new_content_parts.append(title_section)
            
            new_content_parts.append(toc)
            
            if remaining_content.strip():
                new_content_parts.append(remaining_content)
            
            new_content = '\n\n'.join(new_content_parts)
            
            # 파일 쓰기
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ 목차가 성공적으로 생성되었습니다: {file_path}")
            print(f"📝 발견된 헤더 수: {len(headers)}")
            
            return True
            
        except FileNotFoundError:
            print(f"❌ 파일을 찾을 수 없습니다: {file_path}")
            return False
        except PermissionError:
            print(f"❌ 파일에 대한 권한이 없습니다: {file_path}")
            return False
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")
            return False

def main():
    """메인 함수"""
    if len(sys.argv) != 2:
        print("사용법: python contents-generator.py <markdown_file_path>")
        print("예제: python contents-generator.py /docs/example.md")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    # 파일 확장자 확인
    if not file_path.lower().endswith(('.md', '.markdown')):
        print("⚠️  마크다운 파일(.md, .markdown)만 지원됩니다.")
        sys.exit(1)
    
    # 파일 존재 확인
    if not os.path.exists(file_path):
        print(f"❌ 파일이 존재하지 않습니다: {file_path}")
        sys.exit(1)
    
    # 목차 생성기 실행
    generator = MarkdownTOCGenerator()
    success = generator.process_file(file_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()