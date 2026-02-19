# 阿里云服务配置指南

本文档说明如何配置阿里云的各项服务。

---

## 1. 获取访问密钥 (AccessKey)

1. 访问 [阿里云控制台 - AccessKey 管理](https://ram.console.aliyun.com/manage/ak)
2. 如果是首次使用，点击"创建 AccessKey"
3. 建议使用 RAM 子账号 AccessKey，并授予最小权限
4. 记录 `Access Key ID` 和 `Access Key Secret`

**安全提示**: AccessKey Secret 只在创建时显示一次，请妥善保管！

---

## 2. 配置 OCR 服务

### 2.1 开通服务

1. 访问 [阿里云 OCR 控制台](https://ocr.console.aliyun.com/)
2. 开通"通用文字识别"服务
3. 免费额度: 500次/月

### 2.2 配置参数

- **Endpoint**: `ocr-api.cn-hangzhou.aliyuncs.com` (不带 `https://`)
- **地域**: 华东1（杭州）
- **SDK版本**: `alibabacloud-ocr-api20210707`

> **注意**: SDK 会自动处理 HTTPS 连接，配置 endpoint 时只需填写域名部分。

### 2.3 测试

```bash
pip install alibabacloud-ocr-api20210707
```

---

## 3. 配置 OSS 服务

### 3.1 开通服务

1. 访问 [阿里云 OSS 控制台](https://oss.console.aliyun.com/)
2. 开通 OSS 服务
3. 免费额度: 5GB存储 + 5GB流量/月

### 3.2 创建 Bucket

1. 点击"创建 Bucket"
2. 配置参数：
   - **Bucket 名称**: 如 `trip-note`（全局唯一）
   - **地域**: 华东1（杭州）
   - **存储类型**: 标准存储
   - **读写权限**: 公共读（便于图片访问）
3. 创建后记录 Bucket 名称和 Endpoint

### 3.3 配置参数

- **Bucket 名称**: 你创建的 Bucket 名称
- **Endpoint**: `oss-cn-hangzhou.aliyuncs.com`

### 3.4 测试

```bash
pip install oss2
```

---

## 4. 配置 ASR 服务

### 4.1 开通服务

1. 访问 [阿里云语音服务控制台](https://nls-portal.console.aliyun.com/)
2. 开通"语音识别"服务
3. 创建项目，记录项目 AppKey

### 4.2 配置参数

- **Endpoint**: `https://nls-meta.cn-shanghai.aliyuncs.com`
- **App Key**: 在项目管理中获取

### 4.3 测试

```bash
# ASR SDK 需要额外安装，请参考官方文档
# https://help.aliyun.com/document_detail/84428.html
```

---

## 5. 配置 secrets.toml

将以上信息填入 `.streamlit/secrets.toml`:

```toml
# 阿里云统一配置
ALIYUN_ACCESS_KEY_ID = "your-access-key-id"
ALIYUN_ACCESS_KEY_SECRET = "your-access-key-secret"

# OCR
ALIYUN_OCR_ENDPOINT = "https://ocr-api.cn-hangzhou.aliyuncs.com"

# OSS
ALIYUN_OSS_BUCKET_NAME = "trip-note"
ALIYUN_OSS_ENDPOINT = "oss-cn-hangzhou.aliyuncs.com"

# ASR
ALIYUN_ASR_ENDPOINT = "https://nls-meta.cn-shanghai.aliyuncs.com"
ALIYUN_ASR_APP_KEY = "your-asr-app-key"
```

---

## 6. RAM 子账号权限配置（推荐）

为了安全，建议创建 RAM 子账号并授予最小权限：

### 6.1 创建 RAM 子账号

1. 访问 [RAM 控制台](https://ram.console.aliyun.com/)
2. 创建用户，选择"编程访问"
3. 记录 AccessKey ID 和 Secret

### 6.2 授予权限

创建自定义权限策略，包含以下权限：

```json
{
  "Version": "1",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ocr:RecognizeGeneral"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "oss:PutObject",
        "oss:GetObject",
        "oss:DeleteObject"
      ],
      "Resource": [
        "acs:oss:*:*:trip-note",
        "acs:oss:*:*:trip-note/*"
      ]
    }
  ]
}
```

将此策略授予子账号。

---

## 注意事项

1. **费用**: 所有服务都有免费额度，个人使用建议监控用量
2. **安全**: 不要将 AccessKey 提交到代码仓库
3. **跨域**: OSS 设置公共读权限时注意数据安全
4. **测试**: 配置完成后请测试各项服务是否正常
