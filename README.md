# 游记助手 (Trip Note)

> 基于 AI 的图文游记生成应用

![Version](https://img.shields.io/badge/version-v0.3.1-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red)

---

## 项目简介

**游记助手**是一个基于 AI 的图文游记生成应用。用户可以拍照/上传照片、添加语音/文字评论，AI 自动整理成图文并茂的游记。支持 OCR 识别照片中的文字（如景区对联）并进行文化解释，保存到飞书多维表格。

### 核心功能

- [x] 快速登录（一键进入）
- [x] 批次照片上传（多选+拍照）
- [x] 语音输入转文字（内嵌按钮）
- [x] OCR 识别照片文字
- [x] AI 智能整理游记（基于用户真实感受）
- [x] 保存到飞书多维表格
- [x] 游记管理（列表、详情、编辑、导出）

---

## 技术栈

| 组件 | 技术方案 | 说明 |
|------|---------|------|
| 前端框架 | Streamlit | 支持多端访问 |
| AI模型 | DeepSeek API | 游记生成、OCR文字解释 |
| OCR服务 | 阿里云OCR | 500次/月免费 |
| 图片存储 | 阿里云OSS | 5GB+5GB流量/月免费 |
| 语音识别 | 阿里云ASR | 高精度语音转文字 |
| 数据存储 | 飞书多维表格 | 用户数据、游记数据 |
| 部署平台 | Streamlit Cloud | 免费部署 |

---

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd trip_note
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置密钥

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
# 编辑 secrets.toml 填入真实配置
```

### 4. 运行应用

```bash
streamlit run app.py
```

---

## 配置指南

### DeepSeek API

访问 [DeepSeek 平台](https://platform.deepseek.com/) 获取 API Key。

### 阿里云服务

详见 [docs/ALIYUN_SETUP.md](docs/ALIYUN_SETUP.md)

- [ ] OCR 服务
- [ ] OSS 存储
- [ ] ASR 语音识别

### 飞书多维表格

详见 [docs/TABLE_SETUP.md](docs/TABLE_SETUP.md)

---

## 项目结构

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
│   ├── TABLE_SETUP.md              # 飞书配置指南
│   ├── ALIYUN_SETUP.md             # 阿里云配置指南
│   └── DEVELOPMENT_GUIDE.md        # 开发指南
├── .streamlit/secrets.toml.example # 配置模板
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 使用说明

### 创建游记流程

```
1. 快速登录 / 注册账号
   ↓
2. 进入"创建游记"页面
   ↓
3. 填写旅行信息（地点、日期）
   ↓
4. 分批次添加内容
   - 批次 1: 添加照片（多选/拍照）+ 填写评论 → 提交
   - 批次 2: 继续添加照片 + 填写评论 → 提交
   - 可继续添加更多批次...
   ↓
5. 点击"生成游记"
   ↓
6. AI 根据用户真实感受整理成游记
   ↓
7. 自动保存到飞书多维表格
```

---

## 开发路线图

- [x] v0.1.0-init - 项目初始化
- [x] v0.2.0 - 游记管理功能
- [x] v0.3.0 - UI 重构（批次模式）
- [x] v0.3.1 - 提示词优化
- [ ] v1.0.0 - 功能完善和稳定
- [ ] v2.0.0 - 视频功能

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

---

## 许可证

MIT License

---

## 联系方式

如有问题，请提交 Issue。

---

**祝您使用愉快！**
