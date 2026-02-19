# image_utils.py
# -*- coding: utf-8 -*-
"""
图片处理工具模块
提供图片处理相关的工具函数
"""

import io
import base64
from typing import Union, Optional
from PIL import Image
import streamlit as st


def resize_image(image: Image.Image, max_size: tuple = (1920, 1080)) -> Image.Image:
    """
    调整图片大小，保持宽高比

    Args:
        image: PIL Image 对象
        max_size: 最大尺寸 (width, height)

    Returns:
        调整后的图片
    """
    image.thumbnail(max_size, Image.Resampling.LANCZOS)
    return image


def image_to_base64(image: Image.Image, format: str = "JPEG") -> str:
    """
    将图片转换为 base64 字符串

    Args:
        image: PIL Image 对象
        format: 图片格式

    Returns:
        base64 字符串
    """
    buffer = io.BytesIO()
    image.save(buffer, format=format)
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str


def base64_to_image(base64_str: str) -> Image.Image:
    """
    将 base64 字符串转换为图片

    Args:
        base64_str: base64 字符串

    Returns:
        PIL Image 对象
    """
    img_data = base64.b64decode(base64_str)
    return Image.open(io.BytesIO(img_data))


def compress_image(image: Image.Image, quality: int = 85) -> bytes:
    """
    压缩图片为字节

    Args:
        image: PIL Image 对象
        quality: 压缩质量 (1-100)

    Returns:
        压缩后的图片字节
    """
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=quality, optimize=True)
    return buffer.getvalue()


def get_image_info(image: Union[Image.Image, bytes]) -> dict:
    """
    获取图片信息

    Args:
        image: PIL Image 对象或字节

    Returns:
        图片信息字典
    """
    if isinstance(image, bytes):
        image = Image.open(io.BytesIO(image))

    return {
        "format": image.format,
        "mode": image.mode,
        "size": image.size,
        "width": image.width,
        "height": image.height
    }


def validate_image(file) -> Optional[Image.Image]:
    """
    验证并打开上传的图片

    Args:
        file: Streamlit 上传的文件对象

    Returns:
        PIL Image 对象，验证失败返回 None
    """
    try:
        image = Image.open(file)
        # 验证图片格式
        if image.format not in ["JPEG", "PNG", "JPG"]:
            st.error("不支持的图片格式，请上传 JPG 或 PNG 图片")
            return None

        # 转换 RGBA 为 RGB
        if image.mode == "RGBA":
            background = Image.new("RGB", image.size, (255, 255, 255))
            background.paste(image, mask=image.split()[3])
            image = background

        return image
    except Exception as e:
        st.error(f"图片验证失败: {str(e)}")
        return None


def display_image(image: Image.Image, caption: str = None, width: int = None) -> None:
    """
    在 Streamlit 中显示图片

    Args:
        image: PIL Image 对象
        caption: 图片说明
        width: 显示宽度
    """
    if width:
        st.image(image, caption=caption, width=width)
    else:
        st.image(image, caption=caption, use_column_width=True)
