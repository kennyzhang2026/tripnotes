# 飞书多维表格设置指南

本文档说明如何设置飞书多维表格用于存储用户数据和游记数据。

---

## 1. 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/app)
2. 点击"创建企业自建应用"
3. 填写应用信息：
   - 应用名称：游记助手
   - 应用描述：AI驱动的图文游记生成工具
4. 创建后记录 `App ID` 和 `App Secret`

---

## 2. 配置应用权限

在应用管理页面，进入 **权限管理**，添加以下权限：

| 权限名称 | 权限值 | 用途 |
|---------|-------|------|
| 多维表格-查看、评论、编辑和管理 | `bitable:app` | 完整的读写操作 |

> **注意**: 只需要 `bitable:app` 一个权限即可，它已包含完整的增删改查功能。

---

## 3. 创建多维表格

### 3.1 创建表格

1. 打开飞书，创建一个新的多维表格
2. 命名为 "游记助手数据"

### 3.2 创建用户数据表

**表名**: `trip_note_users`

**字段配置**:

| 字段名 | 字段类型 | 字段ID | 说明 |
|--------|---------|-------|------|
| username | 文本 | username | 用户名（设为唯一） |
| password | 文本 | password | 加密后的密码 |
| status | 文本 | status | 状态: pending/active |
| role | 文本 | role | 用户角色: user/admin |

> **注意**: status 使用文本类型而非单选，避免 API 调用时的选项匹配问题。

记录 `App Token` 和 `Table ID`：
- App Token: URL 中的 `bascnxxxxx` 部分
- Table ID: 打开表后，URL 中的 `tblxxxxx` 部分

### 3.3 创建游记数据表

**表名**: `trip_notes`

**字段配置**:

| 字段名 | 字段类型 | 字段ID | 说明 |
|--------|---------|-------|------|
| note_id | 文本 | note_id | 游记唯一ID |
| username | 文本 | username | 关联用户名 |
| title | 文本 | title | 游记标题 |
| location | 文本 | location | 地点/景区 |
| travel_date | 日期 | travel_date | 旅行日期 |
| images | 文本 | images | 图片URL数组(JSON) |
| ocr_results | 文本 | ocr_results | OCR识别结果(JSON) |
| user_notes | 文本 | user_notes | 用户感想/评论 |
| ai_content | 多行文本 | ai_content | AI生成的游记内容 |
| created_at | 创建时间 | created_at | 创建时间 |
| updated_at | 修改时间 | updated_at | 更新时间 |

记录 `App Token` 和 `Table ID`

---

## 4. 配置 secrets.toml

将以上信息填入 `.streamlit/secrets.toml`:

```toml
FEISHU_APP_ID = "cli_xxx"
FEISHU_APP_SECRET = "xxx"

# 用户表
FEISHU_APP_TOKEN_USER = "bascnxxxxx"
FEISHU_TABLE_ID_USER = "tblxxxxx"

# 游记表
FEISHU_APP_TOKEN_NOTE = "bascnxxxxx"
FEISHU_TABLE_ID_NOTE = "tblxxxxx"
```

---

## 5. 发布应用

1. 在飞书开放平台，点击"版本管理与发布"
2. 创建版本，填写版本信息
3. 提交审核（或设置为"仅企业内部"）
4. 审核通过后即可使用

---

## 注意事项

1. **权限**: 确保应用已获得正确的权限
2. **加密**: 密码会经过 SHA256 加密存储
3. **URL 获取**: App Token 和 Table ID 可以从表格 URL 中获取
4. **测试**: 先在测试环境验证配置正确性
