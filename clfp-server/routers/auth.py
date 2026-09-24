# -*- coding: utf-8 -*-
"""认证路由：注册、登录（含连续错误锁定）。"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from security import hash_password, verify_password, create_token
from config import settings

router = APIRouter(prefix="/api/auth", tags=["认证"])


def _unlock_if_due(user: models.User) -> None:
    """锁定到期自动解锁。"""
    if (
        user.status == "locked"
        and user.locked_until is not None
        and datetime.now() >= user.locked_until
    ):
        user.status = "active"
        user.fail_count = 0
        user.locked_until = None


@router.post("/register", summary="用户注册")
def register(data: schemas.RegisterIn, db: Session = Depends(get_db)):
    exists = db.query(models.User).filter(models.User.account == data.account).first()
    if exists:
        raise HTTPException(status_code=400, detail="该学号/工号已注册，请直接登录")

    user = models.User(
        account=data.account,
        password_hash=hash_password(data.password),
        name=data.name,
        college=data.college,
        phone=data.phone,
        email=data.email,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "注册成功", "user_id": user.id}


@router.post("/login", summary="账号密码登录")
def login(data: schemas.LoginIn, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.account == data.account).first()
    if user is None:
        raise HTTPException(status_code=400, detail="账号不存在，请先注册")

    _unlock_if_due(user)

    if user.status == "disabled":
        raise HTTPException(status_code=403, detail="账号已被禁用，请联系管理员")

    if user.status == "locked":
        remain = int((user.locked_until - datetime.now()).total_seconds() // 60) + 1
        raise HTTPException(
            status_code=403,
            detail=f"密码错误过多，账号已锁定，请约 {remain} 分钟后再试",
        )

    if not verify_password(data.password, user.password_hash):
        user.fail_count += 1
        if user.fail_count >= settings.max_login_fail:
            user.status = "locked"
            user.locked_until = datetime.now() + timedelta(minutes=settings.lock_minutes)
            db.commit()
            raise HTTPException(
                status_code=403,
                detail=f"连续 {settings.max_login_fail} 次密码错误，账号锁定 {settings.lock_minutes} 分钟",
            )
        db.commit()
        raise HTTPException(
            status_code=400,
            detail=f"密码错误，还可尝试 {settings.max_login_fail - user.fail_count} 次",
        )

    # 登录成功：重置错误计数
    user.fail_count = 0
    user.locked_until = None
    user.status = "active"
    db.commit()

    token = create_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user": schemas.UserOut.model_validate(user),
    }
