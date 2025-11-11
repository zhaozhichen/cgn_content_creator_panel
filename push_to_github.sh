#!/bin/bash

# Script to push to GitHub repository: cgn_content_creator_panel

echo "🚀 准备推送到GitHub..."
echo ""

# Check if remote already exists
if git remote get-url origin > /dev/null 2>&1; then
    echo "⚠️  远程仓库已存在:"
    git remote -v
    read -p "是否要更新远程URL? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入您的GitHub用户名: " GITHUB_USER
        read -p "使用HTTPS还是SSH? (https/ssh) " PROTOCOL
        
        if [ "$PROTOCOL" = "ssh" ]; then
            git remote set-url origin "git@github.com:${GITHUB_USER}/cgn_content_creator_panel.git"
        else
            git remote set-url origin "https://github.com/${GITHUB_USER}/cgn_content_creator_panel.git"
        fi
    else
        echo "使用现有远程仓库"
    fi
else
    read -p "请输入您的GitHub用户名: " GITHUB_USER
    read -p "使用HTTPS还是SSH? (https/ssh) " PROTOCOL
    
    if [ "$PROTOCOL" = "ssh" ]; then
        git remote add origin "git@github.com:${GITHUB_USER}/cgn_content_creator_panel.git"
    else
        git remote add origin "https://github.com/${GITHUB_USER}/cgn_content_creator_panel.git"
    fi
fi

echo ""
echo "📋 请确保您已经在GitHub上创建了仓库: cgn_content_creator_panel"
echo "   访问: https://github.com/new"
echo ""
read -p "仓库已创建? (y/n) " -n 1 -r
echo

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "🔄 设置分支为main..."
    git branch -M main
    
    echo "📤 推送到GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ 成功推送到GitHub!"
        echo "   仓库地址: $(git remote get-url origin | sed 's/\.git$//' | sed 's/git@github.com:/https:\/\/github.com\//')"
    else
        echo ""
        echo "❌ 推送失败，请检查："
        echo "   1. 仓库是否已创建"
        echo "   2. 认证信息是否正确"
        echo "   3. 网络连接是否正常"
    fi
else
    echo ""
    echo "请先创建仓库，然后重新运行此脚本"
fi

