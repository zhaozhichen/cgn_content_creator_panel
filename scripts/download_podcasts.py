#!/usr/bin/env python3
"""
小宇宙播客下载脚本
下载指定播客的最近N期音频文件
"""

import requests
import json
import os
import sys
from pathlib import Path
from typing import List, Dict
import time

# 小宇宙API端点（需要根据实际情况调整）
XIAOYUZHOU_API_BASE = "https://www.xiaoyuzhoufm.com/api"

def get_podcast_info(podcast_id: str) -> Dict:
    """获取播客基本信息"""
    url = f"{XIAOYUZHOU_API_BASE}/podcast/{podcast_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"获取播客信息失败: {e}")
        return None

def get_episodes(podcast_id: str, limit: int = 3) -> List[Dict]:
    """获取播客的最近N期单集"""
    # 尝试不同的API端点
    endpoints = [
        f"{XIAOYUZHOU_API_BASE}/podcast/{podcast_id}/episodes?limit={limit}",
        f"https://www.xiaoyuzhoufm.com/app/api/v1/podcast/{podcast_id}/episodes?limit={limit}",
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json",
        "Referer": f"https://www.xiaoyuzhoufm.com/podcast/{podcast_id}"
    }
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # 尝试解析不同可能的响应格式
                if isinstance(data, dict):
                    if 'data' in data:
                        episodes = data['data']
                        if isinstance(episodes, list):
                            return episodes[:limit]
                    if 'episodes' in data:
                        return data['episodes'][:limit]
                elif isinstance(data, list):
                    return data[:limit]
        except Exception as e:
            print(f"尝试端点 {endpoint} 失败: {e}")
            continue
    
    # 如果API都失败，尝试从HTML页面解析
    print(f"API获取失败，尝试从网页解析...")
    return parse_episodes_from_html(podcast_id, limit)

def parse_episodes_from_html(podcast_id: str, limit: int) -> List[Dict]:
    """从HTML页面解析单集信息（备用方案）"""
    url = f"https://www.xiaoyuzhoufm.com/podcast/{podcast_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # 查找JSON数据（通常在<script>标签中）
        import re
        # 尝试找到包含单集数据的JSON
        json_pattern = r'window\.__INITIAL_STATE__\s*=\s*({.+?});'
        match = re.search(json_pattern, html)
        
        if match:
            data = json.loads(match.group(1))
            # 根据实际数据结构提取单集
            # 这里需要根据实际页面结构调整
            
        # 简单解析：查找单集链接
        episode_pattern = r'href="(/episode/[^"]+)"'
        episodes = re.findall(episode_pattern, html)
        
        result = []
        for ep_link in episodes[:limit]:
            ep_id = ep_link.split('/')[-1]
            result.append({
                'episode_id': ep_id,
                'episode_link': f"https://www.xiaoyuzhoufm.com{ep_link}"
            })
        return result
    except Exception as e:
        print(f"从HTML解析失败: {e}")
        return []

def get_episode_audio_url(episode_id: str) -> str:
    """获取单集的音频下载链接"""
    endpoints = [
        f"{XIAOYUZHOU_API_BASE}/episode/{episode_id}",
        f"https://www.xiaoyuzhoufm.com/app/api/v1/episode/{episode_id}",
        f"https://www.xiaoyuzhoufm.com/episode/{episode_id}"
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Accept": "application/json"
    }
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, headers=headers, timeout=10)
            if response.status_code == 200:
                data = response.json()
                # 尝试多种可能的数据结构
                audio_url = None
                if isinstance(data, dict):
                    if 'audio' in data:
                        audio_url = data['audio']
                    elif 'audioUrl' in data:
                        audio_url = data['audioUrl']
                    elif 'data' in data and 'audio' in data['data']:
                        audio_url = data['data']['audio']
                
                if audio_url:
                    return audio_url
        except:
            continue
    
    return None

