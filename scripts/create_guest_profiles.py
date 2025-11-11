#!/usr/bin/env python3
"""
制作7位嘉宾的简介卡片（中英文）
"""

import json
from pathlib import Path

# Panel嘉宾信息（基于PDF）
GUEST_PROFILES = {
    "黄俊杰": {
        "name_en": "Junjie Huang",
        "title_zh": "晚点LatePost联合创始人兼总编辑",
        "title_en": "Co-founder and Editor-in-Chief of LatePost",
        "podcast": "晚点聊 LateTalk",
        "highlights_zh": [
            "专注互联网和科技领域的深度商业报道",
            "微信公众号超过120万订阅者",
            "2025年上半年报道观看量超过1200万次",
            "播客《晚点聊》提供最一手的科技访谈"
        ],
        "highlights_en": [
            "Focuses on in-depth business reporting in internet and technology sectors",
            "Over 1.2 million WeChat subscribers",
            "Over 12 million views in first half of 2025",
            "Podcast 'LateTalk' delivers first-hand tech interviews"
        ]
    },
    "李路野": {
        "name_en": "Luye Li",
        "title_zh": "有知有行营销负责人",
        "title_en": "Marketing Manager of Youzhi Youxing",
        "podcast": "知行小酒馆",
        "highlights_zh": [
            "播客《知行小酒馆》帮助用户深化投资理解和实践长期投资",
            "播客订阅量超过800万",
            "致力于投资理财与美好生活的结合",
            "擅长引导用户深度思考"
        ],
        "highlights_en": [
            "Podcast '知行小酒馆' helps users deepen investment understanding",
            "Over 8 million podcast subscribers",
            "Combines investment with meaningful living",
            "Expert in guiding deep thinking"
        ]
    },
    "李翔": {
        "name_en": "Xiang Li",
        "title_zh": "《详谈》丛书作者、《高能量》主理人",
        "title_en": "Author of 'Detailed Conversations' series, Host of 'High Energy' podcast",
        "podcast": "高能量",
        "highlights_zh": [
            "《详谈》系列销量超过50万册，记录当代商业历史",
            "播客《高能量》从商业观察者视角重新理解日常现象",
            "深度对话商业实践者和价值创造者",
            "关注个人成长、职业转型和行业趋势"
        ],
        "highlights_en": [
            "'Detailed Conversations' series sold over 500,000 copies",
            "Podcast 'High Energy' reexamines everyday phenomena through business lens",
            "Deep dialogues with business practitioners and value creators",
            "Focuses on personal growth, career transitions, and industry trends"
        ]
    },
    "翁放": {
        "name_en": "David Weng",
        "title_zh": "《起朱楼宴宾客》主播",
        "title_en": "Host of '起朱楼宴宾客' podcast",
        "podcast": "起朱楼宴宾客",
        "highlights_zh": [
            "播客聚焦投资和金融洞察，对话金融界内行",
            "订阅量超过50万",
            "通过不同地域视角洞察国际间人才和资本竞争",
            "擅长宏观趋势分析和跨文化观察"
        ],
        "highlights_en": [
            "Podcast focuses on investment and finance insights",
            "Over 500,000 subscribers",
            "Observes international talent and capital competition through multi-regional perspectives",
            "Expert in macro trend analysis and cross-cultural observations"
        ]
    },
    "潘乱": {
        "name_en": "Luan Pan",
        "title_zh": "《乱翻书》主播",
        "title_en": "Founder and Host of 'Luan Books' podcast",
        "podcast": "乱翻书",
        "highlights_zh": [
            "2018年《腾讯没有梦想》成为现象级爆款",
            "播客《乱翻书》订阅量超过100万",
            "通过对话深入探讨商业和科技话题",
            "擅长挑战既有观点、揭示深层趋势"
        ],
        "highlights_en": [
            "2018 article 'Tencent Without Dreams' became viral with over 10 million views",
            "Podcast 'Luan Books' has over 1 million subscribers",
            "Deep dialogues on business and technology topics",
            "Expert at challenging conventional wisdom and revealing underlying trends"
        ]
    },
    "曾鸣": {
        "name_en": "Ming Zeng",
        "title_zh": "正面连接创始人",
        "title_en": "Founder of Positive Connection",
        "podcast": "无",
        "highlights_zh": [
            "正面连接专注于深度非虚构和特稿写作",
            "前三大文章在一年内获得超过300万观看量",
            "通过人性化的叙述，捕捉当代中国社会文化脉搏",
            "关注内容真实性、人文关怀和信息生态"
        ],
        "highlights_en": [
            "Positive Connection dedicated to in-depth non-fiction storytelling",
            "Top three articles garnered over 3 million views within a year",
            "Captures contemporary Chinese social and cultural pulse through human-centered narratives",
            "Focuses on content authenticity, humanistic care, and information ecosystem"
        ]
    },
    "张晶": {
        "name_en": "Selina Zhang",
        "title_zh": "知乎副总裁",
        "title_en": "Vice President of Zhihu",
        "podcast": "无",
        "highlights_zh": [
            "知乎是中国领先的问答和新闻聚合平台",
            "负责内容平台运营和社区建设",
            "关注内容生态和用户体验"
        ],
        "highlights_en": [
            "Zhihu is China's leading Q&A and news aggregation platform",
            "Responsible for content platform operations and community building",
            "Focuses on content ecosystem and user experience"
        ]
    }
}

