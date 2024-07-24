<template>
  <div class="problem-set">
    <el-card class="filter-card">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="练习题单" name="practice"></el-tab-pane>
        <el-tab-pane label="比赛列表" name="contest"></el-tab-pane>
      </el-tabs>
      <div class="filter-info">
        <span>共计 {{ totalProblems }} 道题目</span>
      </div>
    </el-card>

    <el-table :data="problems" style="width: 100%" :default-sort="{ prop: 'id', order: 'ascending' }">
      <el-table-column prop="id" label="编号" width="80" sortable></el-table-column>
      <el-table-column label="名称" width="400">
        <template #default="scope">
          <router-link :to="{ name: 'home', query: { id: scope.row.id } }">
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
        :total="totalProblems">
    </el-pagination>
  </div>
</template>

<script setup lang="ts">
import {ref, computed} from 'vue';
import {useRouter} from 'vue-router';

const router = useRouter();

const activeTab = ref('practice');
const currentPage = ref(1);
const pageSize = ref(20);
const totalProblems = ref(55);

const problems = ref([
  {id: 100, name: '[入门]新手入门', completionRate: 80, submissionCount: 23854, acceptedCount: 19083},
  {id: 101, name: '[入门]分支结构', completionRate: 60, submissionCount: 9148, acceptedCount: 5488},
  {id: 102, name: '[入门]循环结构', completionRate: 40, submissionCount: 7972, acceptedCount: 3188},
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

// 如果需要跳转到题目详情页，可以使用这个函数
const goToProblemDetail = (problemId: any) => {
  router.push({name: 'ProblemDetail', params: {id: problemId}});
};
</script>

<style scoped>
.problem-set {
  padding: 20px;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-info {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}

.el-progress {
  margin-right: 20px;
}
</style>