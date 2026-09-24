<template>
  <div class="auth-page">
    <div class="auth-card">
      <h2 class="title">用户注册</h2>
      <p class="subtitle">使用学号 / 工号注册</p>

      <el-form ref="formRef" :model="form" :rules="rules" size="large">
        <el-form-item prop="account">
          <el-input v-model="form.account" placeholder="学号 / 工号" :prefix-icon="Postcard" clearable />
        </el-form-item>
        <el-form-item prop="name">
          <el-input v-model="form.name" placeholder="真实姓名" :prefix-icon="User" clearable />
        </el-form-item>
        <el-form-item prop="college">
          <el-input v-model="form.college" placeholder="所属院系（选填）" :prefix-icon="School" clearable />
        </el-form-item>
        <el-form-item prop="phone">
          <el-input v-model="form.phone" placeholder="手机号（选填）" :prefix-icon="Phone" maxlength="11" clearable />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="form.email" placeholder="邮箱（选填）" :prefix-icon="Message" clearable />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="设置密码（8~20 位，含字母和数字）"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item prop="confirm">
          <el-input
            v-model="form.confirm"
            type="password"
            placeholder="再次输入密码"
            :prefix-icon="Lock"
            show-password
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" class="submit" :loading="loading" @click="onSubmit">
            注 册
          </el-button>
        </el-form-item>
      </el-form>

      <div class="links">
        <span>已有账号？</span>
        <el-link type="primary" @click="router.push('/login')">返回登录</el-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock, Phone, Message, School, Postcard } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { registerApi } from '../api/auth'

const router = useRouter()
const formRef = ref()
const loading = ref(false)

const form = reactive({
  account: '',
  name: '',
  college: '',
  phone: '',
  email: '',
  password: '',
  confirm: ''
})

const validateConfirm = (rule, value, callback) => {
  if (value !== form.password) callback(new Error('两次输入的密码不一致'))
  else callback()
}

const validateEmail = (rule, value, callback) => {
  if (value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
    callback(new Error('邮箱格式不正确'))
  } else callback()
}

const rules = {
  account: [
    { required: true, message: '请输入学号/工号', trigger: 'blur' },
    { min: 4, max: 12, message: '长度 4~12 位', trigger: 'blur' }
  ],
  name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' },
    { min: 2, max: 20, message: '长度 2~20', trigger: 'blur' }
  ],
  phone: [{ pattern: /^\d{11}$/, message: '需为 11 位数字', trigger: 'blur' }],
  email: [{ validator: validateEmail, trigger: 'blur' }],
  password: [
    { required: true, message: '请设置密码', trigger: 'blur' },
    { min: 8, max: 20, message: '长度 8~20 位', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d).+$/, message: '需同时包含字母和数字', trigger: 'blur' }
  ],
  confirm: [
    { required: true, message: '请再次输入密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' }
  ]
}

async function onSubmit() {
  await formRef.value.validate(async (valid) => {
    if (!valid) return
    loading.value = true
    try {
      await registerApi({
        account: form.account,
        name: form.name,
        college: form.college,
        phone: form.phone,
        email: form.email,
        password: form.password
      })
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } catch (e) {
      // 拦截器已提示
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
  max-width: 420px;
  background: #fff;
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.08);
}
.title {
  text-align: center;
  font-size: 24px;
}
.subtitle {
  text-align: center;
  color: #909399;
  margin: 8px 0 24px;
  font-size: 13px;
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