def create_guest_profiles():
    """创建嘉宾简介卡片"""
    output_dir = Path(__file__).parent.parent / "outputs"
    output_dir.mkdir(exist_ok=True)
    
    # 中文版
    profiles_zh_file = output_dir / "guest_profiles_zh.md"
    with open(profiles_zh_file, 'w', encoding='utf-8') as f:
        f.write("# Panel嘉宾简介卡片（中文版）\n\n")
        f.write("用于Panel访谈开场介绍\n\n")
        f.write("---\n\n")
        
        for guest_name, profile in GUEST_PROFILES.items():
            f.write(f"## {guest_name}\n\n")
            f.write(f"**职位**: {profile['title_zh']}\n\n")
            if profile['podcast'] != "无":
                f.write(f"**播客**: {profile['podcast']}\n\n")
            f.write("**亮点**:\n\n")
            for highlight in profile['highlights_zh']:
                f.write(f"- {highlight}\n")
            f.write("\n---\n\n")
    
    # 英文版
    profiles_en_file = output_dir / "guest_profiles_en.md"
    with open(profiles_en_file, 'w', encoding='utf-8') as f:
        f.write("# Panel Guest Profiles (English)\n\n")
        f.write("For panel discussion introduction\n\n")
        f.write("---\n\n")
        
        for guest_name, profile in GUEST_PROFILES.items():
            f.write(f"## {profile['name_en']}\n\n")
            f.write(f"**Title**: {profile['title_en']}\n\n")
            if profile['podcast'] != "无":
                f.write(f"**Podcast**: {profile['podcast']}\n\n")
            f.write("**Highlights**:\n\n")
            for highlight in profile['highlights_en']:
                f.write(f"- {highlight}\n")
            f.write("\n---\n\n")
    
    # 双语对照版
    profiles_bilingual_file = output_dir / "guest_profiles_bilingual.md"
    with open(profiles_bilingual_file, 'w', encoding='utf-8') as f:
        f.write("# Panel嘉宾简介卡片（双语版）\n\n")
        f.write("Bilingual guest profiles for panel introduction\n\n")
        f.write("---\n\n")
        
        for guest_name, profile in GUEST_PROFILES.items():
            f.write(f"## {guest_name} / {profile['name_en']}\n\n")
            f.write(f"**职位 / Title**: {profile['title_zh']} / {profile['title_en']}\n\n")
            if profile['podcast'] != "无":
                f.write(f"**播客 / Podcast**: {profile['podcast']}\n\n")
            f.write("**亮点 / Highlights**:\n\n")
            for i, (zh, en) in enumerate(zip(profile['highlights_zh'], profile['highlights_en']), 1):
                f.write(f"{i}. **中文**: {zh}\n")
                f.write(f"   **English**: {en}\n\n")
            f.write("---\n\n")
    
    print(f"✅ 中文版已保存: {profiles_zh_file}")
    print(f"✅ 英文版已保存: {profiles_en_file}")
    print(f"✅ 双语版已保存: {profiles_bilingual_file}")
    
    # 保存JSON格式
    json_file = output_dir / "guest_profiles.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(GUEST_PROFILES, f, ensure_ascii=False, indent=2)
    
    print(f"✅ JSON格式已保存: {json_file}")

def main():
    """主函数"""
    print("=" * 60)
    print("制作嘉宾简介卡片")
    print("=" * 60)
    print()
    
    create_guest_profiles()
    
    print("\n✅ 所有简介卡片已完成！")

if __name__ == "__main__":
    main()

