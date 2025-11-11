# CGN Content Creator Panel

Research and interview preparation materials for the CGN Content Creator Panel discussion.

## Overview

This project contains automated scripts and research materials for preparing a panel discussion with 7 guests (4 podcast hosts from Xiaoyuzhou FM and 3 other prominent figures).

## Project Structure

```
.
├── scripts/              # Automation scripts
│   ├── download_podcasts_simple.py    # Download podcast episodes
│   ├── transcribe_with_gemini.py      # Transcribe audio using Gemini API
│   ├── analyze_transcriptions.py      # Analyze transcriptions
│   ├── collect_guest_info.py          # Collect guest information
│   ├── design_interview_questions.py  # Design interview questions
│   └── auto_complete_workflow.py      # Main automation workflow
├── outputs/              # Generated output files
│   ├── research_notes.md              # Consolidated research notes
│   ├── interview_outline.md           # Interview outline
│   ├── interview_questions.json       # Interview questions
│   └── guest_profiles_*.md            # Guest profile cards
├── research/             # Research data and analysis
│   ├── host_insights_analysis.json    # Host insights from podcasts
│   └── other_guests_analysis.json     # Analysis of other guests
└── requirements.txt      # Python dependencies
```

## Features

- **Automated Podcast Download**: Downloads episodes from Xiaoyuzhou FM
- **Audio Transcription**: Uses Google Gemini API for Chinese audio transcription
- **Semantic Analysis**: Extracts insights using Gemini API semantic analysis
- **Guest Research**: Collects and analyzes information about panel guests
- **Interview Design**: Generates customized interview questions and outlines

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure API keys:
   - Set `GEMINI_API_KEY` environment variable or update in scripts

## Usage

Run the complete automated workflow:
```bash
python3 scripts/auto_complete_workflow.py
```

## Panel Guests

1. **黄俊杰** - 晚点聊播客主播
2. **李路野** - 知行小酒馆播客主播
3. **李翔** - 高能量播客主播
4. **翁放** - 起朱楼宴宾客播客主播
5. **潘乱** - 知名科技评论人
6. **曾鸣** - 正面连接创始人
7. **张晶** - 知乎副总裁

## Output Files

- `outputs/research_notes.md` - Comprehensive research notes for all guests
- `outputs/interview_outline.md` - Complete interview outline with timing
- `outputs/interview_questions.json` - Structured interview questions
- `outputs/guest_profiles_*.md` - Bilingual guest profile cards

## Notes

- Audio files (MP3) are excluded from the repository
- Transcription files can be regenerated using the scripts
- All analysis uses Google Gemini API for semantic understanding

