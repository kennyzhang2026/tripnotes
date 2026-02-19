# 游记助手 (Trip Note) 项目文档

> 版本: v0.1.0-init
> 更新时间: 2026-02-19
> 状态: 项目初始化阶段

---

## 项目概述

**游记助手**是一个基于AI的图文游记生成应用，用户可以拍照/上传照片、添加语音/文字评论，AI自动整理成图文并茂的游记。支持OCR识别照片中的文字（如景区对联）并进行文化解释，保存到飞书多维表格。

### 核心功能
- 拍照/上传照片
- 语音输入转文字（阿里云ASR）
- OCR识别照片文字（阿里云OCR）
- AI自动生成游记（DeepSeek）
- 保存到飞书多维表格
- 导出分享

### 技术栈
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
│   ├── TABLE_SETUP.md
│   ├── ALIYUN_SETUP.md
│   └── DEVELOPMENT_GUIDE.md
├── .streamlit/secrets.toml         # 密钥配置
├── requirements.txt
├── .gitignore
├── CLAUDE.md                       # 本文档
└── README.md
```

---

## 数据模型

### 飞书多维表格结构

**表1: 用户数据表 (trip_note_users)**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| username | text | 用户名(唯一) |
| password | text | 密码 |
| status | text | 状态(pending/active) |
| role | text | 用户角色(user/admin) |

**表2: 游记数据表 (trip_notes)**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| note_id | text | 游记唯一ID |
| username | text | 关联用户名 |
| title | text | 游记标题 |
| location | text | 地点/景区 |
| travel_date | date | 旅行日期 |
| images | text | 图片URL数组(JSON) |
| ocr_results | text | OCR识别结果(JSON) |
| user_notes | text | 用户感想/评论 |
| ai_content | longtext | AI生成的游记内容 |
| created_at | datetime | 创建时间 |
| updated_at | datetime | 更新时间 |

---

## 核心交互流程

### 创建游记流程
```
用户进入"创建游记"页面
   ↓
显示已添加的照片+评论列表
   ↓
点击 "+" 按钮展开新输入区
   ↓
拍照/上传照片 → 语音输入 → 文字评论
   ↓
继续添加更多照片+评论
   ↓
点击 "生成游记"
   ↓
上传图片到OSS → OCR识别 → AI生成游记 → 保存到飞书
```

### 关键交互点
1. **"+"按钮**：展开新的照片+评论输入区
2. **语音按钮**：长按录音，松开后转换文字
3. **草稿保存**：可以保存草稿，下次继续
4. **快速进入**：首页大按钮直接进入拍照界面

---

## 配置文件

### `.streamlit/secrets.toml`
```toml
# AI配置
DEEPSEEK_API_KEY = "sk-xxx"

# 阿里云统一配置
ALIYUN_ACCESS_KEY_ID = "xxx"
ALIYUN_ACCESS_KEY_SECRET = "xxx"

# 阿里云OCR
ALIYUN_OCR_ENDPOINT = "https://ocr-api.cn-hangzhou.aliyuncs.com"

# 阿里云OSS
ALIYUN_OSS_BUCKET_NAME = "trip-note"
ALIYUN_OSS_ENDPOINT = "oss-cn-hangzhou.aliyuncs.com"

# 阿里云ASR
ALIYUN_ASR_ENDPOINT = "https://nls-meta.cn-shanghai.aliyuncs.com"
ALIYUN_ASR_APP_KEY = "xxx"

# 飞书配置
FEISHU_APP_ID = "cli_xxx"
FEISHU_APP_SECRET = "xxx"
FEISHU_APP_TOKEN_USER = "bascnxxxxx"
FEISHU_TABLE_ID_USER = "tblxxxxx"
FEISHU_APP_TOKEN_NOTE = "bascnxxxxx"
FEISHU_TABLE_ID_NOTE = "tblxxxxx"
```

### `requirements.txt`
```
streamlit>=1.28.0
openai>=1.0.0
requests>=2.31.0
pillow>=10.0.0
oss2>=2.17.0
alibabacloud-ocr-api20210707>=1.0.0
alibabacloud-nls-api>=1.0.0
python-dateutil>=2.8.2
pydantic>=2.0.0
```

---

## 开发分支策略

```bash
# 主分支
master          # 稳定版本

# 功能分支
feature/v1.0-init        # 项目初始化 (当前)
feature/v1.0-clients     # 核心客户端开发
feature/v1.0-ai          # AI集成
feature/v1.0-ui          # UI开发
feature/v1.0-test        # 测试和部署

# 后期扩展
feature/v2.0-video       # 视频功能
```

每个feature分支开发完成后，测试通过，合并到master。

---

## 版本历史

### v0.1.0-init (2026-02-19)

#### 项目初始化
- ✅ 创建项目文档
- ✅ 确定技术方案

#### 配置完成
- ✅ DeepSeek API 配置
- ✅ 阿里云 OCR 配置（修复 endpoint 格式问题）
- ✅ 阿里云 OSS 配置（bucket: tripnote）
- ✅ 阿里云 ASR 配置
- ✅ 飞书多维表格配置

#### 数据模型优化
- ✅ 用户表字段调整
  - `status` 从单选改为文本（避免 API 选项匹配问题）
  - `created_at` 改为 `role`（用户角色管理）

#### 客户端代码
- ✅ OCR 客户端（修复 endpoint 处理逻辑）
- ✅ 飞书客户端（更新用户创建方法）

#### 文档更新
- ✅ TABLE_SETUP.md（飞书表格配置指南）
- ✅ ALIYUN_SETUP.md（阿里云服务配置指南）
- ✅ DEVELOPMENT_GUIDE.md（开发最佳实践）

#### 配置问题修复
- ✅ 阿里云 OCR InvalidVersion 错误修复
- ✅ 飞书权限配置优化（仅需 bitable:app）
- ✅ secrets.toml 格式修正（移除 Markdown 链接格式）

---

## 当前状态

| 模块 | 状态 | 说明 |
|------|------|------|
| 配置管理 | ✅ 完成 | 所有服务密钥已配置 |
| OCR 客户端 | ✅ 完成 | 已修复 endpoint 问题 |
| 飞书客户端 | ✅ 完成 | 用户表结构已优化 |
| AI 客户端 | ⏳ 待开发 | |
| OSS 客户端 | ⏳ 待开发 | |
| ASR 客户端 | ⏳ 待开发 | |
| UI 页面 | ⏳ 待开发 | |

---

## 下一步计划

1. **开发核心客户端**（feature/v1.0-clients）
   - AI 客户端（DeepSeek）
   - OSS 客户端（图片上传）
   - ASR 客户端（语音识别）

2. **开发用户认证**（feature/v1.0-clients）
   - 登录页面
   - 注册页面
   - 权限验证

3. **开发游记功能**（feature/v1.0-ui）
   - 拍照/上传界面
   - 游记生成
   - 数据保存

---

## 参考项目

本项目参考 [travel_guide](d:/AI/travel_guide/) 项目的架构和实现经验。

---

## 成本估算

个人使用月度成本：
- Streamlit: 免费
- DeepSeek API: 免费额度足够
- 阿里云OCR: 500次/月免费
- 阿里云OSS: 5GB存储+5GB流量/月免费
- 阿里云ASR: 有免费额度
- 飞书多维表格: 免费

**预计个人使用完全免费**
