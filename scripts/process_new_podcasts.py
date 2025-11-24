#!/usr/bin/env python3
"""
处理新添加的播客（潘乱和曾鸣）的完整流程：
1. 转录音频（如果未完成）
2. 分析转录内容
3. 更新研究笔记和访谈大纲
"""

import os
import sys
import time
from pathlib import Path
import json

# 尝试从.env文件加载环境变量
def load_env_file():
    """从.env文件加载环境变量"""
    env_file = Path(__file__).parent.parent / ".env"
    if env_file.exists():
        with open(env_file, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip().strip('"').strip("'")

# 加载.env文件
load_env_file()

# 检查环境变量
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ 错误: 未设置 GEMINI_API_KEY 环境变量")
    print("   请设置: export GEMINI_API_KEY='your-api-key'")
    print("   或创建 .env 文件并添加: GEMINI_API_KEY=your-api-key")
    sys.exit(1)

def check_transcription_status():
    """检查转录状态"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    new_podcasts = {
        "乱翻书_潘乱": "潘乱",
        "正面连接_曾鸣": "曾鸣"
    }
    
    status = {}
    for podcast_dir, host_name in new_podcasts.items():
        audio_dir = podcasts_dir / podcast_dir
        trans_dir = transcriptions_dir / podcast_dir
        
        audio_count = len(list(audio_dir.glob("*.mp3"))) if audio_dir.exists() else 0
        trans_count = len(list(trans_dir.glob("*.txt"))) if trans_dir.exists() else 0
        
        status[podcast_dir] = {
            "host": host_name,
            "audio_files": audio_count,
            "transcribed": trans_count,
            "pending": audio_count - trans_count
        }
    
    return status

def transcribe_pending():
    """转录待处理的音频文件"""
    print("\n" + "=" * 60)
    print("步骤 1: 转录音频文件")
    print("=" * 60)
    
    # 导入转录脚本
    sys.path.insert(0, str(Path(__file__).parent))
    from transcribe_with_gemini import batch_transcribe
    
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    output_dir = Path(__file__).parent.parent / "transcriptions"
    
    # 只转录新播客
    new_podcasts = ["乱翻书_潘乱", "正面连接_曾鸣"]
    
    for podcast_name in new_podcasts:
        podcast_dir = podcasts_dir / podcast_name
        if not podcast_dir.exists():
            print(f"⚠️  播客目录不存在: {podcast_dir}")
            continue
        
        print(f"\n处理播客: {podcast_name}")
        batch_transcribe(podcast_dir, output_dir)

def analyze_new_podcasts():
    """分析新播客的转录内容"""
    print("\n" + "=" * 60)
    print("步骤 2: 分析转录内容")
    print("=" * 60)
    
    sys.path.insert(0, str(Path(__file__).parent))
    from analyze_transcriptions import batch_analyze
    
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    output_dir = Path(__file__).parent.parent / "research"
    
    # 分析所有转录文件（脚本会自动处理新播客）
    results = batch_analyze(transcriptions_dir, output_dir)
    
    return results

def update_research_notes():
    """更新研究笔记，整合新播客的分析结果"""
    print("\n" + "=" * 60)
    print("步骤 3: 更新研究笔记和访谈大纲")
    print("=" * 60)
    
    # 读取现有的分析结果
    analysis_file = Path(__file__).parent.parent / "research" / "host_insights_analysis.json"
    if not analysis_file.exists():
        print("⚠️  分析结果文件不存在，请先运行分析")
        return
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        all_analyses = json.load(f)
    
    # 检查是否有新播客的分析结果
    new_hosts = ["潘乱", "曾鸣"]
    has_new_data = False
    
    for host in new_hosts:
        # 查找包含该主播的分析
        for podcast_name, analysis in all_analyses.items():
            if host in podcast_name:
                print(f"✅ 找到 {host} 的分析数据: {podcast_name}")
                has_new_data = True
                break
    
    if not has_new_data:
        print("⚠️  未找到新播客的分析数据")
        return
    
    # 运行更新脚本
    sys.path.insert(0, str(Path(__file__).parent))
    
    # 更新研究笔记
    try:
        from complete_research_and_outline import main as update_main
        print("\n运行研究笔记更新...")
        update_main()
    except ImportError:
        print("⚠️  更新脚本不存在，需要手动更新研究笔记")
    
    # 更新访谈问题
    try:
        from design_interview_questions import main as questions_main
        print("\n运行访谈问题更新...")
        questions_main()
    except ImportError:
        print("⚠️  访谈问题脚本不存在，需要手动更新")

def main():
    """主函数"""
    print("=" * 60)
    print("处理新播客完整流程")
    print("=" * 60)
    print("\n新播客：")
    print("  - 潘乱（乱翻书）")
    print("  - 曾鸣（正面连接）")
    
    # 检查转录状态
    print("\n📊 检查当前状态...")
    status = check_transcription_status()
    
    for podcast, info in status.items():
        print(f"\n{podcast}:")
        print(f"  音频文件: {info['audio_files']}")
        print(f"  已转录: {info['transcribed']}")
        print(f"  待转录: {info['pending']}")
    
    # 检查是否需要转录
    total_pending = sum(info['pending'] for info in status.values())
    
    if total_pending > 0:
        print(f"\n⚠️  还有 {total_pending} 个文件待转录")
        print("开始转录...")
        transcribe_pending()
        
        # 等待转录完成
        print("\n等待转录完成...")
        max_wait = 7200  # 2小时
        wait_interval = 300  # 5分钟检查一次
        waited = 0
        
        while waited < max_wait:
            time.sleep(wait_interval)
            waited += wait_interval
            status = check_transcription_status()
            total_pending = sum(info['pending'] for info in status.values())
            
            if total_pending == 0:
                print("✅ 所有文件转录完成！")
                break
            else:
                print(f"⏳ 还有 {total_pending} 个文件待转录，继续等待...")
    else:
        print("\n✅ 所有文件已转录完成")
    
    # 分析转录内容
    print("\n开始分析转录内容...")
    analyze_new_podcasts()
    
    # 更新研究笔记和访谈大纲
    print("\n更新研究笔记和访谈大纲...")
    update_research_notes()
    
    print("\n" + "=" * 60)
    print("✅ 所有任务完成！")
    print("=" * 60)
    print("\n请检查以下文件：")
    print("  - research/host_insights_analysis.json")
    print("  - research/host_insights_summary.md")
    print("  - outputs/research_notes.md")
    print("  - outputs/interview_outline.md")
    print("  - outputs/interview_questions.json")

if __name__ == "__main__":
    main()

