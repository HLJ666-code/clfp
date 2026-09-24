# -*- coding: utf-8 -*-
"""FastAPI 应用入口。

启动：
    python -m uvicorn main:app --reload --port 8000
接口文档（启动后浏览器打开）：
    http://127.0.0.1:8000/docs
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine
from routers import auth, user, item

# 启动时自动建表（开发期方便；正式项目改用 Alembic 迁移）
Base.metadata.create_all(bind=engine)

app = FastAPI(title="CLFP 校园智能失物招领平台", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # 开发期；上线改为具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(item.router)


@app.get("/", tags=["默认"])
def root():
    return {"message": "CLFP API 正在运行", "docs": "/docs"}
