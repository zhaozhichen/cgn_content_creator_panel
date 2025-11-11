#!/usr/bin/env python3
"""
基于分析结果设计访谈问题
"""

import json
import sys
from pathlib import Path

try:
    import google.generativeai as genai
except ImportError:
    print("请安装 google-generativeai")
    sys.exit(1)

# Gemini API配置
# Gemini API配置 - 从环境变量读取
import os
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ 错误: 未设置 GEMINI_API_KEY 环境变量")
    print("   请设置: export GEMINI_API_KEY='your-api-key'")
    import sys
    sys.exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def load_analysis_results():
    """加载分析结果"""
    research_dir = Path(__file__).parent.parent / "research"
    analysis_file = research_dir / "host_insights_analysis.json"
    
    if not analysis_file.exists():
        print("⚠️  分析结果文件不存在")
        return {}
    
    with open(analysis_file, 'r', encoding='utf-8') as f:
        return json.load(f)

# Panel嘉宾信息
PANEL_GUESTS = {
    "黄俊杰": {
        "role": "晚点LatePost联合创始人兼总编辑",
        "podcast": "晚点聊",
        "focus": "科技报道、商业观察"
    },
    "李路野": {
        "role": "有知有行营销负责人",
        "podcast": "知行小酒馆",
        "focus": "投资理财、生活哲学"
    },
    "李翔": {
        "role": "《详谈》丛书作者、《高能量》主理人",
        "podcast": "高能量",
        "focus": "商业观察、个人成长"
    },
    "翁放": {
        "role": "《起朱楼宴宾客》主播",
        "podcast": "起朱楼宴宾客",
        "focus": "投资金融、国际观察"
    },
    "潘乱": {
        "role": "《乱翻书》主播",
        "podcast": "乱翻书",
        "focus": "科技评论、行业分析"
    },
    "曾鸣": {
        "role": "正面连接创始人",
        "podcast": "无",
        "focus": "非虚构写作、媒体、深度内容"
    },
    "张晶": {
        "role": "知乎副总裁",
        "podcast": "无",
        "focus": "内容平台、社区运营"
    }
}

def design_question_for_guest(guest_name: str, guest_info: dict, analysis_data: dict = None):
    """为嘉宾设计定制问题"""
    print(f"\n为 {guest_name} 设计问题...")
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except:
        model = genai.GenerativeModel("gemini-pro")
    
    # 构建分析信息
    analysis_text = ""
    if analysis_data:
        podcast_name = None
        for pn, data in analysis_data.items():
            if guest_name in pn or guest_name in data.get('host_name', ''):
                podcast_name = pn
                insights = data.get('insights', {})
                
                analysis_text = f"""
基于播客分析结果：
- 专业观察：{insights.get('professional_observations', [])[:3]}
- 内容创作理念：{insights.get('content_creation_philosophy', [])[:3]}
- 行业见解：{insights.get('industry_insights', [])[:3]}
- 讨论主题：{insights.get('discussion_topics', [])[:5]}
"""
                break
    
    prompt = f"""请为Panel访谈设计一个问题。以下是嘉宾信息：

**嘉宾**: {guest_name}
**身份**: {guest_info['role']}
**播客**: {guest_info['podcast']}
**关注领域**: {guest_info['focus']}
{analysis_text}

**设计要求**：
1. 问题要体现该嘉宾的独特背景和工作特点
2. 问题要有普适性，其他6位嘉宾也能参与回答
3. 偏向行业观点讨论，而非个人经历
4. 适合在Google NYC面向华人Google员工提问
5. 问题长度：1-2句话

**输出格式（JSON）**：
{{
    "question": "问题内容",
    "rationale": "设计理由（为什么适合该嘉宾，其他嘉宾如何参与）",
    "key_points": ["讨论要点1", "讨论要点2", "讨论要点3"]
}}

请只输出JSON，不要其他文字。
"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # 提取JSON
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            question_data = json.loads(json_match.group(0))
            return question_data
        else:
            return {
                "question": result_text,
                "rationale": "AI生成",
                "key_points": []
            }
    except Exception as e:
        print(f"  ❌ 设计失败: {e}")
        return None

def design_google_question():
    """设计关于Google的问题"""
    print("\n设计关于Google的问题...")
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except:
        model = genai.GenerativeModel("gemini-pro")
    
    prompt = """请设计一个关于Google的问题，适合在Panel访谈中向7位中国内容创作者提问。

**听众背景**: Chinese Google Network的华人Google员工，在Google NYC举行

**问题要求**：
1. 询问他们对Google公司和产品的看法
2. 适合内容创作者的角度
3. 能引发深入讨论
4. 与7位嘉宾（播客主播、媒体创始人、内容创作者）相关

**输出格式（JSON）**：
{{
    "question": "问题内容",
    "rationale": "设计理由",
    "key_points": ["讨论要点1", "讨论要点2", "讨论要点3"]
}}

请只输出JSON，不要其他文字。
"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {"question": result_text, "rationale": "", "key_points": []}
    except Exception as e:
        print(f"  ❌ 设计失败: {e}")
        return None

