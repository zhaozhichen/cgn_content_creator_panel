#!/bin/bash
# 转录状态检查脚本

echo "🔍 转录状态快速检查"
echo "===================="

# 检查转录文件
if [ -f "transcriptions/曾鸣_采访/面对复杂_通过非虚构写作与社会正面连接_新闻实验室17.txt" ]; then
    echo ""
    echo "✅ 转录文件已存在"
    ls -lh "transcriptions/曾鸣_采访/面对复杂_通过非虚构写作与社会正面连接_新闻实验室17.txt"
    echo ""
    echo "文件大小变化（最近5次检查）："
    stat -f "%z %Sm" "transcriptions/曾鸣_采访/面对复杂_通过非虚构写作与社会正面连接_新闻实验室17.txt"
else
    echo ""
    echo "⏳ 转录文件尚未生成"
fi

# 检查进程
echo ""
echo "🔍 检查转录相关进程："
ps aux | grep -i "python.*transcribe\|python.*gemini" | grep -v grep || echo "   未发现相关进程"

# 检查文件是否被占用
echo ""
echo "🔍 检查音频文件占用："
lsof "podcasts/曾鸣_采访/面对复杂_通过非虚构写作与社会正面连接_新闻实验室17.mp3" 2>/dev/null || echo "   音频文件未被占用"

