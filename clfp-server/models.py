# -*- coding: utf-8 -*-
"""ORM 模型。

User 为胡良均负责的核心表；Item 仅建最小字段，供“我的发布”联调，
后续由许世杰按发布/图片/检索需求扩展字段。
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, Boolean, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account: Mapped[str] = mapped_column(String(20), unique=True, index=True)  # 学号/工号
    password_hash: Mapped[str] = mapped_column(String(128))
    name: Mapped[str] = mapped_column(String(20))
    college: Mapped[str] = mapped_column(String(30), default="")
    phone: Mapped[str] = mapped_column(String(20), default="")
    email: Mapped[str] = mapped_column(String(60), default="")
    avatar: Mapped[str] = mapped_column(String(255), default="")
    role: Mapped[str] = mapped_column(String(10), default="user")     # user / admin
    status: Mapped[str] = mapped_column(String(10), default="active")  # active / locked / disabled
    fail_count: Mapped[int] = mapped_column(Integer, default=0)
    locked_until: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    show_contact: Mapped[bool] = mapped_column(Boolean, default=False)  # 是否授权公开联系方式
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"), index=True)
    post_type: Mapped[str] = mapped_column(String(10))   # lost 寻物 / found 拾物
    title: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(20), default="其他")
    happen_time: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    location: Mapped[str] = mapped_column(String(100), default="")
    description: Mapped[str] = mapped_column(Text, default="")
    images: Mapped[str] = mapped_column(Text, default="")  # JSON 字符串，许世杰扩展
    status: Mapped[str] = mapped_column(String(10), default="待匹配")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
