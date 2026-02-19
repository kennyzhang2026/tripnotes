# user_client.py
# -*- coding: utf-8 -*-
"""
用户客户端模块
处理用户数据和游记管理
"""

import uuid
import json
from datetime import datetime
from clients.feishu_client import FeishuClient


class UserClient:
    """用户客户端"""

    def __init__(self):
        """初始化用户客户端"""
        self.feishu = FeishuClient()

    # ===== 游记管理 =====

    def create_note(
        self,
        username: str,
        title: str,
        location: str,
        travel_date: str,
        images: list = None,
        ocr_results: dict = None,
        user_notes: str = "",
        ai_content: str = ""
    ) -> tuple[bool, str, str]:
        """
        创建游记

        Args:
            username: 用户名
            title: 标题
            location: 地点
            travel_date: 旅行日期
            images: 图片 URL 列表
            ocr_results: OCR 识别结果
            user_notes: 用户感想
            ai_content: AI 生成内容

        Returns:
            (是否成功, 消息, 游记ID)
        """
        note_id = str(uuid.uuid4())

        note_data = {
            "note_id": note_id,
            "username": username,
            "title": title,
            "location": location,
            "travel_date": travel_date,
            "images": images or [],
            "ocr_results": ocr_results or {},
            "user_notes": user_notes,
            "ai_content": ai_content
        }

        try:
            result = self.feishu.create_trip_note(note_data)
            return True, "游记创建成功", note_id
        except Exception as e:
            return False, f"创建游记失败: {str(e)}", None

    def get_note(self, note_id: str) -> dict:
        """
        获取游记详情

        Args:
            note_id: 游记 ID

        Returns:
            游记数据
        """
        record = self.feishu.get_trip_note(note_id)
        if record:
            fields = record.get("fields", {})
            return {
                "record_id": record.get("record_id", ""),
                "note_id": fields.get("note_id", ""),
                "username": fields.get("username", ""),
                "title": fields.get("title", ""),
                "location": fields.get("location", ""),
                "travel_date": fields.get("travel_date", ""),
                "images": json.loads(fields.get("images", "[]")),
                "ocr_results": json.loads(fields.get("ocr_results", "{}")),
                "user_notes": fields.get("user_notes", ""),
                "ai_content": fields.get("ai_content", ""),
                "created_at": fields.get("created_at", None),
                "updated_at": fields.get("updated_at", None)
            }
        return None

    def list_notes(self, username: str, limit: int = 20) -> list:
        """
        获取用户的游记列表

        Args:
            username: 用户名
            limit: 数量限制

        Returns:
            游记列表
        """
        records = self.feishu.list_trip_notes(username, limit)

        notes = []
        for record in records:
            fields = record.get("fields", {})
            notes.append({
                "record_id": record.get("record_id", ""),
                "note_id": fields.get("note_id", ""),
                "title": fields.get("title", ""),
                "location": fields.get("location", ""),
                "travel_date": fields.get("travel_date", ""),
                "created_at": fields.get("created_at", None)
            })

        return notes

    def update_note(
        self,
        note_id: str,
        title: str = None,
        location: str = None,
        travel_date: str = None,
        images: list = None,
        ocr_results: dict = None,
        user_notes: str = None,
        ai_content: str = None
    ) -> tuple[bool, str]:
        """
        更新游记

        Args:
            note_id: 游记 ID
            title: 标题
            location: 地点
            travel_date: 旅行日期
            images: 图片 URL 列表
            ocr_results: OCR 识别结果
            user_notes: 用户感想
            ai_content: AI 生成内容

        Returns:
            (是否成功, 消息)
        """
        # 获取记录 ID
        record = self.feishu.get_trip_note(note_id)
        if not record:
            return False, "游记不存在"

        record_id = record.get("record_id", "")

        # 构建更新数据
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if location is not None:
            update_data["location"] = location
        if travel_date is not None:
            update_data["travel_date"] = travel_date
        if images is not None:
            update_data["images"] = images
        if ocr_results is not None:
            update_data["ocr_results"] = ocr_results
        if user_notes is not None:
            update_data["user_notes"] = user_notes
        if ai_content is not None:
            update_data["ai_content"] = ai_content

        try:
            self.feishu.update_trip_note(record_id, update_data)
            return True, "更新成功"
        except Exception as e:
            return False, f"更新失败: {str(e)}"

    def delete_note(self, note_id: str) -> tuple[bool, str]:
        """
        删除游记

        Args:
            note_id: 游记 ID

        Returns:
            (是否成功, 消息)
        """
        try:
            record = self.feishu.get_trip_note(note_id)
            if not record:
                return False, "游记不存在"

            record_id = record.get("record_id", "")
            self.feishu.delete_trip_note(record_id)
            return True, "删除成功"
        except Exception as e:
            return False, f"删除失败: {str(e)}"

    # ===== 用户统计 =====

    def get_user_stats(self, username: str) -> dict:
        """
        获取用户统计信息

        Args:
            username: 用户名

        Returns:
            统计信息
        """
        notes = self.list_notes(username, limit=1000)

        total_notes = len(notes)
        total_images = 0

        for note in notes:
            note_data = self.get_note(note["note_id"])
            if note_data:
                total_images += len(note_data.get("images", []))

        return {
            "total_notes": total_notes,
            "total_images": total_images
        }
