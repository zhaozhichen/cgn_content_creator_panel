#!/usr/bin/env python3
"""
小宇宙播客下载脚本 - 使用Python内置库
下载指定播客的最近N期音频文件
"""

import json
import os
import sys
import re
import time
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.parse import urljoin
from typing import List, Dict

def http_get(url: str, headers: dict = None) -> bytes:
    """使用urllib进行HTTP GET请求"""
    if headers is None:
        headers = {}
    
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "text/html,application/json"
    }
    default_headers.update(headers)
    
    req = Request(url, headers=default_headers)
    try:
        with urlopen(req, timeout=10) as response:
            return response.read()
    except Exception as e:
        print(f"HTTP请求失败: {e}")
        return None

def get_podcast_html(podcast_id: str) -> str:
    """获取播客页面HTML"""
    url = f"https://www.xiaoyuzhoufm.com/podcast/{podcast_id}"
    data = http_get(url)
    if data:
        return data.decode('utf-8', errors='ignore')
    return None

def extract_episodes_from_html(html: str, limit: int = 10) -> List[Dict]:
    """从HTML中提取单集信息"""
    episodes = []
    
    # 方法1: 查找包含单集信息的JSON数据
    json_patterns = [
        r'window\.__INITIAL_STATE__\s*=\s*({.+?});',
        r'window\.__NEXT_DATA__\s*=\s*({.+?})</script>',
        r'"episodes":\s*(\[[^\]]+\])',
    ]
    
    for pattern in json_patterns:
        matches = re.findall(pattern, html, re.DOTALL)
        for match in matches:
            try:
                data = json.loads(match)
                # 尝试从JSON中提取单集
                if isinstance(data, dict):
                    if 'episodes' in data:
                        eps = data['episodes']
                    elif 'data' in data and 'episodes' in data['data']:
                        eps = data['data']['episodes']
                    elif 'podcast' in data and 'episodes' in data['podcast']:
                        eps = data['podcast']['episodes']
                    else:
                        # 尝试查找任何包含episode信息的数组
                        for key, value in data.items():
                            if isinstance(value, list) and len(value) > 0:
                                if isinstance(value[0], dict) and ('title' in value[0] or 'episode_title' in value[0]):
                                    eps = value
                                    break
                    
                    if eps and isinstance(eps, list):
                        for ep in eps[:limit]:
                            episodes.append({
                                'episode_id': ep.get('id') or ep.get('eid') or ep.get('episode_id'),
                                'title': ep.get('title') or ep.get('episode_title') or 'Untitled',
                                'audio_url': ep.get('audio') or ep.get('audioUrl') or ep.get('audio_url')
                            })
                        if episodes:
                            return episodes
            except:
                continue
    
    # 方法2: 直接从HTML中查找单集链接和标题
    episode_link_pattern = r'<a[^>]+href="(/episode/[^"]+)"[^>]*>.*?<span[^>]*>([^<]+)</span>'
    matches = re.findall(episode_link_pattern, html, re.DOTALL)
    
    # 也尝试查找简单的episode链接
    simple_episode_pattern = r'href="(/episode/([a-zA-Z0-9]+))"'
    simple_matches = re.findall(simple_episode_pattern, html)
    
    # 合并两种方式找到的单集
    all_ep_ids = set([e.get('episode_id') for e in episodes])
    
    for link, title in matches[:limit * 2]:  # 获取更多以便筛选
        ep_id = link.split('/')[-1]
        if ep_id and ep_id not in all_ep_ids:
            episodes.append({
                'episode_id': ep_id,
                'title': title.strip(),
                'audio_url': None
            })
            all_ep_ids.add(ep_id)
    
    # 从简单链接中补充
    for link, ep_id in simple_matches[:limit * 2]:
        if ep_id not in all_ep_ids:
            episodes.append({
                'episode_id': ep_id,
                'title': f'Episode_{ep_id}',
                'audio_url': None
            })
            all_ep_ids.add(ep_id)
    
    return episodes[:limit]

def get_episode_audio_url(episode_id: str) -> str:
    """获取单集的音频URL"""
    url = f"https://www.xiaoyuzhoufm.com/episode/{episode_id}"
    html = http_get(url)
    
    if not html:
        return None
    
    html_str = html.decode('utf-8', errors='ignore')
    
    # 查找音频URL
    patterns = [
        r'"audioUrl"\s*:\s*"([^"]+)"',
        r'"audio"\s*:\s*"([^"]+)"',
        r'src="([^"]+\.mp3[^"]*)"',
        r'https://[^"]+\.mp3[^"]*',
        r'https://[^"]+\.m4a[^"]*',
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, html_str)
        for match in matches:
            if match and ('mp3' in match or 'm4a' in match or 'audio' in match.lower()):
                return match.strip('"').strip("'")
    
    return None

def download_audio(url: str, output_path: Path) -> bool:
    """下载音频文件"""
    if not url:
        return False
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.xiaoyuzhoufm.com/"
    }
    
    try:
        data = http_get(url, headers)
        if data:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(data)
            return True
    except Exception as e:
        print(f"  下载失败: {e}")
    
    return False

