#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Job Search OS - 실시간 일일 신문 수집기 (RSS Aggregator)
외장 라이브러리 의존성 없이 Python 3 내장 라이브러리만을 사용하여 작동합니다.
"""

import os
import re
import html
import ssl
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

# 1. 수집 타겟 RSS 피드 목록
FEEDS = {
    "긱뉴스 (IT 및 개발 트렌드)": "https://news.hada.io/rss/news",
    "CG 채널 (VFX, CG, 버추얼 프로덕션 업계 소식)": "https://www.cgchannel.com/feed/",
    "엔비디아 개발자 블로그 (실시간 그래픽스 및 AI 기술)": "https://developer.nvidia.com/blog/feed/",
    "블렌더 네이션 (3D CG 오픈소스 소식)": "https://www.blendernation.com/feed/"
}

# 2. 이모지 제거 헬퍼 함수 (미니멀리즘 스타일 유지)
def remove_emojis(text):
    if not text:
        return ""
    # 유니코드 이모지 영역 정의 및 제거
    emoji_pattern = re.compile(
        "["
        "\U00010000-\U0010ffff"  # Supplemental Planes (이모지 포함)
        "\u2600-\u27BF"          # Miscellaneous Symbols and Dingbats
        "\u200d"                 # Zero Width Joiner
        "\ufe0f"                 # Variation Selector 16
        "]+", flags=re.UNICODE
    )
    return emoji_pattern.sub(r"", text).strip()

# 3. HTML 태그 제거 및 텍스트 정제
def clean_text(text, max_len=180):
    if not text:
        return ""
    # HTML 태그 제거
    clean = re.sub(r'<[^>]+>', '', text)
    # HTML 엔티티 복원 (예: &amp; -> &)
    clean = html.unescape(clean)
    # 연속된 공백 문자 축소
    clean = re.sub(r'\s+', ' ', clean)
    clean = clean.strip()
    # 이모지 제거
    clean = remove_emojis(clean)
    # 글자 수 제한
    if len(clean) > max_len:
        clean = clean[:max_len] + "..."
    return clean

# 4. 개별 RSS 및 Atom 피드 파싱
def fetch_feed(feed_name, url):
    print(f"[수집 시작] {feed_name}...")
    articles = []
    
    # SSL 인증서 검증 우회 설정 (네트워크 환경 호환성 확보)
    context = ssl._create_unverified_context()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'ko-KR,ko;q=0.8,en-US;q=0.5,en;q=0.3'
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, context=context, timeout=10) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        
        # 1. RSS 포맷 검사 (<item> 태그 탐색)
        items = root.findall('.//item')
        if items:
            for item in items[:6]:
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                pub_date = item.find('pubDate')
                
                title_text = remove_emojis(title.text) if title is not None else "제목 없음"
                link_text = link.text.strip() if link is not None else ""
                desc_text = clean_text(desc.text) if desc is not None else ""
                
                date_str = ""
                if pub_date is not None and pub_date.text:
                    date_str = f"({pub_date.text.strip()[:16]})"
                    
                articles.append({
                    "title": title_text,
                    "link": link_text,
                    "desc": desc_text,
                    "date": date_str
                })
        else:
            # 2. Atom 포맷 검사 ({http://www.w3.org/2005/Atom}entry 태그 탐색)
            # 네임스페이스를 고려하여 와일드카드 태그 탐색 활용
            entries = root.findall('.//{*}entry')
            for entry in entries[:6]:
                title = entry.find('{*}title')
                link_nodes = entry.findall('{*}link')
                link_text = ""
                for l_node in link_nodes:
                    href = l_node.attrib.get('href', '')
                    rel = l_node.attrib.get('rel', 'alternate')
                    if rel == 'alternate' and href:
                        link_text = href
                        break
                if not link_text and link_nodes:
                    link_text = link_nodes[0].attrib.get('href', '')
                
                desc = entry.find('{*}content')
                if desc is None:
                    desc = entry.find('{*}summary')
                
                pub_date = entry.find('{*}published')
                if pub_date is None:
                    pub_date = entry.find('{*}updated')
                
                title_text = remove_emojis(title.text) if title is not None else "제목 없음"
                desc_text = clean_text(desc.text) if desc is not None else ""
                
                date_str = ""
                if pub_date is not None and pub_date.text:
                    raw_date = pub_date.text.strip()
                    date_str = f"({raw_date.replace('T', ' ')[:16]})"
                    
                articles.append({
                    "title": title_text,
                    "link": link_text,
                    "desc": desc_text,
                    "date": date_str
                })
                
    except Exception as e:
        print(f"[경고] {feed_name} 수집 실패: {e}")
        
    return articles

# 5. 마크다운 파일로 뉴스페이퍼 저장
def generate_newspaper():
    today_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 저장 폴더 경로 확인 및 생성
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, "11_모니터링")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "일일_신문.md")
    
    markdown_content = []
    
    # Frontmatter 작성
    markdown_content.append("---")
    markdown_content.append("status: active")
    markdown_content.append("priority: high")
    markdown_content.append("category: Newspaper")
    markdown_content.append("review_cycle: daily")
    markdown_content.append(f"last_verified: {datetime.now().strftime('%Y-%m-%d')}")
    markdown_content.append("monitoring_method: automatic")
    markdown_content.append("related_notes: \"[[01_대시보드]]\"")
    markdown_content.append("---")
    markdown_content.append("")
    
    # 제목 및 메타정보
    markdown_content.append("# 11. 일일 신문 (Real-Time Newspaper)")
    markdown_content.append(f"최종 갱신일시: `{today_str}`")
    markdown_content.append("")
    markdown_content.append("> [!NOTE]")
    markdown_content.append("> 이 문서는 `일일_신문_수집기.py`를 통해 실시간으로 자동 갱신되는 맞춤형 기술 신문입니다.")
    markdown_content.append("> 업스트림 신호(새로운 오픈소스 버전, 그래픽스 R&D 동향, 업계 구인)를 빠르게 모니터링하기 위해 사용합니다.")
    markdown_content.append("")
    markdown_content.append("---")
    markdown_content.append("")
    
    # 섹션별 피드 병합
    for feed_name, url in FEEDS.items():
        articles = fetch_feed(feed_name, url)
        
        markdown_content.append(f"## {feed_name}")
        markdown_content.append("")
        
        if not articles:
            markdown_content.append("일시적으로 데이터를 가져올 수 없거나 업데이트가 없습니다.")
            markdown_content.append("")
            continue
            
        for art in articles:
            markdown_content.append(f"### [{art['title']}]({art['link']}) {art['date']}")
            if art['desc']:
                markdown_content.append(f"- {art['desc']}")
            markdown_content.append("")
        
        markdown_content.append("---")
        markdown_content.append("")
        
    # 저장 실행
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(markdown_content))
        
    print(f"\n[성공] 일일 신문 작성이 완료되었습니다: {output_path}")

if __name__ == "__main__":
    generate_newspaper()
