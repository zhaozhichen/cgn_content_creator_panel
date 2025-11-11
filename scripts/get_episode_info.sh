#!/bin/bash
# 小宇宙播客单集信息提取脚本

PODCAST_ID=$1
LIMIT=${2:-3}

echo "获取播客ID: $PODCAST_ID 的最近 $LIMIT 期单集"

# 获取播客页面
HTML=$(curl -s "https://www.xiaoyuzhoufm.com/podcast/$PODCAST_ID" \
  -H "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36")

# 提取单集链接（从href中）
echo "$HTML" | grep -o 'href="/episode/[^"]*"' | head -$LIMIT | sed 's/href="//' | sed 's/"//' | while read -r ep_link; do
    EP_ID=$(echo "$ep_link" | sed 's/\/episode\///')
    echo "单集ID: $EP_ID"
    echo "链接: https://www.xiaoyuzhoufm.com$ep_link"
    echo "---"
done

