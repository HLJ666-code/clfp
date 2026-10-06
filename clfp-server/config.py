# -*- coding: utf-8 -*-
"""全局配置：通过同目录 .env 文件或环境变量覆盖。"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CLFP 校园智能失物招领平台"

    # 默认 SQLite，零配置即可运行；最终演示按文档切换 MySQL：
    # DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/clfp_biz?charset=utf8mb4
    database_url: str = "sqlite:///./clfp.db"

    jwt_secret: str = "clfp-dev-secret-please-change-in-prod-2026-09"  # 生产请用 .env 覆盖
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7  # 7 天

    max_login_fail: int = 5     # 连续错误次数上限
    lock_minutes: int = 30      # 锁定时长（分钟）

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
