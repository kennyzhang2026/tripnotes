# asr_client.py
# -*- coding: utf-8 -*-
"""
ASR 客户端模块
使用阿里云语音识别 (ASR) 进行语音转文字
"""

import json
import uuid
from typing import Optional
import requests
from utils.config import get_config


class ASRClient:
    """阿里云语音识别客户端"""

    def __init__(self):
        """初始化 ASR 客户端"""
        config = get_config()
        self.access_key_id = config.get_aliyun_access_key_id()
        self.access_key_secret = config.get_aliyun_access_key_secret()
        self.endpoint = config.get_aliyun_asr_endpoint()
        self.app_key = config.get_aliyun_asr_app_key()

    def transcribe_file(
        self,
        audio_file_path: str,
        format: str = "wav",
        sample_rate: int = 16000,
        language: str = "zh-CN"
    ) -> str:
        """
        转写音频文件

        Args:
            audio_file_path: 音频文件路径
            format: 音频格式 (wav, mp3, etc.)
            sample_rate: 采样率
            language: 语言代码

        Returns:
            识别的文字内容
        """
        # 读取音频文件
        with open(audio_file_path, "rb") as f:
            audio_data = f.read()

        return self.transcribe_bytes(
            audio_data,
            format=format,
            sample_rate=sample_rate,
            language=language
        )

    def transcribe_bytes(
        self,
        audio_bytes: bytes,
        format: str = "wav",
        sample_rate: int = 16000,
        language: str = "zh-CN"
    ) -> str:
        """
        转写音频字节

        Args:
            audio_bytes: 音频字节
            format: 音频格式
            sample_rate: 采样率
            language: 语言代码

        Returns:
            识别的文字内容
        """
        # 构建请求
        url = f"{self.endpoint}/stream/v1/asr"
        task_id = str(uuid.uuid4())

        headers = {
            "Content-Type": "application/octet-stream",
            "X-NLS-Token": "",
            "X-NLS-AppKey": self.app_key,
            "X-NLS-RequestId": task_id,
            "X-NLS-Stream": "false"
        }

        params = {
            "format": format,
            "sample_rate": sample_rate,
            "language": language
        }

        try:
            response = requests.post(
                url,
                params=params,
                headers=headers,
                data=audio_bytes,
                timeout=30
            )

            if response.status_code == 200:
                result = response.json()
                if result.get("status") == 200000:
                    return result.get("result", "")
                else:
                    raise Exception(f"ASR 识别失败: {result.get('message', '未知错误')}")
            else:
                raise Exception(f"ASR 请求失败: HTTP {response.status_code}")

        except requests.exceptions.RequestException as e:
            raise Exception(f"ASR 请求异常: {str(e)}")

    def transcribe_with_fallback(
        self,
        audio_bytes: bytes,
        format: str = "wav"
    ) -> Optional[str]:
        """
        带容错的转写方法

        Args:
            audio_bytes: 音频字节
            format: 音频格式

        Returns:
            识别的文字内容，失败返回 None
        """
        try:
            return self.transcribe_bytes(audio_bytes, format=format)
        except Exception as e:
            print(f"语音识别失败: {str(e)}")
            return None

    def get_supported_formats(self) -> list:
        """
        获取支持的音频格式

        Returns:
            支持的格式列表
        """
        return [
            "wav", "pcm", "opus",
            "speex", "amr", "flac",
            "mp3", "mp4", "m4a"
        ]

    def get_supported_languages(self) -> list:
        """
        获取支持的语言

        Returns:
            支持的语言代码列表
        """
        return [
            ("zh-CN", "中文普通话"),
            ("en-US", "英语"),
            ("ja-JP", "日语"),
            ("ko-KR", "韩语"),
            ("th-TH", "泰语"),
            ("vi-VN", "越南语")
        ]
