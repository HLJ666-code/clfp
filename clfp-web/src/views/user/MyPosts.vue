<template>
  <div>
    <!-- 顶部统计 -->
    <el-row :gutter="12" class="stats">
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="num">{{ stats.total }}</div>
          <div class="label">总发布</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="num lost">{{ stats.lost }}</div>
          <div class="label">寻物</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="num found">{{ stats.found }}</div>
          <div class="label">拾物</div>
        </el-card>
      </el-col>
      <el-col :xs="12" :sm="6">
        <el-card shadow="never" class="stat-card">
          <div class="num done">{{ stats.done }}</div>
          <div class="label">已完成</div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 列表 -->
    <el-card shadow="never">
      <template #header>
        <div class="head">
          <span class="title">发布记录</span>
          <el-radio-group v-model="postType" size="small" @change="load">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="lost">寻物</el-radio-button>
            <el-radio-button label="found">拾物</el-radio-button>
          </el-radio-group>
        </div>
      </template>

      <el-table v-loading="loading" :data="list" stripe>
        <el-table-column label="类型" width="80">
          <template #default="{ row }">
            <el-tag :type="row.post_type === 'lost' ? 'danger' : 'success'" size="small">
              {{ row.post_type === 'lost' ? '寻物' : '拾物' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="title" label="物品名称" min-width="140" />
        <el-table-column prop="category" label="类别" width="100" />
        <el-table-column prop="location" label="地点" min-width="120" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag size="small" effect="plain">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="发布时间" width="150" />
        <template #empty>
          <el-empty description="还没有发布记录" />
        </template>
      </el-table>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { getMyItems, getMyStats } from '../../api/user'

const loading = ref(false)
const postType = ref('')
const list = ref([])
const stats = reactive({ total: 0, lost: 0, found: 0, done: 0 })

async function load() {
  loading.value = true
  try {
    list.value = await getMyItems(postType.value ? { post_type: postType.value } : {})
  } finally {
    loading.value = false
  }
}

async function loadStats() {
  try {
    const s = await getMyStats()
    Object.assign(stats, s)
  } catch (e) {
    // 统计失败不阻塞列表
  }
}

onMounted(() => {
  load()
  loadStats()
})
</script>

<style scoped>
.stats {
  margin-bottom: 14px;
}
.stat-card {
  text-align: center;
  margin-bottom: 12px;
}
.num {
  font-size: 26px;
  font-weight: bold;
  color: #409eff;
}
.num.lost {
  color: #f56c6c;
}
.num.found {
  color: #67c23a;
}
.num.done {
  color: #909399;
}
.label {
  color: #909399;
  font-size: 13px;
  margin-top: 2px;
}
.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.title {
  font-weight: bold;
}
@media (max-width: 768px) {
  .head {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
}
</style>
