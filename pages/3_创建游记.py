# pages/3_创建游记.py
# -*- coding: utf-8 -*-
"""
创建游记页面
核心功能页面：拍照/上传、语音输入、OCR识别、AI生成游记
"""

import streamlit as st
import uuid
from datetime import datetime
from utils.auth import require_login
from utils.image_utils import validate_image, compress_image
from clients.ai_client import AIClient
from clients.ocr_client import OCRClient
from clients.image_client import ImageClient
from clients.asr_client import ASRClient
from clients.user_client import UserClient

# 页面配置
st.set_page_config(
    page_title="创建游记 - 游记助手",
    page_icon="📝",
    layout="wide"
)

# 初始化 session state
if "photo_entries" not in st.session_state:
    st.session_state.photo_entries = []
if "current_entry_id" not in st.session_state:
    st.session_state.current_entry_id = None


def require_auth():
    """检查登录状态"""
    if not require_login():
        st.stop()
    return st.session_state.username


def show_create_note_page():
    """显示创建游记页面"""
    username = require_auth()

    st.title("📝 创建游记")
    st.markdown("---")

    # 游记基本信息
    col1, col2, col3 = st.columns(3)

    with col1:
        location = st.text_input("📍 地点/景区", placeholder="如：西湖风景区")

    with col2:
        travel_date = st.date_input("📅 旅行日期", datetime.now().date())

    with col3:
        auto_title = st.checkbox("🤖 AI 自动生成标题", value=True)

    # 已添加的照片+评论列表
    if st.session_state.photo_entries:
        st.markdown("---")
        st.markdown("### 📸 已添加的照片")

        for i, entry in enumerate(st.session_state.photo_entries):
            with st.expander(f"照片 {i + 1}: {entry.get('note', '无备注')}"):
                col_img, col_info = st.columns([1, 2])

                with col_img:
                    if entry.get("image"):
                        st.image(entry["image"], width=400)

                with col_info:
                    st.markdown(f"**用户备注**: {entry.get('note', '无')}")
                    if entry.get("ocr_text"):
                        st.markdown(f"**OCR识别**: {entry['ocr_text']}")
                    if entry.get("voice_text"):
                        st.markdown(f"**语音内容**: {entry['voice_text']}")

                if st.button(f"删除", key=f"delete_{i}"):
                    st.session_state.photo_entries.pop(i)
                    st.rerun()

    # 添加新照片区域
    st.markdown("---")
    st.markdown("### ➕ 添加新照片")

    # 只在第一次或需要新的 entry_id 时生成
    if st.session_state.current_entry_id is None:
        st.session_state.current_entry_id = str(uuid.uuid4())
    entry_id = st.session_state.current_entry_id

    # 创建两列布局
    col_upload, col_note = st.columns([1, 1])

    with col_upload:
        st.markdown("#### 📷 上传照片")
        uploaded_file = st.file_uploader(
            "选择照片",
            type=["jpg", "jpeg", "png"],
            key=f"upload_{entry_id}"
        )

        if uploaded_file:
            image = validate_image(uploaded_file)
            if image:
                st.image(image, width=400)
                st.session_state[f"temp_image_{entry_id}"] = image

                # OCR 识别按钮
                if st.button(f"🔍 OCR 识别", key=f"ocr_{entry_id}"):
                    with st.spinner("正在识别文字..."):
                        try:
                            ocr_client = OCRClient()
                            img_bytes = compress_image(image)
                            ocr_text = ocr_client.extract_text_from_image(img_bytes)

                            if ocr_text:
                                st.success(f"识别成功：{ocr_text[:50]}...")
                                st.session_state[f"temp_ocr_{entry_id}"] = ocr_text
                            else:
                                st.info("未识别到文字")
                        except Exception as e:
                            st.error(f"OCR 识别失败: {str(e)}")

    with col_note:
        st.markdown("#### 📝 添加备注")

        user_note = st.text_area(
            "文字备注",
            placeholder="记录你的感想...",
            key=f"note_{entry_id}",
            height=100
        )

        # 语音输入
        st.markdown("#### 🎤 语音输入")
        audio_file = st.file_uploader(
            "录制或上传音频",
            type=["wav", "mp3", "m4a"],
            key=f"audio_{entry_id}"
        )

        if audio_file:
            st.audio(audio_file)

            if st.button(f"🎵 转换为文字", key=f"transcribe_{entry_id}"):
                with st.spinner("正在转换..."):
                    try:
                        asr_client = ASRClient()
                        audio_bytes = audio_file.read()
                        text = asr_client.transcribe_bytes(audio_bytes, format="wav")

                        if text:
                            st.success(f"转换成功：{text}")
                            st.session_state[f"temp_voice_{entry_id}"] = text
                        else:
                            st.warning("未能识别到语音")
                    except Exception as e:
                        st.error(f"语音转换失败: {str(e)}")

    # 添加到列表按钮
    if st.button(f"➕ 添加此照片", use_container_width=True, type="primary"):
        if f"temp_image_{entry_id}" in st.session_state:
            entry = {
                "id": entry_id,
                "image": st.session_state[f"temp_image_{entry_id}"],
                "note": user_note,
                "ocr_text": st.session_state.get(f"temp_ocr_{entry_id}", ""),
                "voice_text": st.session_state.get(f"temp_voice_{entry_id}", "")
            }
            st.session_state.photo_entries.append(entry)

            # 清理临时数据
            for key in list(st.session_state.keys()):
                if key.startswith(f"temp_{entry_id}"):
                    del st.session_state[key]

            # 重置 entry_id，以便下次添加新照片
            st.session_state.current_entry_id = None

            st.success("已添加！继续添加或点击生成游记")
            st.rerun()
        else:
            st.warning("请先上传照片")

    # 生成游记按钮
    st.markdown("---")
    st.markdown("### 🚀 生成游记")

    if st.button("✨ 生成游记", use_container_width=True, type="primary"):
        if not st.session_state.photo_entries:
            st.warning("请先至少添加一张照片")
            return

        if not location:
            st.error("请填写地点/景区")
            return

        generate_trip_note(username, location, str(travel_date), auto_title)


