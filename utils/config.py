# config.py
# -*- coding: utf-8 -*-
"""
配置管理模块
从 streamlit secrets 中读取配置，并提供统一访问接口
"""

import streamlit as st


class Config:
    """配置类 - 从 streamlit secrets 读取配置"""

    @staticmethod
    def get_deepseek_api_key() -> str:
        """获取 DeepSeek API Key"""
        return st.secrets["DEEPSEEK_API_KEY"]

    @staticmethod
    def get_aliyun_access_key_id() -> str:
        """获取阿里云 Access Key ID"""
        return st.secrets["ALIYUN_ACCESS_KEY_ID"]

    @staticmethod
    def get_aliyun_access_key_secret() -> str:
        """获取阿里云 Access Key Secret"""
        return st.secrets["ALIYUN_ACCESS_KEY_SECRET"]

    @staticmethod
    def get_aliyun_ocr_endpoint() -> str:
        """获取阿里云 OCR 端点"""
        return st.secrets.get("ALIYUN_OCR_ENDPOINT", "https://ocr-api.cn-hangzhou.aliyuncs.com")

    @staticmethod
    def get_aliyun_oss_bucket_name() -> str:
        """获取阿里云 OSS Bucket 名称"""
        return st.secrets["ALIYUN_OSS_BUCKET_NAME"]

    @staticmethod
    def get_aliyun_oss_endpoint() -> str:
        """获取阿里云 OSS 端点"""
        return st.secrets["ALIYUN_OSS_ENDPOINT"]

    @staticmethod
    def get_aliyun_asr_endpoint() -> str:
        """获取阿里云 ASR 端点"""
        return st.secrets.get("ALIYUN_ASR_ENDPOINT", "https://nls-meta.cn-shanghai.aliyuncs.com")

    @staticmethod
    def get_aliyun_asr_app_key() -> str:
        """获取阿里云 ASR App Key"""
        return st.secrets["ALIYUN_ASR_APP_KEY"]

    @staticmethod
    def get_feishu_app_id() -> str:
        """获取飞书 App ID"""
        return st.secrets["FEISHU_APP_ID"]

    @staticmethod
    def get_feishu_app_secret() -> str:
        """获取飞书 App Secret"""
        return st.secrets["FEISHU_APP_SECRET"]

    @staticmethod
    def get_feishu_app_token_user() -> str:
        """获取飞书用户表 App Token"""
        return st.secrets["FEISHU_APP_TOKEN_USER"]

    @staticmethod
    def get_feishu_table_id_user() -> str:
        """获取飞书用户表 Table ID"""
        return st.secrets["FEISHU_TABLE_ID_USER"]

    @staticmethod
    def get_feishu_app_token_note() -> str:
        """获取飞书记录表 App Token"""
        return st.secrets["FEISHU_APP_TOKEN_NOTE"]

    @staticmethod
    def get_feishu_table_id_note() -> str:
        """获取飞书记录表 Table ID"""
        return st.secrets["FEISHU_TABLE_ID_NOTE"]


# 便捷访问函数
def get_config() -> Config:
    """获取配置实例"""
    return Config()
