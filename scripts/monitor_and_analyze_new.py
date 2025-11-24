#!/usr/bin/env python3
"""
监控新播客转录进度，完成后自动执行分析步骤
"""

import os
import sys
import time
import subprocess
from pathlib import Path
from datetime import datetime

# 从.env文件加载
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

def check_transcription_complete():
    """检查转录是否完成"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    new_podcasts = {
        "乱翻书_潘乱": "潘乱",
        "正面连接_曾鸣": "曾鸣"
    }
    
    total_audio = 0
    total_transcribed = 0
    status = {}
    
    for podcast_dir, host_name in new_podcasts.items():
        audio_dir = podcasts_dir / podcast_dir
        trans_dir = transcriptions_dir / podcast_dir
        
        audio_count = len(list(audio_dir.glob("*.mp3"))) if audio_dir.exists() else 0
        trans_count = len(list(trans_dir.glob("*.txt"))) if trans_dir.exists() else 0
        
        total_audio += audio_count
        total_transcribed += trans_count
        
        status[podcast_dir] = {
            'audio': audio_count,
            'transcribed': trans_count,
            'pending': audio_count - trans_count
        }
    
    return total_transcribed >= total_audio and total_audio > 0, total_transcribed, total_audio, status

def run_analysis_steps():
    """执行分析步骤"""
    print("\n" + "=" * 60)
    print("开始执行分析步骤")
    print("=" * 60)
    
    scripts_dir = Path(__file__).parent
    project_root = scripts_dir.parent
    
    # 步骤1: 分析转录内容
    print("\n【步骤 1】分析转录内容")
    print("-" * 60)
    try:
        script_path = scripts_dir / "analyze_transcriptions.py"
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=project_root,
            timeout=3600  # 最多1小时
        )
        if result.returncode == 0:
            print("✅ 分析完成")
        else:
            print(f"⚠️  分析完成（退出码: {result.returncode}）")
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return False
    
    # 步骤2: 更新研究笔记
    print("\n【步骤 2】更新研究笔记")
    print("-" * 60)
    try:
        script_path = scripts_dir / "complete_research_and_outline.py"
        if script_path.exists():
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=project_root,
                timeout=1800  # 最多30分钟
            )
            if result.returncode == 0:
                print("✅ 研究笔记更新完成")
            else:
                print(f"⚠️  研究笔记更新完成（退出码: {result.returncode}）")
        else:
            print("⚠️  研究笔记更新脚本不存在")
    except Exception as e:
        print(f"⚠️  研究笔记更新失败: {e}")
    
    # 步骤3: 更新访谈问题
    print("\n【步骤 3】更新访谈问题和大纲")
    print("-" * 60)
    try:
        script_path = scripts_dir / "design_interview_questions.py"
        if script_path.exists():
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=project_root,
                timeout=1800  # 最多30分钟
            )
            if result.returncode == 0:
                print("✅ 访谈问题更新完成")
            else:
                print(f"⚠️  访谈问题更新完成（退出码: {result.returncode}）")
        else:
            print("⚠️  访谈问题脚本不存在")
    except Exception as e:
        print(f"⚠️  访谈问题更新失败: {e}")
    
    print("\n" + "=" * 60)
    print("✅ 所有分析步骤完成！")
    print("=" * 60)
    print("\n请检查以下文件：")
    print("  - research/host_insights_analysis.json")
    print("  - research/host_insights_summary.md")
    print("  - outputs/research_notes.md")
    print("  - outputs/interview_outline.md")
    print("  - outputs/interview_questions.json")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("监控新播客转录并执行分析")
    print("=" * 60)
    
    check_interval = 300  # 5分钟检查一次
    max_wait = 14400  # 最多等待4小时
    
    start_time = time.time()
    last_status = None
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait:
            print(f"\n⏱️  等待超时（{max_wait//3600}小时），检查当前状态...")
            break
        
        complete, transcribed, total, status = check_transcription_complete()
        progress = (transcribed / total * 100) if total > 0 else 0
        
        # 显示进度
        status_str = f"{transcribed}/{total} ({progress:.1f}%)"
        if status_str != last_status:
            print(f"\n[{datetime.now().strftime('%H:%M:%S')}] 转录进度: {status_str}")
            for podcast, info in status.items():
                print(f"  {podcast}: {info['transcribed']}/{info['audio']}")
            last_status = status_str
        
        if complete:
            print(f"\n✅ 转录完成！({transcribed}/{total})")
            print("开始执行分析步骤...")
            run_analysis_steps()
            break
        
        # 等待下次检查
        elapsed_min = elapsed // 60
        print(f"⏳ 等待中... 已等待 {elapsed_min} 分钟 | 下次检查: {check_interval//60} 分钟后")
        time.sleep(check_interval)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 执行出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

