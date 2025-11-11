#!/usr/bin/env python3
"""
为其他3位嘉宾（潘乱、曾鸣、张晶）收集并分析信息
使用Gemini API分析他们的公开内容
"""

import json
import sys
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("请安装 google-generativeai")
    sys.exit(1)

# Gemini API配置 - 从环境变量读取
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ 错误: 未设置 GEMINI_API_KEY 环境变量")
    print("   请设置: export GEMINI_API_KEY='your-api-key'")
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# 其他3位嘉宾信息
OTHER_GUESTS = {
    "潘乱": {
        "role": "《乱翻书》主播",
        "podcast": "乱翻书",
        "known_for": "2018年《腾讯没有梦想》成为现象级爆款，超过1000万观看",
        "focus": "科技评论、商业分析",
        "search_terms": ["潘乱", "乱翻书", "腾讯没有梦想", "科技评论"]
    },
    "曾鸣": {
        "role": "正面连接创始人",
        "podcast": "无",
        "known_for": "正面连接专注深度非虚构和特稿写作，前三大文章一年内超过300万观看量",
        "focus": "非虚构写作、媒体、深度内容",
        "search_terms": ["曾鸣", "正面连接", "非虚构", "特稿"]
    },
    "张晶": {
        "role": "知乎副总裁",
        "podcast": "无",
        "known_for": "知乎是中国领先的问答和新闻聚合平台",
        "focus": "内容平台、社区运营",
        "search_terms": ["张晶", "知乎", "内容平台", "社区"]
    }
}

