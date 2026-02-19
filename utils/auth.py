# auth.py
# -*- coding: utf-8 -*-
"""
认证工具模块
提供用户认证相关的工具函数
"""

import hashlib
import streamlit as st
from typing import Optional


def hash_password(password: str) -> str:
    """
    对密码进行哈希加密

    Args:
        password: 原始密码

    Returns:
        加密后的密码
    """
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
    """
    验证密码是否正确

    Args:
        password: 原始密码
        hashed: 加密后的密码

    Returns:
        是否匹配
    """
    return hash_password(password) == hashed


def is_logged_in() -> bool:
    """
    检查用户是否已登录

    Returns:
        是否已登录
    """
    return "username" in st.session_state and st.session_state.username is not None


def get_current_user() -> Optional[str]:
    """
    获取当前登录用户名

    Returns:
        当前用户名，未登录返回 None
    """
    return st.session_state.get("username")


def set_logged_in(username: str) -> None:
    """
    设置用户登录状态

    Args:
        username: 用户名
    """
    st.session_state.username = username
    st.session_state.logged_in = True


def logout() -> None:
    """用户登出"""
    st.session_state.username = None
    st.session_state.logged_in = False
    # 清除其他会话数据
    for key in list(st.session_state.keys()):
        if key not in ["logged_in", "username"]:
            del st.session_state[key]


def require_login() -> bool:
    """
    要求用户登录，未登录则跳转到登录页

    Returns:
        是否已登录
    """
    if not is_logged_in():
        st.switch_page("pages/1_登录.py")
        return False
    return True
