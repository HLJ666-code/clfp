# -*- coding: utf-8 -*-
"""Pydantic 请求/响应模型。"""
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class RegisterIn(BaseModel):
    account: str = Field(min_length=4, max_length=12, description="学号/工号")
    password: str = Field(min_length=8, max_length=20)
    name: str = Field(min_length=2, max_length=20)
    college: str = ""
    phone: str = ""
    email: str = ""

    @field_validator("password")
    @classmethod
    def _pwd_rule(cls, v: str) -> str:
        if not (any(c.isalpha() for c in v) and any(c.isdigit() for c in v)):
            raise ValueError("密码需同时包含字母和数字")
        return v

    @field_validator("phone")
    @classmethod
    def _phone_rule(cls, v: str) -> str:
        if v and (not v.isdigit() or len(v) != 11):
            raise ValueError("手机号需为 11 位数字")
        return v


class LoginIn(BaseModel):
    account: str
    password: str


class UserOut(BaseModel):
    id: int
    account: str
    name: str
    college: str
    phone: str
    email: str
    avatar: str
    role: str
    show_contact: bool

    # SQLAlchemy 对象 -> Pydantic
    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=20)
    college: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    show_contact: Optional[bool] = None


class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=20)

    @field_validator("new_password")
    @classmethod
    def _pwd_rule(cls, v: str) -> str:
        if not (any(c.isalpha() for c in v) and any(c.isdigit() for c in v)):
            raise ValueError("新密码需同时包含字母和数字")
        return v
