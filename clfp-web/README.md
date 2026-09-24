# CLFP 前端（clfp-web）

校园智能失物招领平台前端，Vue 3 + Vite + Element Plus + Pinia。
本目录为 **胡良均负责的「用户与入口」前端 + 全站工程骨架**。

## 1. 环境要求
- Node.js 18+（已在 v22 验证）
- VS Code，建议装插件 Volar（Vue - Official）

## 2. 安装与启动
```bash
npm install --registry=https://registry.npmmirror.com
npm run dev
```
启动后浏览器打开终端提示的地址（默认 http://localhost:5173 ）。
> 前端通过 `vite.config.js` 把 `/api` 代理到本机 8000 端口，请先把后端 clfp-server 跑起来。

## 3. 目录结构
```
src/
├─ main.js              # 入口，注册 Element Plus / Pinia / 路由
├─ App.vue
├─ style.css            # 全局样式
├─ router/index.js      # 路由表 + 登录守卫
├─ api/
│  ├─ request.js        # axios 封装：自动带 token、统一报错、401 跳登录
│  ├─ auth.js           # 注册/登录接口
│  └─ user.js           # 个人信息/我的发布/联系方式接口
├─ store/user.js        # Pinia：当前登录用户
├─ utils/mask.js        # 脱敏兜底
├─ layout/Layout.vue    # 全站布局：顶部导航 + 内容区 + 页脚（响应式）
└─ views/
   ├─ Login.vue         # 登录页
   ├─ Register.vue      # 注册页
   ├─ Home.vue          # 首页（信息流占位，许世杰接入）
   └─ user/
      ├─ Profile.vue    # 个人中心：资料 + 公开联系方式开关 + 改密码
      └─ MyPosts.vue    # 我的发布（全部/寻物/拾物）
```

## 4. 已打通的流程
注册 → 登录（JWT 存 localStorage）→ 路由守卫放行 → 个人中心查看/修改 → 我的发布列表 → 退出登录。`npm run build` 已验证可编译。

## 5. 你还要自己补的
1. **头像上传**：等许世杰的上传接口，在个人中心加 `el-upload`，成功后把 URL 写回。
2. **后台管理入口**：`Layout.vue` 里管理员下拉已有“后台管理”，彭定星做好页面后接上跳转。
3. **未读消息角标**：彭定星的站内信做好后，在导航加红点数字。

## 6. 和组员的约定（重要）
- 新页面统一放 `src/views/`，并在 `src/router/index.js` 的 Layout 子路由里注册（已留注释）。
- 调接口统一用 `src/api/request.js`，不要自己再写 axios。
- 孟炅新建 `src/views/match/`；彭定星新建 `src/views/claim/`、`src/views/admin/`；许世杰完善 `Home.vue` 和发布页。

## 7. 部署（可选）
```bash
npm run build      # 产物在 dist/
```
构建时主 chunk > 500kB 的提示是 Element Plus 全量引入所致，不影响使用；想优化可改“按需引入”。
