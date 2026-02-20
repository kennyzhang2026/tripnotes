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

# 初始化 session state (v0.3.0 重构)
# current_batch_photos: 当前批次的照片列表
# current_batch_comment: 当前批次的评论
# submitted_batches: 已提交的批次列表
# _processed_files: 已处理的文件集合（防止重复处理）
if "current_batch_photos" not in st.session_state:
    st.session_state.current_batch_photos = []
if "current_batch_comment" not in st.session_state:
    st.session_state.current_batch_comment = ""
if "submitted_batches" not in st.session_state:
    st.session_state.submitted_batches = []
if "_processed_files" not in st.session_state:
    st.session_state._processed_files = set()


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

    # 已提交的批次列表
    if st.session_state.submitted_batches:
        st.markdown("---")
        st.markdown(f"### 📦 已提交批次 ({len(st.session_state.submitted_batches)})")

        for i, batch in enumerate(st.session_state.submitted_batches):
            with st.expander(f"批次 {i + 1}: {len(batch['image_urls'])} 张照片 - {batch.get('comment', '无评论')[:30]}..."):
                # 显示照片网格
                cols = st.columns(min(4, len(batch["image_urls"])))
                for j, col in enumerate(cols):
                    if j < len(batch["image_urls"]):
                        with col:
                            st.image(batch["image_urls"][j], width="stretch")

                # 显示评论
                if batch.get("comment"):
                    st.markdown(f"**💬 评论**: {batch['comment']}")

                # 删除批次按钮
                if st.button("🗑️ 删除此批次", key=f"del_batch_{i}"):
                    removed = st.session_state.submitted_batches.pop(i)
                    print(f"[DEBUG] 删除批次: {removed['batch_id']}")
                    st.rerun()

    # ==================== v0.3.0 批次输入区域 ====================
    st.markdown("---")

    # 创建两列布局：左侧照片，右侧评论
    col_photos, col_comment = st.columns([1, 1])

    with col_photos:
        st.markdown("#### 📷 照片区域")

        # 隐藏 file_uploader 默认 UI
        st.markdown("""
        <style>
        /* 隐藏 file_uploader 的默认界面 */
        div[data-testid="stFileUploader"] {
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
        }
        div[data-testid="stFileUploader"] > label {
            display: none !important;
        }
        div[data-testid="stFileUploader"] div[data-testid="stoCloudUploadIcon"] {
            display: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        # 照片添加选项卡
        photo_tab1, photo_tab2 = st.tabs(["📁 照片", "📷 拍照"])

        with photo_tab1:
            # 从文件选择（隐藏UI）
            uploaded_files = st.file_uploader(
                "点击选择照片",
                type=["jpg", "jpeg", "png"],
                accept_multiple_files=True,
                key="batch_photo_upload_files",
                label_visibility="visible"
            )

            if uploaded_files:
                # 处理新上传的文件（使用文件名+位置作为唯一标识）
                new_files_added = False
                for uploaded_file in uploaded_files:
                    # 创建唯一标识：文件名 + 文件大小
                    file_id = f"{uploaded_file.name}_{uploaded_file.size}"

                    # 检查是否已处理过此文件
                    if file_id not in st.session_state._processed_files:
                        is_duplicate = any(
                            p.get("filename") == uploaded_file.name
                            for p in st.session_state.current_batch_photos
                        )
                        if not is_duplicate:
                            image = validate_image(uploaded_file)
                            if image:
                                st.session_state.current_batch_photos.append({
                                    "image": image,
                                    "filename": uploaded_file.name
                                })
                                print(f"[DEBUG] 添加照片: {uploaded_file.name}")
                                st.session_state._processed_files.add(file_id)
                                new_files_added = True

                # 只有在添加了新文件时才 rerun
                if new_files_added:
                    st.rerun()

        with photo_tab2:
            # 拍照
            camera_image = st.camera_input("拍照", key="batch_photo_camera", label_visibility="collapsed")
            if camera_image:
                # 使用时间戳+文件大小作为唯一标识
                file_id = f"camera_{camera_image.name}_{camera_image.size}"

                if file_id not in st.session_state._processed_files:
                    image = validate_image(camera_image)
                    if image:
                        filename = f"camera_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                        st.session_state.current_batch_photos.append({
                            "image": image,
                            "filename": filename
                        })
                        print(f"[DEBUG] 添加拍照: {filename}")
                        st.session_state._processed_files.add(file_id)
                        st.rerun()

        # 显示已添加的照片网格
        if st.session_state.current_batch_photos:
            st.markdown(f"**已添加 {len(st.session_state.current_batch_photos)} 张照片**")

            # 网格布局显示照片（每行3张）
            for i in range(0, len(st.session_state.current_batch_photos), 3):
                cols = st.columns(3)
                for j, col in enumerate(cols):
                    idx = i + j
                    if idx < len(st.session_state.current_batch_photos):
                        photo = st.session_state.current_batch_photos[idx]
                        with col:
                            st.image(photo["image"], width="content")
                            # 删除按钮
                            if st.button("🗑️", key=f"del_photo_{idx}"):
                                removed = st.session_state.current_batch_photos.pop(idx)
                                print(f"[DEBUG] 删除照片: {removed['filename']}")
                                st.rerun()

    with col_comment:
        st.markdown("#### 📝 我的感想")

        # 评论输入区域
        comment = st.text_area(
            "在这里记录你的旅行感受...",
            placeholder="""提示：可以包含以下信息
• 时间：今天下午、傍晚时分...
• 地点：西湖边、断桥上、雷峰塔下...
• 人物：和家人、和朋友...
• 感受：风景很美、心情愉快...""",
            key="batch_comment",
            height=350,
            label_visibility="collapsed"
        )
        st.session_state.current_batch_comment = comment

    # 提交这批内容按钮
    st.markdown("---")
    if st.button("📤 提交这批内容", use_container_width=True, type="primary"):
        if not st.session_state.current_batch_photos:
            st.warning("请先添加照片")
            return

        # 提交批次
        with st.spinner("正在提交批次..."):
            try:
                print(f"[DEBUG] 开始提交批次，照片数量: {len(st.session_state.current_batch_photos)}")

                # 上传照片到 OSS
                image_client = ImageClient()
                batch_id = str(uuid.uuid4())
                image_urls = []

                for i, photo in enumerate(st.session_state.current_batch_photos):
                    print(f"[DEBUG] 上传照片 {i+1}/{len(st.session_state.current_batch_photos)}")
                    img_bytes = compress_image(photo["image"])
                    filename = f"batch_{batch_id}_photo_{i+1}.jpg"
                    url = image_client.upload_image(img_bytes, username, batch_id, filename)
                    image_urls.append(url)
                    print(f"[DEBUG] 照片上传成功: {url}")

                # 创建批次记录
                batch = {
                    "batch_id": batch_id,
                    "image_urls": image_urls,
                    "comment": st.session_state.current_batch_comment,
                    "timestamp": datetime.now().isoformat()
                }

                st.session_state.submitted_batches.append(batch)
                print(f"[DEBUG] 提交批次 {batch_id}: {len(image_urls)} 张照片")

                # 清空当前批次
                st.session_state.current_batch_photos = []
                st.session_state.current_batch_comment = ""

                st.success(f"✅ 已提交批次 {len(st.session_state.submitted_batches)}！继续添加或生成游记")
                st.rerun()

            except Exception as e:
                st.error(f"提交失败: {str(e)}")
                print(f"[DEBUG] 提交批次错误: {e}")
                import traceback
                traceback.print_exc()

    # 生成游记按钮
    st.markdown("---")
    if st.button("✨ 生成游记", use_container_width=True, type="primary"):
        if not st.session_state.submitted_batches:
            st.warning("请先至少提交一批内容")
            return

        # 使用默认值
        location = "未命名地点"
        travel_date = str(datetime.now().date())
        auto_title = True

        generate_trip_note(username, location, travel_date, auto_title)


def generate_trip_note(username: str, location: str, travel_date: str, auto_title: bool):
    """生成游记 - v0.3.0 批次模式"""
    with st.spinner("正在生成游记..."):
        try:
            # 初始化客户端
            ai_client = AIClient()
            ocr_client = OCRClient()
            user_client = UserClient()

            # 生成游记 ID
            note_id = str(uuid.uuid4())

            # 收集所有照片信息（从已提交的批次中）
            all_image_urls = []
            all_comments = []
            ocr_results = {}

            with st.expander("处理进度", expanded=True):
                total_photos = sum(len(batch.get("image_urls", [])) for batch in st.session_state.submitted_batches)
                processed = 0

                for i, batch in enumerate(st.session_state.submitted_batches):
                    st.markdown(f"处理批次 {i + 1}/{len(st.session_state.submitted_batches)}...")

                    # 收集照片 URL 和评论
                    image_urls = batch.get("image_urls", [])
                    comment = batch.get("comment", "")

                    all_image_urls.extend(image_urls)
                    if comment:
                        all_comments.append(f"批次{i+1}: {comment}")

                    # OCR 识别（下载图片进行识别）
                    for j, url in enumerate(image_urls):
                        try:
                            # 尝试从 URL 下载图片进行 OCR
                            import requests
                            from io import BytesIO

                            response = requests.get(url, timeout=10)
                            if response.status_code == 200:
                                img_bytes = response.content
                                ocr_text = ocr_client.extract_text_from_image(img_bytes)
                                if ocr_text:
                                    ocr_results[f"batch{i+1}_photo{j+1}"] = ocr_text
                        except Exception as e:
                            print(f"[DEBUG] OCR 识别失败: {e}")

                    processed += len(image_urls)
                    st.progress(processed / total_photos)

                st.markdown("📝 正在生成游记...")

            # 使用整体游记生成方法
            ai_content = ai_client.generate_trip_note(
                location=location,
                travel_date=travel_date,
                batches=st.session_state.submitted_batches,
                ocr_results=ocr_results if ocr_results else None
            )

            # 提取标题（AI 生成的内容第一行通常是标题）
            title = ai_content.split("\n")[0].strip("#").strip()
            if not title or auto_title:
                # 如果 AI 没有生成标题或需要自动生成，使用专门的标题生成
                title = ai_client.generate_title(location, travel_date, len(all_image_urls))

            # 准备保存数据
            user_notes_str = "\n".join(all_comments) if all_comments else ""
            ocr_results_str = ocr_results if ocr_results else {}

            # 保存到飞书
            success, message, _ = user_client.create_note(
                username=username,
                title=title,
                location=location,
                travel_date=travel_date,
                images=all_image_urls,
                ocr_results=ocr_results_str,
                user_notes=user_notes_str,
                ai_content=ai_content
            )

            if success:
                st.success("🎉 游记创建成功！")

                # 显示生成的游记
                st.markdown("---")
                st.markdown("### 📖 生成的游记")

                # 添加 CSS 样式控制游记中的图片大小
                st.markdown("""
                <style>
                /* 游记内容中的图片样式 */
                .stMarkdown img {
                    max-width: 600px;
                    width: 100%;
                    height: auto;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                    margin: 16px 0;
                }
                </style>
                """, unsafe_allow_html=True)

                # 使用 Markdown 渲染 AI 生成的内容
                st.markdown(ai_content)

                # 清空临时数据
                st.session_state.submitted_batches = []
                st.session_state.current_batch_photos = []
                st.session_state.current_batch_comment = ""

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
