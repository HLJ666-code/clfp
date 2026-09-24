# -*- coding: utf-8 -*-
"""物品路由（最小版）：仅提供“我的发布”列表，供胡良均联调。
发布/上传/搜索等由许世杰在本文件继续扩展。
"""
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
import models
from deps import get_current_user

router = APIRouter(prefix="/api/item", tags=["物品"])


@router.get("/mine", summary="我的发布列表")
def my_items(
    post_type: Optional[str] = None,
    user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(models.Item).filter(models.Item.owner_id == user.id)
    if post_type:
        query = query.filter(models.Item.post_type == post_type)
    items = query.order_by(models.Item.created_at.desc()).all()
    return [
        {
            "id": i.id,
            "post_type": i.post_type,
            "title": i.title,
            "category": i.category,
            "location": i.location,
            "status": i.status,
            "created_at": i.created_at.strftime("%Y-%m-%d %H:%M") if i.created_at else "",
        }
        for i in items
    ]
