#!/usr/bin/env python3
"""
下载曾鸣的采访播客单集
"""

import json
import re
import time
from pathlib import Path
from urllib.request import urlopen, Request

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
        with urlopen(req, timeout=30) as response:
            return response.read()
    except Exception as e:
        print(f"HTTP请求失败: {e}")
        return None

def get_episode_audio_url(episode_id: str) -> str:
    """获取单集的音频URL"""
    url = f"https://www.xiaoyuzhoufm.com/episode/{episode_id}"
    print(f"正在获取单集页面: {url}")
    
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
                audio_url = match.strip('"').strip("'")
                print(f"找到音频URL: {audio_url[:80]}...")
                return audio_url
    
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
        print(f"正在下载音频...")
        data = http_get(url, headers)
        if data:
            output_path.parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(data)
            file_size = output_path.stat().st_size / (1024 * 1024)
            print(f"✅ 下载成功 ({file_size:.1f}MB): {output_path}")
            return True
    except Exception as e:
        print(f"❌ 下载失败: {e}")
    
    return False

def main():
    """主函数"""
    episode_id = "617fa8e8e93949169b018042"
    episode_title = "面对复杂_通过非虚构写作与社会正面连接_新闻实验室17"
    
    output_dir = Path(__file__).parent.parent / "podcasts" / "曾鸣_采访"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 检查是否已下载
    existing_files = list(output_dir.glob("*.mp3"))
    if existing_files:
        print(f"✅ 音频文件已存在: {existing_files[0]}")
        return str(existing_files[0])
    
    # 获取音频URL
    audio_url = get_episode_audio_url(episode_id)
    
    if not audio_url:
        print("❌ 无法获取音频URL")
        return None
    
    # 下载音频
    output_file = output_dir / f"{episode_title}.mp3"
    if download_audio(audio_url, output_file):
        return str(output_file)
    else:
        return None

if __name__ == "__main__":
    main()

