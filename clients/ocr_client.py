# ocr_client.py
# -*- coding: utf-8 -*-
"""
OCR 客户端模块
使用阿里云 OCR API 进行文字识别
"""

import json
from typing import Optional, Dict, Any, List
from alibabacloud_ocr_api20210707.client import Client as OcrClient
from alibabacloud_tea_openapi import models as open_api_models
from alibabacloud_ocr_api20210707 import models as ocr_models
from utils.config import get_config


class OCRClient:
    """阿里云 OCR 客户端"""

    def __init__(self):
        """初始化 OCR 客户端"""
        config = get_config()
        self.access_key_id = config.get_aliyun_access_key_id()
        self.access_key_secret = config.get_aliyun_access_key_secret()
        self.endpoint = config.get_aliyun_ocr_endpoint()

        print(f"[DEBUG OCR] Endpoint: {self.endpoint}")

        self.client = self._create_client()

    def _create_client(self) -> OcrClient:
        """创建 OCR 客户端实例"""
        # 从 endpoint 中提取域名（移除 https:// 前缀）
        endpoint_domain = self.endpoint.replace("https://", "").replace("http://", "")

        config = open_api_models.Config(
            access_key_id=self.access_key_id,
            access_key_secret=self.access_key_secret
        )
        config.endpoint = endpoint_domain
        return OcrClient(config)

    def recognize_general(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        通用文字识别

        Args:
            image_bytes: 图片字节

        Returns:
            识别结果，包含文字内容和位置信息
        """
        request = ocr_models.RecognizeGeneralRequest()
        request.body = image_bytes

        try:
            response = self.client.recognize_general(request)
            return self._parse_response(response)
        except Exception as e:
            raise Exception(f"OCR 识别失败: {str(e)}")

    def recognize_table(self, image_bytes: bytes) -> Dict[str, Any]:
        """
        表格识别

        Args:
            image_bytes: 图片字节

        Returns:
            识别结果
        """
        request = ocr_models.RecognizeTableRequest()
        request.body = image_bytes

        try:
            response = self.client.recognize_table(request)
            return self._parse_response(response)
        except Exception as e:
            raise Exception(f"OCR 表格识别失败: {str(e)}")

    def _parse_response(self, response) -> Dict[str, Any]:
        """
        解析 OCR 响应

        Args:
            response: API 响应

        Returns:
            解析后的结果
        """
        if not response or not response.body:
            return {"success": False, "text": "", "data": None}

        result = {
            "success": True,
            "text": "",
            "data": response.body.to_map()
        }

        # 提取所有文字
        if hasattr(response.body, "data") and response.body.data:
            if isinstance(response.body.data, dict):
                prisms = response.body.data.get("prisms", [])
                text_list = []
                for prism in prisms:
                    if isinstance(prism, dict):
                        text_list.append(prism.get("text", ""))
                result["text"] = "\n".join(text_list)
            elif hasattr(response.body.data, "prisms"):
                text_list = [p.text for p in response.body.data.prisms if hasattr(p, "text")]
                result["text"] = "\n".join(text_list)

        return result

    def extract_text_from_image(self, image_bytes: bytes) -> str:
        """
        从图片中提取文字（便捷方法）

        Args:
            image_bytes: 图片字节

        Returns:
            提取的文字内容
        """
        result = self.recognize_general(image_bytes)
        return result.get("text", "")

    def has_text(self, image_bytes: bytes) -> bool:
        """
        检查图片中是否包含文字

        Args:
            image_bytes: 图片字节

        Returns:
            是否包含文字
        """
        text = self.extract_text_from_image(image_bytes)
        return len(text.strip()) > 0

    def recognize_multiple(self, images: List[bytes]) -> List[Dict[str, Any]]:
        """
        批量识别多张图片

        Args:
            images: 图片字节列表

        Returns:
            识别结果列表
        """
        results = []
        for image_bytes in images:
            try:
                result = self.recognize_general(image_bytes)
                results.append(result)
            except Exception as e:
                results.append({
                    "success": False,
                    "text": "",
                    "error": str(e)
                })
        return results
