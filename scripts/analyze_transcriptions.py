#!/usr/bin/env python3
"""
使用Gemini API分析播客转录文本，重点提取主播（Panel嘉宾）的观点
"""

import json
import re
import time
from pathlib import Path
from typing import List, Dict

try:
    import google.generativeai as genai
except ImportError:
    print("请安装 google-generativeai: pip install google-generativeai")
    import sys
    sys.exit(1)

# Gemini API配置
GEMINI_API_KEY = "REMOVED_API_KEY"
genai.configure(api_key=GEMINI_API_KEY)

def identify_host_statements(text: str, host_keywords: List[str] = None) -> List[str]:
    """识别主播的发言 - 重点提取Panel嘉宾（播客主播）的观点"""
    if host_keywords is None:
        # 常见的主播标识
        host_keywords = [
            "主持人", "主播", "我", "我们", "今天", "这一期",
            "邀请", "欢迎", "接下来", "刚才", "刚才我们"
        ]
    
    host_statements = []
    
    # 方法1：如果转录中有[主播]标签，直接提取
    if '[主播]' in text or '主播' in text:
        # 按行分割，查找主播标记的段落
        lines = text.split('\n')
        current_statement = []
        
        for line in lines:
            if '[主播]' in line or line.strip().startswith('[主播]'):
                if current_statement:
                    host_statements.append(' '.join(current_statement))
                current_statement = [line]
            elif current_statement and not line.strip().startswith('['):
                # 继续当前主播发言
                current_statement.append(line)
            elif current_statement:
                # 主播发言结束
                if current_statement:
                    host_statements.append(' '.join(current_statement))
                current_statement = []
    
    # 方法2：如果没有明确标签，使用启发式方法
    if not host_statements:
        paragraphs = text.split('\n\n')
        
        for para in paragraphs:
            para_lower = para.lower()
            
            # 检查是否明确标注为主播
            if '[主播]' in para or '主播：' in para or '主播:' in para:
                host_statements.append(para)
                continue
            
            # 检查是否包含主播关键词（排除嘉宾发言）
            if any(keyword in para_lower for keyword in host_keywords):
                # 排除可能是嘉宾说的话（包含"我"但上下文像是回答问题的）
                if not (re.search(r'[嘉宾]|受访者|被访谈', para)):
                    # 检查是否是提问句（主播更可能提问）
                    if '?' in para or '？' in para:
                        host_statements.append(para)
                    # 检查是否是引导性语句
                    elif re.match(r'^(让我们|现在|接下来|这一期|今天|欢迎)', para):
                        host_statements.append(para)
                    # 检查是否包含节目引导词
                    elif re.search(r'(要聊|要讨论|来聊聊|来谈谈|来听听)', para):
                        host_statements.append(para)
    
    return host_statements

