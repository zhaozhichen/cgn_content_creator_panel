#!/usr/bin/env python3
"""
使用Gemini API转录音频文件
"""

import os
import sys
from pathlib import Path
import json
import time
from typing import List, Dict

try:
    import google.generativeai as genai
except ImportError:
    print("请安装 google-generativeai: pip install google-generativeai")
    sys.exit(1)

# Gemini API配置 - 从环境变量读取
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    print("❌ 错误: 未设置 GEMINI_API_KEY 环境变量")
    print("   请设置: export GEMINI_API_KEY='your-api-key'")
    sys.exit(1)

def setup_gemini():
    """配置Gemini API"""
    genai.configure(api_key=GEMINI_API_KEY)
    return genai

def transcribe_audio_with_gemini(audio_file: Path, output_file: Path = None) -> str:
    """使用Gemini API转录音频文件"""
    print(f"\n转录音频: {audio_file.name}")
    
    if not audio_file.exists():
        print(f"  ❌ 文件不存在: {audio_file}")
        return None
    
    # 检查文件大小
    file_size_mb = audio_file.stat().st_size / (1024 * 1024)
    print(f"  文件大小: {file_size_mb:.1f}MB")
    
    # Gemini API支持的最大文件大小通常是20MB，但Gemini 1.5支持更大文件
    # 如果超过限制，可能需要使用其他方法
    
    try:
        # 初始化Gemini (已在setup_gemini中配置)
        if not GEMINI_API_KEY:
            print("  ❌ 错误: GEMINI_API_KEY 未设置")
            return None
        
        # 上传音频文件
        print(f"  上传音频文件到Gemini...")
        uploaded_file = genai.upload_file(
            path=str(audio_file),
            display_name=audio_file.name
        )
        print(f"  文件已上传: {uploaded_file.name}")
        
        # 等待文件处理完成
        max_wait = 300  # 最多等待5分钟
        wait_time = 0
        while uploaded_file.state.name == "PROCESSING":
            if wait_time >= max_wait:
                print(f"  ⚠️  处理超时")
                break
            print(f"  处理中... ({wait_time}秒)")
            time.sleep(10)
            wait_time += 10
            uploaded_file = genai.get_file(uploaded_file.name)
        
        if uploaded_file.state.name == "FAILED":
            print(f"  ❌ 文件处理失败")
            try:
                genai.delete_file(uploaded_file.name)
            except:
                pass
            return None
        
        if uploaded_file.state.name != "ACTIVE":
            print(f"  ⚠️  文件状态异常: {uploaded_file.state.name}")
        
        # 使用Gemini模型进行转录
        print(f"  开始转录...")
        # 使用gemini-2.5-flash模型
        try:
            model = genai.GenerativeModel("models/gemini-2.5-flash")
            print(f"  使用模型: gemini-2.5-flash")
        except Exception as e:
            print(f"  ⚠️  无法使用gemini-2.5-flash: {e}")
            # 备用方案：尝试其他模型
            try:
                model = genai.GenerativeModel("models/gemini-2.0-flash")
                print(f"  使用备用模型: gemini-2.0-flash")
            except:
                model = genai.GenerativeModel("gemini-pro")
                print(f"  使用默认模型: gemini-pro")
        
        prompt = """请将这段中文播客音频完整转录为文字。重要要求：

**关键要求**：
- 必须明确区分"主播/主持人"和"节目嘉宾"的发言
- 主播是播客的主持人/制作者，通常是提问者和讨论引导者
- 节目嘉宾是播客邀请的访谈对象
- 在转录时，请清晰标注说话人身份，例如：[主播]、[嘉宾]

**转录要求**：
1. 保持对话的原始顺序和时间顺序
2. 明确区分并标注说话人：使用[主播]、[嘉宾]、[其他]等标签
3. 主播的发言要特别标记清楚（这些是Panel嘉宾的观点）
4. 保留重要的语气词和停顿标记
5. 使用中文标点符号
6. 如果内容较长，请分段输出，每段标明大致时间点
7. 保持原意，不要添加或删减内容
8. 转录格式示例：
   [主播]：今天我们要聊的话题是...
   [嘉宾]：我认为这个问题...
   [主播]：那你觉得...
"""
        
        print(f"  发送转录请求...")
        response = model.generate_content([uploaded_file, prompt])
        
        transcription = response.text
        
        # 保存转录文本
        if output_file:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(transcription)
            print(f"  ✅ 转录完成，已保存到: {output_file}")
            print(f"  转录文本长度: {len(transcription)} 字符")
        else:
            print(f"  ✅ 转录完成")
        
        # 清理上传的文件
        try:
            genai.delete_file(uploaded_file.name)
            print(f"  已清理上传文件")
        except Exception as e:
            print(f"  清理文件时出错: {e}")
        
        return transcription
        
    except Exception as e:
        print(f"  ❌ 转录失败: {e}")
        import traceback
        traceback.print_exc()
        # 尝试清理
        try:
            if 'uploaded_file' in locals():
                genai.delete_file(uploaded_file.name)
        except:
            pass
        return None

def batch_transcribe(podcasts_dir: Path, output_dir: Path = None):
    """批量转录音频文件"""
    if output_dir is None:
        output_dir = Path(__file__).parent.parent / "transcriptions"
    
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 查找所有音频文件
    audio_files = []
    for ext in ['*.mp3', '*.m4a', '*.wav', '*.aac']:
        audio_files.extend(podcasts_dir.rglob(ext))
    
    if not audio_files:
        print(f"未找到音频文件在: {podcasts_dir}")
        return
    
    print(f"找到 {len(audio_files)} 个音频文件")
    
    results = []
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}]")
        
        # 生成输出文件名
        rel_path = audio_file.relative_to(podcasts_dir)
        output_file = output_dir / rel_path.with_suffix('.txt')
        
        # 如果已存在转录文件，跳过
        if output_file.exists():
            print(f"  跳过（已存在）: {output_file.name}")
            with open(output_file, 'r', encoding='utf-8') as f:
                transcription = f.read()
        else:
            transcription = transcribe_audio_with_gemini(audio_file, output_file)
        
        if transcription:
            results.append({
                'audio_file': str(audio_file),
                'transcription_file': str(output_file),
                'status': 'success'
            })
        
        time.sleep(2)  # 避免API请求过快
    
    # 保存转录记录
    record_file = output_dir / "transcription_records.json"
    with open(record_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 批量转录完成！记录已保存到: {record_file}")
    print(f"成功转录: {len(results)} 个文件")

def main():
    """主函数"""
    podcasts_dir = Path(__file__).parent.parent / "podcasts"
    output_dir = Path(__file__).parent.parent / "transcriptions"
    
    if not podcasts_dir.exists():
        print(f"播客目录不存在: {podcasts_dir}")
        print("请先运行 download_podcasts.py 下载音频文件")
        return
    
    batch_transcribe(podcasts_dir, output_dir)

if __name__ == "__main__":
    main()

