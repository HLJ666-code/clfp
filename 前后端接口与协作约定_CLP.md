# CLFP 前后端接口与协作约定（全员遵守）

> 项目：基于 RAG 的校园智能失物招领平台（Web）
> 成员：胡良均、许世杰、孟炅、彭定星
> 用法：本文档由胡良均维护，所有人按此开发；接口有改动先在群里说，再改文档。

---

## 一、技术栈与端口（统一，别各用各的）

| 项 | 约定 |
|---|---|
| 前端 | Vue 3 + Vite + Element Plus + Pinia，端口 **5173** |
| 后端 | FastAPI，端口 **8000** |
| 业务库 | 开发期 SQLite（各自本地）；后期统一 MySQL，库名 `clfp_biz` |
| 向量库 | Chroma（孟炅负责） |
| 前端调后端 | 统一走 Vite 代理 `/api` → `http://127.0.0.1:8000`，已配好，别写死 IP |

> 不需要每人一个端口。大家 git pull 之后，本地 8000 就是**包含所有人模块的完整后端**。

---

## 二、统一规则（最重要，先看这个）

1. **路径前缀**：所有业务接口以 `/api` 开头；每人一个模块前缀，互不冲突（见第三节）。
2. **登录鉴权**：
   - 登录成功返回 `access_token`，前端存 `localStorage`。
   - 所有“需要登录”的接口，前端自动带请求头 `Authorization: Bearer <token>`（request.js 已处理）。
   - 后端需要登录的接口，参数加 `user: User = Depends(get_current_user)`，不要自己写校验。
3. **成功返回**：直接返回 JSON 对象或数组；**分页统一**返回：
   ```json
   { "total": 123, "items": [ ... ] }
   ```
4. **失败返回**：用 `HTTPException(状态码, detail="中文提示")`，格式 `{ "detail": "..." }`，前端会自动弹窗，不用自己处理。
   - 400 业务错误 / 401 未登录或过期 / 403 无权限或锁定 / 404 不存在。
5. **时间格式**：字符串 `YYYY-MM-DD HH:mm:ss`。
6. **图片**：上传接口返回可访问 URL，开发期为 `/uploads/xxx.jpg`（后端用 StaticFiles 挂载 uploads 目录）。
7. **联系方式**：任何地方展示手机号/邮箱，统一调胡良均的 `/api/user/contact/{id}`，默认脱敏，不要自己拼。

---

## 三、后端接口清单（按人认领）

### 胡良均 · 认证与用户（已完成 ✅）
| 方法 | 路径 | 说明 | 登录 |
|---|---|---|---|
| POST | /api/auth/register | 学号/工号注册 | 否 |
| POST | /api/auth/login | 登录，5 次错误锁定 30 分钟 | 否 |
| GET | /api/user/me | 当前用户信息 | 是 |
| PUT | /api/user/me | 修改资料/公开联系方式开关 | 是 |
| POST | /api/user/change-password | 改密码 | 是 |
| GET | /api/user/contact/{user_id} | 他人联系方式（脱敏/授权） | 是 |

### 许世杰 · 发布/浏览/搜索
| 方法 | 路径 | 说明 | 登录 |
|---|---|---|---|
| POST | /api/upload | 图片上传，返回 `{url}` | 是 |
| POST | /api/item/lost | 发布寻物 | 是 |
| POST | /api/item/found | 发布拾物 | 是 |
| PUT | /api/item/{id} | 编辑本人信息 | 是 |
| DELETE | /api/item/{id} | 删除本人信息 | 是 |
| GET | /api/item/list | 信息流分页，支持 category/time/location 筛选 | 否 |
| GET | /api/item/{id} | 物品详情 | 否 |
| GET | /api/item/mine | 我的发布（补全字段，胡良均页面在用） | 是 |
| GET | /api/search?keyword= | 关键词搜索，分页 | 否 |

### 孟炅 · RAG 智能匹配（核心）
| 方法 | 路径 | 说明 | 登录 |
|---|---|---|---|
| （内部） | — | 发布后自动向量化入库（≤5 秒），监听 item 新增 | 系统 |
| GET | /api/match/list | 我的匹配列表，分页（含置信度/理由/反馈状态） | 是 |
| GET | /api/match/{id} | 匹配详情（双方物品信息） | 是 |
| POST | /api/match/feedback | 反馈：是我的/不是/待核实 | 是 |

