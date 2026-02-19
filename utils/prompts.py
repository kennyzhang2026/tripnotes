# prompts.py
# -*- coding: utf-8 -*-
"""
AI 提示词模板
用于 DeepSeek API 的游记生成和文化解释
"""

# 游记生成提示词模板
TRIP_NOTE_PROMPT = """
你是一位专业的游记作家。请根据以下素材，写一篇优美的游记：

## 旅行信息
- 地点：{location}
- 日期：{travel_date}

## 照片素材
{images_context}

## 用户感想
{user_notes}

## OCR 识别内容（如有）
{ocr_context}

要求：
1. 标题：为游记起一个富有诗意的标题
2. 开头：用优美的文字引入，营造氛围
3. 正文：结合照片内容和用户感想，描述旅行见闻
4. OCR 内容：如照片中识别出文字（如对联、碑文等），请进行文化解释和赏析
5. 结尾：总结感悟，升华主题
6. 语言：文笔流畅，富有感染力，约 500-800 字

请以 Markdown 格式输出，包含适当的标题层级。
"""

# OCR 文化解释提示词模板
OCR_CULTURE_PROMPT = """
请对以下从照片中识别出的文字进行文化解释：

## 识别内容
{text}

## 照片场景
{scene_context}

要求：
1. 解释文字的含义和背景
2. 如是诗词、对联，请赏析其文学价值
3. 如是碑文、题字，请说明其历史背景
4. 解释相关的文化典故
5. 100-200 字，简洁明了
"""

# 游记标题生成提示词
TITLE_GENERATION_PROMPT = """
根据以下旅行信息，生成一个富有诗意的游记标题：

- 地点：{location}
- 日期：{travel_date}
- 核心元素：{key_elements}

要求：
1. 10-20 字
2. 富有诗意和画面感
3. 体现地方特色
4. 只返回标题，不要其他内容
"""

# 图片场景描述提示词（用于辅助 OCR 理解）
IMAGE_SCENE_PROMPT = """
请描述这张照片的主要内容和场景：

要求：
1. 识别照片中的主要物体和场景
2. 如有文字（对联、碑文、招牌等），请说明其位置
3. 50 字以内简洁描述
"""


def get_trip_note_prompt(location: str, travel_date: str, images_context: str,
                         user_notes: str, ocr_context: str) -> str:
    """生成游记生成提示词"""
    return TRIP_NOTE_PROMPT.format(
        location=location,
        travel_date=travel_date,
        images_context=images_context or "暂无照片",
        user_notes=user_notes or "用户暂无感想",
        ocr_context=ocr_context or "暂无 OCR 识别内容"
    )


def get_ocr_culture_prompt(text: str, scene_context: str) -> str:
    """生成 OCR 文化解释提示词"""
    return OCR_CULTURE_PROMPT.format(
        text=text,
        scene_context=scene_context or "未知场景"
    )


def get_title_prompt(location: str, travel_date: str, key_elements: str) -> str:
    """生成标题生成提示词"""
    return TITLE_GENERATION_PROMPT.format(
        location=location,
        travel_date=travel_date,
        key_elements=key_elements or "风景游览"
    )
