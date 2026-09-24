# CLFP 后端（clfp-server）

校园智能失物招领平台后端，FastAPI + SQLAlchemy。
本目录为 **胡良均负责的「用户与入口」后端**，其他组员在 `routers/` 下继续加自己的路由。

## 1. 环境要求
- Python 3.10+（Python 3.9 亦可，已兼容）
- 建议用 VS Code 打开本目录

## 2. 安装依赖
> 注意：若你的电脑 `pip` 和 `python` 指向不同解释器，用 `python -m pip`，包装到当前 python。

```bash
python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 3. 配置（可选）
- 默认用 **SQLite**，零配置，启动后自动生成 `clfp.db`，方便先把登录跑通。
- 最终按需求文档用 **MySQL 8.0**：把 `.env.example` 复制为 `.env`，取消 MySQL 那行注释并填密码：
  ```
  DATABASE_URL=mysql+pymysql://root:你的密码@localhost:3306/clfp_biz?charset=utf8mb4
  ```
  SQLAlchemy 会自动建表，代码不用改。

## 4. 启动
```bash
python -m uvicorn main:app --reload --port 8000
```
启动后浏览器打开 **http://127.0.0.1:8000/docs** ，可在线调试全部接口。

## 5. 已实现接口（胡良均）
| 方法 | 路径 | 说明 | 对应需求 |
|---|---|---|---|
| POST | /api/auth/register | 学号/工号注册，密码 bcrypt 哈希 | *SRS-1.1.0 |
| POST | /api/auth/login | 登录，连续 5 次错误锁定 30 分钟 | *SRS-1.2.0 / 1.3.0 |
| GET | /api/user/me | 获取当前登录用户 | *SRS-1.4.0 |
| PUT | /api/user/me | 修改姓名/院系/手机/邮箱/授权开关 | *SRS-1.4.0 |
| POST | /api/user/change-password | 修改密码 | *SRS-1.4.0 |
| GET | /api/user/contact/{id} | 他人联系方式，默认脱敏、授权后完整 | *USR-0014 |
| GET | /api/item/mine | 我的发布列表（联调用，许世杰扩展） | *USR-0018 |

## 6. 你还要自己补的
1. **头像上传**：图片上传接口归许世杰（`/api/upload`），他做好后把返回的 URL 存到 `user.avatar`。
2. **管理员账号**：注册的默认是 `user`；演示前可在 `/docs` 里手动把自己账号 `role` 改成 `admin`。
3. **认领后自动放开联系方式**：`/contact` 里目前只看 `show_contact`；彭定星的认领模块做好后，加一条“双方认领关系成立则返回完整号码”。

## 7. 和组员的约定
- 所有业务接口统一加 `/api` 前缀、统一返回 JSON；报错用 `HTTPException(detail="中文提示")`。
- 需要登录的接口，参数里加 `user: User = Depends(get_current_user)`。
- 许世杰扩展 `routers/item.py`；孟炅新建 `routers/match.py`；彭定星新建 `routers/claim.py`、`routers/notify.py`、`routers/admin.py`，并在 `main.py` 里 `include_router`。
