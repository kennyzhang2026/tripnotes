# 游记助手 (Trip Note) 项目文档

> 版本: v0.2.1
> 更新时间: 2026-02-20
> 状态: 稳定版本 - 核心功能已完成

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
| AI模型 | DeepSeek API | 游记生成、标题生成 |
| OCR服务 | 阿里云OCR | 500次/月免费（通用文字识别） |
| 图片存储 | 阿里云OSS | 华北2（北京）5GB+5GB流量/月免费 |
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
│   ├── 3_创建游记.py
│   ├── 4_我的游记.py
│   ├── 5_游记详情.py
│   └── 6_编辑游记.py
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
| password | text | 密码（明文存储） |
| status | text | 状态(pending/active) |
| role | text | 用户角色(user/admin) |

**表2: 游记数据表 (trip_notes)**
| 字段名 | 类型 | 说明 |
|--------|------|------|
| note_id | text | 游记唯一ID |
| username | text | 关联用户名 |
| title | text | 游记标题 |
| location | text | 地点/景区 |
| travel_date | date | 旅行日期（毫秒时间戳） |
| images | text | 图片URL数组(JSON) |
| ocr_results | text | OCR识别结果(JSON) |
| user_notes | text | 用户感想/评论 |
| ai_content | longtext | AI生成的游记内容 |

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
2. **语音按钮**：上传音频文件转换文字
3. **快速进入**：首页大按钮直接进入创建游记

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

# 阿里云OSS - 华北2（北京）
ALIYUN_OSS_BUCKET_NAME = "tripnote"
ALIYUN_OSS_ENDPOINT = "oss-cn-beijing.aliyuncs.com"

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
feature/v1.0-init        # 项目初始化
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

### v0.2.1 (2026-02-20) - Git Tag: `v0.2.1` ✅ 稳定版本

#### 核心功能修复
- ✅ 修复 OSS endpoint 配置（华北2北京）
- ✅ 修复飞书保存字段类型问题（移除自动字段，修复日期格式）
- ✅ 修复照片添加 entry_id 问题
- ✅ 修复 use_column_width 废弃警告

#### 已验证功能
- ✅ 用户登录/注册
- ✅ 照片上传到 OSS
- ✅ AI 生成游记
- ✅ 保存到飞书多维表格

#### 待测试功能
- ⏳ OCR 识别功能
- ⏳ 语音转文字功能
- ⏳ 游记列表/详情/编辑
- ⏳ 游记导出

---

### v0.2.0 (2026-02-19) - Git Tag: `v0.2.0`

#### 游记管理功能
- ✅ 游记列表页面 - 搜索、排序、删除
- ✅ 游记详情页面 - 查看完整内容、导出
- ✅ 游记编辑页面 - 编辑内容、添加照片、重新生成
- ✅ 首页导航优化 - 添加"我的游记"快速入口

#### 功能增强
- ✅ 游记卡片显示（图片、摘要、操作按钮）
- ✅ 游记导出（Markdown/纯文本）
- ✅ 游记内容重新生成
- ✅ 添加/删除照片
- ✅ OCR 识别结果展示

---

### v0.1.0-init (2026-02-19) - Git Tag: `v0.1.0-init`

#### 项目初始化
- ✅ 创建项目文档
- ✅ 确定技术方案
- ✅ 初始化 Git 仓库

#### 配置完成
- ✅ DeepSeek API 配置
- ✅ 阿里云 OCR 配置（修复 endpoint 格式问题）
- ✅ 阿里云 OSS 配置（bucket: tripnote）
- ✅ 阿里云 ASR 配置
- ✅ 飞书多维表格配置

#### 核心客户端开发
- ✅ AI 客户端（DeepSeek API）- 游记生成、标题生成
- ✅ OCR 客户端（阿里云）- 通用文字识别、表格识别
- ✅ OSS 客户端（阿里云）- 图片上传、删除、批量操作
- ✅ ASR 客户端（阿里云）- 语音转文字
- ✅ 飞书客户端（多维表格）- 用户数据、游记数据管理
- ✅ 认证客户端 - 注册、登录、密码管理
- ✅ 用户客户端 - 游记 CRUD 操作

#### 工具模块开发
- ✅ config.py - 配置管理（Streamlit secrets 集成）
- ✅ prompts.py - AI 提示词模板
- ✅ auth.py - 认证工具
- ✅ image_utils.py - 图片处理（压缩、验证、格式转换）

#### UI 页面开发
- ✅ app.py - 主应用入口（首页）
- ✅ pages/1_登录.py - 用户登录页面
- ✅ pages/2_注册.py - 用户注册页面
- ✅ pages/3_创建游记.py - 创建游记核心功能页面
- ✅ pages/4_我的游记.py - 游记列表页面
- ✅ pages/5_游记详情.py - 游记详情页面
- ✅ pages/6_编辑游记.py - 游记编辑页面

#### 数据模型设计
- ✅ 用户数据表（trip_note_users）
- ✅ 游记数据表（trip_notes）

#### 文档更新
- ✅ TABLE_SETUP.md（飞书表格配置指南）
- ✅ ALIYUN_SETUP.md（阿里云服务配置指南）
- ✅ DEVELOPMENT_GUIDE.md（开发最佳实践）
- ✅ README.md（项目说明）
- ✅ CLAUDE.md（项目文档）

---

## 当前状态

| 模块 | 状态 | 说明 |
|------|------|------|
| 配置管理 | ✅ 完成 | 所有服务密钥已配置 |
| AI 客户端 | ✅ 完成 | DeepSeek API 集成 |
| OCR 客户端 | ✅ 完成 | 阿里云 OCR 集成（通用文字识别） |
| OSS 客户端 | ✅ 完成 | 阿里云 OSS（华北2北京） |
| ASR 客户端 | ✅ 完成 | 阿里云语音识别 |
| 飞书客户端 | ✅ 完成 | 多维表格操作 |
| 认证系统 | ✅ 完成 | 登录/注册功能 |
| 工具模块 | ✅ 完成 | 配置、提示词、图片处理 |
| UI 页面 | ✅ 完成 | 全部 6 个页面完成 |
| 游记创建 | ✅ 完成 | 上传、生成、保存核心流程 |
| 游记管理 | ⏳ 待测 | 列表、详情、编辑、导出 |

---

## 下一步计划

### v0.2.2 - 功能完善
1. 测试 OCR 识别功能
2. 测试语音转文字功能
3. 测试游记列表/详情/编辑
4. 测试游记导出
5. 创建 v0.2.2 稳定标签

### 功能增强（v2.0）
1. 草稿保存功能
2. 游记分享功能
3. 多用户协作
4. 游记模板系统
5. 统计分析面板

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
