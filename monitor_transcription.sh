#!/bin/bash
# 转录进度监控脚本

AUDIO_FILE="podcasts/曾鸣_采访/面对复杂_通过非虚构写作与社会正面连接_新闻实验室17.mp3"
OUTPUT_FILE="transcriptions/曾鸣_采访/面对复杂_通过非虚构写作与社会正面连接_新闻实验室17.txt"

echo "🔍 转录进度监控"
echo "=================="
echo ""

# 检查音频文件
if [ -f "$AUDIO_FILE" ]; then
    AUDIO_SIZE=$(stat -f%z "$AUDIO_FILE" 2>/dev/null || stat -c%s "$AUDIO_FILE" 2>/dev/null)
    AUDIO_SIZE_MB=$((AUDIO_SIZE / 1024 / 1024))
    echo "✅ 音频文件: ${AUDIO_SIZE_MB} MB"
else
    echo "❌ 音频文件不存在"
    exit 1
fi

echo ""

# 检查转录文件
if [ -f "$OUTPUT_FILE" ]; then
    OUTPUT_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null)
    OUTPUT_SIZE_KB=$((OUTPUT_SIZE / 1024))
    MOD_TIME=$(stat -f%Sm "$OUTPUT_FILE" 2>/dev/null || stat -c%y "$OUTPUT_FILE" 2>/dev/null)
    
    echo "✅ 转录文件已存在"
    echo "   大小: ${OUTPUT_SIZE_KB} KB"
    echo "   修改时间: $MOD_TIME"
    echo ""
    
    # 估算进度（粗略）
    if [ $OUTPUT_SIZE_KB -gt 100 ]; then
        echo "📊 状态: 转录可能已完成或接近完成"
    else
        echo "📊 状态: 转录可能正在进行中"
    fi
else
    echo "⏳ 转录文件尚未生成"
    echo ""
    echo "📊 状态: 转录可能正在进行中，或尚未开始"
fi

echo ""

# 检查进程
echo "🔍 检查相关进程："
PROCESSES=$(ps aux | grep -E "python.*transcribe|python.*gemini" | grep -v grep)
if [ -n "$PROCESSES" ]; then
    echo "✅ 发现相关进程："
    echo "$PROCESSES" | head -3
else
    echo "⏳ 未发现明显的转录进程"
    echo "   （进程可能在后台运行，或已完成）"
fi

echo ""
echo "💡 提示："
echo "   - 100MB音频文件通常需要10-20分钟转录"
echo "   - 可以定期运行此脚本检查进度"
echo "   - 或使用: watch -n 30 ./monitor_transcription.sh"

