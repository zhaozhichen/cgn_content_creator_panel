#!/usr/bin/env python3
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
        f.write("# Panel嘉宾研究笔记\n\n")
        f.write("基于播客转录文本的Gemini API分析结果\n\n")
        f.write("---\n\n")
        
        for podcast_name, summary in analysis_results.items():
            host_name = summary.get('host_name', 'Unknown')
            f.write(f"## {host_name} - {podcast_name}\n\n")
            
            insights = summary.get('insights', {})
            
            if insights.get('professional_observations'):
                f.write("### 专业观察\n\n")
                for obs in insights['professional_observations'][:5]:
                    f.write(f"- {obs}\n")
                f.write("\n")
            
            if insights.get('content_creation_philosophy'):
                f.write("### 内容创作理念\n\n")
                for idea in insights['content_creation_philosophy'][:5]:
                    f.write(f"- {idea}\n")
                f.write("\n")
            
            f.write("---\n\n")
    
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
        f.write("# Panel访谈大纲\n\n")
        f.write("时长：1小时（包含观众提问）\n\n")
        f.write("## 时间分配\n\n")
        f.write("1. 开场介绍（5分钟）\n")
        f.write("2. 定制问题环节（40分钟）\n")
        f.write("3. 通用问题环节（15分钟）\n")
        f.write("   - 关于Google的问题\n")
        f.write("   - 关于AI的问题\n")
        f.write("4. 观众提问（5分钟）\n\n")
        
        f.write("## 问题设计\n\n")
        f.write("（待完善，基于分析结果）\n\n")
    
    print(f"✅ 访谈大纲框架已保存: {outline_file}")
    return outline_file

def main():
    print("\n开始后续任务...\n")
    
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
    
    print("\n✅ 后续任务完成")

if __name__ == "__main__":
    main()
