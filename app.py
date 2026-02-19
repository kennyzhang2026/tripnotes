# app.py
# -*- coding: utf-8 -*-
"""
游记助手 - 主应用入口
基于 Streamlit 的多页面应用
"""

import streamlit as st
from utils.auth import is_logged_in, get_current_user

# 页面配置
st.set_page_config(
    page_title="游记助手",
    page_icon="📸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 自定义 CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
    }
    .hero-title {
        font-size: 2.5rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: white;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .big-button {
        width: 100%;
        padding: 1rem;
        font-size: 1.2rem;
        border-radius: 10px;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


def show_home_page():
    """显示首页"""
    st.markdown("""
    <div class="main-header">
        <div class="hero-title">📸 游记助手</div>
        <div class="hero-subtitle">AI 驱动的图文游记生成工具</div>
    </div>
    """, unsafe_allow_html=True)

    # 如果未登录
    if not is_logged_in():
        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔐 登录", use_container_width=True, type="primary"):
                st.switch_page("pages/1_登录.py")

        with col2:
            if st.button("✨ 注册", use_container_width=True):
                st.switch_page("pages/2_注册.py")

        st.markdown("---")

        # 功能介绍
        st.markdown("### ✨ 核心功能")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown("""
            <div class="feature-card">
                <h4>📷 拍照记录</h4>
                <p>随时拍照上传，记录美好瞬间</p>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown("""
            <div class="feature-card">
                <h4>🎤 语音输入</h4>
                <p>语音转文字，快速记录感想</p>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown("""
            <div class="feature-card">
                <h4>🤖 AI 生成</h4>
                <p>智能整理，生成精美游记</p>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 📚 更多功能")
        st.markdown("- OCR 文字识别与文化解释")
        st.markdown("- 保存到飞书多维表格")
        st.markdown("- 支持导出分享")

    # 如果已登录
    else:
        username = get_current_user()
        st.success(f"👋 欢迎，{username}！")

        # 大按钮快速进入
        if st.button("📝 创建新游记", use_container_width=True, type="primary"):
            st.switch_page("pages/3_创建游记.py")

        # 查看我的游记
        st.markdown("---")
        st.markdown("### 📚 我的游记")

        try:
            from clients.user_client import UserClient
            user_client = UserClient()
            notes = user_client.list_notes(username, limit=10)

            if notes:
                for note in notes[:5]:  # 显示最近5篇
                    with st.expander(f"📖 {note.get('title', '未命名游记')} - {note.get('location', '')}"):
                        st.markdown(f"**日期**: {note.get('travel_date', '未知')}")
                        st.markdown(f"**游记ID**: {note.get('note_id', '')}")
            else:
                st.info("暂无游记，快去创建第一篇吧！")

        except Exception as e:
            st.warning(f"加载游记列表失败: {str(e)}")

        # 退出登录
        st.markdown("---")
        if st.button("🚪 退出登录", use_container_width=True):
            from utils.auth import logout
            logout()
            st.rerun()


def main():
    """主函数"""
    # 初始化 session state
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = None

    # 显示首页
    show_home_page()


if __name__ == "__main__":
    main()
