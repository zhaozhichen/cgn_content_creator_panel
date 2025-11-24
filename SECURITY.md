# 安全说明

## API Key 管理

### 当前状态
- ✅ 所有硬编码的API key已从代码中移除
- ✅ API key已从Git历史记录中完全清除
- ✅ 所有脚本现在使用环境变量 `GEMINI_API_KEY`

### 重要安全措施

#### 1. 撤销已泄露的API Key
由于API key曾经被提交到GitHub，**强烈建议立即撤销旧的API key并创建新的**：

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 导航到 **APIs & Services** > **Credentials**
3. 找到并删除旧的Gemini API key
4. 创建新的API key
5. 更新本地环境变量：
   ```bash
   export GEMINI_API_KEY='your-new-api-key'
   ```

#### 2. 检查API使用情况
在Google Cloud Console中检查：
- API key的使用日志
- 是否有未授权的访问
- 使用配额和限制

#### 3. 环境变量配置

**方法1: 使用.env文件（推荐）**
```bash
# 复制模板
cp .env.example .env

# 编辑.env文件，添加您的API key
# GEMINI_API_KEY=your-api-key-here
```

**方法2: 直接设置环境变量**
```bash
export GEMINI_API_KEY='your-api-key-here'
```

**方法3: 在shell配置文件中永久设置**
```bash
# 添加到 ~/.zshrc 或 ~/.bashrc
echo 'export GEMINI_API_KEY="your-api-key-here"' >> ~/.zshrc
source ~/.zshrc
```

### 安全最佳实践

1. **永远不要提交API key到Git**
   - `.env` 文件已添加到 `.gitignore`
   - 使用 `.env.example` 作为模板

2. **定期轮换API key**
   - 建议每3-6个月更换一次
   - 如果怀疑泄露，立即撤销

3. **限制API key权限**
   - 在Google Cloud Console中设置适当的限制
   - 限制IP地址、引用来源等

4. **监控API使用**
   - 定期检查使用日志
   - 设置使用配额和警报

### 如果API key泄露了怎么办？

1. **立即撤销泄露的key**
2. **创建新的API key**
3. **检查使用日志，确认是否有未授权访问**
4. **更新所有使用该key的环境**
5. **通知团队成员更新他们的配置**

### 相关文件

- `.env.example` - 环境变量模板
- `.gitignore` - 确保.env文件不会被提交
- `scripts/*.py` - 所有脚本现在从环境变量读取API key


