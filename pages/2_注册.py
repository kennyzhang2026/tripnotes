# pages/2_注册.py
# -*- coding: utf-8 -*-
"""
注册页面
"""

import streamlit as st
from clients.auth_client import AuthClient

# 页面配置
st.set_page_config(
    page_title="注册 - 游记助手",
    page_icon="✨",
    layout="centered"
)

# 自定义 CSS
st.markdown("""
<style>
    .register-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    .register-title {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def show_register_page():
    """显示注册页面"""
    st.markdown('<div class="register-title">✨ 用户注册</div>', unsafe_allow_html=True)

    # 注册表单
    with st.form("register_form"):
        username = st.text_input(
            "👤 用户名",
            placeholder="请输入用户名（至少3个字符）",
            max_chars=20,
            help="用户名只能包含字母和数字"
        )
        password = st.text_input(
            "🔑 密码",
            type="password",
            placeholder="请输入密码（至少6个字符）",
            max_chars=50,
            help="密码至少需要6个字符"
        )
        confirm_password = st.text_input(
            "🔐 确认密码",
            type="password",
            placeholder="请再次输入密码",
            max_chars=50
        )

        submit = st.form_submit_button("注册", use_container_width=True, type="primary")

        if submit:
            # 验证输入
            if not username:
                st.error("请输入用户名")
                return

            if not password:
                st.error("请输入密码")
                return

            if password != confirm_password:
                st.error("两次输入的密码不一致")
                return

            # 尝试注册
            with st.spinner("注册中..."):
                try:
                    auth_client = AuthClient()
                    success, message = auth_client.register(username, password)

                    if success:
                        st.success(f"{message}！请登录")
                        if st.button("去登录", use_container_width=True):
                            st.switch_page("pages/1_登录.py")
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"注册失败: {str(e)}")

    st.markdown("---")

    # 登录链接
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center;">已有账号？</div>', unsafe_allow_html=True)
        if st.button("去登录", use_container_width=True):
            st.switch_page("pages/1_登录.py")


def main():
    """主函数"""
    show_register_page()


if __name__ == "__main__":
    main()
