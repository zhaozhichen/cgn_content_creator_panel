#!/bin/bash

echo "🚀 自动创建GitHub仓库并推送代码"
echo ""

# 检查仓库是否已存在
echo "检查仓库是否已存在..."
if curl -s https://api.github.com/repos/zhaozhichen/cgn_content_creator_panel | grep -q '"name"'; then
    echo "✅ 仓库已存在"
    REPO_EXISTS=true
else
    echo "❌ 仓库不存在，需要创建"
    REPO_EXISTS=false
fi

echo ""
echo "请选择认证方式："
echo "1. 使用GitHub Personal Access Token (推荐)"
echo "2. 使用SSH (需要密钥已添加到GitHub)"
echo "3. 手动操作指南"
read -p "请选择 (1/2/3): " choice

case $choice in
    1)
        read -p "请输入您的GitHub Personal Access Token: " GITHUB_TOKEN
        if [ -z "$GITHUB_TOKEN" ]; then
            echo "❌ Token不能为空"
            exit 1
        fi
        
        # 创建仓库（如果不存在）
        if [ "$REPO_EXISTS" = false ]; then
            echo "创建仓库..."
            curl -X POST \
                -H "Authorization: token $GITHUB_TOKEN" \
                -H "Accept: application/vnd.github.v3+json" \
                https://api.github.com/user/repos \
                -d '{"name":"cgn_content_creator_panel","private":false}' 2>&1 | grep -E '"name"|"message"' || echo "仓库创建中..."
        fi
        
        # 切换到HTTPS并使用token推送
        git remote set-url origin https://${GITHUB_TOKEN}@github.com/zhaozhichen/cgn_content_creator_panel.git
        git push -u origin main
        ;;
    2)
        echo "测试SSH连接..."
        if ssh -T git@github.com 2>&1 | grep -q "successfully authenticated\|Hi zhaozhichen"; then
            echo "✅ SSH已配置，开始推送..."
            git push -u origin main
        else
            echo "❌ SSH未配置"
            echo "请先添加SSH密钥到GitHub: https://github.com/settings/keys"
            exit 1
        fi
        ;;
    3)
        echo ""
        echo "📋 手动操作步骤："
        echo "1. 创建仓库: https://github.com/new (名称: cgn_content_creator_panel)"
        echo "2. 配置认证后运行: git push -u origin main"
        ;;
esac
