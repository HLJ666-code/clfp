<template>
  <el-container class="layout">
    <el-header class="header">
      <div class="brand" @click="router.push('/')">
        <el-icon><Search /></el-icon>
        <span>校园失物招领</span>
      </div>

      <el-menu
        class="nav"
        mode="horizontal"
        :ellipsis="false"
        router
        :default-active="route.path"
      >
        <el-menu-item index="/">首页</el-menu-item>
        <el-menu-item index="/my-posts">我的发布</el-menu-item>
        <!-- 孟炅：我的匹配；彭定星：我的认领 —— 后续在此追加 -->
      </el-menu>

      <div class="right">
        <template v-if="userStore.isLogin">
          <el-dropdown @command="onCommand">
            <span class="user">
              <el-avatar :size="28" :src="userStore.user?.avatar">
                {{ userStore.user?.name?.[0] }}
              </el-avatar>
              <span class="username">{{ userStore.user?.name }}</span>
              <el-icon><ArrowDown /></el-icon>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">
                  <el-icon><User /></el-icon>个人中心
                </el-dropdown-item>
                <el-dropdown-item command="my-posts">
                  <el-icon><Document /></el-icon>我的发布
                </el-dropdown-item>
                <el-dropdown-item v-if="userStore.isAdmin" command="admin">
                  <el-icon><Setting /></el-icon>后台管理
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon>退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
        <template v-else>
          <el-button size="small" @click="router.push('/login')">登录</el-button>
          <el-button size="small" type="primary" @click="router.push('/register')">注册</el-button>
        </template>
      </div>
    </el-header>

    <el-main class="main">
      <div class="page-container">
        <router-view />
      </div>
    </el-main>

    <el-footer class="footer">
      基于 RAG 的校园智能失物招领平台 · 课程项目（胡良均 / 许世杰 / 孟炅 / 彭定星）
    </el-footer>
  </el-container>
</template>

<script setup>
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import { useUserStore } from '../store/user'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

onMounted(() => {
  if (!userStore.loaded) userStore.fetchMe()
})

function onCommand(command) {
  if (command === 'profile') router.push('/profile')
  else if (command === 'my-posts') router.push('/my-posts')
  else if (command === 'logout') {
    ElMessageBox.confirm('确定退出登录吗？', '提示', { type: 'warning' })
      .then(() => {
        userStore.logout()
        router.push('/login')
      })
      .catch(() => {})
  }
}
</script>

<style scoped>
.layout {
  min-height: 100%;
}
.header {
  display: flex;
  align-items: center;
  background: #fff;
  border-bottom: 1px solid #ebeef5;
  padding: 0 20px;
  height: 60px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
  cursor: pointer;
  white-space: nowrap;
}
.nav {
  flex: 1;
  border-bottom: none;
  margin-left: 20px;
}
.right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.user {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: pointer;
  outline: none;
}
.username {
  font-size: 14px;
}
.main {
  padding: 20px;
  min-height: calc(100vh - 60px - 50px);
}
.footer {
  display: flex;
  align-items: center;
  justify-content: center;
  color: #909399;
  font-size: 12px;
  background: #fff;
  border-top: 1px solid #ebeef5;
}
@media (max-width: 768px) {
  .header {
    padding: 0 10px;
  }
  .nav {
    display: none;
  }
  .username {
    display: none;
  }
}
</style>