def analyze_guest_with_gemini(guest_name: str, guest_info: dict, collected_content: str = None):
    """使用Gemini API分析嘉宾信息"""
    print(f"\n分析 {guest_name}...")
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except:
        try:
            model = genai.GenerativeModel("models/gemini-2.0-flash")
        except:
            model = genai.GenerativeModel("gemini-pro")
    
    # 准备分析提示词
    analysis_prompt = f"""请分析以下嘉宾信息，提取其核心观点和洞察。

**嘉宾信息**：
- 姓名：{guest_name}
- 身份：{guest_info['role']}
- 播客/作品：{guest_info.get('podcast', '无')}
- 知名作品/成就：{guest_info.get('known_for', '')}
- 关注领域：{guest_info.get('focus', '')}

**收集到的内容**：
{collected_content if collected_content else "基于公开信息（PDF中的介绍）和一般了解"}

**请提取以下内容**：

1. **专业观察**：该嘉宾对行业、技术、商业的专业观察和判断（3-5条）
2. **内容创作理念**：如何做内容、选择话题的理念和方法（3-5条）
3. **行业见解**：对媒体、内容、科技行业的看法和趋势判断（3-5条）
4. **个人观点**：独特的个人观点和价值判断（3-5条）
5. **讨论主题**：该嘉宾可能关注的主要话题（5-10个关键词或短语）
6. **表达风格**：推测的提问方式、引导技巧、表达风格的特点

**输出格式（JSON）**：
{{
    "professional_observations": ["观察1", "观察2", ...],
    "content_creation_philosophy": ["理念1", "理念2", ...],
    "industry_insights": ["见解1", "见解2", ...],
    "personal_views": ["观点1", "观点2", ...],
    "discussion_topics": ["主题1", "主题2", ...],
    "expression_style": "表达风格描述"
}}

请基于已有信息进行合理分析和推断，确保提取的都是该嘉宾可能的观点和特点。
"""
    
    try:
        response = model.generate_content(analysis_prompt)
        result_text = response.text
        
        # 提取JSON
        import re
        json_match = re.search(r'\{.*?\}', result_text, re.DOTALL)
        if json_match:
            insights = json.loads(json_match.group(0))
        else:
            insights = {
                'raw_analysis': result_text,
                'professional_observations': [],
                'content_creation_philosophy': [],
                'industry_insights': [],
                'personal_views': [],
                'discussion_topics': [],
                'expression_style': ''
            }
        
        # 确保所有键都存在
        default_keys = {
            'professional_observations': [],
            'content_creation_philosophy': [],
            'industry_insights': [],
            'personal_views': [],
            'discussion_topics': [],
            'expression_style': ''
        }
        
        for key, default_value in default_keys.items():
            if key not in insights:
                insights[key] = default_value
        
        insights['guest_name'] = guest_name
        insights['role'] = guest_info['role']
        
        print(f"  ✅ 分析完成")
        return insights
        
    except Exception as e:
        print(f"  ❌ 分析失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def collect_guest_info_from_pdf(guest_name: str):
    """从PDF信息中提取嘉宾信息"""
    pdf_info = {
        "潘乱": {
            "content": """
            潘乱：《乱翻书》主播
            - 2018年《腾讯没有梦想》成为现象级爆款，超过1000万观看
            - 播客《乱翻书》订阅量超过100万
            - 通过对话深入探讨商业和科技话题
            - 擅长挑战既有观点、揭示深层趋势
            """
        },
        "曾鸣": {
            "content": """
            曾鸣：正面连接创始人
            - 正面连接专注深度非虚构和特稿写作
            - 前三大文章在一年内获得超过300万观看量
            - 通过人性化的叙述，捕捉当代中国社会文化脉搏
            - 关注内容真实性、人文关怀和信息生态
            """
        },
        "张晶": {
            "content": """
            张晶：知乎副总裁
            - 知乎是中国领先的问答和新闻聚合平台
            - 负责内容平台运营和社区建设
            """
        }
    }
    
    return pdf_info.get(guest_name, {}).get('content', '')

def main():
    """主函数"""
    print("=" * 60)
    print("分析其他3位嘉宾（潘乱、曾鸣、张晶）")
    print("=" * 60)
    
    output_dir = Path(__file__).parent.parent / "research"
    output_dir.mkdir(exist_ok=True)
    
    results = {}
    
    for guest_name, guest_info in OTHER_GUESTS.items():
        print(f"\n处理 {guest_name}...")
        
        # 从PDF收集信息
        pdf_content = collect_guest_info_from_pdf(guest_name)
        
        # 使用Gemini分析
        insights = analyze_guest_with_gemini(guest_name, guest_info, pdf_content)
        
        if insights:
            results[guest_name] = {
                'role': guest_info['role'],
                'podcast': guest_info.get('podcast', '无'),
                'insights': insights
            }
        
        import time
        time.sleep(3)  # API间隔
    
    # 保存结果
    results_file = output_dir / "other_guests_analysis.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 分析完成！结果已保存到: {results_file}")
    
    # 生成摘要
    summary_file = output_dir / "other_guests_summary.md"
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("# 其他3位嘉宾分析总结\n\n")
        f.write("**说明**: 这3位嘉宾没有小宇宙播客转录，基于公开信息和PDF内容进行分析\n\n")
        f.write("---\n\n")
        
        for guest_name, data in results.items():
            insights = data.get('insights', {})
            f.write(f"## {guest_name}\n\n")
            f.write(f"**身份**: {data.get('role', '')}\n\n")
            f.write(f"**播客/作品**: {data.get('podcast', '无')}\n\n")
            
            if insights.get('professional_observations'):
                f.write("### 专业观察\n\n")
                for i, obs in enumerate(insights['professional_observations'][:5], 1):
                    f.write(f"{i}. {obs}\n\n")
            
            if insights.get('content_creation_philosophy'):
                f.write("### 内容创作理念\n\n")
                for i, idea in enumerate(insights['content_creation_philosophy'][:5], 1):
                    f.write(f"{i}. {idea}\n\n")
            
            if insights.get('industry_insights'):
                f.write("### 行业见解\n\n")
                for i, insight in enumerate(insights['industry_insights'][:5], 1):
                    f.write(f"{i}. {insight}\n\n")
            
            if insights.get('personal_views'):
                f.write("### 个人观点\n\n")
                for i, view in enumerate(insights['personal_views'][:5], 1):
                    f.write(f"{i}. {view}\n\n")
            
            if insights.get('discussion_topics'):
                f.write("### 讨论主题\n\n")
                for topic in insights['discussion_topics'][:10]:
                    f.write(f"- {topic}\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    print(f"✅ 摘要已保存到: {summary_file}")
    
    # 更新研究笔记
    update_research_notes(results)

def update_research_notes(other_guests_results):
    """更新研究笔记，包含所有7位嘉宾"""
    output_dir = Path(__file__).parent.parent / "outputs"
    
    # 读取已有的分析结果
    research_dir = Path(__file__).parent.parent / "research"
    existing_analysis_file = research_dir / "host_insights_analysis.json"
    
    existing_data = {}
    if existing_analysis_file.exists():
        with open(existing_analysis_file, 'r', encoding='utf-8') as f:
            existing_data = json.load(f)
    
    # 读取其他嘉宾分析
    other_guests_file = research_dir / "other_guests_analysis.json"
    if other_guests_file.exists():
        with open(other_guests_file, 'r', encoding='utf-8') as f:
            other_data = json.load(f)
    else:
        other_data = {}
    
    # 更新研究笔记
    notes_file = output_dir / "research_notes.md"
    
    with open(notes_file, 'w', encoding='utf-8') as f:
        f.write("# Panel嘉宾研究笔记（完整版）\n\n")
        f.write("包含7位嘉宾的分析结果\n\n")
        f.write("---\n\n")
        
        # 先写有播客转录的4位
        f.write("## 有播客转录的4位嘉宾（基于播客转录分析）\n\n")
        f.write("---\n\n")
        
        for podcast_name, summary in existing_data.items():
            host_name = summary.get('host_name', 'Unknown')
            f.write(f"### {host_name} - {podcast_name}\n\n")
            
            insights = summary.get('insights', {})
            
            if insights.get('professional_observations'):
                f.write("#### 专业观察\n\n")
                for obs in insights['professional_observations'][:5]:
                    f.write(f"- {obs}\n")
                f.write("\n")
            
            if insights.get('content_creation_philosophy'):
                f.write("#### 内容创作理念\n\n")
                for idea in insights['content_creation_philosophy'][:5]:
                    f.write(f"- {idea}\n")
                f.write("\n")
            
            f.write("---\n\n")
        
        # 再写其他3位
        f.write("## 其他3位嘉宾（基于公开信息分析）\n\n")
        f.write("**说明**: 这3位嘉宾没有小宇宙播客转录，基于PDF信息和公开内容进行分析\n\n")
        f.write("---\n\n")
        
        for guest_name, data in other_data.items():
            f.write(f"### {guest_name}\n\n")
            f.write(f"**身份**: {data.get('role', '')}\n\n")
            f.write(f"**播客/作品**: {data.get('podcast', '无')}\n\n")
            
            insights = data.get('insights', {})
            
            if insights.get('professional_observations'):
                f.write("#### 专业观察\n\n")
                for obs in insights['professional_observations'][:5]:
                    f.write(f"- {obs}\n")
                f.write("\n")
            
            if insights.get('content_creation_philosophy'):
                f.write("#### 内容创作理念\n\n")
                for idea in insights['content_creation_philosophy'][:5]:
                    f.write(f"- {idea}\n")
                f.write("\n")
            
            if insights.get('industry_insights'):
                f.write("#### 行业见解\n\n")
                for insight in insights['industry_insights'][:5]:
                    f.write(f"- {insight}\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    print(f"✅ 研究笔记已更新: {notes_file}")

if __name__ == "__main__":
    main()

