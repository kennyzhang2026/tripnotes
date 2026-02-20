# prompts.py
# -*- coding: utf-8 -*-
"""
AI 提示词模板
用于 DeepSeek API 的游记生成和文化解释
"""

# 单张照片描述生成提示词
PHOTO_DESC_PROMPT = """
你是一位专业的游记作家。请根据用户备注和照片中的文字内容，生成一段优美的描述文字。

## 旅行地点
{location}

## 用户备注
{user_note}

## 照片中识别出的文字（如有）
{ocr_text}

要求：
1. 结合用户备注和 OCR 识别的文字，扩展成一段优美的描述
2. 如 OCR 识别出文字（如对联、碑文等），请进行文化解释并融入描述中
3. 语言流畅，富有感染力，约 80-150 字
4. 第一人称视角，如同亲身经历
5. 只返回描述文字，不要标题或其他内容
"""

# 游记标题生成提示词
TITLE_GENERATION_PROMPT = """
根据以下旅行信息，生成一个富有诗意的游记标题：

- 地点：{location}
- 日期：{travel_date}
- 照片数量：{photo_count}张

要求：
1. 10-20 字
2. 富有诗意和画面感
3. 体现地方特色
4. 只返回标题，不要其他内容
"""

# 整体游记生成提示词（v0.3.0 批次模式）
TRIP_NOTE_PROMPT = """
你是一位专业的游记作家。请根据用户提供的多组照片和评论，写一篇完整的游记。

## 旅行信息
- 地点：{location}
- 日期：{travel_date}

## 照片列表（请在游记中引用这些照片）
{photo_list}

## 用户素材（按提交批次）
{batch_info}

## OCR 识别结果（如有）
{ocr_info}

要求：
1. 写一篇完整的游记，有开头、发展、高潮、结尾
2. 按时间线或空间顺序组织内容
3. **重要**：在游记中引用照片时，必须复制"照片列表"中的完整 URL 地址
4. 照片引用语法：`![照片描述](完整URL)`
   - 正确示例：`![冬日湖景](https://tripnote.oss-cn-beijing.aliyuncs.com/trip_note/user/20260220/photo.jpg)`
   - 错误示例：`![照片](照片1_URL)` 或 `![照片](照片URL)`
5. 每张照片的描述要具体生动，与上下文相关
6. 融入用户评论，保持第一人称视角
7. 对OCR识别的文化内容（如对联、碑文）进行解释
8. 文笔流畅，富有感染力，约 600-1000 字

请以 Markdown 格式输出，标题用 # 开头。
"""


def get_photo_desc_prompt(location: str, user_note: str, ocr_text: str = "") -> str:
    """生成单张照片描述提示词"""
    return PHOTO_DESC_PROMPT.format(
        location=location,
        user_note=user_note or "暂无备注",
        ocr_text=ocr_text or "无"
    )


def get_title_prompt(location: str, travel_date: str, photo_count: int) -> str:
    """生成标题生成提示词"""
    return TITLE_GENERATION_PROMPT.format(
        location=location,
        travel_date=travel_date,
        photo_count=photo_count
    )


def get_trip_note_prompt(location: str, travel_date: str, batches: list, ocr_results: dict = None) -> str:
    """
    生成整体游记提示词（v0.3.0 批次模式）

    Args:
        location: 地点
        travel_date: 旅行日期
        batches: 批次列表，每个批次包含 image_urls, comment 等
        ocr_results: OCR 识别结果字典
    """
    # 构建照片列表（包含实际 URL）
    photo_list_parts = []
    photo_index = 1
    for i, batch in enumerate(batches):
        image_urls = batch.get("image_urls", [])
        for url in image_urls:
            photo_list_parts.append(f"照片{photo_index}: {url}")
            photo_index += 1

    photo_list = "\n".join(photo_list_parts) if photo_list_parts else "无"

    # 构建批次信息
    batch_info_parts = []
    for i, batch in enumerate(batches):
        batch_num = i + 1
        photo_count = len(batch.get("image_urls", []))
        comment = batch.get("comment", "无评论")
        batch_info_parts.append(f"- 批次{batch_num}：{photo_count}张照片，评论：「{comment}」")

    batch_info = "\n".join(batch_info_parts) if batch_info_parts else "无"

    # 构建 OCR 信息
    ocr_info = "无"
    if ocr_results:
        ocr_parts = []
        for key, value in ocr_results.items():
            if value:
                ocr_parts.append(f"- {key}: {value}")
        if ocr_parts:
            ocr_info = "\n".join(ocr_parts)

    return TRIP_NOTE_PROMPT.format(
        location=location,
        travel_date=travel_date,
        photo_list=photo_list,
        batch_info=batch_info,
        ocr_info=ocr_info
    )
