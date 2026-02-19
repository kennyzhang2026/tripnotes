# pages/1_登录.py
# -*- coding: utf-8 -*-
"""
登录页面
"""

import streamlit as st
from clients.auth_client import AuthClient
from utils.auth import set_logged_in

# 页面配置
st.set_page_config(
    page_title="登录 - 游记助手",
    page_icon="🔐",
    layout="centered"
)

# 自定义 CSS
st.markdown("""
<style>
    .login-container {
        max-width: 400px;
        margin: 0 auto;
        padding: 2rem;
    }
    .login-title {
        text-align: center;
        font-size: 2rem;
        margin-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def show_login_page():
    """显示登录页面"""
    st.markdown('<div class="login-title">🔐 用户登录</div>', unsafe_allow_html=True)

    # 如果已登录，提示并跳转
    from utils.auth import is_logged_in
    if is_logged_in():
        st.success("您已登录！")
        if st.button("返回首页", use_container_width=True):
            st.switch_page("app.py")
        return

    # 登录表单
    with st.form("login_form"):
        username = st.text_input(
            "👤 用户名",
            placeholder="请输入用户名",
            max_chars=20
        )
        password = st.text_input(
            "🔑 密码",
            type="password",
            placeholder="请输入密码",
            max_chars=50
        )

        submit = st.form_submit_button("登录", use_container_width=True, type="primary")

        if submit:
            if not username or not password:
                st.error("请输入用户名和密码")
                return

            # 尝试登录
            with st.spinner("登录中..."):
                try:
                    auth_client = AuthClient()
                    success, message = auth_client.login(username, password)

                    if success:
                        set_logged_in(username)
                        st.success("登录成功！正在跳转...")
                        st.switch_page("app.py")
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"登录失败: {str(e)}")

    st.markdown("---")

    # 注册链接
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown('<div style="text-align: center;">还没有账号？</div>', unsafe_allow_html=True)
        if st.button("去注册", use_container_width=True):
            st.switch_page("pages/2_注册.py")


def main():
    """主函数"""
    show_login_page()


if __name__ == "__main__":
    main()
