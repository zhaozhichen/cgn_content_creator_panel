#!/usr/bin/env python3
"""
确保转录完成后执行分析步骤
"""

import os
import sys
import time
from pathlib import Path

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
    
    for podcast_dir, host_name in new_podcasts.items():
        audio_dir = podcasts_dir / podcast_dir
        trans_dir = transcriptions_dir / podcast_dir
        
        audio_count = len(list(audio_dir.glob("*.mp3"))) if audio_dir.exists() else 0
        trans_count = len(list(trans_dir.glob("*.txt"))) if trans_dir.exists() else 0
        
        total_audio += audio_count
        total_transcribed += trans_count
    
    return total_transcribed >= total_audio and total_audio > 0, total_transcribed, total_audio

def run_analysis_steps():
    """执行分析步骤"""
    print("=" * 60)
    print("开始执行分析步骤")
    print("=" * 60)
    
    sys.path.insert(0, str(Path(__file__).parent))
    
    # 步骤1: 分析转录内容
    print("\n步骤 1: 分析转录内容")
    try:
        from analyze_transcriptions import batch_analyze
        transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
        output_dir = Path(__file__).parent.parent / "research"
        results = batch_analyze(transcriptions_dir, output_dir)
        print("✅ 分析完成")
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return False
    
    # 步骤2: 更新研究笔记
    print("\n步骤 2: 更新研究笔记")
    try:
        from complete_research_and_outline import main as update_main
        update_main()
        print("✅ 研究笔记更新完成")
    except ImportError:
        print("⚠️  研究笔记更新脚本不存在")
    except Exception as e:
        print(f"⚠️  研究笔记更新失败: {e}")
    
    # 步骤3: 更新访谈问题
    print("\n步骤 3: 更新访谈问题和大纲")
    try:
        from design_interview_questions import main as questions_main
        questions_main()
        print("✅ 访谈问题更新完成")
    except ImportError:
        print("⚠️  访谈问题脚本不存在")
    except Exception as e:
        print(f"⚠️  访谈问题更新失败: {e}")
    
    return True

def main():
    """主函数"""
    print("=" * 60)
    print("确保分析步骤执行")
    print("=" * 60)
    
    # 检查转录是否完成
    complete, transcribed, total = check_transcription_complete()
    
    print(f"\n转录状态: {transcribed}/{total}")
    
    if complete:
        print("✅ 转录已完成，开始执行分析步骤...")
        run_analysis_steps()
    else:
        print(f"⏳ 转录未完成 ({transcribed}/{total})，等待中...")
        print("请等待转录完成后运行此脚本")

if __name__ == "__main__":
    main()
