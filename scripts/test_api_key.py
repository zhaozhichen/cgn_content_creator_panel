#!/usr/bin/env python3
"""测试Gemini API key是否可用"""

import os
import sys
from pathlib import Path

# 从.env文件加载
env_file = Path(__file__).parent.parent / ".env"
if env_file.exists():
    with open(env_file, 'r') as f:
        for line in f:
            if line.strip() and not line.startswith('#') and '=' in line:
                key, value = line.split('=', 1)
                os.environ[key.strip()] = value.strip().strip('"').strip("'")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ GEMINI_API_KEY未设置")
    sys.exit(1)

print(f"✅ API key已加载（长度: {len(GEMINI_API_KEY)}）")
print(f"   前10字符: {GEMINI_API_KEY[:10]}...")
print()

try:
    import google.generativeai as genai
    genai.configure(api_key=GEMINI_API_KEY)
    
    print("测试API连接...")
    model = genai.GenerativeModel('gemini-2.0-flash')
    response = model.generate_content("Say hello")
    
    print("✅ API key可用！连接成功！")
    print(f"   响应: {response.text[:50]}...")
    
except Exception as e:
    error_msg = str(e)
    print(f"❌ API key错误:")
    print(f"   {error_msg}")
    
    if "leaked" in error_msg.lower() or "403" in error_msg:
        print()
        print("💡 解决方案:")
        print("   1. 在Google Cloud Console创建全新的API key")
        print("   2. 确保新API key从未被使用过")
        print("   3. 更新.env文件")
    
    sys.exit(1)

