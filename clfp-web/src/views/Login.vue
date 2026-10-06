<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="title">账号登录</h2>
      <p class="subtitle">校园智能失物招领平台</p>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        size="large"
        @keyup.enter="onSubmit"
      >
        <el-form-item prop="account">
          <el-input
            v-model="form.account"
            placeholder="请输入学号 / 工号"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <div class="form-options">
          <el-checkbox v-model="remember">记住账号</el-checkbox>
        </div>
        <el-form-item>
          <el-button
            type="primary"
            class="submit"
            :loading="loading"
            @click="onSubmit"
          >
            登 录
          </el-button>
        </el-form-item>
      </el-form>

      <div class="links">
        <span>还没有账号？</span>
        <el-link type="primary" @click="router.push('/register')">立即注册</el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { loginApi } from '../api/auth'
import { useUserStore } from '../store/user'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const formRef = ref()
const loading = ref(false)
const remember = ref(true)
const form = reactive({ account: '', password: '' })

const rules = {
  account: [{ required: true, message: '请输入学号/工号', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
}

// 读取上次记住的账号
onMounted(() => {
  const saved = localStorage.getItem('clfp_remember_account')
  if (saved) form.account = saved
})

async function onSubmit() {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      const res = await loginApi({ ...form })
      localStorage.setItem('clfp_token', res.access_token)
      // 记住账号处理
      if (remember.value) localStorage.setItem('clfp_remember_account', form.account)
      else localStorage.removeItem('clfp_remember_account')
      userStore.setUser(res.user)
      ElMessage.success('登录成功')
      const redirect = route.query.redirect || '/'
      router.push(redirect)
    } catch (e) {
      // 错误提示已由拦截器统一处理（含锁定剩余时间）
    } finally {
      loading.value = false
    }
  })
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #409eff20, #67c23a20);
  padding: 20px;
}
.auth-card {
  width: 100%;
  max-width: 400px;
  background: #fff;
  border-radius: 12px;
  padding: 36px 32px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}
.title {
  text-align: center;
  font-size: 24px;
}
.subtitle {
  text-align: center;
  color: #909399;
  margin: 8px 0 28px;
  font-size: 13px;
}
.form-options {
  margin: -4px 0 12px;
}
.submit {
  width: 100%;
}
.links {
  text-align: center;
  font-size: 14px;
  color: #606266;
}
</style>
