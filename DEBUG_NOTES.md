# 调试备忘录

> 更新时间: 2026-02-19

---

## 当前问题

用户登录失败，显示"用户名或密码错误"

---

## 已完成的修改

### 1. 简化认证流程
- 移除密码哈希，改用明文密码直接比较
- 注册时状态设为 `pending`，需管理员手动改为 `active`

### 2. 修复飞书 API
- 移除服务端 filter 查询
- 改为获取所有记录后在客户端代码中过滤

### 3. 添加调试日志
在 `clients/auth_client.py` 和 `clients/feishu_client.py` 中添加了详细的调试输出

---

## 需要确认的配置

### 飞书表格 `trip_note_users` 确认

应该有以下记录：
```
| username | password | status | role |
|----------|----------|--------|------|
| kenny    | 你的密码 | active  | user  |
```

### `.streamlit/secrets.toml` 确认

```toml
FEISHU_APP_ID = "cli_xxx"
FEISHU_APP_SECRET = "xxx"

# 用户表配置
FEISHU_APP_TOKEN_USER = "bascnxxxxx"  # 从表格 URL 获取
FEISHU_TABLE_ID_USER = "tblxxxxx"    # 从表格 URL 获取

# 游记表配置
FEISHU_APP_TOKEN_NOTE = "bascnxxxxx"
FEISHU_TABLE_ID_NOTE = "tblxxxxx"
```

---

## 调试步骤

1. **运行应用**
   ```bash
   streamlit run app.py
   ```

2. **尝试登录**
   - 用户名: `kenny`
   - 密码: 你在飞书表格中设置的密码

3. **查看终端调试输出**

   期望看到的输出：
   ```
   [DEBUG] 尝试登录 - 用户名: kenny
   [DEBUG] 飞书查询 - AppToken: xxx, TableID: xxx
   [DEBUG] 飞书返回记录数: X
   [DEBUG] 检查记录 - username字段: 'xxx', 查找: 'kenny'
   [DEBUG] 找到匹配用户: {...}
   [DEBUG] 用户字段: {...}
   [DEBUG] 存储的密码: 'xxx', 输入密码: 'xxx'
   [DEBUG] 账号状态: active
   [DEBUG] 登录成功
   ```

4. **根据调试信息判断问题**
   - 如果 `飞书返回记录数: 0` → AppToken/TableID 配置错误
   - 如果显示 `未找到用户: kenny` → 用户名不匹配或表格中没有数据
   - 如果 `账号状态异常` → 状态不是 active
   - 如果 `密码不匹配` → 密码字段值不正确

---

## 下次对话继续时

1. 先查看终端调试输出
2. 把调试信息发给我
3. 我会根据调试信息定位具体问题
