# auth_client.py
# -*- coding: utf-8 -*-
"""
认证客户端模块
处理用户注册、登录等认证相关业务
"""

import uuid
from datetime import datetime
from utils.auth import hash_password, verify_password
from clients.feishu_client import FeishuClient


class AuthClient:
    """认证客户端"""

    def __init__(self):
        """初始化认证客户端"""
        self.feishu = FeishuClient()

    def register(self, username: str, password: str) -> tuple[bool, str]:
        """
        用户注册

        Args:
            username: 用户名
            password: 密码

        Returns:
            (是否成功, 消息)
        """
        # 验证用户名
        if not username or len(username) < 3:
            return False, "用户名至少需要3个字符"

        if not username.isalnum():
            return False, "用户名只能包含字母和数字"

        # 验证密码
        if not password or len(password) < 6:
            return False, "密码至少需要6个字符"

        # 检查用户是否已存在
        existing_user = self.feishu.get_user(username)
        if existing_user:
            return False, "用户名已被注册"

        # 创建用户 - 直接存储明文密码，状态为 pending 等待管理员激活
        try:
            self.feishu.create_user(username, password, status="pending")
            return True, "注册成功，请等待管理员激活账号"
        except Exception as e:
            return False, f"注册失败: {str(e)}"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        """
        用户登录

        Args:
            username: 用户名
            password: 密码

        Returns:
            (是否成功, 消息)
        """
        # DEBUG: 输出登录信息
        print(f"[DEBUG] 尝试登录 - 用户名: {username}")

        # 检查用户是否存在
        user = self.feishu.get_user(username)
        print(f"[DEBUG] 获取用户结果: {user}")

        if not user:
            print(f"[DEBUG] 用户不存在")
            return False, "用户名或密码错误"

        # 验证密码 - 直接明文比较
        fields = user.get("fields", {})
        print(f"[DEBUG] 用户字段: {fields}")

        stored_password = fields.get("password", "")
        print(f"[DEBUG] 存储的密码: '{stored_password}', 输入密码: '{password}'")

        # 直接比较明文密码
        if password != stored_password:
            print(f"[DEBUG] 密码不匹配")
            return False, "用户名或密码错误"

        # 检查账号状态
        status = fields.get("status", "")
        print(f"[DEBUG] 账号状态: {status}")

        if status != "active":
            print(f"[DEBUG] 账号状态异常")
            return False, f"账号状态异常: {status}"

        print(f"[DEBUG] 登录成功")
        return True, "登录成功"

    def get_user_info(self, username: str) -> dict:
        """
        获取用户信息

        Args:
            username: 用户名

        Returns:
            用户信息
        """
        user = self.feishu.get_user(username)
        if user:
            fields = user.get("fields", {})
            return {
                "username": fields.get("username", ""),
                "status": fields.get("status", ""),
                "created_at": fields.get("created_at", None)
            }
        return None

    def change_password(
        self,
        username: str,
        old_password: str,
        new_password: str
    ) -> tuple[bool, str]:
        """
        修改密码

        Args:
            username: 用户名
            old_password: 旧密码
            new_password: 新密码

        Returns:
            (是否成功, 消息)
        """
        # 验证旧密码
        success, msg = self.login(username, old_password)
        if not success:
            return False, "旧密码错误"

        # 验证新密码
        if len(new_password) < 6:
            return False, "新密码至少需要6个字符"

        # 更新密码
        try:
            user = self.feishu.get_user(username)
            record_id = user.get("record_id", "")

            # 使用专门的密码更新方法
            self.feishu.update_user_password(record_id, new_password)
            return True, "密码修改成功"
        except Exception as e:
            return False, f"修改密码失败: {str(e)}"
