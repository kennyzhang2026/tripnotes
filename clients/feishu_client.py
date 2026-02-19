# feishu_client.py
# -*- coding: utf-8 -*-
"""
飞书客户端模块
使用飞书 API 操作多维表格
"""

import json
import time
from typing import Optional, Dict, Any, List
import requests
from utils.config import get_config


class FeishuClient:
    """飞书多维表格客户端"""

    def __init__(self):
        """初始化飞书客户端"""
        config = get_config()
        self.app_id = config.get_feishu_app_id()
        self.app_secret = config.get_feishu_app_secret()
        self.app_token_user = config.get_feishu_app_token_user()
        self.table_id_user = config.get_feishu_table_id_user()
        self.app_token_note = config.get_feishu_app_token_note()
        self.table_id_note = config.get_feishu_table_id_note()

        self.access_token = None
        self.token_expire_time = 0

    def _get_access_token(self) -> str:
        """
        获取访问令牌

        Returns:
            访问令牌
        """
        # 检查是否需要刷新令牌
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token

        url = "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal"
        payload = {
            "app_id": self.app_id,
            "app_secret": self.app_secret
        }

        try:
            response = requests.post(url, json=payload)
            data = response.json()

            if data.get("code") == 0:
                self.access_token = data.get("tenant_access_token")
                # 设置过期时间（提前5分钟刷新）
                self.token_expire_time = time.time() + data.get("expire", 7200) - 300
                return self.access_token
            else:
                raise Exception(f"获取访问令牌失败: {data.get('msg')}")
        except Exception as e:
            raise Exception(f"飞书认证失败: {str(e)}")

    def _request(
        self,
        method: str,
        url: str,
        data: dict = None,
        params: dict = None
    ) -> dict:
        """
        发送 HTTP 请求

        Args:
            method: 请求方法
            url: 请求 URL
            data: 请求体
            params: 查询参数

        Returns:
            响应数据
        """
        headers = {
            "Authorization": f"Bearer {self._get_access_token()}",
            "Content-Type": "application/json"
        }

        if method == "GET":
            response = requests.get(url, headers=headers, params=params)
        elif method == "POST":
            response = requests.post(url, headers=headers, json=data)
        elif method == "PATCH":
            response = requests.patch(url, headers=headers, json=data)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, json=data)
        else:
            raise ValueError(f"不支持的请求方法: {method}")

        result = response.json()

        if result.get("code") != 0:
            raise Exception(f"飞书 API 请求失败: {result.get('msg')}")

        return result.get("data", {})

    # ===== 用户数据操作 =====

    def create_user(self, username: str, password: str, status: str = "pending", role: str = "user") -> dict:
        """
        创建用户

        Args:
            username: 用户名
            password: 密码
            status: 状态 (pending/active)
            role: 用户角色 (user/admin)

        Returns:
            创建的用户记录
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_user}/tables/{self.table_id_user}/records"

        data = {
            "fields": {
                "username": username,
                "password": password,
                "status": status,
                "role": role
            }
        }

        return self._request("POST", url, data=data)

    def get_user(self, username: str) -> Optional[dict]:
        """
        根据用户名获取用户

        Args:
            username: 用户名

        Returns:
            用户记录，不存在返回 None
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_user}/tables/{self.table_id_user}/records"

        # 获取所有记录，然后在代码中过滤
        result = self._request("GET", url, params={"page_size": 100})
        items = result.get("items", [])

        # 在代码中查找匹配的用户名
        for item in items:
            fields = item.get("fields", {})
            if fields.get("username") == username:
                return item

        return None

    def update_user_status(self, record_id: str, status: str) -> dict:
        """
        更新用户状态

        Args:
            record_id: 记录 ID
            status: 新状态

        Returns:
            更新后的记录
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_user}/tables/{self.table_id_user}/records/{record_id}"

        data = {"fields": {"status": status}}

        return self._request("PATCH", url, data=data)

    # ===== 游记数据操作 =====

    def create_trip_note(self, note_data: dict) -> dict:
        """
        创建游记

        Args:
            note_data: 游记数据

        Returns:
            创建的游记记录
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_note}/tables/{self.table_id_note}/records"

        # 转换数据格式
        fields = {
            "note_id": note_data.get("note_id"),
            "username": note_data.get("username"),
            "title": note_data.get("title", ""),
            "location": note_data.get("location", ""),
            "travel_date": note_data.get("travel_date", ""),
            "images": json.dumps(note_data.get("images", []), ensure_ascii=False),
            "ocr_results": json.dumps(note_data.get("ocr_results", {}), ensure_ascii=False),
            "user_notes": note_data.get("user_notes", ""),
            "ai_content": note_data.get("ai_content", ""),
            "created_at": int(time.time() * 1000),
            "updated_at": int(time.time() * 1000)
        }

        data = {"fields": fields}

        return self._request("POST", url, data=data)

    def get_trip_note(self, note_id: str) -> Optional[dict]:
        """
        获取游记

        Args:
            note_id: 游记 ID

        Returns:
            游记记录，不存在返回 None
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_note}/tables/{self.table_id_note}/records"

        # 获取所有记录，然后在代码中过滤
        result = self._request("GET", url, params={"page_size": 100})
        items = result.get("items", [])

        # 在代码中查找匹配的 note_id
        for item in items:
            fields = item.get("fields", {})
            if fields.get("note_id") == note_id:
                return item

        return None

    def list_trip_notes(self, username: str, limit: int = 20) -> List[dict]:
        """
        列出用户的游记

        Args:
            username: 用户名
            limit: 返回数量限制

        Returns:
            游记记录列表
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_note}/tables/{self.table_id_note}/records"

        # 获取所有记录，然后在代码中过滤
        result = self._request("GET", url, params={"page_size": 100})
        all_items = result.get("items", [])

        # 在代码中过滤属于该用户的游记
        filtered_items = []
        for item in all_items:
            fields = item.get("fields", {})
            if fields.get("username") == username:
                filtered_items.append(item)
                if len(filtered_items) >= limit:
                    break

        return filtered_items

    def update_trip_note(self, record_id: str, note_data: dict) -> dict:
        """
        更新游记

        Args:
            record_id: 记录 ID
            note_data: 更新数据

        Returns:
            更新后的记录
        """
        url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_note}/tables/{self.table_id_note}/records/{record_id}"

        fields = {"updated_at": int(time.time() * 1000)}

        # 只更新提供的字段
        for key in ["title", "location", "travel_date", "images", "ocr_results", "user_notes", "ai_content"]:
            if key in note_data:
                if key in ["images", "ocr_results"]:
                    fields[key] = json.dumps(note_data[key], ensure_ascii=False)
                else:
                    fields[key] = note_data[key]

        data = {"fields": fields}

        return self._request("PATCH", url, data=data)

    def delete_trip_note(self, record_id: str) -> bool:
        """
        删除游记

        Args:
            record_id: 记录 ID

        Returns:
            是否删除成功
        """
        try:
            url = f"https://open.feishu.cn/open-apis/bitable/v1/apps/{self.app_token_note}/tables/{self.table_id_note}/records/{record_id}"
            self._request("DELETE", url)
            return True
        except Exception as e:
            print(f"删除游记失败: {str(e)}")
            return False
