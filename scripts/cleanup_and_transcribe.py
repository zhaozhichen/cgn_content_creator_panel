#!/usr/bin/env python3
"""
清理多余的音频文件，只保留每个播客最新的10个
然后转录剩余的音频文件
"""

import os
from pathlib import Path
import subprocess
import sys

def cleanup_excess_files(podcasts_dir: Path, limit: int = 10):
    """清理每个播客目录中多余的音频文件，只保留最新的N个"""
    print("=" * 60)
    print("清理多余的音频文件")
    print("=" * 60)
    
    for podcast_dir in podcasts_dir.iterdir():
        if not podcast_dir.is_dir():
            continue
        
        podcast_name = podcast_dir.name
        audio_files = sorted(
            podcast_dir.glob("*.mp3"),
            key=lambda f: f.stat().st_mtime,
            reverse=True  # 最新的在前
        )
        
        if len(audio_files) <= limit:
            print(f"\n{podcast_name}: {len(audio_files)} 个文件（不需要清理）")
            continue
        
        print(f"\n{podcast_name}: {len(audio_files)} 个文件，保留最新的 {limit} 个")
        
        # 删除多余的旧文件
        for old_file in audio_files[limit:]:
            print(f"  删除: {old_file.name}")
            old_file.unlink()
        
        print(f"  ✅ 清理完成，保留 {len(list(podcast_dir.glob('*.mp3')))} 个文件")

def check_transcription_status(podcasts_dir: Path, transcriptions_dir: Path):
    """检查转录状态"""
    print("\n" + "=" * 60)
    print("检查转录状态")
    print("=" * 60)
    
    for podcast_dir in podcasts_dir.iterdir():
        if not podcast_dir.is_dir():
            continue
        
        podcast_name = podcast_dir.name
        audio_files = list(podcast_dir.glob("*.mp3"))
        
        # 找到对应的转录目录
        transcription_podcast_dir = transcriptions_dir / podcast_name.replace('_', '_').replace(' ', '_')
        # 尝试不同的目录名格式
        possible_names = [
            podcast_name,
            podcast_name.replace('_', '_'),
            podcast_name.replace(' ', '_'),
        ]
        
        transcription_dir = None
        for name in possible_names:
            test_dir = transcriptions_dir / name
            if test_dir.exists():
                transcription_dir = test_dir
                break
        
        transcribed_count = 0
        if transcription_dir and transcription_dir.exists():
            transcribed_files = [f for f in transcription_dir.glob("*.txt") if f.stat().st_size > 1024]
            transcribed_count = len(transcribed_files)
        
        audio_count = len(audio_files)
        remaining = audio_count - transcribed_count
        
        print(f"\n{podcast_name}:")
        print(f"  音频文件: {audio_count} 个")
        print(f"  已转录: {transcribed_count} 个")
        print(f"  待转录: {remaining} 个")
        
        if remaining > 0:
            print(f"  ⏳ 需要转录 {remaining} 个文件")

def main():
    """主函数"""
    project_root = Path(__file__).parent.parent
    podcasts_dir = project_root / "podcasts"
    transcriptions_dir = project_root / "transcriptions"
    
    # 步骤1: 清理多余的音频文件
    print("\n【步骤1】清理多余的音频文件")
    cleanup_excess_files(podcasts_dir, limit=10)
    
    # 步骤2: 检查转录状态
    print("\n【步骤2】检查转录状态")
    check_transcription_status(podcasts_dir, transcriptions_dir)
    
    # 步骤3: 启动转录
    print("\n【步骤3】启动转录进程")
    print("运行转录脚本...")
    
    transcribe_script = project_root / "scripts" / "transcribe_with_gemini.py"
    if transcribe_script.exists():
        print(f"  ✅ 转录脚本存在: {transcribe_script}")
        print("  建议在后台运行: python3 scripts/transcribe_with_gemini.py")
    else:
        print(f"  ❌ 转录脚本不存在")

if __name__ == "__main__":
    main()

