<template>
  <el-card shadow="never">
    <template #header>
      <div class="head">
        <span class="title">我的发布</span>
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
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getMyItems } from '../../api/user'

const loading = ref(false)
const postType = ref('')
const list = ref([])

async function load() {
  loading.value = true
  try {
    list.value = await getMyItems(postType.value ? { post_type: postType.value } : {})
  } finally {
    loading.value = false
  }
}

onMounted(load)
</script>

<style scoped>
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