def download_audio(url: str, output_path: Path) -> bool:
    """下载音频文件"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Referer": "https://www.xiaoyuzhoufm.com/"
    }
    
    try:
        response = requests.get(url, headers=headers, stream=True, timeout=30)
        response.raise_for_status()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False

def download_podcast_episodes(podcast_id: str, podcast_name: str, limit: int = 3, output_dir: Path = None):
    """下载播客的最近N期"""
    if output_dir is None:
        output_dir = Path("podcasts")
    
    output_dir = Path(output_dir) / podcast_name
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n开始下载播客: {podcast_name} (ID: {podcast_id})")
    print(f"目标: 最近 {limit} 期")
    
    # 获取单集列表
    episodes = get_episodes(podcast_id, limit)
    
    if not episodes:
        print(f"⚠️  无法获取单集列表，请手动检查播客链接")
        return []
    
    print(f"找到 {len(episodes)} 期单集")
    
    downloaded = []
    for i, episode in enumerate(episodes, 1):
        ep_id = episode.get('episode_id') or episode.get('id') or episode.get('eid')
        ep_title = episode.get('title') or episode.get('episode_title') or f"Episode_{ep_id}"
        
        # 清理文件名
        ep_title = "".join(c for c in ep_title if c.isalnum() or c in (' ', '-', '_')).strip()
        ep_title = ep_title.replace(' ', '_')[:50]  # 限制长度
        
        print(f"\n[{i}/{len(episodes)}] 处理单集: {ep_title}")
        
        # 获取音频URL
        audio_url = get_episode_audio_url(ep_id)
        
        if not audio_url:
            # 如果API获取失败，尝试从单集页面解析
            ep_link = episode.get('episode_link') or f"https://www.xiaoyuzhoufm.com/episode/{ep_id}"
            audio_url = parse_audio_from_episode_page(ep_link)
        
        if not audio_url:
            print(f"  ⚠️  无法获取音频URL")
            continue
        
        print(f"  音频URL: {audio_url[:80]}...")
        
        # 下载音频
        output_file = output_dir / f"{i:02d}_{ep_title}.mp3"
        if download_audio(audio_url, output_file):
            print(f"  ✅ 下载成功: {output_file.name}")
            downloaded.append({
                'episode_id': ep_id,
                'title': ep_title,
                'audio_file': str(output_file),
                'audio_url': audio_url
            })
        else:
            print(f"  ❌ 下载失败")
        
        time.sleep(1)  # 避免请求过快
    
    return downloaded

def parse_audio_from_episode_page(episode_url: str) -> str:
    """从单集页面解析音频URL（备用方案）"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    }
    
    try:
        response = requests.get(episode_url, headers=headers, timeout=10)
        response.raise_for_status()
        html = response.text
        
        # 查找音频URL的模式
        import re
        patterns = [
            r'"audioUrl"\s*:\s*"([^"]+)"',
            r'audio.*?src="([^"]+\.mp3[^"]*)"',
            r'https://[^"]+\.mp3[^"]*'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, html)
            for match in matches:
                if '.mp3' in match or 'audio' in match.lower():
                    return match.strip('"')
    except:
        pass
    
    return None

def main():
    """主函数"""
    # 播客配置
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
        }
    ]
    
    output_dir = Path(__file__).parent.parent / "podcasts"
    limit = 3  # 每播客下载3期
    
    all_downloaded = {}
    
    for podcast in podcasts:
        downloaded = download_podcast_episodes(
            podcast['id'],
            podcast['name'],
            limit=limit,
            output_dir=output_dir
        )
        all_downloaded[podcast['name']] = downloaded
        time.sleep(2)  # 播客之间稍作延迟
    
    # 保存下载记录
    record_file = output_dir / "download_records.json"
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(all_downloaded, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 下载完成！记录已保存到: {record_file}")
    print(f"总计下载: {sum(len(eps) for eps in all_downloaded.values())} 个音频文件")

if __name__ == "__main__":
    main()

