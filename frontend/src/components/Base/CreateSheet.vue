<script lang="ts" setup>
import {ref, onMounted} from 'vue';
import {ElMessage, ElMessageBox} from 'element-plus';
import API from "@/plugins/axios";

const activeTab = ref('practice');
const currentPage = ref(1);
const pageSize = ref(20);
const totalProblems = ref(0);
const data = defineProps(['username']);
const problems = ref([
  {id: 100, name: '【入门】新手入门', completionRate: 80, submissionCount: 23854, acceptedCount: 19083},
  {id: 101, name: '【入门】分支结构', completionRate: 60, submissionCount: 9148, acceptedCount: 5488},
  {id: 102, name: '【入门】循环结构', completionRate: 40, submissionCount: 7972, acceptedCount: 3188},
]);

// 对话框相关的响应式变量
const createDialogVisible = ref(false);
const updateDialogVisible = ref(false);
const shareDialogVisible = ref(false);
const newProblemGroup = ref({
  username: '',
  title: '',
  description: '',
  tag: [],
});
const updateProblemGroup = ref({
  username: '',
  problem_group_id: 0,
  title: '',
  description: ''
});

onMounted(() => {
  fetchProblems();
});

const fetchProblems = async () => {
  try {
    const response = await API.post('/get_problem_groups', {
      username: data.username,
      mode: 2,
      filter_group: '',
      page: currentPage.value,
      number_per_page: pageSize.value
    });
    if (response.data.code === 200) {
      problems.value = response.data.data.problems;
      totalProblems.value = response.data.data.total;
    }
  } catch (error) {
    console.error('获取题目列表失败:', error);
    ElMessage.error('获取题目列表失败，请重试');
  }
};

const percentageFormat = (percentage: number) => {
  return percentage === 100 ? '完成' : `${percentage}%`;
};

const handleSizeChange = (val: number) => {
  pageSize.value = val;
  fetchProblems();
};

const handleCurrentChange = (val: number) => {
  currentPage.value = val;
  fetchProblems();
};

const openCreateDialog = () => {
  createDialogVisible.value = true;
  newProblemGroup.value.username = data.username;
};

const createNewProblemGroup = async () => {
  try {
    console.log(newProblemGroup.value)
    const response = await API.post('/problem_group_create', newProblemGroup.value);
    if (response.data.code === 200) {
      ElMessage.success('题目创建成功');
      createDialogVisible.value = false;
      fetchProblems();
    } else {
      console.log(response.data.code)
      ElMessage.error('题目创建失败');
    }
  } catch (error) {
    console.error('题目创建失败:', error);
    ElMessage.error('题目创建失败，请重试');
  }
};

const openUpdateDialog = (problem: any) => {
  updateDialogVisible.value = true;
  updateProblemGroup.value = {
    username: data.username,
    problem_group_id: problem.id,
    title: problem.name,
    description: problem.description || ''
  };
};

const updateProblemGroupFunc = async () => {
  try {
    const response = await API.post('/problem_group_update', updateProblemGroup.value);
    if (response.data.code === 200) {
      ElMessage.success('题目更新成功');
      updateDialogVisible.value = false;
      fetchProblems();
    } else {
      ElMessage.error('题目更新失败');
    }
  } catch (error) {
    console.error('题目更新失败:', error);
    ElMessage.error('题目更新失败，请重试');
  }
};

const openShareDialog = (problem: any) => {
  shareDialogVisible.value = true;
  // 这里可以添加share相关的逻辑
};

const deleteProblemGroup = async (problem: any) => {
  try {
    await ElMessageBox.confirm('确定要删除这个题目组吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    });
    const response = await API.post('/problem_group_delete', {
      username: data.username,
      problem_group_id: problem.id
    });
    if (response.data.code === 200) {
      ElMessage.success('题目删除成功');
      fetchProblems();
    } else {
      ElMessage.error('题目删除失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('题目删除失败:', error);
      ElMessage.error('题目删除失败，请重试');
    }
  }
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
          <el-button type="primary" @click="openCreateDialog">新建题单</el-button>
        </div>
        <div class="filter-info">
          <span>共计 {{ problems.length }} 个题单</span>
        </div>
      </el-card>

      <el-table :data="problems" style="width: 100%" :default-sort="{ prop: 'id', order: 'ascending' }">
        <el-table-column prop="id" label="编号" width="80" sortable></el-table-column>
        <el-table-column label="名称" width="300">
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
        <el-table-column label="操作" width="300">
          <template #default="scope">
            <div class="button-container">
              <el-button size="small" @click="openUpdateDialog(scope.row)">Update</el-button>
              <el-button size="small" @click="openShareDialog(scope.row)">Share</el-button>
              <el-button size="small" type="danger" icon="el-icon-delete" @click="deleteProblemGroup(scope.row)">
                Delete
              </el-button>
            </div>
          </template>
        </el-table-column>
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

    <!-- 新建题单对话框 -->
    <el-dialog v-model="createDialogVisible" title="新建题单" width="30%">
      <el-form :model="newProblemGroup" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="newProblemGroup.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="问题组标题">
          <el-input v-model="newProblemGroup.title"></el-input>
        </el-form-item>
        <el-form-item label="问题组描述">
          <el-input v-model="newProblemGroup.description" type="textarea"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="createNewProblemGroup">确定</el-button>
          <el-button @click="createDialogVisible = false">取消</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- 更新题单对话框 -->
    <el-dialog v-model="updateDialogVisible" title="更新题单" width="30%">
      <el-form :model="updateProblemGroup" label-width="100px">
        <el-form-item label="用户名">
          <el-input v-model="updateProblemGroup.username" disabled></el-input>
        </el-form-item>
        <el-form-item label="问题组ID">
          <el-input v-model="updateProblemGroup.problem_group_id" disabled></el-input>
        </el-form-item>
        <el-form-item label="问题组标题">
          <el-input v-model="updateProblemGroup.title"></el-input>
        </el-form-item>
        <el-form-item label="问题组描述">
          <el-input v-model="updateProblemGroup.description" type="textarea"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button type="primary" @click="updateProblemGroupFunc">确定</el-button>
          <el-button @click="updateDialogVisible = false">取消</el-button>
        </span>
      </template>
    </el-dialog>

    <!-- Share对话框 -->
    <el-dialog v-model="shareDialogVisible" title="分享题单" width="30%">
      <!-- 这里可以添加分享相关的表单或内容 -->
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="shareDialogVisible = false">关闭</el-button>
        </span>
      </template>
    </el-dialog>
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
  color: #3498db;
}

.problem-link:visited {
  color: #3498db
}

.button-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.button-container .el-button {
  margin-right: 5px;
}

.button-container .el-button:last-child {
  margin-right: 0;
}
</style>