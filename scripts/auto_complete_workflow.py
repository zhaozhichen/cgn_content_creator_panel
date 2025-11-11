#!/usr/bin/env python3
"""
自动化完整工作流程
1. 监控转录进度
2. 转录完成后自动分析和更新
3. 确保所有后续工作自动进行
"""

import time
import subprocess
import sys
from pathlib import Path
import os

def check_transcription_status():
    """检查转录状态"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    total_audio = sum(1 for _ in podcasts_dir.rglob("*.mp3"))
    total_transcribed = sum(1 for f in transcriptions_dir.rglob("*.txt") if f.stat().st_size > 1024)
    
    return total_audio, total_transcribed

def wait_for_transcription(check_interval=300, max_wait_hours=48):
    """等待转录完成"""
    print("\n" + "=" * 60)
    print("等待转录完成")
    print("=" * 60)
    
    max_wait_seconds = max_wait_hours * 3600
    start_time = time.time()
    last_count = 0
    check_count = 0
    
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
        
        # 显示进度
        check_count += 1
        elapsed_min = int(elapsed // 60)
        elapsed_hr = elapsed_min // 60
        
        if total_transcribed > last_count:
            print(f"\n[{check_count}] 📈 进度更新: {total_transcribed}/{total_audio} ({progress:.1f}%)")
            print(f"    ⏱️  已等待: {elapsed_hr}小时{elapsed_min%60}分钟")
            last_count = total_transcribed
        elif check_count % 3 == 0:  # 每3次检查显示一次
            print(f"[{check_count}] ⏳ 转录中... {total_transcribed}/{total_audio} ({progress:.1f}%) | "
                  f"等待 {elapsed_hr}小时{elapsed_min%60}分钟")
        
        time.sleep(check_interval)
    
    return False

def run_script_safely(script_path, description, timeout=7200):
    """安全运行脚本"""
    print(f"\n{'='*60}")
    print(f"【执行】{description}")
    print(f"脚本: {script_path.name}")
    print("="*60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent.parent,
            timeout=timeout,
            capture_output=False
        )
        
        if result.returncode == 0:
            print(f"\n✅ {description} 完成")
            return True
        else:
            print(f"\n⚠️  {description} 完成（退出码: {result.returncode}）")
            return False
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  {description} 超时")
        return False
    except Exception as e:
        print(f"\n❌ {description} 出错: {e}")
        import traceback
        traceback.print_exc()
        return False

def run_analysis_and_update():
    """执行分析和更新流程"""
    print("\n" + "=" * 60)
    print("开始自动分析和更新")
    print("=" * 60)
    
    scripts_dir = Path(__file__).parent
    project_root = scripts_dir.parent
    
    # 任务列表
    tasks = [
        ("analyze_transcriptions.py", "重新分析所有40期转录文本", 7200),
        ("design_interview_questions.py", "更新访谈问题和大纲", 3600),
    ]
    
    results = {}
    
    for script_name, description, timeout in tasks:
        script_path = scripts_dir / script_name
        
        if not script_path.exists():
            print(f"\n⚠️  脚本不存在: {script_name}，跳过")
            results[script_name] = False
            continue
        
        success = run_script_safely(script_path, description, timeout)
        results[script_name] = success
        
        if success:
            time.sleep(3)  # 短暂休息
        else:
            print(f"\n⚠️  {description} 未完全成功，但继续执行...")
            time.sleep(2)
    
    return results

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("自动化完整工作流程")
    print("=" * 60)
    print("\n此脚本将：")
    print("1. 监控转录进度")
    print("2. 转录完成后自动分析所有40期转录文本")
    print("3. 自动更新访谈问题和大纲")
    print("4. 生成更新的研究笔记")
    print("\n开始执行...\n")
    
    # 检查当前状态
    total_audio, total_transcribed = check_transcription_status()
    print(f"\n📊 当前状态:")
    print(f"  音频文件: {total_audio} 个")
    print(f"  已转录: {total_transcribed} 个")
    print(f"  待转录: {total_audio - total_transcribed} 个")
    
    # 如果转录已完成，直接进行分析
    if total_transcribed >= total_audio:
        print("\n✅ 所有转录已完成，直接进行重新分析和更新")
        run_analysis_and_update()
    else:
        print(f"\n⏳ 等待转录完成...")
        if wait_for_transcription(check_interval=300, max_wait_hours=48):
            print("\n✅ 转录完成，开始自动分析和更新")
            run_analysis_and_update()
        else:
            print("\n⚠️  转录可能未完全完成，但仍继续分析和更新")
            run_analysis_and_update()
    
    # 最终总结
    print("\n" + "=" * 60)
    print("自动化工作流程完成")
    print("=" * 60)
    
    print("\n📁 请检查以下输出文件：")
    output_files = [
        "outputs/research_notes.md - 研究笔记（已更新）",
        "outputs/interview_outline.md - 访谈大纲（已更新）",
        "outputs/interview_questions.json - 访谈问题（已更新）",
        "research/host_insights_analysis.json - 详细分析结果",
        "research/host_insights_summary.md - 分析摘要"
    ]
    
    for file_desc in output_files:
        print(f"  - {file_desc}")
    
    print("\n" + "=" * 60)

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

