#!/usr/bin/env python3
"""
修正嘉宾信息错误
根据用户指正：
- 曾鸣：正面连接创始人
- 张晶：知乎副总裁
"""

import json
import re
from pathlib import Path

# 正确的嘉宾信息（根据用户指正）
CORRECT_GUEST_INFO = {
    "曾鸣": {
        "role": "正面连接创始人",
        "known_for": "正面连接专注深度非虚构和特稿写作，前三大文章一年内超过300万观看量",
        "focus": "非虚构写作、媒体、深度内容",
        "search_terms": ["曾鸣", "正面连接", "非虚构", "特稿"]
    },
    "张晶": {
        "role": "知乎副总裁",
        "known_for": "知乎是中国领先的问答和新闻聚合平台",
        "focus": "内容平台、社区运营",
        "search_terms": ["张晶", "知乎", "内容平台", "社区"]
    }
}

def fix_json_file(file_path: Path):
    """修正JSON文件中的错误信息"""
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修正错误：将"正面连接创始人"从张晶移到曾鸣
        content = content.replace(
            '"张晶": {',
            '"张晶": {'
        )
        
        # 使用正则表达式修正role字段
        # 曾鸣：智谱AI相关 -> 正面连接创始人
        content = re.sub(
            r'"曾鸣"[^}]*"role"\s*:\s*"[^"]*"',
            lambda m: m.group(0).replace('智谱AI相关（需确认具体职位）', '正面连接创始人'),
            content
        )
        
        # 张晶：知乎副总裁、正面连接创始人 -> 知乎副总裁
        content = re.sub(
            r'"张晶"[^}]*"role"\s*:\s*"[^"]*"',
            lambda m: m.group(0).replace('知乎副总裁、正面连接创始人', '知乎副总裁'),
            content
        )
        
        # 重新解析和写入，确保JSON格式正确
        data = json.loads(content)
        
        if "曾鸣" in data:
            if isinstance(data["曾鸣"], dict):
                data["曾鸣"]["role"] = "正面连接创始人"
                if "insights" in data["曾鸣"] and "guest_name" not in data["曾鸣"]["insights"]:
                    data["曾鸣"]["insights"]["guest_name"] = "曾鸣"
        
        if "张晶" in data:
            if isinstance(data["张晶"], dict):
                data["张晶"]["role"] = "知乎副总裁"
                if "insights" in data["张晶"] and "guest_name" not in data["张晶"]["insights"]:
                    data["张晶"]["insights"]["guest_name"] = "张晶"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return True
    except Exception as e:
        print(f"  ❌ 修正失败: {e}")
        return False

def fix_markdown_file(file_path: Path):
    """修正Markdown文件中的错误信息"""
    if not file_path.exists():
        return False
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 修正曾鸣的身份
        content = re.sub(
            r'### 曾鸣[^#]*\*\*身份\*\*:\s*[^\n]*',
            lambda m: m.group(0).replace('智谱AI相关（需确认具体职位）', '正面连接创始人'),
            content
        )
        
        # 修正张晶的身份
        content = re.sub(
            r'### 张晶[^#]*\*\*身份\*\*:\s*[^\n]*',
            lambda m: m.group(0).replace('知乎副总裁、正面连接创始人', '知乎副总裁'),
            content
        )
        
        # 修正其他提及正面连接的文本
        # 在张晶部分移除正面连接相关描述
        content = re.sub(
            r'(### 张晶[^#]*)(正面连接[^#]*)',
            lambda m: m.group(1),
            content
        )
        
        # 在曾鸣部分添加正面连接相关描述
        content = re.sub(
            r'(### 曾鸣[^#]*\*\*播客/作品\*\*:[^\n]*)',
            lambda m: m.group(0) + '\n\n**正面连接**：专注深度非虚构和特稿写作，前三大文章一年内超过300万观看量',
            content
        )
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return True
    except Exception as e:
        print(f"  ❌ 修正失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("修正嘉宾信息错误")
    print("=" * 60)
    print()
    print("根据用户指正：")
    print("  - 曾鸣：正面连接创始人（而非智谱AI）")
    print("  - 张晶：知乎副总裁（而非正面连接创始人）")
    print()
    
    project_root = Path(__file__).parent.parent
    fixed_files = []
    
    # 需要修正的文件列表
    files_to_fix = [
        # JSON文件
        project_root / "research" / "other_guests_analysis.json",
        project_root / "research" / "guest_info_structure.json",
        project_root / "outputs" / "guest_profiles.json",
        project_root / "outputs" / "interview_questions.json",
        # Markdown文件
        project_root / "research" / "other_guests_summary.md",
        project_root / "outputs" / "research_notes.md",
        project_root / "outputs" / "guest_profiles_zh.md",
        project_root / "outputs" / "guest_profiles_en.md",
        project_root / "outputs" / "guest_profiles_bilingual.md",
        project_root / "outputs" / "interview_outline.md",
        # 其他文件
        project_root / "research" / "guest_info_collection.md",
    ]
    
    print("开始修正文件...")
    print()
    
    for file_path in files_to_fix:
        if not file_path.exists():
            print(f"  ⚠️  文件不存在: {file_path.name}")
            continue
        
        print(f"  修正: {file_path.name}")
        
        if file_path.suffix == '.json':
            if fix_json_file(file_path):
                fixed_files.append(file_path)
                print(f"    ✅ 已修正")
            else:
                print(f"    ❌ 修正失败")
        else:
            if fix_markdown_file(file_path):
                fixed_files.append(file_path)
                print(f"    ✅ 已修正")
            else:
                print(f"    ❌ 修正失败")
    
    print()
    print(f"✅ 共修正 {len(fixed_files)} 个文件")
    print()
    print("⚠️  注意：Python脚本文件需要手动修正")
    print("   - scripts/analyze_other_guests.py")
    print("   - scripts/create_guest_profiles.py")
    print("   - scripts/design_interview_questions.py")
    print("   - scripts/collect_guest_info.py")

if __name__ == "__main__":
    main()

