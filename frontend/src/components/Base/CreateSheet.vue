<script lang="ts" setup>
import {ref, computed} from 'vue';
import {useRouter} from 'vue-router';

const router = useRouter();

const activeTab = ref('practice');
const currentPage = ref(1);
const pageSize = ref(20);
const totalProblems = ref(55);
const data = defineProps(['username'])
const problems = ref([
  {id: 100, name: '【入门】新手入门', completionRate: 80, submissionCount: 23854, acceptedCount: 19083},
  {id: 101, name: '【入门】分支结构', completionRate: 60, submissionCount: 9148, acceptedCount: 5488},
  {id: 102, name: '【入门】循环结构', completionRate: 40, submissionCount: 7972, acceptedCount: 3188},
  // ... 添加更多题目数据
]);

const percentageFormat = (percentage: any) => {
  return percentage === 100 ? '完成' : `${percentage}%`;
};

const handleSizeChange = (val: any) => {
  pageSize.value = val;
  // 这里应该调用API重新获取数据
};

const handleCurrentChange = (val: any) => {
  currentPage.value = val;
  // 这里应该调用API重新获取数据
};

const goToUploadPage = () => {
  router.push(
      {
        name: 'upload',
        query: {
          username: data.username
        }
      }
  ); // 跳转到上传页面
};
</script>

<template>
  <div class="problem-set-container">
    <div class="problem-set">
      <el-card class="filter-card">
        <div class="header-content">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="练习题单" name="practice"></el-tab-pane>
          </el-tabs>
          <el-button type="primary" @click="goToUploadPage">上传题目</el-button>
        </div>
        <div class="filter-info">
          <span>共计 {{ problems.length }} 个题单</span>
        </div>
      </el-card>

      <el-table :data="problems" style="width: 100%" :default-sort="{ prop: 'id', order: 'ascending' }">
        <el-table-column prop="id" label="编号" width="80" sortable></el-table-column>
        <el-table-column label="名称" width="400">
          <template #default="scope">
            <router-link :to="{ name: 'upload', query: { username:data.username,sheetId: scope.row.id } }"
                         class="problem-link">
              {{ scope.row.name }}
            </router-link>
          </template>
        </el-table-column>
        <el-table-column label="完成度" width="200">
          <template #default="scope">
            <el-progress :percentage="scope.row.completionRate" :format="percentageFormat"></el-progress>
          </template>
        </el-table-column>
        <el-table-column prop="submissionCount" label="总提交" width="100" sortable></el-table-column>
        <el-table-column prop="acceptedCount" label="通过数" width="100" sortable></el-table-column>
      </el-table>

      <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="currentPage"
          :page-sizes="[20, 50, 100]"
          :page-size="pageSize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="problems.length">
      </el-pagination>
    </div>
  </div>
</template>

<style scoped>
.problem-set-container {
  display: flex;
  justify-content: center;
  padding: 20px;
}

.problem-set {
  width: 100%;
  max-width: 1200px; /* 调整这个值以适应你的设计 */
}

.filter-card {
  margin-bottom: 20px;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filter-info {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}

.el-progress {
  margin-right: 20px;
}

.problem-link {
  text-decoration: none;
  color: #303133;
}

.problem-link:visited {
  color: #3498db
}
</style>