def generate_trip_note(username: str, location: str, travel_date: str, auto_title: bool):
    """生成游记"""
    with st.spinner("正在生成游记..."):
        try:
            # 初始化客户端
            ai_client = AIClient()
            ocr_client = OCRClient()
            image_client = ImageClient()
            user_client = UserClient()

            # 生成游记 ID
            note_id = str(uuid.uuid4())

            # 上传图片并收集 OCR 结果
            image_urls = []
            all_ocr_results = {}
            all_user_notes = []

            with st.expander("处理进度", expanded=True):
                for i, entry in enumerate(st.session_state.photo_entries):
                    st.markdown(f"处理照片 {i + 1}/{len(st.session_state.photo_entries)}...")

                    # 压缩并上传图片
                    img_bytes = compress_image(entry["image"])
                    filename = f"photo_{i + 1}.jpg"
                    url = image_client.upload_image(img_bytes, username, note_id, filename)
                    image_urls.append(url)

                    # OCR 识别
                    ocr_text = entry.get("ocr_text", "")
                    if not ocr_text:
                        try:
                            ocr_text = ocr_client.extract_text_from_image(img_bytes)
                        except:
                            pass

                    if ocr_text:
                        all_ocr_results[f"photo_{i + 1}"] = ocr_text

                    # 收集用户备注
                    if entry.get("note"):
                        all_user_notes.append(f"照片{i + 1}: {entry['note']}")
                    if entry.get("voice_text"):
                        all_user_notes.append(f"语音{i + 1}: {entry['voice_text']}")

                    st.progress((i + 1) / len(st.session_state.photo_entries))

                st.markdown("📝 正在生成游记内容...")

            # 构建上下文
            images_context = f"共{len(image_urls)}张照片，记录了{location}的风景"
            user_notes = "\n".join(all_user_notes) if all_user_notes else "用户暂无备注"
            ocr_context = "\n".join([f"{k}: {v}" for k, v in all_ocr_results.items()]) if all_ocr_results else ""

            # 生成游记内容
            ai_content = ai_client.generate_trip_note(
                location=location,
                travel_date=travel_date,
                images_context=images_context,
                user_notes=user_notes,
                ocr_context=ocr_context
            )

            # 生成标题
            if auto_title:
                title = ai_client.generate_title(location, travel_date, images_context)
            else:
                title = f"{location}游记"

            # 保存到飞书
            success, message, _ = user_client.create_note(
                username=username,
                title=title,
                location=location,
                travel_date=travel_date,
                images=image_urls,
                ocr_results=all_ocr_results,
                user_notes=user_notes,
                ai_content=ai_content
            )

            if success:
                st.success("🎉 游记创建成功！")

                # 显示生成的游记
                st.markdown("---")
                st.markdown("### 📖 生成的游记")

                st.markdown(f"# {title}")
                st.markdown(f"**地点**: {location}")
                st.markdown(f"**日期**: {travel_date}")

                st.markdown("---")
                st.markdown(ai_content)

                # 显示图片
                if image_urls:
                    st.markdown("---")
                    st.markdown("### 📷 照片集")
                    for url in image_urls:
                        st.image(url, width=600)

                # 清空临时数据
                st.session_state.photo_entries = []

                if st.button("🏠 返回首页", use_container_width=True):
                    st.switch_page("app.py")
            else:
                st.error(f"保存失败: {message}")

        except Exception as e:
            st.error(f"生成游记失败: {str(e)}")
            st.exception(e)


def main():
    """主函数"""
    show_create_note_page()


if __name__ == "__main__":
    main()