def extract_host_insights_with_gemini(text: str, host_name: str, podcast_name: str) -> Dict:
    """使用Gemini API提取主播的核心观点和洞察"""
    print(f"  使用Gemini API分析文本...")
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
    except:
        try:
            model = genai.GenerativeModel("models/gemini-2.0-flash")
        except:
            model = genai.GenerativeModel("gemini-pro")
    
    # 准备分析提示词
    analysis_prompt = f"""请分析以下播客转录文本，重点提取主播（{host_name}）的核心观点和洞察。

**重要说明**：
- 主播是播客的主持人/制作者（{host_name}），这是Panel的嘉宾
- 节目中的嘉宾是播客邀请的访谈对象，不是我们要分析的
- 请重点关注主播的观点、观察、提问方式和内容创作理念

**请提取以下内容**：

1. **专业观察**：主播对行业、技术、商业的专业观察和判断（3-5条）
2. **内容创作理念**：主播如何做内容、选择话题、采访嘉宾的理念和方法（3-5条）
3. **行业见解**：主播对媒体、内容、科技行业的看法和趋势判断（3-5条）
4. **个人观点**：主播独特的个人观点和价值判断（3-5条）
5. **讨论主题**：主播在这一期节目中关注的主要话题（列出5-10个关键词或短语）
6. **表达风格**：主播的提问方式、引导技巧、表达风格的特点

**输出格式（JSON）**：
{{
    "professional_observations": ["观察1", "观察2", ...],
    "content_creation_philosophy": ["理念1", "理念2", ...],
    "industry_insights": ["见解1", "见解2", ...],
    "personal_views": ["观点1", "观点2", ...],
    "discussion_topics": ["主题1", "主题2", ...],
    "expression_style": "主播的表达风格描述"
}}

**转录文本**：
{text[:20000] if len(text) > 20000 else text}

请以JSON格式输出，确保提取的都是主播的观点，而非节目中嘉宾的观点。

**注意**：如果转录文本很长，这是前20000字符的摘要。请基于这部分内容进行分析，重点关注主播的发言部分。
"""
    
    try:
        response = model.generate_content(analysis_prompt)
        result_text = response.text
        
        # 尝试提取JSON
        import json as json_module
        # 查找JSON部分
        json_match = re.search(r'\{[^{}]*\{[^{}]*\{.*?\}\}\}', result_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            # 如果没有找到，尝试提取第一个{}
            json_match = re.search(r'\{.*?\}', result_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = result_text
        
        try:
            insights = json_module.loads(json_str)
        except:
            # 如果不是有效JSON，返回文本结果
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
        
        insights['host_name'] = host_name
        insights['podcast_name'] = podcast_name
        
        print(f"    ✅ Gemini分析完成")
        return insights
        
    except Exception as e:
        print(f"    ❌ Gemini分析失败: {e}")
        import traceback
        traceback.print_exc()
        return {
            'host_name': host_name,
            'podcast_name': podcast_name,
            'error': str(e),
            'professional_observations': [],
            'content_creation_philosophy': [],
            'industry_insights': [],
            'personal_views': [],
            'discussion_topics': [],
            'expression_style': ''
        }

def analyze_transcription_file(transcription_file: Path, host_name: str, podcast_name: str) -> Dict:
    """分析单个转录文件 - 使用Gemini API"""
    print(f"\n分析转录文件: {transcription_file.name}")
    
    if not transcription_file.exists():
        print(f"  ❌ 文件不存在")
        return None
    
    with open(transcription_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    if len(text.strip()) < 100:
        print(f"  ⚠️  文本过短，跳过")
        return None
    
    print(f"  文本长度: {len(text)} 字符")
    
    # 使用Gemini API提取洞察
    insights = extract_host_insights_with_gemini(text, host_name, podcast_name)
    
    # 识别主播发言（用于统计）
    host_statements = identify_host_statements(text)
    
    result = {
        'file': str(transcription_file),
        'episode_name': transcription_file.stem,
        'host_statements_count': len(host_statements),
        'insights': insights,
        'text_length': len(text),
        'paragraph_count': len(text.split('\n\n'))
    }
    
    print(f"  ✅ 分析完成")
    print(f"    主播发言段数: {len(host_statements)}")
    print(f"    专业观察: {len(insights.get('professional_observations', []))} 条")
    print(f"    内容创作理念: {len(insights.get('content_creation_philosophy', []))} 条")
    
    return result

def batch_analyze(transcriptions_dir: Path, output_dir: Path = None) -> Dict:
    """批量分析转录文件"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "research"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有转录文件
    transcription_files = list(transcriptions_dir.rglob('*.txt'))
    
    if not transcription_files:
        print(f"未找到转录文件在: {transcriptions_dir}")
        return {}
    
    print(f"找到 {len(transcription_files)} 个转录文件")
    
    # 按播客分组
    podcast_analyses = {}
    
    for txt_file in transcription_files:
        # 从路径推断播客名称
        rel_path = txt_file.relative_to(transcriptions_dir)
        parts = rel_path.parts
        if len(parts) >= 2:
            podcast_name = parts[0]  # 播客目录名
            if podcast_name not in podcast_analyses:
                podcast_analyses[podcast_name] = []
            
            # 提取主播名称（从播客名称）
            host_name = podcast_name.split('_')[1] if '_' in podcast_name else podcast_name
            
            analysis = analyze_transcription_file(txt_file, host_name, podcast_name)
            if analysis:
                podcast_analyses[podcast_name].append(analysis)
            
            # API请求间隔
            time.sleep(3)
    
    # 汇总每个播客的主播观点
    summaries = {}
    for podcast_name, analyses in podcast_analyses.items():
        host_name = podcast_name.split('_')[1] if '_' in podcast_name else podcast_name
        
        # 合并所有分析结果（基于Gemini分析的结果）
        merged_insights = {
            'professional_observations': [],
            'content_creation_philosophy': [],
            'industry_insights': [],
            'personal_views': [],
            'discussion_topics': [],
            'expression_styles': []
        }
        
        for analysis in analyses:
            if 'insights' in analysis:
                insights = analysis['insights']
                for key in merged_insights:
                    if key in insights:
                        if isinstance(insights[key], list):
                            merged_insights[key].extend(insights[key])
                        elif insights[key]:  # 如果是字符串
                            merged_insights[key].append(insights[key])
                
                # 收集表达风格
                if 'expression_style' in insights and insights['expression_style']:
                    merged_insights['expression_styles'].append(insights['expression_style'])
        
        # 去重并整理
        summaries[podcast_name] = {
            'host_name': host_name,
            'podcast_name': podcast_name,
            'episode_count': len(analyses),
            'insights': {
                key: list(dict.fromkeys(values))[:15] if isinstance(values, list) else values  # 去重保留顺序
                for key, values in merged_insights.items()
                if key != 'expression_styles'
            },
            'expression_style_summary': ' | '.join(merged_insights['expression_styles'][:3]) if merged_insights['expression_styles'] else '',
            'key_themes': list(dict.fromkeys(merged_insights['discussion_topics']))[:10]
        }
    
    # 保存分析结果
    summary_file = output_dir / "host_insights_analysis.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summaries, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 分析完成！结果已保存到: {summary_file}")
    
    # 生成文本摘要
    summary_text_file = output_dir / "host_insights_summary.md"
    with open(summary_text_file, 'w', encoding='utf-8') as f:
        f.write("# 播客主播观点分析总结\n\n")
        f.write("**重要说明**: 本分析使用Gemini API分析转录文本，重点关注播客主播（Panel嘉宾）的观点，而非播客节目中邀请的嘉宾观点。\n\n")
        
        for podcast_name, summary in summaries.items():
            host_name = summary['host_name']
            f.write(f"## {host_name} - {podcast_name}\n\n")
            f.write(f"**分析期数**: {summary['episode_count']} 期\n\n")
            
            insights = summary.get('insights', {})
            
            if insights.get('professional_observations'):
                f.write("### 专业观察\n\n")
                for i, obs in enumerate(insights['professional_observations'][:5], 1):
                    obs_text = obs if isinstance(obs, str) else str(obs)
                    f.write(f"{i}. {obs_text[:200]}\n\n")
            
            if insights.get('content_creation_philosophy'):
                f.write("### 内容创作理念\n\n")
                for i, idea in enumerate(insights['content_creation_philosophy'][:5], 1):
                    idea_text = idea if isinstance(idea, str) else str(idea)
                    f.write(f"{i}. {idea_text[:200]}\n\n")
            
            if insights.get('industry_insights'):
                f.write("### 行业见解\n\n")
                for i, insight in enumerate(insights['industry_insights'][:5], 1):
                    insight_text = insight if isinstance(insight, str) else str(insight)
                    f.write(f"{i}. {insight_text[:200]}\n\n")
            
            if insights.get('personal_views'):
                f.write("### 个人观点\n\n")
                for i, view in enumerate(insights['personal_views'][:5], 1):
                    view_text = view if isinstance(view, str) else str(view)
                    f.write(f"{i}. {view_text[:200]}\n\n")
            
            if summary.get('expression_style_summary'):
                f.write("### 表达风格\n\n")
                f.write(f"{summary['expression_style_summary']}\n\n")
            
            if summary.get('key_themes'):
                f.write("### 讨论主题\n\n")
                for theme in summary['key_themes'][:10]:
                    theme_text = theme if isinstance(theme, str) else str(theme)
                    f.write(f"- {theme_text[:150]}\n")
                f.write("\n")
            
            f.write("---\n\n")
    
    print(f"文本摘要已保存到: {summary_text_file}")
    
    return summaries

def main():
    """主函数"""
    transcriptions_dir = Path(__file__).parent.parent / "transcriptions"
    output_dir = Path(__file__).parent.parent / "research"
    
    if not transcriptions_dir.exists():
        print(f"转录目录不存在: {transcriptions_dir}")
        print("请先运行 transcribe_with_gemini.py 进行转录")
        return
    
    batch_analyze(transcriptions_dir, output_dir)

if __name__ == "__main__":
    main()

