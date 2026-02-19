# pages/6_编辑游记.py
# -*- coding: utf-8 -*-
"""
编辑游记页面
编辑已有的游记
"""

import streamlit as st
import uuid
from datetime import datetime
from utils.auth import require_login
from utils.image_utils import validate_image, compress_image
from clients.user_client import UserClient
from clients.ai_client import AIClient
from clients.ocr_client import OCRClient
from clients.image_client import ImageClient

# 页面配置
st.set_page_config(
    page_title="编辑游记 - 游记助手",
    page_icon="✏️",
    layout="wide"
)

# 初始化 session state
if "edit_photo_entries" not in st.session_state:
    st.session_state.edit_photo_entries = []
if "current_entry_id" not in st.session_state:
    st.session_state.current_entry_id = None


def require_auth():
    """检查登录状态"""
    if not require_login():
        st.stop()
    return st.session_state.username


def load_note_for_edit(note_id: str):
    """
    加载游记数据用于编辑

    Args:
        note_id: 游记 ID

    Returns:
        游记数据或 None
    """
    try:
        user_client = UserClient()
        note = user_client.get_note(note_id)
        return note
    except Exception as e:
        st.error(f"加载游记失败: {str(e)}")
        return None


def show_edit_page():
    """显示编辑页面"""
    username = require_auth()

    # 获取要编辑的游记 ID
    note_id = st.session_state.get("edit_note_id", "")

    if not note_id:
        st.error("缺少游记 ID")
        if st.button("返回", use_container_width=True):
            st.switch_page("pages/4_我的游记.py")
        return

    # 加载游记数据
    note = load_note_for_edit(note_id)

    if not note:
        if st.button("返回", use_container_width=True):
            st.switch_page("pages/4_我的游记.py")
        return

    # 验证权限
    if note.get("username") != username:
        st.error("无权编辑此游记")
        if st.button("返回", use_container_width=True):
            st.switch_page("pages/4_我的游记.py")
        return

    st.title(f"✏️ 编辑游记: {note.get('title', '未命名')}")

    # 基本信息
    col1, col2 = st.columns(2)

    with col1:
        new_title = st.text_input("标题", value=note.get("title", ""))

    with col2:
        new_location = st.text_input("地点/景区", value=note.get("location", ""))

    new_travel_date = st.date_input("旅行日期", datetime.now().date())

    st.markdown("---")

    # 选项卡
    tab1, tab2, tab3 = st.tabs(["📝 编辑内容", "📷 管理照片", "🤖 重新生成"])

    with tab1:
        st.markdown("### 编辑游记内容")

        # AI 生成的内容
        st.markdown("#### AI 生成的游记")
        edit_ai_content = st.text_area(
            "游记内容",
            value=note.get("ai_content", ""),
            height=300,
            help="你可以直接编辑 AI 生成的内容"
        )

        # 用户备注
        st.markdown("#### 我的感想")
        user_notes = note.get("user_notes", "")
        edit_user_notes = st.text_area(
            "感想备注",
            value=user_notes,
            height=100,
            help="添加或修改你的旅行感想"
        )

    with tab2:
        st.markdown("### 管理照片")

        # 显示现有照片
        images = note.get("images", [])
        if images:
            st.markdown("#### 现有照片")

            for i, img_url in enumerate(images):
                col1, col2, col3 = st.columns([1, 3, 1])

                with col1:
                    st.image(img_url, use_column_width=True)

                with col2:
                    st.markdown(f"照片 {i + 1}")
                    st.caption(img_url)

                with col3:
                    if st.button("删除", key=f"del_img_{i}"):
                        if st.session_state.get(f"confirm_del_img_{i}", False):
                            images.pop(i)
                            st.success("已删除")
                            st.rerun()
                        else:
                            st.session_state[f"confirm_del_img_{i}"] = True
                            st.rerun()

        # 添加新照片
        st.markdown("---")
        st.markdown("#### 添加新照片")

        uploaded_file = st.file_uploader(
            "上传新照片",
            type=["jpg", "jpeg", "png"],
            key="edit_upload"
        )

        if uploaded_file:
            image = validate_image(uploaded_file)
            if image:
                col1, col2 = st.columns([1, 1])

                with col1:
                    st.image(image, use_column_width=True)

                with col2:
                    photo_note = st.text_area("照片备注", key=f"new_photo_note")

                    # OCR 识别
                    if st.button("🔍 OCR 识别", key=f"ocr_new"):
                        with st.spinner("正在识别..."):
                            try:
                                ocr_client = OCRClient()
                                img_bytes = compress_image(image)
                                ocr_text = ocr_client.extract_text_from_image(img_bytes)

                                if ocr_text:
                                    st.success(f"识别到文字: {ocr_text[:50]}...")
                                    st.session_state.new_ocr_text = ocr_text
                                else:
                                    st.info("未识别到文字")
                            except Exception as e:
                                st.error(f"OCR 失败: {str(e)}")

                    if st.button("➕ 添加到游记", type="primary"):
                        st.session_state.pending_new_photo = {
                            "image": image,
                            "note": photo_note,
                            "ocr": st.session_state.get("new_ocr_text", "")
                        }
                        st.success("照片已添加，点击保存按钮保存更改")

    with tab3:
        st.markdown("### 重新生成游记")

        st.info("📌 使用当前照片和备注重新生成游记内容，将覆盖现有内容")

        col1, col2 = st.columns(2)

        with col1:
            use_current_photos = st.checkbox("使用现有照片", value=True)

        with col2:
            include_ocr = st.checkbox("包含 OCR 识别内容", value=True)

        if st.button("🤖 开始重新生成", type="primary"):
            with st.spinner("正在生成游记..."):
                try:
                    ai_client = AIClient()

                    # 构建上下文
                    images_context = f"共{len(images)}张照片" if use_current_photos else ""
                    user_notes_context = edit_user_notes or "用户暂无备注"

                    # 生成新内容
                    new_content = ai_client.generate_trip_note(
                        location=new_location,
                        travel_date=str(new_travel_date),
                        images_context=images_context,
                        user_notes=user_notes_context,
                        ocr_context=""
                    )

                    # 更新编辑区
                    edit_ai_content = new_content
                    st.session_state.edit_ai_content = new_content
                    st.success("游记内容已更新！请切换到"编辑内容"标签查看")

                except Exception as e:
                    st.error(f"生成失败: {str(e)}")

    st.markdown("---")

    # 底部操作按钮
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        if st.button("💾 保存更改", use_container_width=True, type="primary"):
            with st.spinner("保存中..."):
                try:
                    user_client = UserClient()

                    # 准备更新数据
                    update_data = {
                        "title": new_title,
                        "location": new_location,
                        "travel_date": str(new_travel_date),
                        "user_notes": edit_user_notes,
                        "ai_content": edit_ai_content
                    }

                    # 更新游记
                    success, message = user_client.update_note(note_id, **update_data)

                    if success:
                        st.success("保存成功！")

                        # 处理新增照片
                        if st.session_state.get("pending_new_photo"):
                            try:
                                image_client = ImageClient()
                                pending = st.session_state.pending_new_photo

                                # 上传图片
                                img_bytes = compress_image(pending["image"])
                                filename = f"new_photo_{uuid.uuid4().hex[:8]}.jpg"
                                url = image_client.upload_image(img_bytes, username, note_id, filename)

                                # 添加到图片列表
                                images.append(url)

                                # 更新游记
                                user_client.update_note(note_id, images=images)

                                st.success("新照片已上传")

                                # 清理临时数据
                                del st.session_state.pending_new_photo

                            except Exception as e:
                                st.warning(f"照片上传失败: {str(e)}")

                        # 返回详情页
                        if st.button("查看游记", use_container_width=True):
                            st.session_state.view_note_id = note_id
                            st.switch_page("pages/5_游记详情.py")

                    else:
                        st.error(f"保存失败: {message}")

                except Exception as e:
                    st.error(f"保存失败: {str(e)}")

    with col2:
        if st.button("👁️ 预览", use_container_width=True):
            st.session_state.view_note_id = note_id
            st.switch_page("pages/5_游记详情.py")

    with col3:
        if st.button("📚 返回列表", use_container_width=True):
            st.switch_page("pages/4_我的游记.py")

    with col4:
        if st.button("🏠 返回首页", use_container_width=True):
            st.switch_page("app.py")


def main():
    """主函数"""
    show_edit_page()


if __name__ == "__main__":
    main()
