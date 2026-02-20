# pages/4_我的游记.py
# -*- coding: utf-8 -*-
"""
我的游记页面
显示用户的游记列表
"""

import streamlit as st
from datetime import datetime
from utils.auth import require_login
from clients.user_client import UserClient

# 页面配置
st.set_page_config(
    page_title="我的游记 - 游记助手",
    page_icon="📚",
    layout="wide"
)


def require_auth():
    """检查登录状态"""
    if not require_login():
        st.stop()
    return st.session_state.username


def show_note_card(note, index):
    """
    显示游记卡片

    Args:
        note: 游记数据
        index: 索引
    """
    col1, col2 = st.columns([1, 3])

    with col1:
        # 显示第一张图片
        images = note.get("images", [])
        if images and len(images) > 0:
            st.image(images[0], width="content")
        else:
            st.image("https://via.placeholder.com/300x200?text=无图片", width="content")

    with col2:
        # 标题和操作按钮
        col_title, col_actions = st.columns([3, 1])

        with col_title:
            st.markdown(f"### {note.get('title', '未命名游记')}")

        with col_actions:
            if st.button("👁️", key=f"view_{note['note_id']}", help="查看详情"):
                st.session_state.view_note_id = note["note_id"]
                st.switch_page("pages/5_游记详情.py")

            if st.button("✏️", key=f"edit_{note['note_id']}", help="编辑"):
                st.session_state.edit_note_id = note["note_id"]
                st.switch_page("pages/6_编辑游记.py")

            if st.button("🗑️", key=f"delete_{note['note_id']}", help="删除"):
                st.session_state.delete_note_id = note["note_id"]
                st.session_state.show_delete_confirm = True

        # 元信息
        col_meta1, col_meta2, col_meta3 = st.columns(3)
        with col_meta1:
            st.markdown(f"📍 {note.get('location', '未知地点')}")
        with col_meta2:
            st.markdown(f"📅 {note.get('travel_date', '未知日期')}")
        with col_meta3:
            if note.get("created_at"):
                created_dt = datetime.fromtimestamp(note["created_at"] / 1000)
                st.markdown(f"🕒 {created_dt.strftime('%Y-%m-%d')}")

        # 摘要
        ai_content = note.get("ai_content", "")
        if ai_content:
            # 提取前 150 字作为摘要
            summary = ai_content[:150].replace("#", "").replace("*", "").strip()
            if len(ai_content) > 150:
                summary += "..."
            st.markdown(f"*{summary}*")

        # 图片数量
        images_count = len(note.get("images", []))
        if images_count > 0:
            st.markdown(f"📷 {images_count} 张照片")

        st.markdown("---")


def show_delete_confirmation():
    """显示删除确认对话框"""
    if st.session_state.get("show_delete_confirm", False):
        note_id = st.session_state.get("delete_note_id", "")

        st.warning("⚠️ 确定要删除这篇游记吗？此操作无法撤销！")

        col1, col2, col3 = st.columns([1, 1, 2])

        with col1:
            if st.button("确认删除", type="primary"):
                with st.spinner("删除中..."):
                    try:
                        user_client = UserClient()
                        success, message = user_client.delete_note(note_id)

                        if success:
                            st.success("游记已删除")
                            st.session_state.show_delete_confirm = False
                            st.session_state.delete_note_id = None
                            st.rerun()
                        else:
                            st.error(f"删除失败: {message}")
                    except Exception as e:
                        st.error(f"删除失败: {str(e)}")

        with col2:
            if st.button("取消"):
                st.session_state.show_delete_confirm = False
                st.session_state.delete_note_id = None
                st.rerun()


def show_my_notes_page():
    """显示我的游记页面"""
    username = require_auth()

    st.title("📚 我的游记")
    st.markdown("---")

    # 顶部操作栏
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        search = st.text_input("🔍 搜索游记", placeholder="输入标题或地点搜索...")

    with col2:
        sort_by = st.selectbox(
            "排序方式",
            ["创建时间降序", "创建时间升序", "旅行日期降序", "旅行日期升序"],
            label_visibility="collapsed"
        )

    with col3:
        if st.button("➕ 新建游记", use_container_width=True, type="primary"):
            st.switch_page("pages/3_创建游记.py")

    st.markdown("---")

    # 获取游记列表
    try:
        user_client = UserClient()
        notes = user_client.list_notes(username, limit=100)

        # 过滤和排序
        if search:
            notes = [
                n for n in notes
                if search.lower() in n.get("title", "").lower() or
                   search.lower() in n.get("location", "").lower()
            ]

        # 排序
        if sort_by == "创建时间降序":
            notes.sort(key=lambda x: x.get("created_at", 0), reverse=True)
        elif sort_by == "创建时间升序":
            notes.sort(key=lambda x: x.get("created_at", 0))
        elif sort_by == "旅行日期降序":
            notes.sort(key=lambda x: x.get("travel_date", ""), reverse=True)
        elif sort_by == "旅行日期升序":
            notes.sort(key=lambda x: x.get("travel_date", ""))

        # 显示游记
        if notes:
            for i, note in enumerate(notes):
                # 获取完整游记数据
                full_note = user_client.get_note(note["note_id"])
                if full_note:
                    show_note_card(full_note, i)

            # 删除确认对话框
            show_delete_confirmation()

        else:
            # 空状态
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <div style="font-size: 4rem;">📝</div>
                <h3>还没有游记</h3>
                <p>点击上方"新建游记"按钮，开始记录你的旅行吧！</p>
            </div>
            """, unsafe_allow_html=True)

            if st.button("创建第一篇游记", use_container_width=True, type="primary"):
                st.switch_page("pages/3_创建游记.py")

    except Exception as e:
        st.error(f"加载游记列表失败: {str(e)}")
        st.exception(e)

    # 返回首页按钮
    st.markdown("---")
    if st.button("🏠 返回首页", use_container_width=True):
        st.switch_page("app.py")


def main():
    """主函数"""
    show_my_notes_page()


if __name__ == "__main__":
    main()