### 彭定星 · 认领/通知/后台
| 方法 | 路径 | 说明 | 登录 |
|---|---|---|---|
| POST | /api/claim | 发起认领（带凭证） | 是 |
| GET | /api/claim/list | 我的认领列表 | 是 |
| POST | /api/claim/{id}/audit | 审核通过/拒绝 | 是 |
| POST | /api/claim/{id}/handover | 交接确认 | 是 |
| GET | /api/notify/unread_count | 未读消息数（导航红点用） | 是 |
| GET | /api/notify/list | 站内信列表，分页 | 是 |
| POST | /api/notify/read | 标记已读 | 是 |
| GET | /api/admin/items | 待审核内容列表 | 管理员 |
| POST | /api/admin/item/{id}/offline | 下架/删除 | 管理员 |
| GET | /api/admin/stats | 统计数据 | 管理员 |
| POST | /api/admin/announcement | 发布公告 | 管理员 |

---

## 四、前端页面与路由（在胡良均骨架上加）

| 路径 | 页面 | 负责人 |
|---|---|---|
| /login、/register | 登录、注册 | 胡良均 ✅ |
| / | 首页信息流 | 许世杰（替换现有占位） |
| /publish/lost、/publish/found | 发布寻物/拾物 | 许世杰 |
| /item/:id | 物品详情 | 许世杰 |
| /my-posts | 我的发布 | 胡良均（页面）+ 许世杰（数据） |
| /match、/match/:id | 我的匹配、详情 | 孟炅 |
| /claim | 我的认领 | 彭定星 |
| /profile | 个人中心 | 胡良均 ✅ |
| /admin | 后台管理 | 彭定星 |

新页面放 `src/views/`，调接口统一用 `src/api/request.js`。

---

## 五、代码怎么合（Git）

1. 胡良均在 GitHub 维护仓库 `clfp`，邀请三人协作。
2. 每人每天流程：
   ```
   git pull          # 先拉最新
   # 写自己模块的代码
   git add .
   git commit -m "说明今天改了啥"
   git push
   ```
3. **公共文件只有胡良均能改**（最容易冲突）：
   - 后端 `main.py`（注册新 router）
   - 前端 `src/router/index.js`（注册新页面）
   其他三人**不要动这两个文件**；做好模块后，把“要注册的路由/页面路径”发给胡良均，由他统一加。
4. 每人只在自己的文件里写：
   - 后端：`routers/xxx.py`；前端：`src/views/自己模块/`、`src/api/xxx.js`。
5. 不会 Git 就用 VS Code 左侧“源代码管理”，图形界面点就行；遇到冲突喊胡良均。

> `node_modules`、`__pycache__`、`clfp.db`、`.env`、`dist`、`uploads` 已在 `.gitignore`，不会传上去，各人依赖自己装。

---

## 六、对接顺序与时间点

| 时间 | 谁和谁对接 | 对什么 |
|---|---|---|
| 第 1~2 天 | 许世杰 → 全员 | 先给出 `/api/upload` 和物品数据字段，大家都要用图 |
| 第 3 天 | 许世杰 ↔ 孟炅 | 发布成功后触发向量化；约定 item 字段 |
| 第 4 天 | 孟炅 → 彭定星 | “是我的物品/匹配详情”能跳到发起认领 |
| 第 4 天 | 彭定星 → 胡良均 | 认领成立后放开完整联系方式；未读数接导航 |
| 第 5 天 | 全员 | git 合并、跑通完整闭环、一起测一遍 |

**联调方法**：对方接口没好之前，前端可以先写页面、用假数据（写死一个对象）；对方 push 后 `git pull`，把假数据换成真实接口即可。

---

## 七、常见问题
- 前端报 `404 Not Found`：后端没起，或对方模块还没 pull。
- 前端报 `401`：token 过期，重新登录（已自动跳转）。
- 后端起不来、端口被占：上次的 uvicorn 没关，任务管理器结束 python，或换 `--port 8002` 临时调试。
- 数据库表对不上：开发期直接删掉 `clfp.db` 重启，会自动重建。
