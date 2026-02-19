# ai_client.py
# -*- coding: utf-8 -*-
"""
AI 客户端模块
使用 DeepSeek API 进行游记生成和文化解释
"""

import json
from typing import Optional, Dict, Any
from openai import OpenAI
from utils.config import get_config
from utils.prompts import (
    get_trip_note_prompt,
    get_ocr_culture_prompt,
    get_title_prompt
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

    def generate_trip_note(
        self,
        location: str,
        travel_date: str,
        images_context: str = "",
        user_notes: str = "",
        ocr_context: str = ""
    ) -> str:
        """
        生成游记内容

        Args:
            location: 地点/景区
            travel_date: 旅行日期
            images_context: 图片场景描述
            user_notes: 用户感想
            ocr_context: OCR 识别内容

        Returns:
            生成的游记内容
        """
        prompt = get_trip_note_prompt(
            location=location,
            travel_date=travel_date,
            images_context=images_context,
            user_notes=user_notes,
            ocr_context=ocr_context
        )

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
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI 生成游记失败: {str(e)}")

    def explain_ocr_text(
        self,
        text: str,
        scene_context: str = ""
    ) -> str:
        """
        解释 OCR 识别的文字内容

        Args:
            text: OCR 识别的文字
            scene_context: 场景描述

        Returns:
            文化解释内容
        """
        prompt = get_ocr_culture_prompt(text, scene_context)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "你是一位文化学者，擅长解释诗词、对联、碑文等传统文化内容。"},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"AI 解释 OCR 内容失败: {str(e)}")

    def generate_title(
        self,
        location: str,
        travel_date: str,
        key_elements: str = ""
    ) -> str:
        """
        生成游记标题

        Args:
            location: 地点
            travel_date: 旅行日期
            key_elements: 核心元素

        Returns:
            生成的标题
        """
        prompt = get_title_prompt(location, travel_date, key_elements)

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
