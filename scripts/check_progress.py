#!/usr/bin/env python3
"""
检查新播客处理进度
"""

from pathlib import Path
import time
from datetime import datetime

def check_progress():
    """检查处理进度"""
    project_root = Path(__file__).parent.parent
    transcriptions_dir = project_root / "transcriptions"
    podcasts_dir = project_root / "podcasts"
    
    new_podcasts = {
        "乱翻书_潘乱": "潘乱",
        "正面连接_曾鸣": "曾鸣"
    }
    
    print("=" * 60)
    print(f"进度检查 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    total_audio = 0
    total_transcribed = 0
    
    for podcast_dir, host_name in new_podcasts.items():
        audio_dir = podcasts_dir / podcast_dir
        trans_dir = transcriptions_dir / podcast_dir
        
        audio_count = len(list(audio_dir.glob("*.mp3"))) if audio_dir.exists() else 0
        trans_count = len(list(trans_dir.glob("*.txt"))) if trans_dir.exists() else 0
        
        total_audio += audio_count
        total_transcribed += trans_count
        
        progress = (trans_count / audio_count * 100) if audio_count > 0 else 0
        
        print(f"{host_name} ({podcast_dir}):")
        print(f"  音频文件: {audio_count}")
        print(f"  已转录: {trans_count}")
        print(f"  进度: {progress:.1f}%")
        print()
    
    print(f"总计: {total_transcribed} / {total_audio} ({total_transcribed/total_audio*100 if total_audio > 0 else 0:.1f}%)")
    print()
    
    # 检查脚本是否运行
    import subprocess
    try:
        result = subprocess.run(
            ["pgrep", "-f", "process_new_podcasts"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("✅ 处理脚本正在运行")
        else:
            print("⚠️  处理脚本未运行")
    except:
        print("⚠️  无法检查脚本状态")
    
    print()
    
    # 检查是否有分析结果
    analysis_file = project_root / "research" / "host_insights_analysis.json"
    if analysis_file.exists():
        import json
        with open(analysis_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        has_new = False
        for podcast_name in new_podcasts.keys():
            if any(podcast_name in key for key in data.keys()):
                has_new = True
                break
        
        if has_new:
            print("✅ 已找到分析结果")
        else:
            print("⏳ 分析结果待生成")
    else:
        print("⏳ 分析结果待生成")
    
    print("=" * 60)
    
    return total_transcribed, total_audio

if __name__ == "__main__":
    check_progress()

