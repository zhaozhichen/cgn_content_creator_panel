# CGN Content Creator Panel

Research and interview preparation materials for the CGN Content Creator Panel discussion at Google NYC.

## Overview

This project contains automated scripts and comprehensive research materials for preparing a panel discussion with 7 prominent Chinese content creators. The project uses AI-powered analysis (Google Gemini API) to extract insights from podcast transcriptions and generate customized interview questions and outlines.

## Project Structure

```
.
├── scripts/              # Automation scripts
│   ├── download_podcasts_simple.py    # Download podcast episodes from Xiaoyuzhou FM
│   ├── transcribe_with_gemini.py      # Transcribe audio using Gemini API
│   ├── analyze_transcriptions.py      # Analyze transcriptions to extract host insights
│   ├── analyze_other_guests.py        # Analyze information for non-podcast guests
│   ├── design_interview_questions.py  # Design customized interview questions
│   ├── complete_research_and_outline.py  # Generate research notes and interview outline
│   ├── process_new_podcasts.py       # Process new podcasts (transcription + analysis)
│   └── ...                            # Additional utility scripts
├── outputs/              # Generated output files
│   ├── research_notes.md              # Comprehensive research notes for all 7 guests
│   ├── interview_outline.md           # Complete interview outline with timing and questions
│   ├── interview_questions.json       # Structured interview questions (JSON format)
│   ├── guest_profiles_zh.md          # Guest profile cards (Chinese)
│   ├── guest_profiles_en.md           # Guest profile cards (English)
│   ├── guest_profiles_bilingual.md    # Guest profile cards (Bilingual)
│   └── guest_profiles.json           # Guest profiles (JSON format)
├── research/             # Research data and analysis
│   ├── host_insights_analysis.json    # Detailed host insights from podcast analysis
│   ├── host_insights_summary.md       # Summary of host insights
│   ├── other_guests_analysis.json     # Analysis of non-podcast guests
│   ├── other_guests_summary.md        # Summary of other guests
│   ├── guest_info_structure.json     # Guest information structure
│   └── guest_info_collection.md      # Guest information collection guide
├── podcasts/             # Downloaded podcast audio files (not in git)
├── transcriptions/       # Transcribed podcast texts (in git)
└── requirements.txt     # Python dependencies
```

## Features

- **Automated Podcast Download**: Downloads episodes from Xiaoyuzhou FM (小宇宙)
- **Audio Transcription**: Uses Google Gemini 2.5 Flash API for Chinese audio transcription with speaker identification
- **Semantic Analysis**: Extracts insights using Gemini API semantic analysis across multiple dimensions:
  - Professional observations
  - Content creation philosophy
  - Industry insights
  - Personal views
  - Discussion topics
  - Expression style
- **Guest Research**: Collects and analyzes information about all panel guests
- **Interview Design**: Generates customized interview questions and outlines based on analysis
- **Multi-language Support**: Generates bilingual (Chinese/English) guest profiles

## Panel Guests

### Podcast Hosts (6 guests with podcasts)

1. **黄俊杰 (Junjie Huang)**
   - 晚点LatePost联合创始人兼总编辑
   - Podcast: 晚点聊 LateTalk
   - Focus: In-depth business reporting in internet and technology sectors

2. **李路野 (Luye Li)**
   - 「有知有行」市场经理
   - Podcast: 知行小酒馆
   - Focus: Investment understanding and long-term investment practices

3. **李翔 (Xiang Li)**
   - 资深媒体人，「高能量」播客创始人兼主播，《详谈》系列作者
   - Podcast: 高能量
   - Focus: Business observations and contemporary business history

4. **翁放 (David Weng)**
   - 财经评论人、内容创作者，「起朱楼宴宾客」播客主播
   - Podcast: 起朱楼宴宾客
   - Focus: Investment and finance insights

5. **潘乱 (Luan Pan)**
   - 自媒体人，「乱翻书」播客创始人兼主播
   - Podcast: 乱翻书
   - Focus: Business and technology commentary (famous for "腾讯没有梦想" article)

6. **曾鸣 (Ming Zeng)**
   - 独立媒体「正面连接」创始人
   - Podcast: 正面连接
   - Focus: In-depth non-fiction and feature storytelling

