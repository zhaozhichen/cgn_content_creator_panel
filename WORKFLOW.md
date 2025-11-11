# Panel访谈准备流程

## 当前进度

### ✅ 已完成
1. **项目结构设置** - 已完成
2. **播客下载** - 已完成（12个音频文件）
3. **转录脚本配置** - 已完成（使用Gemini 2.5 Flash，已配置区分主播/嘉宾观点）
4. **分析脚本配置** - 已完成（使用Gemini API分析，不使用关键词检索）
5. **信息收集指南** - 已完成

### ⏳ 进行中
1. **音频转录** - 进行中
   - 进度：2/12 (16.7%)
   - 已完成：起朱楼宴宾客_翁放（2期）
   - 等待：剩余10个文件

### 📋 待执行（等待转录完成后）
1. **分析转录文本** - 使用Gemini API提取主播观点
2. **收集其他信息源** - 搜索嘉宾在公众号、微博等平台的信息
3. **整理研究笔记** - 汇总所有嘉宾信息
4. **设计访谈问题** - 为7位嘉宾各设计1个定制问题
5. **制定访谈大纲** - 包含时间分配和问题顺序
6. **制作嘉宾简介卡片** - 中英文版本

## 转录完成后执行步骤

### 1. 检查转录状态
```bash
python3 scripts/check_transcription_status.py
```

### 2. 分析转录文本
```bash
python3 scripts/analyze_transcriptions.py
```
这将使用Gemini API分析所有转录文本，提取主播（Panel嘉宾）的核心观点。

### 3. 继续后续任务
- 收集其他信息源
- 整理研究笔记
- 设计访谈问题

## 重要说明

- **主播 vs 嘉宾**：Panel的嘉宾是播客主播，而非播客节目中邀请的访谈对象
- **分析重点**：重点关注主播的观点、观察、提问方式和内容创作理念
- **不使用关键词检索**：使用Gemini API进行语义分析，而非简单的关键词匹配

## 文件结构

```
cgn_podcast/
├── podcasts/              # 下载的音频文件
├── transcriptions/        # 转录文本（进行中）
├── research/              # 研究笔记和分析结果
├── scripts/               # Python脚本
│   ├── download_podcasts_simple.py      # 下载播客
│   ├── transcribe_with_gemini.py       # 转录音频
│   ├── analyze_transcriptions.py       # 分析转录文本
│   ├── collect_guest_info.py           # 收集嘉宾信息
│   └── check_transcription_status.py   # 检查转录状态
└── outputs/               # 最终交付物（待生成）
    ├── research_notes.md
    ├── interview_outline.md
    └── guest_profiles.md
```

## 后续工作流程

1. ✅ 等待转录完成（当前进度：16.7%）
2. ⏳ 分析转录文本（Gemini API）
3. ⏳ 收集其他信息源
4. ⏳ 整理研究笔记
5. ⏳ 设计访谈问题
6. ⏳ 制定访谈大纲
7. ⏳ 制作嘉宾简介卡片

