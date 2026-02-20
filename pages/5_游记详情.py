# pages/5_游记详情.py
# -*- coding: utf-8 -*-
"""
游记详情页面
查看单篇游记的完整内容
"""

import streamlit as st
from datetime import datetime
from utils.auth import require_login
from clients.user_client import UserClient

# 页面配置
st.set_page_config(
    page_title="游记详情 - 游记助手",
    page_icon="📖",
    layout="wide"
)


def require_auth():
    """检查登录状态"""
    if not require_login():
        st.stop()
    return st.session_state.username


def show_note_detail(note_id: str):
    """
    显示游记详情

    Args:
        note_id: 游记 ID
    """
    username = require_auth()

    try:
        user_client = UserClient()
        note = user_client.get_note(note_id)

        if not note:
            st.error("游记不存在或已被删除")
            if st.button("返回", use_container_width=True):
                st.switch_page("pages/4_我的游记.py")
            return

        # 验证权限
        if note.get("username") != username:
            st.error("无权查看此游记")
            if st.button("返回", use_container_width=True):
                st.switch_page("pages/4_我的游记.py")
            return

        # 标题和操作栏
        col1, col2 = st.columns([4, 1])

        with col1:
            st.title(note.get("title", "未命名游记"))

        with col2:
            if st.button("✏️ 编辑", use_container_width=True):
                st.session_state.edit_note_id = note_id
                st.switch_page("pages/6_编辑游记.py")

        # 元信息
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(f"📍 **地点**: {note.get('location', '未知')}")

        with col2:
            st.markdown(f"📅 **日期**: {note.get('travel_date', '未知')}")

        with col3:
            if note.get("created_at"):
                created_dt = datetime.fromtimestamp(note["created_at"] / 1000)
                st.markdown(f"🕒 **创建**: {created_dt.strftime('%Y-%m-%d %H:%M')}")

        with col4:
            images_count = len(note.get("images", []))
            st.markdown(f"📷 **照片**: {images_count} 张")

        st.markdown("---")

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

        # 游记内容（全宽显示，照片嵌入在内容中）
        st.markdown("## 📝 游记内容")

        # AI 生成的游记内容
        ai_content = note.get("ai_content", "")
        if ai_content:
            st.markdown(ai_content)
        else:
            st.info("暂无游记内容")

        # 用户备注
        user_notes = note.get("user_notes", "")
        if user_notes:
            st.markdown("---")
            st.markdown("### 💭 我的感想")
            st.markdown(user_notes)

        # OCR 识别结果
        ocr_results = note.get("ocr_results", {})
        if ocr_results:
            st.markdown("---")
            st.markdown("### 🔍 OCR 识别内容")

            for photo_name, ocr_text in ocr_results.items():
                if ocr_text:
                    with st.expander(f"📷 {photo_name}"):
                        st.markdown(ocr_text)

        st.markdown("---")

        # 底部操作栏
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            if st.button("🏠 返回首页", use_container_width=True):
                st.switch_page("app.py")

        with col2:
            if st.button("📚 返回列表", use_container_width=True):
                st.switch_page("pages/4_我的游记.py")

        with col3:
            if st.button("✏️ 编辑游记", use_container_width=True):
                st.session_state.edit_note_id = note_id
                st.switch_page("pages/6_编辑游记.py")

        with col4:
            if st.button("📤 导出游记", use_container_width=True):
                st.session_state.export_note_id = note_id
                st.session_state.show_export_options = True

        # 导出选项对话框
        if st.session_state.get("show_export_options", False):
            show_export_options(note)

    except Exception as e:
        st.error(f"加载游记失败: {str(e)}")
        st.exception(e)

        if st.button("返回", use_container_width=True):
            st.switch_page("pages/4_我的游记.py")


def show_export_options(note):
    """显示导出选项"""
    st.markdown("---")
    st.markdown("### 📤 导出游记")

    export_format = st.radio(
        "选择导出格式",
        ["Markdown", "纯文本"],
        horizontal=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("确认导出", type="primary"):
            content = generate_export_content(note, export_format)

            # 提供下载
            st.download_button(
                label=f"下载 {export_format} 文件",
                data=content,
                file_name=f"{note['title']}.{('md' if export_format == 'Markdown' else 'txt')}",
                mime="text/plain"
            )

    with col2:
        if st.button("取消"):
            st.session_state.show_export_options = False
            st.session_state.export_note_id = None
            st.rerun()


def generate_export_content(note, format_type: str) -> str:
    """
    生成导出内容

    Args:
        note: 游记数据
        format_type: 格式类型

    Returns:
        导出内容
    """
    title = note.get("title", "未命名游记")
    location = note.get("location", "")
    travel_date = note.get("travel_date", "")
    ai_content = note.get("ai_content", "")
    user_notes = note.get("user_notes", "")
    images = note.get("images", [])
    ocr_results = note.get("ocr_results", {})

    if format_type == "Markdown":
        content = f"""# {title}

**地点**: {location}
**日期**: {travel_date}

---

## 游记内容

{ai_content}

"""

        if user_notes:
            content += f"""## 我的感想

{user_notes}

"""

        if images:
            content += f"""## 照片集

共 {len(images)} 张照片
"""

        if ocr_results:
            content += """## OCR 识别内容

"""
            for photo_name, ocr_text in ocr_results.items():
                if ocr_text:
                    content += f"""### {photo_name}

{ocr_text}

"""

    else:  # 纯文本
        content = f"""{title}

地点: {location}
日期: {travel_date}

{'=' * 50}

游记内容

{ai_content}

"""

        if user_notes:
            content += f"""我的感想

{user_notes}

"""

        if images:
            content += f"""照片集: 共 {len(images)} 张照片
"""

        if ocr_results:
            content += """OCR 识别内容

"""
            for photo_name, ocr_text in ocr_results.items():
                if ocr_text:
                    content += f"""[{photo_name}]
{ocr_text}

"""

    return content


def main():
    """主函数"""
    # 从 URL 参数或 session state 获取 note_id
    note_id = st.session_state.get("view_note_id", "")

    if not note_id:
        st.error("缺少游记 ID 参数")
        if st.button("返回游记列表", use_container_width=True):
            st.switch_page("pages/4_我的游记.py")
        return

    show_note_detail(note_id)


if __name__ == "__main__":
    main()
