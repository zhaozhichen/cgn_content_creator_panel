#!/bin/bash
# 提取所有播客的最近3期单集ID

PODCASTS=(
  "61933ace1b4320461e91fd55:晚点聊_黄俊杰"
  "6013f9f58e2f7ee375cf4216:知行小酒馆_李路野"
  "62c6ae08c4eaa82b112b9c84:高能量_李翔"
  "61dd99a47b29652ff572257b:起朱楼宴宾客_翁放"
)

OUTPUT_DIR="podcasts"
mkdir -p "$OUTPUT_DIR"

for PODCAST in "${PODCASTS[@]}"; do
  IFS=':' read -r PODCAST_ID PODCAST_NAME <<< "$PODCAST"
  echo "=========================================="
  echo "处理播客: $PODCAST_NAME (ID: $PODCAST_ID)"
  echo "=========================================="
  
  # 获取播客页面
  HTML=$(curl -s "https://www.xiaoyuzhoufm.com/podcast/$PODCAST_ID" \
    -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
  
  # 提取单集链接
  EPISODES=$(echo "$HTML" | grep -o 'href="/episode/[^"]*"' | head -3 | sed 's/href="\/episode\///' | sed 's/"//')
  
  COUNT=1
  for EP_ID in $EPISODES; do
    echo ""
    echo "单集 $COUNT: $EP_ID"
    echo "获取单集页面..."
    
    EP_HTML=$(curl -s "https://www.xiaoyuzhoufm.com/episode/$EP_ID" \
      -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")
    
    # 尝试多种方式提取音频URL
    AUDIO_URL=$(echo "$EP_HTML" | grep -o '"audioUrl":"[^"]*"' | head -1 | sed 's/"audioUrl":"//' | sed 's/"//')
    
    if [ -z "$AUDIO_URL" ]; then
      AUDIO_URL=$(echo "$EP_HTML" | grep -o '"audio":"[^"]*"' | head -1 | sed 's/"audio":"//' | sed 's/"//')
    fi
    
    if [ -z "$AUDIO_URL" ]; then
      AUDIO_URL=$(echo "$EP_HTML" | grep -o 'https://[^"]*\.mp3[^"]*' | head -1)
    fi
    
    if [ -z "$AUDIO_URL" ]; then
      AUDIO_URL=$(echo "$EP_HTML" | grep -o 'https://[^"]*\.m4a[^"]*' | head -1)
    fi
    
    if [ -n "$AUDIO_URL" ]; then
      echo "找到音频URL: ${AUDIO_URL:0:60}..."
      
      # 保存信息
      PODCAST_DIR="$OUTPUT_DIR/$PODCAST_NAME"
      mkdir -p "$PODCAST_DIR"
      
      echo "$EP_ID|$AUDIO_URL" >> "$PODCAST_DIR/episodes_list.txt"
      
      # 尝试下载
      OUTPUT_FILE="$PODCAST_DIR/${COUNT}_${EP_ID}.mp3"
      echo "下载音频..."
      curl -s -L "$AUDIO_URL" \
        -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
        -H "Referer: https://www.xiaoyuzhoufm.com/" \
        --output "$OUTPUT_FILE" --fail-with-body 2>&1 | head -5
      
      if [ -f "$OUTPUT_FILE" ] && [ -s "$OUTPUT_FILE" ]; then
        FILE_SIZE=$(stat -f%z "$OUTPUT_FILE" 2>/dev/null || stat -c%s "$OUTPUT_FILE" 2>/dev/null || echo "0")
        FILE_SIZE_MB=$(echo "scale=2; $FILE_SIZE / 1024 / 1024" | bc 2>/dev/null || echo "计算中...")
        echo "✅ 下载成功: $OUTPUT_FILE (${FILE_SIZE_MB}MB)"
      else
        echo "❌ 下载失败"
        rm -f "$OUTPUT_FILE"
      fi
    else
      echo "⚠️  无法找到音频URL"
    fi
    
    COUNT=$((COUNT + 1))
    sleep 2  # 避免请求过快
  done
  
  echo ""
  sleep 3  # 播客之间稍作延迟
done

echo ""
echo "=========================================="
echo "✅ 完成！"
echo "=========================================="

