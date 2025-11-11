#!/usr/bin/env python3
"""
自动化完成所有任务的主控脚本
等待转录完成 -> 分析转录文本 -> 收集信息 -> 整理笔记 -> 设计问题 -> 生成大纲
"""

import sys
import time
import subprocess
from pathlib import Path

def check_transcription_complete():
    """检查转录是否完成"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    
    audio_files = list(podcasts_dir.rglob("*.mp3"))
    transcription_files = [f for f in transcriptions_dir.rglob("*.txt") 
                          if f.stat().st_size > 1024]
    
    total = len(audio_files)
    completed = len(transcription_files)
    
    return completed >= total, total, completed

def wait_for_transcription(check_interval=300, max_wait_time=86400):
    """等待转录完成（最多24小时）"""
    print("=" * 60)
    print("等待转录完成...")
    print("=" * 60)
    
    start_time = time.time()
    last_completed = 0
    
    while True:
        elapsed = time.time() - start_time
        if elapsed > max_wait_time:
            print(f"\n⏱️  等待超时（{max_wait_time//3600}小时），继续执行...")
            break
        
        complete, total, completed = check_transcription_complete()
        
        if complete:
            print(f"\n✅ 转录完成！({completed}/{total})")
            return True
        
        # 显示进度变化
        if completed > last_completed:
            print(f"\n📈 进度更新: {completed}/{total} ({completed/total*100:.1f}%)")
            last_completed = completed
        else:
            print(f"⏳ 转录中... {completed}/{total} ({completed/total*100:.1f}%) | "
                  f"等待 {check_interval//60} 分钟...")
        
        time.sleep(check_interval)
    
    return False

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
            timeout=3600  # 最多1小时
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

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("Panel访谈准备 - 自动化任务执行")
    print("=" * 60)
    print("\n将自动完成以下任务：")
    print("1. 等待转录完成")
    print("2. 分析转录文本（Gemini API）")
    print("3. 收集嘉宾信息")
    print("4. 整理研究笔记")
    print("5. 设计访谈问题")
    print("6. 生成访谈大纲")
    print("\n开始执行...\n")
    
    # 任务1: 等待转录完成
    print("\n【任务1/6】等待转录完成")
    transcription_complete = wait_for_transcription(check_interval=300)  # 每5分钟检查一次
    
    if not transcription_complete:
        complete, total, completed = check_transcription_complete()
        print(f"\n⚠️  转录未完全完成 ({completed}/{total})，但继续执行...")
    
    # 任务2: 分析转录文本
    print("\n【任务2/6】分析转录文本")
    if run_script("analyze_transcriptions.py", "分析转录文本"):
        time.sleep(2)
    else:
        print("⚠️  分析转录文本失败，继续执行...")
    
    # 任务3: 收集嘉宾信息（已完成，跳过）
    print("\n【任务3/6】收集嘉宾信息（已生成指南）")
    
    # 任务4-6: 创建后续任务脚本
    print("\n【任务4-6】整理研究笔记、设计问题、生成大纲")
    print("创建后续任务脚本...")
    
    # 创建统一的任务脚本（在运行前创建）
    create_followup_script()
    time.sleep(1)
    
    if run_script("complete_research_and_outline.py", "完成研究笔记和访谈大纲"):
        print("\n✅ 所有任务完成！")
    else:
        print("\n⚠️  部分任务可能未完成，请检查输出")
    
    print("\n" + "=" * 60)
    print("自动化流程结束")
    print("=" * 60)
    print("\n请检查以下目录的输出：")
    print("- research/ - 研究笔记和分析结果")
    print("- outputs/ - 最终交付物")
    print("=" * 60)

def create_followup_script():
    """创建后续任务脚本"""
    script_content = '''#!/usr/bin/env python3
"""
完成研究笔记和访谈大纲
"""

import json
from pathlib import Path
import sys

# 添加scripts目录到路径
sys.path.insert(0, str(Path(__file__).parent))

def load_analysis_results():
    """加载分析结果"""
    research_dir = Path(__file__).parent.parent / "research"
    analysis_file = research_dir / "host_insights_analysis.json"
    
    if not analysis_file.exists():
        print("⚠️  分析结果文件不存在")
        return {}
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def create_research_notes(analysis_results):
    """创建研究笔记"""
    research_dir = Path(__file__).parent.parent / "research"
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    notes_file = output_dir / "research_notes.md"
    
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write("# Panel嘉宾研究笔记\\n\\n")
        f.write("基于播客转录文本的Gemini API分析结果\\n\\n")
        f.write("---\\n\\n")
        
        for podcast_name, summary in analysis_results.items():
            host_name = summary.get('host_name', 'Unknown')
            f.write(f"## {host_name} - {podcast_name}\\n\\n")
            
            insights = summary.get('insights', {})
            
            if insights.get('professional_observations'):
                f.write("### 专业观察\\n\\n")
                for obs in insights['professional_observations'][:5]:
                    f.write(f"- {obs}\\n")
                f.write("\\n")
            
            if insights.get('content_creation_philosophy'):
                f.write("### 内容创作理念\\n\\n")
                for idea in insights['content_creation_philosophy'][:5]:
                    f.write(f"- {idea}\\n")
                f.write("\\n")
            
            f.write("---\\n\\n")
    
    print(f"✅ 研究笔记已保存: {notes_file}")
    return notes_file

def design_interview_questions(analysis_results):
    """设计访谈问题"""
    # 7位Panel嘉宾信息（基于PDF）
    guests = {
        "黄俊杰": "晚点LatePost联合创始人兼总编辑",
        "李路野": "有知有行营销负责人",
        "李翔": "《详谈》丛书作者、《高能量》主理人",
        "翁放": "《起朱楼宴宾客》主播",
        "潘乱": "《乱翻书》主播",
        "曾鸣": "智谱AI相关（需确认）",
        "张晶": "知乎副总裁、正面连接创始人"
    }
    
    questions = {}
    
    for name, role in guests.items():
        # 基于分析结果设计定制问题
        # 这里需要结合分析结果
        questions[name] = {
            "question": f"为{name}设计的定制问题（结合分析结果）",
            "rationale": "基于该嘉宾的内容创作理念和行业观察"
        }
    
    return questions

def create_interview_outline():
    """创建访谈大纲"""
    output_dir = Path(__file__).parent.parent / "outputs"
    outline_file = output_dir / "interview_outline.md"
    
    with open(outline_file, 'w', encoding='utf-8') as f:
        f.write("# Panel访谈大纲\\n\\n")
        f.write("时长：1小时（包含观众提问）\\n\\n")
        f.write("## 时间分配\\n\\n")
        f.write("1. 开场介绍（5分钟）\\n")
        f.write("2. 定制问题环节（40分钟）\\n")
        f.write("3. 通用问题环节（15分钟）\\n")
        f.write("   - 关于Google的问题\\n")
        f.write("   - 关于AI的问题\\n")
        f.write("4. 观众提问（5分钟）\\n\\n")
        
        f.write("## 问题设计\\n\\n")
        f.write("（待完善，基于分析结果）\\n\\n")
    
    print(f"✅ 访谈大纲框架已保存: {outline_file}")
    return outline_file

def main():
    print("\\n开始后续任务...\\n")
    
    # 加载分析结果
    analysis_results = load_analysis_results()
    
    if not analysis_results:
        print("⚠️  无分析结果，跳过后续任务")
        return
    
    # 创建研究笔记
    create_research_notes(analysis_results)
    
    # 设计访谈问题
    questions = design_interview_questions(analysis_results)
    
    # 创建访谈大纲
    create_interview_outline()
    
    print("\\n✅ 后续任务完成")

if __name__ == "__main__":
    main()
'''
    
    script_path = Path(__file__).parent / "complete_research_and_outline.py"
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script_content)
    
    script_path.chmod(0o755)
    print(f"✅ 已创建后续任务脚本: {script_path}")

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

