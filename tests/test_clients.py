# tests/test_clients.py
# -*- coding: utf-8 -*-
"""
客户端模块单元测试
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


class TestAIClient(unittest.TestCase):
    """AI 客户端测试"""

    @patch('clients.ai_client.OpenAI')
    def test_generate_trip_note(self, mock_openai):
        """测试游记生成"""
        from clients.ai_client import AIClient

        # Mock 响应
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "这是一篇测试游记..."

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = AIClient()
        result = client.generate_trip_note(
            location="西湖",
            travel_date="2026-02-19",
            images_context="美丽的风景",
            user_notes="很开心",
            ocr_context=""
        )

        self.assertIsNotNone(result)
        self.assertIn("游记", result)

    @patch('clients.ai_client.OpenAI')
    def test_generate_title(self, mock_openai):
        """测试标题生成"""
        from clients.ai_client import AIClient

        # Mock 响应
        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = "春游西湖"

        mock_client = Mock()
        mock_client.chat.completions.create.return_value = mock_response
        mock_openai.return_value = mock_client

        client = AIClient()
        result = client.generate_title("西湖", "2026-02-19", "风景")

        self.assertIsNotNone(result)
        self.assertEqual(result, "春游西湖")


class TestImageClient(unittest.TestCase):
    """图片客户端测试"""

    @patch('clients.image_client.oss2')
    def test_generate_key(self, mock_oss2):
        """测试 OSS 对象键生成"""
        from clients.image_client import ImageClient

        client = ImageClient()
        key = client.generate_key("testuser", "note123", "photo.jpg")

        self.assertIn("testuser", key)
        self.assertIn("note123", key)
        self.assertIn("photo.jpg", key)


class TestAuthClient(unittest.TestCase):
    """认证客户端测试"""

    @patch('clients.auth_client.FeishuClient')
    def test_register_success(self, mock_feishu):
        """测试用户注册成功"""
        from clients.auth_client import AuthClient

        # Mock 飞书客户端
        mock_feishu_instance = Mock()
        mock_feishu_instance.get_user.return_value = None  # 用户不存在
        mock_feishu.return_value = mock_feishu_instance

        client = AuthClient()
        success, message = client.register("testuser", "password123")

        self.assertTrue(success)
        self.assertEqual(message, "注册成功")

    @patch('clients.auth_client.FeishuClient')
    def test_register_user_exists(self, mock_feishu):
        """测试用户已存在"""
        from clients.auth_client import AuthClient

        # Mock 飞书客户端
        mock_feishu_instance = Mock()
        mock_feishu_instance.get_user.return_value = {"record_id": "123"}  # 用户已存在
        mock_feishu.return_value = mock_feishu_instance

        client = AuthClient()
        success, message = client.register("testuser", "password123")

        self.assertFalse(success)
        self.assertEqual(message, "用户名已被注册")

    def test_password_too_short(self):
        """测试密码过短"""
        from clients.auth_client import AuthClient

        client = AuthClient()
        success, message = client.register("testuser", "12345")

        self.assertFalse(success)
        self.assertIn("至少需要", message)


class TestUserClient(unittest.TestCase):
    """用户客户端测试"""

    @patch('clients.user_client.FeishuClient')
    def test_create_note(self, mock_feishu):
        """测试创建游记"""
        from clients.user_client import UserClient

        # Mock 飞书客户端
        mock_feishu_instance = Mock()
        mock_feishu_instance.create_trip_note.return_value = {"record_id": "123"}
        mock_feishu.return_value = mock_feishu_instance

        client = UserClient()
        success, message, note_id = client.create_note(
            username="testuser",
            title="测试游记",
            location="西湖",
            travel_date="2026-02-19",
            images=["url1", "url2"],
            ocr_results={},
            user_notes="很开心",
            ai_content="游记内容"
        )

        self.assertTrue(success)
        self.assertIsNotNone(note_id)


class TestUtils(unittest.TestCase):
    """工具函数测试"""

    def test_hash_password(self):
        """测试密码哈希"""
        from utils.auth import hash_password

        password = "test123"
        hashed = hash_password(password)

        self.assertIsNotNone(hashed)
        self.assertNotEqual(password, hashed)

    def test_verify_password(self):
        """测试密码验证"""
        from utils.auth import hash_password, verify_password

        password = "test123"
        hashed = hash_password(password)

        self.assertTrue(verify_password(password, hashed))
        self.assertFalse(verify_password("wrong", hashed))

    def test_image_compression(self):
        """测试图片压缩"""
        from utils.image_utils import compress_image
        from PIL import Image
        import io

        # 创建测试图片
        img = Image.new('RGB', (100, 100), color='red')
        result = compress_image(img)

        self.assertIsInstance(result, bytes)
        self.assertGreater(len(result), 0)


if __name__ == '__main__':
    unittest.main()