### Other Guests (1 guest)

7. **张晶 (Selina Zhang)**
   - 知乎副总裁
   - Focus: Content platform operations and community building

## Output Files

### Main Outputs (`outputs/`)

- **`research_notes.md`** - Comprehensive research notes for all 7 guests, including:
  - Professional observations
  - Content creation philosophy
  - Industry insights
  - Based on analysis of 10 podcast episodes per host

- **`interview_outline.md`** - Complete interview outline with:
  - Time allocation (1 hour total)
  - Customized questions for each guest
  - General questions about Google and AI
  - Discussion points and rationale

- **`interview_questions.json`** - Structured interview questions in JSON format:
  - Custom questions for each guest
  - Google-related questions
  - AI-related questions
  - Rationale and key discussion points

- **`guest_profiles_*.md`** - Guest profile cards in multiple formats:
  - Chinese version (`guest_profiles_zh.md`)
  - English version (`guest_profiles_en.md`)
  - Bilingual version (`guest_profiles_bilingual.md`)
  - JSON format (`guest_profiles.json`)

### Research Data (`research/`)

- **`host_insights_analysis.json`** - Detailed JSON analysis of podcast hosts
- **`host_insights_summary.md`** - Summary of host insights
- **`other_guests_analysis.json`** - Analysis of non-podcast guests
- **`other_guests_summary.md`** - Summary of other guests
- **`guest_info_structure.json`** - Guest information structure and metadata
- **`guest_info_collection.md`** - Guide for collecting guest information

## Setup

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Configure API keys:**
   - Create a `.env` file (see `.env.example`)
   - Set `GEMINI_API_KEY` environment variable:
   ```bash
   export GEMINI_API_KEY='your-api-key-here'
   ```
   Or add to `.env` file:
   ```
   GEMINI_API_KEY=your-api-key-here
   ```

3. **Install Python dependencies:**
   - `google-generativeai` - For Gemini API
   - `python-dotenv` - For environment variable management
   - `requests` - For HTTP requests
   - `beautifulsoup4` - For HTML parsing

## Usage

### Complete Workflow

Run the complete automated workflow:
```bash
python3 scripts/auto_complete_workflow.py
```

### Individual Steps

1. **Download podcasts:**
```bash
python3 scripts/download_podcasts_simple.py
```

2. **Transcribe audio:**
```bash
python3 scripts/transcribe_with_gemini.py
```

3. **Analyze transcriptions:**
```bash
python3 scripts/analyze_transcriptions.py
```

4. **Analyze other guests:**
```bash
python3 scripts/analyze_other_guests.py
```

5. **Generate research notes and outline:**
```bash
python3 scripts/complete_research_and_outline.py
```

6. **Design interview questions:**
```bash
python3 scripts/design_interview_questions.py
```

## Analysis Methodology

The project uses Google Gemini API for semantic analysis of podcast transcriptions. The analysis focuses on:

1. **Professional Observations**: Industry insights and professional perspectives
2. **Content Creation Philosophy**: Approaches to content creation and storytelling
3. **Industry Insights**: Observations about relevant industries
4. **Personal Views**: Personal opinions and values
5. **Discussion Topics**: Topics frequently discussed
6. **Expression Style**: Communication and expression characteristics

Each podcast host has 10 episodes analyzed to ensure comprehensive understanding.

## Data Sources

- **Podcasts**: Downloaded from Xiaoyuzhou FM (小宇宙)
  - 晚点聊 (LateTalk)
  - 知行小酒馆
  - 高能量
  - 起朱楼宴宾客
  - 乱翻书
  - 正面连接

- **Guest Information**: Collected from public sources and verified

## Notes

- Audio files (MP3) are excluded from the repository (see `.gitignore`)
- Transcription files (`.txt`) are included in the repository
- All analysis uses Google Gemini API for semantic understanding
- The project maintains accuracy through cross-validation and error correction
- Guest information has been verified and corrected based on authoritative sources

## Repository

GitHub: https://github.com/zhaozhichen/cgn_content_creator_panel

## License

This project is for internal use by Chinese Google Network (CGN) for panel discussion preparation.