def design_ai_question():
    """设计关于AI的问题"""
    print("\n设计关于AI的问题...")
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except:
        model = genai.GenerativeModel("gemini-pro")
    
    prompt = """请设计一个关于AI的问题，适合在Panel访谈中向7位中国内容创作者提问。

**问题要求**：
1. 询问AI对内容创作和传播媒介在未来5年的影响
2. 适合内容创作者的角度
3. 能引发深入讨论
4. 与7位嘉宾（播客主播、媒体创始人、内容创作者）相关

**输出格式（JSON）**：
{{
    "question": "问题内容",
    "rationale": "设计理由",
    "key_points": ["讨论要点1", "讨论要点2", "讨论要点3"]
}}

请只输出JSON，不要其他文字。
"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        import re
        json_match = re.search(r'\{.*\}', result_text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group(0))
        return {"question": result_text, "rationale": "", "key_points": []}
    except Exception as e:
        print(f"  ❌ 设计失败: {e}")
        return None

def main():
    """主函数"""
    print("=" * 60)
    print("设计Panel访谈问题")
    print("=" * 60)
    
    # 加载分析结果
    analysis_data = load_analysis_results()
    
    # 为每位嘉宾设计问题
    guest_questions = {}
    for guest_name, guest_info in PANEL_GUESTS.items():
        question = design_question_for_guest(guest_name, guest_info, analysis_data)
        if question:
            guest_questions[guest_name] = question
        import time
        time.sleep(2)  # API间隔
    
    # 设计通用问题
    google_question = design_google_question()
    import time
    time.sleep(2)
    ai_question = design_ai_question()
    
    # 保存问题
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    questions_file = output_dir / "interview_questions.json"
    with open(questions_file, 'w', encoding='utf-8') as f:
        json.dump({
            'guest_questions': guest_questions,
            'google_question': google_question,
            'ai_question': ai_question
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 问题设计完成！已保存到: {questions_file}")
    
    # 更新访谈大纲
    update_outline(guest_questions, google_question, ai_question)

def update_outline(guest_questions, google_question, ai_question):
    """更新访谈大纲"""
    output_dir = Path(__file__).parent.parent / "outputs"
    outline_file = output_dir / "interview_outline.md"
    
    with open(outline_file, 'w', encoding='utf-8') as f:
        f.write("# Panel访谈大纲\n\n")
        f.write("**听众**: Chinese Google Network的华人Google员工\n")
        f.write("**地点**: Google NYC\n")
        f.write("**时长**: 1小时（包含观众提问）\n\n")
        f.write("---\n\n")
        
        f.write("## 时间分配\n\n")
        f.write("1. **开场介绍**（5分钟）\n")
        f.write("   - 介绍主题和7位嘉宾\n\n")
        f.write("2. **定制问题环节**（40分钟，约6分钟/人）\n")
        f.write("   - 为每位嘉宾设计1个定制问题\n")
        f.write("   - 问题既有针对性又具普适性，其他嘉宾也可参与\n\n")
        f.write("3. **通用问题环节**（15分钟）\n")
        f.write("   - 关于Google的问题（7分钟）\n")
        f.write("   - 关于AI的问题（8分钟）\n\n")
        f.write("4. **观众提问**（5分钟）\n\n")
        f.write("---\n\n")
        
        f.write("## 定制问题设计\n\n")
        for guest_name, question_data in guest_questions.items():
            f.write(f"### {guest_name}\n\n")
            f.write(f"**问题**: {question_data.get('question', '')}\n\n")
            f.write(f"**设计理由**: {question_data.get('rationale', '')}\n\n")
            if question_data.get('key_points'):
                f.write("**讨论要点**:\n")
                for point in question_data['key_points']:
                    f.write(f"- {point}\n")
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## 通用问题\n\n")
        
        if google_question:
            f.write("### 关于Google的问题\n\n")
            f.write(f"**问题**: {google_question.get('question', '')}\n\n")
            f.write(f"**设计理由**: {google_question.get('rationale', '')}\n\n")
            if google_question.get('key_points'):
                f.write("**讨论要点**:\n")
                for point in google_question['key_points']:
                    f.write(f"- {point}\n")
            f.write("\n")
        
        if ai_question:
            f.write("### 关于AI的问题\n\n")
            f.write(f"**问题**: {ai_question.get('question', '')}\n\n")
            f.write(f"**设计理由**: {ai_question.get('rationale', '')}\n\n")
            if ai_question.get('key_points'):
                f.write("**讨论要点**:\n")
                for point in ai_question['key_points']:
                    f.write(f"- {point}\n")
            f.write("\n")
        
        f.write("---\n\n")
        f.write("## 主持人引导建议\n\n")
        f.write("1. 在每个定制问题后，鼓励其他嘉宾分享观点\n")
        f.write("2. 注意时间控制，确保每位嘉宾都有机会发言\n")
        f.write("3. 在通用问题环节，可以邀请对Google或AI有特别看法的嘉宾先发言\n")
        f.write("4. 预留观众提问时间，鼓励互动\n\n")
    
    print(f"✅ 访谈大纲已更新: {outline_file}")

if __name__ == "__main__":
    main()

