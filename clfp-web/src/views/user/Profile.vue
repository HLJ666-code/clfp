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
        <el-upload
          class="avatar-upload"
          :show-file-list="false"
          :auto-upload="false"
          accept="image/*"
          :on-change="onAvatarChange"
        >
          <el-avatar :size="72" :src="form.avatar">{{ form.name?.[0] }}</el-avatar>
          <div class="avatar-tip">点击更换头像</div>
        </el-upload>
        <div>
          <div class="u-name">{{ form.name || '未设置' }}</div>
          <div class="u-account">学号/工号：{{ form.account }}</div>
          <el-tag v-if="form.role === 'admin'" size="small" type="warning" class="role-tag">管理员</el-tag>
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
          <el-input v-model="form.phone" maxlength="11" placeholder="选填" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="选填" />
        </el-form-item>
        <el-form-item label="公开手机号">
          <el-switch v-model="form.show_phone" />
          <span class="hint">关闭时他人看到 138****0000</span>
        </el-form-item>
        <el-form-item label="公开邮箱">
          <el-switch v-model="form.show_email" />
          <span class="hint">关闭时他人看到 l***i@xx.com</span>
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
  role: 'user',
  show_phone: false,
  show_email: false
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

// 头像：当前为本地预览。等许世杰 /api/upload 接口好后，
// 把这里改成先上传、拿到返回的 url 再赋给 form.avatar，并在保存时一并提交。
function onAvatarChange(file) {
  if (file.raw) form.avatar = URL.createObjectURL(file.raw)
}

async function saveProfile() {
  if (!form.name || form.name.length < 2) {
    ElMessage.warning('姓名至少 2 个字')
    return
  }
  if (form.phone && !/^\d{11}$/.test(form.phone)) {
    ElMessage.warning('手机号需为 11 位数字')
    return
  }
  if (form.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    ElMessage.warning('邮箱格式不正确')
    return
  }
  saving.value = true
  try {
    await updateMe({
      name: form.name,
      college: form.college,
      phone: form.phone,
      email: form.email,
      show_phone: form.show_phone,
      show_email: form.show_email
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
  gap: 16px;
  margin-bottom: 20px;
}
.avatar-upload {
  text-align: center;
}
.avatar-tip {
  font-size: 12px;
  color: #909399;
  margin-top: 6px;
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
.role-tag {
  margin-top: 6px;
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
