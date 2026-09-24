<template>
  <div>
    <!-- 顶部横幅 -->
    <div class="banner">
      <h1>让每一件遗失物品都能回家</h1>
      <p>统一发布失物 / 拾物信息，AI-RAG 语义匹配，失主拾主双向推送</p>
      <div class="actions">
        <el-button type="primary" size="large" :disabled="!userStore.isLogin" @click="todo('发布寻物')">
          我丢了东西
        </el-button>
        <el-button size="large" :disabled="!userStore.isLogin" @click="todo('发布拾物')">
          我捡到东西
        </el-button>
      </div>
      <p v-if="!userStore.isLogin" class="tip">登录后即可发布信息</p>
    </div>

    <!-- 信息流占位：数据与卡片由许世杰接入 -->
    <div class="section-head">
      <h3>最新信息</h3>
      <el-link type="primary">查看全部</el-link>
    </div>
    <el-row :gutter="16">
      <el-col v-for="n in 4" :key="n" :xs="12" :sm="8" :md="6">
        <el-card class="item-card" shadow="hover">
          <div class="ph img-ph"></div>
          <div class="ph line-ph"></div>
          <div class="ph line-ph short"></div>
        </el-card>
      </el-col>
    </el-row>
    <el-alert
      class="note"
      type="info"
      :closable="false"
      title="信息流卡片、筛选与搜索由许世杰接入；“我的匹配”由孟炅接入；认领交接由彭定星接入。"
    />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../store/user'

const userStore = useUserStore()

onMounted(() => {
  if (!userStore.loaded) userStore.fetchMe()
})

function todo(name) {
  ElMessage.info(`「${name}」页面由许世杰开发，接入后即可使用`)
}
</script>

<style scoped>
.banner {
  background: linear-gradient(135deg, #409eff, #36cfc9);
  color: #fff;
  border-radius: 12px;
  padding: 40px 24px;
  text-align: center;
  margin-bottom: 24px;
}
.banner h1 {
  font-size: 28px;
  margin-bottom: 12px;
}
.banner p {
  opacity: 0.92;
  margin-bottom: 24px;
}
.actions {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}
.tip {
  margin-top: 12px;
  font-size: 12px;
  opacity: 0.85;
}
.section-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}
.item-card {
  margin-bottom: 16px;
}
.ph {
  background: #f0f2f5;
  border-radius: 4px;
}
.img-ph {
  height: 120px;
  margin-bottom: 10px;
}
.line-ph {
  height: 14px;
  margin-bottom: 8px;
}
.line-ph.short {
  width: 60%;
}
.note {
  margin-top: 8px;
}
</style>
