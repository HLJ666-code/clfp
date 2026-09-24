<template>
  <div class="profile">
    <!-- 资料维护 -->
    <el-card class="box" shadow="never">
      <template #header>
        <div class="card-head">
          <el-icon><User /></el-icon>
          <span>个人信息</span>
        </div>
      </template>

      <div class="user-bar">
        <el-avatar :size="56" :src="form.avatar">{{ form.name?.[0] }}</el-avatar>
        <div>
          <div class="u-name">{{ form.name || '未设置' }}</div>
          <div class="u-account">学号/工号：{{ form.account }}</div>
        </div>
      </div>

      <el-form ref="formRef" :model="form" label-width="90px" class="form">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="form.name" />
        </el-form-item>
        <el-form-item label="所属院系">
          <el-input v-model="form.college" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" maxlength="11" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="公开联系方式">
          <el-switch v-model="form.show_contact" />
          <span class="hint">关闭时他人只能看到脱敏号码（如 138****0000）</span>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="saving" @click="saveProfile">保存修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 修改密码 -->
    <el-card class="box" shadow="never">
      <template #header>
        <div class="card-head">
          <el-icon><Lock /></el-icon>
          <span>修改密码</span>
        </div>
      </template>
      <el-form ref="pwdRef" :model="pwd" :rules="pwdRules" label-width="90px" class="form">
        <el-form-item label="原密码" prop="old_password">
          <el-input v-model="pwd.old_password" type="password" show-password />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input v-model="pwd.new_password" type="password" show-password placeholder="8~20 位，含字母和数字" />
        </el-form-item>
        <el-form-item label="确认新密码" prop="confirm">
          <el-input v-model="pwd.confirm" type="password" show-password />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" :loading="pwdLoading" @click="savePassword">确认修改</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User, Lock } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import { getMe, updateMe, changePassword } from '../../api/user'
import { useUserStore } from '../../store/user'

const router = useRouter()
const userStore = useUserStore()

const formRef = ref()
const pwdRef = ref()
const saving = ref(false)
const pwdLoading = ref(false)

const form = reactive({
  account: '',
  name: '',
  college: '',
  phone: '',
  email: '',
  avatar: '',
  show_contact: false
})

const pwd = reactive({ old_password: '', new_password: '', confirm: '' })

const validateConfirm = (rule, value, callback) => {
  if (value !== pwd.new_password) callback(new Error('两次输入的新密码不一致'))
  else callback()
}

const pwdRules = {
  old_password: [{ required: true, message: '请输入原密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, max: 20, message: '长度 8~20 位', trigger: 'blur' },
    { pattern: /^(?=.*[A-Za-z])(?=.*\d).+$/, message: '需同时包含字母和数字', trigger: 'blur' }
  ],
  confirm: [
    { required: true, message: '请再次输入新密码', trigger: 'blur' },
    { validator: validateConfirm, trigger: 'blur' }
  ]
}

onMounted(async () => {
  const me = await userStore.fetchMe()
  if (me) Object.assign(form, me)
})

async function saveProfile() {
  if (!form.name || form.name.length < 2) {
    ElMessage.warning('姓名至少 2 个字')
    return
  }
  saving.value = true
  try {
    await updateMe({
      name: form.name,
      college: form.college,
      phone: form.phone,
      email: form.email,
      show_contact: form.show_contact
    })
    await userStore.fetchMe()
    ElMessage.success('保存成功')
  } finally {
    saving.value = false
  }
}

async function savePassword() {
  await pwdRef.value.validate(async (valid) => {
    if (!valid) return
    pwdLoading.value = true
    try {
      await changePassword({
        old_password: pwd.old_password,
        new_password: pwd.new_password
      })
      ElMessage.success('密码修改成功，请重新登录')
      userStore.logout()
      router.push('/login')
    } finally {
      pwdLoading.value = false
    }
  })
}
</script>

<style scoped>
.profile {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.card-head {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: bold;
}
.user-bar {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
}
.u-name {
  font-size: 18px;
  font-weight: bold;
}
.u-account {
  color: #909399;
  font-size: 13px;
  margin-top: 4px;
}
.hint {
  margin-left: 10px;
  color: #909399;
  font-size: 12px;
}
@media (max-width: 768px) {
  .form :deep(.el-form-item__label) {
    width: 80px !important;
  }
}
</style>
