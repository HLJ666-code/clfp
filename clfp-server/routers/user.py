# -*- coding: utf-8 -*-
"""用户路由：个人信息、修改密码、联系方式查看（分级脱敏/授权）、个人统计。"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import models
import schemas
from deps import get_current_user
from security import verify_password, hash_password
from utils.mask import mask_phone, mask_email

router = APIRouter(prefix="/api/user", tags=["用户"])


@router.get("/me", summary="获取当前用户信息", response_model=schemas.UserOut)
def read_me(user: models.User = Depends(get_current_user)):
    return user


@router.put("/me", summary="更新个人信息")
def update_me(
    data: schemas.ProfileUpdate,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    db.commit()
    return {"message": "保存成功"}


@router.post("/change-password", summary="修改密码")
def change_password(
    data: schemas.ChangePasswordIn,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not verify_password(data.old_password, user.password_hash):
        raise HTTPException(status_code=400, detail="原密码不正确")
    if data.new_password.lower() == user.account.lower():
        raise HTTPException(status_code=400, detail="新密码不能与学号/工号相同")
    user.password_hash = hash_password(data.new_password)
    db.commit()
    return {"message": "密码修改成功，请重新登录"}


@router.get("/me/stats", summary="我的发布统计")
def my_stats(
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    base = db.query(models.Item).filter(models.Item.owner_id == user.id)
    lost = base.filter(models.Item.post_type == "lost").count()
    found = base.filter(models.Item.post_type == "found").count()
    done = base.filter(models.Item.status == "已完成").count()
    return {"lost": lost, "found": found, "total": lost + found, "done": done}


@router.get("/contact/{user_id}", summary="查看他人联系方式")
def get_contact(
    user_id: int,
    db: Session = Depends(get_db),
    me: models.User = Depends(get_current_user),
):
    """
    手机 / 邮箱分别授权：
    - 对方授权了对应项 -> 返回完整；
    - 否则该项返回脱敏值。
    认领关系成立后自动放开完整号码的逻辑，由彭定星的认领模块补充。
    """
    target = db.query(models.User).filter(models.User.id == user_id).first()
    if target is None:
        raise HTTPException(status_code=404, detail="用户不存在")

    phone = target.phone if target.show_phone else mask_phone(target.phone)
    email = target.email if target.show_email else mask_email(target.email)
    return {
        "phone": phone,
        "email": email,
        "phone_masked": not target.show_phone,
        "email_masked": not target.show_email,
    }
