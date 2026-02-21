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
你是一位专业的游记编辑。请根据用户提供的照片和评论，整理成一篇简洁真实的游记。

## 旅行信息
- 地点：{location}
- 日期：{travel_date}

## 照片资源（用于配图）
{photo_list}

## 用户的真实感受（按提交批次）
{batch_info}

## OCR 识别内容（照片中的文字）
{ocr_info}

## 核心原则（严格遵守）
**以用户的真实感受为中心，不要主观臆断！**

## 具体要求
1. **内容来源**：只写用户在评论中提到的内容，不要编造用户没说的情节、感受或细节
2. **照片使用**：照片要素（景色、人物、建筑等）作为"背景参考"，理解用户想要表达什么，但不要凭空描述照片内容
3. **照片插入**：在内容相关的段落自然插入照片，形成图文并茂效果
   - 照片引用语法：`![简要描述](完整URL)`
   - 示例：`![湖边漫步](https://tripnote.oss-cn-beijing.aliyuncs.com/...)`
4. **OCR处理**：如果用户评论中提到了照片中的文字（对联、碑文等），可以补充简短的文化背景解释；若用户未提及，不必强行解释
5. **字数**：根据用户评论内容多少自然决定，约 300-500 字即可，不要为了凑字数而扩充
6. **文笔**：保持第一人称，语言流畅自然，但不要过度修辞

请以 Markdown 格式输出，标题用 # 开头。

记住：这是"用户的游记"，不是"你的创作"。
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
