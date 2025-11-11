#!/usr/bin/env python3
"""
处理所有10期播客的完整流程
1. 清理多余文件
2. 转录所有未转录的音频
3. 重新分析所有转录文本
4. 更新嘉宾信息和访谈问题
"""

import subprocess
import sys
import time
from pathlib import Path

def run_script(script_name, description):
    """运行Python脚本"""
    script_path = Path(__file__).parent / script_name
    
    if not script_path.exists():
        print(f"⚠️  脚本不存在: {script_name}")
        return False
    
    print("\n" + "=" * 60)
    print(f"执行: {description}")
    print(f"脚本: {script_name}")
    print("=" * 60)
    
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=script_path.parent.parent,
            capture_output=False,
            timeout=7200  # 最多2小时
        )
        
        if result.returncode == 0:
            print(f"\n✅ {description} 完成")
            return True
        else:
            print(f"\n❌ {description} 失败 (退出码: {result.returncode})")
            return False
    except subprocess.TimeoutExpired:
        print(f"\n⏱️  {description} 超时")
        return False
    except Exception as e:
        print(f"\n❌ {description} 出错: {e}")
        return False

def wait_for_transcription(check_interval=300, max_wait_time=86400):
    """等待转录完成（最多24小时）"""
    print("\n等待所有转录完成...")
    print(f"检查间隔: {check_interval}秒（{check_interval//60}分钟）\n")
    
    from pathlib import Path
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    start_time = time.time()
    last_completed = 0
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait_time:
            print(f"\n⏱️  等待超时（{max_wait_time//3600}小时），继续执行...")
            break
        
        # 统计总音频和已转录文件
        total_audio = sum(1 for _ in podcasts_dir.rglob("*.mp3"))
        total_transcribed = sum(1 for f in transcriptions_dir.rglob("*.txt") if f.stat().st_size > 1024)
        
        if total_transcribed >= total_audio:
            print(f"\n✅ 转录完成！({total_transcribed}/{total_audio})")
            return True
        
        # 显示进度变化
        if total_transcribed > last_completed:
            print(f"\n📈 进度更新: {total_transcribed}/{total_audio} ({total_transcribed/total_audio*100:.1f}%)")
            last_completed = total_transcribed
        else:
            print(f"⏳ 转录中... {total_transcribed}/{total_audio} ({total_transcribed/total_audio*100:.1f}%) | "
                  f"等待 {check_interval//60} 分钟...")
        
        time.sleep(check_interval)
    
    return False

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("处理所有10期播客 - 完整流程")
    print("=" * 60)
    print("\n将执行以下任务：")
    print("1. 清理多余的音频文件（保留每个播客最新的10个）")
    print("2. 转录所有未转录的音频文件")
    print("3. 重新分析所有10期转录文本（Gemini API）")
    print("4. 更新嘉宾信息和研究笔记")
    print("5. 更新访谈问题和大纲")
    print("\n开始执行...\n")
    
    # 步骤1: 清理多余文件
    print("\n【任务1/5】清理多余的音频文件")
    run_script("cleanup_and_transcribe.py", "清理多余文件")
    
    # 步骤2: 启动转录（如果还没有完成）
    print("\n【任务2/5】转录所有未转录的音频")
    print("检查转录状态...")
    
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    total_audio = sum(1 for _ in podcasts_dir.rglob("*.mp3"))
    total_transcribed = sum(1 for f in transcriptions_dir.rglob("*.txt") if f.stat().st_size > 1024)
    
    print(f"  音频文件: {total_audio} 个")
    print(f"  已转录: {total_transcribed} 个")
    print(f"  待转录: {total_audio - total_transcribed} 个")
    
    if total_transcribed < total_audio:
        print("\n  ⏳ 转录仍在进行中，等待完成...")
        wait_for_transcription(check_interval=300)
    else:
        print("\n  ✅ 所有转录已完成")
    
    # 步骤3: 重新分析所有转录文本
    print("\n【任务3/5】重新分析所有转录文本")
    if run_script("analyze_transcriptions.py", "分析转录文本"):
        time.sleep(2)
    else:
        print("⚠️  分析失败，但继续执行...")
    
    # 步骤4: 更新嘉宾信息
    print("\n【任务4/5】更新嘉宾信息和研究笔记")
    print("（分析结果已包含在研究笔记中）")
    
    # 步骤5: 更新访谈问题和大纲
    print("\n【任务5/5】更新访谈问题和大纲")
    if run_script("design_interview_questions.py", "设计访谈问题"):
        print("\n✅ 所有任务完成！")
    else:
        print("\n⚠️  部分任务可能未完成，请检查输出")
    
    print("\n" + "=" * 60)
    print("处理流程结束")
    print("=" * 60)
    print("\n请检查以下目录的输出：")
    print("- research/host_insights_analysis.json - 详细分析结果")
    print("- research/host_insights_summary.md - 分析摘要")
    print("- outputs/research_notes.md - 研究笔记")
    print("- outputs/interview_outline.md - 访谈大纲")
    print("- outputs/interview_questions.json - 访谈问题")
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

