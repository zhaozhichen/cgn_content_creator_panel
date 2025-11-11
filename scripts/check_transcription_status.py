#!/usr/bin/env python3
"""
检查转录状态，并在完成后自动进行分析
"""

import time
from pathlib import Path

def check_transcription_status():
    """检查转录状态"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    # 统计音频文件
    audio_files = list(podcasts_dir.rglob("*.mp3"))
    total_count = len(audio_files)
    
    # 统计已完成的转录文件（大于1KB）
    transcription_files = list(transcriptions_dir.rglob("*.txt"))
    completed_count = sum(1 for f in transcription_files if f.stat().st_size > 1024)
    
    progress = (completed_count / total_count * 100) if total_count > 0 else 0
    
    return {
        'total': total_count,
        'completed': completed_count,
        'progress': progress,
        'remaining': total_count - completed_count
    }

def wait_for_completion(check_interval=300):  # 5分钟检查一次
    """等待转录完成"""
    print("等待所有转录完成...")
    print(f"检查间隔: {check_interval}秒（{check_interval//60}分钟）\n")
    
    while True:
        status = check_transcription_status()
        
        print(f"转录进度: {status['completed']}/{status['total']} ({status['progress']:.1f}%)")
        print(f"剩余文件: {status['remaining']} 个\n")
        
        if status['remaining'] == 0:
            print("✅ 所有转录已完成！")
            return True
        
        print(f"等待 {check_interval//60} 分钟后再次检查...\n")
        time.sleep(check_interval)

def main():
    """主函数"""
    print("=" * 60)
    print("转录状态检查工具")
    print("=" * 60)
    print()
    
    status = check_transcription_status()
    
    print(f"总音频文件: {status['total']} 个")
    print(f"已完成转录: {status['completed']} 个")
    print(f"剩余文件: {status['remaining']} 个")
    print(f"完成进度: {status['progress']:.1f}%\n")
    
    if status['remaining'] == 0:
        print("✅ 所有转录已完成！")
        print("\n可以运行分析脚本:")
        print("  python3 scripts/analyze_transcriptions.py")
        return
    
    print("转录仍在进行中...")
    print("\n选择操作:")
    print("1. 退出（稍后手动检查）")
    print("2. 等待所有转录完成（每5分钟检查一次）")
    
    choice = input("\n请输入选择 (1/2): ").strip()
    
    if choice == '2':
        wait_for_completion()
        print("\n✅ 转录完成！可以开始分析了。")
        print("运行: python3 scripts/analyze_transcriptions.py")

if __name__ == "__main__":
    main()

