# 基于 RAG 的校园智能失物招领平台（CLFP）

校园里丢东西、捡东西的信息分散在微信群、朋友圈、公告栏，失主与拾主难以自动匹配。
本平台统一管理失物/拾物信息，并利用 **RAG（检索增强生成）** 技术做语义智能匹配与双向推送，提升物品找回率。

- 形态：B/S 架构 Web 网页（电脑、手机浏览器均可）
- 成员：胡良均、许世杰、孟炅、彭定星
- 登录：学号/工号 + 密码

## 仓库结构

```
clfp-server/   后端（FastAPI + SQLAlchemy + MySQL/SQLite + Chroma）
clfp-web/      前端（Vue 3 + Vite + Element Plus + Pinia）
前后端接口与协作约定_CLP.md   全员接口与协作规范（开发前必读）
```

## 技术栈

| 层 | 技术 |
|---|---|
| 前端 | Vue 3、Element Plus、Vite、Pinia、Vue Router、Axios |
| 后端 | Python、FastAPI、SQLAlchemy、JWT、bcrypt |
| 数据库 | MySQL 8.0（开发期可用 SQLite 零配置） |
| 向量/检索 | Chroma、bge-small-zh（本地 CPU 推理）、云端 LLM 按需调用并可降级 |

## 快速开始

**1. 后端（终端 1）**
```bash
cd clfp-server
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
接口文档：http://127.0.0.1:8000/docs

**2. 前端（终端 2）**
```bash
cd clfp-web
npm install
npm run dev
```
浏览器打开 http://localhost:5173

## 四人分工（按业务域全栈切分）

| 成员 | 负责域 |
|---|---|
| 胡良均 | 用户与入口：工程搭建、注册、登录（含锁定）、个人中心、我的发布、联系方式脱敏 |
| 许世杰 | 信息发布与浏览：发布寻物/拾物、图片上传、编辑删除、信息流、筛选、关键词搜索 |
| 孟炅 | RAG 智能匹配（核心）：向量化、向量库、语义检索、RAG 精排与 LLM、我的匹配、反馈 |
| 彭定星 | 认领交接、通知与后台：认领审核、交接确认、状态机、站内信/邮件、后台管理、测试 |

> 带 `*` 的需求为基本需求（必做项），详见需求文档与协作约定。
