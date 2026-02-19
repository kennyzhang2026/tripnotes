# 游记助手 - 开发指南

本文档介绍游记助手项目的开发相关内容。

---

## 1. 项目结构

```
trip_note/
├── app.py                          # 主应用入口
├── pages/                          # 多页面应用
│   ├── 1_登录.py
│   ├── 2_注册.py
│   └── 3_创建游记.py
├── clients/                        # 客户端模块
│   ├── ai_client.py                # AI客户端(DeepSeek)
│   ├── ocr_client.py               # OCR客户端(阿里云)
│   ├── image_client.py             # 图片存储(阿里云OSS)
│   ├── asr_client.py               # 语音识别(阿里云ASR)
│   ├── feishu_client.py            # 飞书多维表格
│   ├── user_client.py              # 用户数据
│   └── auth_client.py              # 认证
├── utils/                          # 工具模块
│   ├── config.py                   # 配置管理
│   ├── prompts.py                  # 提示词模板
│   ├── auth.py                     # 认证工具
│   └── image_utils.py              # 图片处理
├── docs/                           # 文档
│   ├── TABLE_SETUP.md
│   ├── ALIYUN_SETUP.md
│   └── DEVELOPMENT_GUIDE.md
├── .streamlit/
│   └── secrets.toml.example        # 配置模板
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 2. 本地开发

### 2.1 环境准备

```bash
# 克隆项目
git clone <repository-url>
cd trip_note

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt
```

### 2.2 配置密钥

```bash
# 复制配置模板
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# 编辑配置，填入真实密钥
vim .streamlit/secrets.toml
```

### 2.3 运行应用

```bash
streamlit run app.py
```

---

## 3. 部署

### 3.1 Streamlit Cloud 部署

1. 将代码推送到 GitHub
2. 访问 [Streamlit Cloud](https://share.streamlit.io/)
3. 点击"New app"
4. 选择仓库和文件
5. 在 Secrets 中配置所有密钥

### 3.2 注意事项

- ASR 功能可能需要额外处理，因为依赖本地音频文件
- 确保所有服务密钥都已配置
- 部署后测试各项功能

---

## 4. 开发分支策略

```bash
# 主分支
master          # 稳定版本

# 功能分支
feature/v1.0-init        # 项目初始化 (当前)
feature/v1.0-clients     # 核心客户端开发
feature/v1.0-ai          # AI集成
feature/v1.0-ui          # UI开发
feature/v1.0-test        # 测试和部署
```

---

## 5. 测试

### 5.1 单元测试

```bash
# 运行测试
pytest tests/
```

### 5.2 手动测试流程

1. 用户注册 → 登录
2. 上传照片 → OCR识别
3. 添加文字备注 → 语音转文字
4. 生成游记 → 保存到飞书
5. 查看游记列表

---

## 6. 常见问题

### Q1: OCR 识别失败
- 检查 AccessKey 是否正确
- 确认 OCR 服务已开通
- 检查图片格式和大小

### Q2: OSS 上传失败
- 检查 Bucket 是否创建
- 确认 Endpoint 配置正确
- 检查读写权限设置

### Q3: 飞书 API 调用失败
- 检查 App Token 和 Table ID
- 确认应用权限已配置
- 检查表格字段是否正确

### Q4: AI 生成失败
- 检查 DeepSeek API Key
- 确认 API 额度充足
- 检查网络连接

---

## 7. 扩展功能建议

- [ ] 用户个人资料管理
- [ ] 游记编辑/删除功能
- [ ] 游记分享功能
- [ ] 游记导出 (PDF/Markdown)
- [ ] 地图集成
- [ ] 视频支持
- [ ] 社交功能 (评论/点赞)
