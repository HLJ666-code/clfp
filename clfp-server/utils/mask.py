# -*- coding: utf-8 -*-
"""联系方式脱敏工具。"""


def mask_phone(phone: str) -> str:
    if not phone:
        return ""
    if len(phone) < 7:
        return phone
    return phone[:3] + "****" + phone[-4:]


def mask_email(email: str) -> str:
    if not email or "@" not in email:
        return email or ""
    name, domain = email.split("@", 1)
    if len(name) <= 1:
        return "*@" + domain
    return name[0] + "***" + name[-1] + "@" + domain