def download_podcast_episodes(podcast_id: str, podcast_name: str, limit: int = 3, output_dir: Path = None, skip_existing: bool = True):
    """下载播客的最近N期"""
    if output_dir is None:
        output_dir = Path("podcasts")
    
    output_dir = Path(output_dir) / podcast_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n开始处理播客: {podcast_name} (ID: {podcast_id})")
    print(f"目标: 最近 {limit} 期")
    
    # 检查已下载的文件
    existing_files = set()
    if skip_existing:
        for file in output_dir.glob("*.mp3"):
            existing_files.add(file.name)
        print(f"  已存在 {len(existing_files)} 个文件")
    
    # 获取播客页面
    print("  获取播客页面...")
    html = get_podcast_html(podcast_id)
    
    if not html:
        print(f"  ❌ 无法获取播客页面")
        return []
    
    # 提取单集信息（获取更多期以便跳过已下载的）
    print("  解析单集列表...")
    # 需要至少提取limit + 已存在数量，以便有足够的新单集
    episodes = extract_episodes_from_html(html, limit + len(existing_files) + 5)  # 获取更多期以便筛选
    
    if not episodes:
        print(f"  ⚠️  无法从页面提取单集信息")
        return []
    
    print(f"  找到 {len(episodes)} 期单集")
    
    # 跳过已下载的，只下载新的
    new_episodes = []
    episode_counter = len(existing_files) + 1  # 从已存在文件数+1开始编号
    
    for episode in episodes:
        ep_id = episode.get('episode_id')
        ep_title = episode.get('title', f"Episode_{ep_id}")
        
        # 清理文件名用于检查
        clean_title = "".join(c for c in ep_title if c.isalnum() or c in (' ', '-', '_', '：', '，')).strip()
        clean_title = clean_title.replace(' ', '_').replace('：', '_').replace('，', '_')[:50]
        
        # 检查是否已存在
        already_exists = False
        if skip_existing:
            for existing_file in existing_files:
                if ep_id in existing_file or clean_title[:30] in existing_file:
                    already_exists = True
                    break
        
        if not already_exists:
            new_episodes.append({
                'episode': episode,
                'episode_counter': episode_counter,
                'clean_title': clean_title
            })
            episode_counter += 1
            
            if len(new_episodes) >= limit:
                break
    
    print(f"  需要下载 {len(new_episodes)} 期新单集")
    
    if not new_episodes:
        print("  ✅ 所有单集已下载，无需重复下载")
        return []
    
    downloaded = []
    for i, item in enumerate(new_episodes, 1):
        episode = item['episode']
        ep_id = episode.get('episode_id')
        ep_title = episode.get('title', f"Episode_{ep_id}")
        clean_title = item['clean_title']
        ep_counter = item['episode_counter']
        
        print(f"\n  [{i}/{len(new_episodes)}] {ep_title}")
        
        # 获取音频URL
        audio_url = episode.get('audio_url')
        if not audio_url:
            print(f"    获取音频URL...")
            audio_url = get_episode_audio_url(ep_id)
        
        if not audio_url:
            print(f"    ⚠️  无法获取音频URL")
            continue
        
        print(f"    音频URL: {audio_url[:60]}...")
        
        # 下载音频（使用连续编号）
        output_file = output_dir / f"{ep_counter:02d}_{ep_id}_{clean_title}.mp3"
        if download_audio(audio_url, output_file):
            file_size = output_file.stat().st_size / (1024 * 1024)
            print(f"    ✅ 下载成功 ({file_size:.1f}MB): {output_file.name}")
            downloaded.append({
                'episode_id': ep_id,
                'title': ep_title,
                'audio_file': str(output_file),
                'audio_url': audio_url
            })
        else:
            print(f"    ❌ 下载失败")
        
        time.sleep(2)  # 避免请求过快
    
    return downloaded

def main():
    """主函数"""
    podcasts = [
        {
            'id': '61933ace1b4320461e91fd55',
            'name': '晚点聊_黄俊杰'
        },
        {
            'id': '6013f9f58e2f7ee375cf4216',
            'name': '知行小酒馆_李路野'
        },
        {
            'id': '62c6ae08c4eaa82b112b9c84',
            'name': '高能量_李翔'
        },
        {
            'id': '61dd99a47b29652ff572257b',
            'name': '起朱楼宴宾客_翁放'
        },
        {
            'id': '61358d971c5d56efe5bcb5d2',
            'name': '乱翻书_潘乱'
        },
        {
            'id': '61a3847fc9d6793ec50e0e65',
            'name': '正面连接_曾鸣'
        }
    ]
    
    output_dir = Path(__file__).parent.parent / "podcasts"
    limit = 10  # 每个播客下载10期
    
    all_downloaded = {}
    
    for podcast in podcasts:
        downloaded = download_podcast_episodes(
            podcast['id'],
            podcast['name'],
            limit=limit,
            output_dir=output_dir,
            skip_existing=True  # 跳过已下载的
        )
        all_downloaded[podcast['name']] = downloaded
        time.sleep(3)
    
    # 保存下载记录
    record_file = output_dir / "download_records.json"
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(all_downloaded, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 下载完成！记录已保存到: {record_file}")
    total = sum(len(eps) for eps in all_downloaded.values())
    print(f"总计下载: {total} 个音频文件")

if __name__ == "__main__":
    main()

