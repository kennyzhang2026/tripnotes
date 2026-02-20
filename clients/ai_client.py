# ai_client.py
# -*- coding: utf-8 -*-
"""
AI 客户端模块
使用 DeepSeek API 进行游记生成和文化解释
"""

import json
from typing import Optional, Dict, Any, List
from openai import OpenAI
from utils.config import get_config
from utils.prompts import (
    get_photo_desc_prompt,
    get_title_prompt,
    get_trip_note_prompt
)


class AIClient:
    """DeepSeek API 客户端"""

    def __init__(self):
        """初始化 AI 客户端"""
        config = get_config()
        self.client = OpenAI(
            api_key=config.get_deepseek_api_key(),
            base_url="https://api.deepseek.com"
        )
        self.model = "deepseek-chat"

    def generate_photo_desc(self, location: str, user_note: str, ocr_text: str = "") -> str:
        """
        为单张照片生成描述文字

        Args:
            location: 地点/景区
            user_note: 用户备注
            ocr_text: OCR 识别的文字

        Returns:
            生成的描述文字
        """
        prompt = get_photo_desc_prompt(location, user_note, ocr_text)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的游记作家，擅长用优美的文字记录旅行见闻。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=300
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"AI 生成描述失败: {str(e)}")

    def generate_title(
        self,
        location: str,
        travel_date: str,
        photo_count: int = 1
    ) -> str:
        """
        生成游记标题

        Args:
            location: 地点
            travel_date: 旅行日期
            photo_count: 照片数量

        Returns:
            生成的标题
        """
        prompt = get_title_prompt(location, travel_date, photo_count)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位擅长起标题的编辑。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.9,
                max_tokens=100
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"AI 生成标题失败: {str(e)}")

    def generate_trip_note(
        self,
        location: str,
        travel_date: str,
        batches: list,
        ocr_results: dict = None
    ) -> str:
        """
        生成整体游记（v0.3.0 批次模式）

        Args:
            location: 地点
            travel_date: 旅行日期
            batches: 批次列表，每个批次包含 image_urls, comment 等
            ocr_results: OCR 识别结果字典

        Returns:
            生成的游记内容（Markdown 格式）
        """
        prompt = get_trip_note_prompt(location, travel_date, batches, ocr_results)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位专业的游记作家，擅长用优美的文字记录旅行见闻。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=2000
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"AI 生成游记失败: {str(e)}")

    def chat(
        self,
        message: str,
        system_prompt: str = "你是一个友好的助手。",
        history: list = None
    ) -> str:
        """
        通用对话接口

        Args:
            message: 用户消息
            system_prompt: 系统提示词
            history: 对话历史

        Returns:
            AI 回复
        """
        messages = [{"role": "system", "content": system_prompt}]

        if history:
            messages.extend(history)

        messages.append({"role": "user", "content": message})

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.7,
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI 对话失败: {str(e)}")
