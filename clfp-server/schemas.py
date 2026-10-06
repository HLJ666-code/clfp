# -*- coding: utf-8 -*-
"""Pydantic 请求/响应模型。"""
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator, model_validator

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def _check_strength(pw: str) -> None:
    if not (any(c.isalpha() for c in pw) and any(c.isdigit() for c in pw)):
        raise ValueError("密码需同时包含字母和数字")


class RegisterIn(BaseModel):
    account: str = Field(min_length=4, max_length=20, description="学号/工号")
    password: str = Field(min_length=8, max_length=20)
    name: str = Field(min_length=2, max_length=20)
    college: str = ""
    phone: str = ""
    email: str = ""

    @field_validator("account")
    @classmethod
    def _account_rule(cls, v: str) -> str:
        if not v.isalnum():
            raise ValueError("学号/工号只能包含数字和字母")
        return v

    @field_validator("password")
    @classmethod
    def _pwd_rule(cls, v: str) -> str:
        _check_strength(v)
        return v

    @field_validator("phone")
    @classmethod
    def _phone_rule(cls, v: str) -> str:
        if v and (not v.isdigit() or len(v) != 11):
            raise ValueError("手机号需为 11 位数字")
        return v

    @field_validator("email")
    @classmethod
    def _email_rule(cls, v: str) -> str:
        if v and not EMAIL_RE.match(v):
            raise ValueError("邮箱格式不正确")
        return v

    @model_validator(mode="after")
    def _not_same_as_account(self):
        if self.password.lower() == self.account.lower():
            raise ValueError("密码不能与学号/工号相同")
        return self


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
    show_phone: bool
    show_email: bool

    # SQLAlchemy 对象 -> Pydantic
    model_config = {"from_attributes": True}


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=2, max_length=20)
    college: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    avatar: Optional[str] = None
    show_phone: Optional[bool] = None
    show_email: Optional[bool] = None

    @field_validator("phone")
    @classmethod
    def _phone_rule(cls, v):
        if v and (not v.isdigit() or len(v) != 11):
            raise ValueError("手机号需为 11 位数字")
        return v

    @field_validator("email")
    @classmethod
    def _email_rule(cls, v):
        if v and not EMAIL_RE.match(v):
            raise ValueError("邮箱格式不正确")
        return v


class ChangePasswordIn(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8, max_length=20)

    @field_validator("new_password")
    @classmethod
    def _pwd_rule(cls, v: str) -> str:
        _check_strength(v)
        return v
