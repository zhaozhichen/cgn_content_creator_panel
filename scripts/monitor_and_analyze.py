#!/usr/bin/env python3
"""
监控转录进度，转录完成后自动进行重新分析和更新
"""

import time
import subprocess
import sys
from pathlib import Path

def check_transcription_status():
    """检查转录状态"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    total_audio = sum(1 for _ in podcasts_dir.rglob("*.mp3"))
    total_transcribed = sum(1 for f in transcriptions_dir.rglob("*.txt") if f.stat().st_size > 1024)
    
    return total_audio, total_transcribed

def wait_for_transcription_completion(check_interval=300, max_wait_hours=48):
    """等待转录完成"""
    print("\n" + "=" * 60)
    print("等待转录完成")
    print("=" * 60)
    
    max_wait_seconds = max_wait_hours * 3600
    start_time = time.time()
    last_count = 0
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait_seconds:
            print(f"\n⏱️  等待超时（{max_wait_hours}小时），继续执行...")
            break
        
        total_audio, total_transcribed = check_transcription_status()
        progress = (total_transcribed / total_audio * 100) if total_audio > 0 else 0
        
        if total_transcribed >= total_audio:
            print(f"\n✅ 转录完成！({total_transcribed}/{total_audio})")
            return True
        
        # 显示进度变化
        if total_transcribed > last_count:
            print(f"\n📈 进度更新: {total_transcribed}/{total_audio} ({progress:.1f}%)")
            last_count = total_transcribed
        else:
            elapsed_min = elapsed // 60
            print(f"⏳ 转录中... {total_transcribed}/{total_audio} ({progress:.1f}%) | "
                  f"已等待 {elapsed_min} 分钟 | 下次检查: {check_interval//60} 分钟后")
        
        time.sleep(check_interval)
    
    return False

def run_analysis_and_update():
    """运行分析和更新流程"""
    print("\n" + "=" * 60)
    print("开始重新分析和更新")
    print("=" * 60)
    
    scripts_dir = Path(__file__).parent
    project_root = scripts_dir.parent
    
    scripts = [
        ("analyze_transcriptions.py", "重新分析所有转录文本"),
        ("design_interview_questions.py", "更新访谈问题和大纲"),
    ]
    
    for script_name, description in scripts:
        script_path = scripts_dir / script_name
        
        if not script_path.exists():
            print(f"\n⚠️  脚本不存在: {script_name}")
            continue
        
        print(f"\n【执行】{description}")
        print(f"脚本: {script_name}")
        
        try:
            result = subprocess.run(
                [sys.executable, str(script_path)],
                cwd=project_root,
                timeout=7200  # 最多2小时
            )
            
            if result.returncode == 0:
                print(f"✅ {description} 完成")
            else:
                print(f"⚠️  {description} 完成（退出码: {result.returncode}）")
        except subprocess.TimeoutExpired:
            print(f"⏱️  {description} 超时")
        except Exception as e:
            print(f"❌ {description} 出错: {e}")
        
        time.sleep(2)

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("转录监控和自动分析脚本")
    print("=" * 60)
    
    # 检查当前状态
    total_audio, total_transcribed = check_transcription_status()
    print(f"\n当前状态:")
    print(f"  音频文件: {total_audio} 个")
    print(f"  已转录: {total_transcribed} 个")
    print(f"  待转录: {total_audio - total_transcribed} 个")
    
    if total_transcribed >= total_audio:
        print("\n✅ 所有转录已完成，直接进行重新分析和更新")
        run_analysis_and_update()
    else:
        print(f"\n⏳ 等待转录完成...")
        if wait_for_transcription_completion(check_interval=300, max_wait_hours=24):
            print("\n✅ 转录完成，开始重新分析和更新")
            run_analysis_and_update()
        else:
            print("\n⚠️  转录未完全完成，但仍继续分析和更新")
            run_analysis_and_update()
    
    print("\n" + "=" * 60)
    print("处理完成")
    print("=" * 60)
    print("\n请检查以下输出文件：")
    print("- outputs/research_notes.md - 研究笔记（已更新）")
    print("- outputs/interview_outline.md - 访谈大纲（已更新）")
    print("- outputs/interview_questions.json - 访谈问题（已更新）")
    print("=" * 60)

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

