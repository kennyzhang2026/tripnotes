# image_client.py
# -*- coding: utf-8 -*-
"""
图片存储客户端模块
使用阿里云 OSS 进行图片存储
"""

import oss2
from typing import Optional, List
from datetime import datetime
from utils.config import get_config


class ImageClient:
    """阿里云 OSS 图片存储客户端"""

    def __init__(self):
        """初始化 OSS 客户端"""
        config = get_config()
        self.access_key_id = config.get_aliyun_access_key_id()
        self.access_key_secret = config.get_aliyun_access_key_secret()
        self.bucket_name = config.get_aliyun_oss_bucket_name()
        self.endpoint = config.get_aliyun_oss_endpoint()

        auth = oss2.Auth(self.access_key_id, self.access_key_secret)
        self.bucket = oss2.Bucket(auth, f"https://{self.endpoint}", self.bucket_name)

    def generate_key(self, username: str, note_id: str, filename: str) -> str:
        """
        生成 OSS 对象键

        Args:
            username: 用户名
            note_id: 游记ID
            filename: 文件名

        Returns:
            OSS 对象键
        """
        timestamp = datetime.now().strftime("%Y%m%d")
        return f"trip_note/{username}/{note_id}/{timestamp}/{filename}"

    def upload_image(
        self,
        image_bytes: bytes,
        username: str,
        note_id: str,
        filename: str
    ) -> str:
        """
        上传图片到 OSS

        Args:
            image_bytes: 图片字节
            username: 用户名
            note_id: 游记ID
            filename: 文件名

        Returns:
            图片的公开访问 URL
        """
        key = self.generate_key(username, note_id, filename)

        try:
            # 上传图片
            result = self.bucket.put_object(key, image_bytes)

            # 生成公开访问 URL
            url = f"https://{self.bucket_name}.{self.endpoint}/{key}"

            return url
        except Exception as e:
            raise Exception(f"图片上传失败: {str(e)}")

    def upload_image_from_file(
        self,
        file_path: str,
        username: str,
        note_id: str
    ) -> str:
        """
        从文件上传图片

        Args:
            file_path: 文件路径
            username: 用户名
            note_id: 游记ID

        Returns:
            图片的公开访问 URL
        """
        filename = file_path.split("/")[-1]
        with open(file_path, "rb") as f:
            image_bytes = f.read()

        return self.upload_image(image_bytes, username, note_id, filename)

    def delete_image(self, url: str) -> bool:
        """
        删除图片

        Args:
            url: 图片 URL

        Returns:
            是否删除成功
        """
        try:
            # 从 URL 中提取 key
            key = url.split(f"{self.bucket_name}.{self.endpoint}/")[-1]
            self.bucket.delete_object(key)
            return True
        except Exception as e:
            print(f"删除图片失败: {str(e)}")
            return False

    def get_image_info(self, url: str) -> Optional[dict]:
        """
        获取图片信息

        Args:
            url: 图片 URL

        Returns:
            图片信息
        """
        try:
            key = url.split(f"{self.bucket_name}.{self.endpoint}/")[-1]
            info = self.bucket.get_object_meta(key)
            return {
                "size": int(info.headers.get("Content-Length", 0)),
                "content_type": info.headers.get("Content-Type", ""),
                "last_modified": info.headers.get("Last-Modified", "")
            }
        except Exception as e:
            print(f"获取图片信息失败: {str(e)}")
            return None

    def list_images_by_note(self, username: str, note_id: str) -> List[str]:
        """
        列出指定游记的所有图片

        Args:
            username: 用户名
            note_id: 游记ID

        Returns:
            图片 URL 列表
        """
        prefix = f"trip_note/{username}/{note_id}/"
        urls = []

        try:
            for obj in oss2.ObjectIterator(self.bucket, prefix=prefix):
                url = f"https://{self.bucket_name}.{self.endpoint}/{obj.key}"
                urls.append(url)
        except Exception as e:
            print(f"列出图片失败: {str(e)}")

        return urls

    def batch_upload(
        self,
        images: List[bytes],
        username: str,
        note_id: str
    ) -> List[str]:
        """
        批量上传图片

        Args:
            images: 图片字节列表
            username: 用户名
            note_id: 游记ID

        Returns:
            图片 URL 列表
        """
        urls = []
        for i, image_bytes in enumerate(images):
            filename = f"image_{i + 1}.jpg"
            try:
                url = self.upload_image(image_bytes, username, note_id, filename)
                urls.append(url)
            except Exception as e:
                print(f"上传第 {i + 1} 张图片失败: {str(e)}")
                urls.append("")

        return urls
