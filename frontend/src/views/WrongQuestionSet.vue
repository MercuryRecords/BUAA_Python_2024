<script lang="ts" setup>
import {ref, reactive, computed, onMounted} from 'vue'
import {ElMessage} from 'element-plus'
import axios from 'axios'
import Navigator from "@/components/Base/Navigator.vue";
import router from "@/router";
import {useRoute} from 'vue-router'
import API from "@/plugins/axios";

const route = useRoute()

const searchForm = reactive({
  keyword: '',
  tags: [] as string[],
  selectedTags: [] as string[]
})

interface data {
  id: number,
  problem_title: string,
  creator: string,
  problem_group_title: string,
  tags: string[],
  all_count: number,
  all_right_count: number,
  user_count: number,
  user_right_count: number,
  accuracy: number,
  type: string,
  content: string
}

const allProblems = ref<data[]>([
  // ... 其他问题数据
])

const currentPage = ref(1)
const pageSize = ref(20)
const tagDialogVisible = ref(false)
const tagCategories = ref([
  {name: '数学', tags: ['多项式', '矩阵', '行列式', '线性代数']},
  {name: '算法', tags: ['动态规划', '贪心', '搜索', '图论', '数论', '字符串']},
  {name: '数据结构', tags: ['栈', '队列', '链表', '树', '图', '堆']},
  {name: '题目类型', tags: ['选择题', '填空题']},
])

const filteredProblems = ref<data[]>([])

const problems = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredProblems.value.slice(start, end)
})

const total = computed(() => filteredProblems.value.length)

const onSearch = () => {
  filteredProblems.value = allProblems.value.filter(problem => {
    const matchKeyword = searchForm.keyword === '' ||
        problem.problem_title.includes(searchForm.keyword) ||
        problem.id === parseInt(searchForm.keyword) ||
        problem.creator.includes(searchForm.keyword) ||
        problem.problem_group_title.includes(searchForm.keyword) ||
        problem.content.includes(searchForm.keyword)
    const matchTags = searchForm.selectedTags.length === 0 ||
        searchForm.selectedTags.every(tag => problem.tags.includes(tag))
    return matchKeyword && matchTags
  })
  currentPage.value = 1
  ElMessage.success(`找到 ${total.value} 个匹配的题目`)
}

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

const handleSolve = (problem: data, tmp_id: number) => {
  ElMessage.success(`准备解决题目: ${problem.problem_title}`)
  const currentProblems = problems.value;
  const currentIndex = currentProblems.findIndex(p => p.id === problem.id);
  console.log(tmp_id);
  console.log(currentProblems);
  router.push({
    name: 'solve',
    query: {
      username: route.query.username as string,
      index: currentIndex as number,
      problem_group_id: tmp_id,
    },
  });
}

const jumpToQuestion = (problem: data) => {
  const problemIds = problems.value.map(problem => problem.id);
  console.log(problemIds);
  API.post('/temporary_problem_group_create', {
    username: route.query.username,
    problem_ids: problemIds,
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      function (response) {
        if (response.data.code === 200) {
          // 创建成功
          console.log("Ready to solve")
          handleSolve(problem, response.data.data);
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
}

const clearFilters = () => {
  searchForm.keyword = ''
  searchForm.tags = []
  searchForm.selectedTags = []
  onSearch()
}

const openTagDialog = () => {
  tagDialogVisible.value = true
}

const confirmTagSelection = () => {
  tagDialogVisible.value = false
  searchForm.selectedTags = [...searchForm.tags]
  onSearch()
}

const removeTag = (tag: string) => {
  searchForm.selectedTags = searchForm.selectedTags.filter(t => t !== tag)
  searchForm.tags = searchForm.tags.filter(t => t !== tag)
  onSearch()
}

const getAccuracyColor = (accuracy: number) => {
  if (accuracy >= 0.7) return 'success'
  if (accuracy < 0.3) return 'danger'
  return 'warning'
}

function getProblems(group_label: string) {
  console.log(allProblems.value);
  API.post('/get_records', {
    username: route.query.username,
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      function (response) {
        if (response.data.code === 200) {
          allProblems.value = []
          for (let i = 0; i < response.data.data.length; i++) {
            console.log(response.data.data[i]);
            allProblems.value[i] = response.data.data[i];
            allProblems.value[i].accuracy = response.data.data[i].all_count == 0 ? 0 : response.data.data[i].all_right_count / response.data.data[i].all_count
            if (response.data.data[i].type == 'b') {
              allProblems.value[i].tags.push("填空题");
            } else {
              allProblems.value[i].tags.push("选择题");
            }
            console.log(allProblems)
          }
          onSearch()  // Perform initial search after fetching problems
        } else {
          console.log("Mission failed")
          ElMessage.error(response.data.message);
          allProblems.value = [];
          onSearch();
        }
        console.log(response.data)
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
}

function getProblemsNumber() {
  let number = 0;
  console.log(route.query.username)
  API.post('/get_problems_num', {
    username: route.query.username,
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      function (response) {
        if (response.data.code === 200) {
          number = response.data;
          console.log(number);
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
  return number;
}

const formatDate = (dateString: string): string => {
  const date = new Date(dateString);
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  const hours = date.getHours().toString().padStart(2, '0');
  const minutes = date.getMinutes().toString().padStart(2, '0');
  const seconds = date.getSeconds().toString().padStart(2, '0');
  return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
};

const formatRelativeDate = (dateString) => {
  const now = new Date(); // 当前时间
  const pastDate = new Date(dateString); // 后端获得的时间
  const diffInSeconds = Math.floor((now - pastDate) / 1000); // 计算时间差，单位为秒

  const units = [
    {name: 'year', seconds: 60 * 60 * 24 * 365},
    {name: 'month', seconds: 60 * 60 * 24 * 30}, // 简化的月份，实际月份天数不同
    {name: 'day', seconds: 60 * 60 * 24},
    {name: 'hour', seconds: 60 * 60},
    {name: 'minute', seconds: 60},
    {name: 'second', seconds: 1}
  ];

  for (const unit of units) {
    const count = diffInSeconds / unit.seconds;
    if (count >= 1) {
      return `${Math.floor(count)} ${unit.name}${Math.floor(count) > 1 ? 's' : ''} ago`; // 返回相对时间
    }
  }

  return 'just now'; // 如果时间差小于1秒，则显示 "just now"
};
const fetchProblems = async () => {
  getProblems('');
}

const userGroups: string[] = reactive([])

const fetchGroups = async () => {
  API.post('/group_get_groups', {
    username: route.query.username,
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      function (response) {
        if (response.data.code === 200) {
          for (let i = 0; i < response.data.groups.length; i++) {
            userGroups.push(response.data.groups[i].name);
          }
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
}

const selectedGroup = ref('')

const handleCommand = (command: any) => {
  selectedGroup.value = command
  if (command !== '') {
    if (command === '公开分享') {
      getProblems('_shared_to_all');
      // window.location.reload();
    } else {
      console.log(command, 666666666666666666666666666666)
      getProblems(command as string);
      // window.location.reload();
    }
  }
}

onMounted(() => {
  fetchProblems();
  fetchGroups();
})
</script>
<template>
  <div class="common-layout">
    <el-container class="main-container">
      <el-aside width="auto" class="sidebar">
        <Navigator :username="$route.query.username"></Navigator>
      </el-aside>

      <el-container class="content-container">
        <el-main class="main-content">
          <div class="problem-list">
            <el-card class="search-card">
              <el-form :inline="true" :model="searchForm" class="search-form">
                <el-form-item class="search-input">
                  <el-input v-model="searchForm.keyword" placeholder="搜索关键词（题号、标题、上传者、所属题单）"
                            @keyup.enter="onSearch"></el-input>
                </el-form-item>
                <el-form-item class="button-group">
                  <el-button @click="onSearch">搜索</el-button>
                  <el-button @click="openTagDialog">选择标签</el-button>
                  <el-button type="primary" @click="clearFilters">清除所有筛选条件</el-button>

                  <el-dropdown @command="handleCommand" class="group-dropdown">
                    <span class="el-dropdown-link">
                      {{ selectedGroup || '选择用户组' }}
                      <el-icon class="el-icon--right"></el-icon>
                    </span>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="公开分享">公开分享</el-dropdown-item>
                        <el-dropdown-item v-for="group in userGroups" :key="group" :command="group">
                          {{ group }}
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </el-form-item>
              </el-form>

              <div v-if="searchForm.selectedTags.length > 0" class="selected-tags">
                <el-tag
                    v-for="tag in searchForm.selectedTags"
                    :key="tag"
                    closable
                    @close="removeTag(tag)"
                    class="tag"
                >
                  {{ tag }}
                </el-tag>
              </div>
            </el-card>

            <el-table :data="problems" style="width: 100%" class="problem-table">
              <el-table-column label="最近错误时间" min-width="150">
                <template #default="scope">
                  {{ formatRelativeDate(scope.row.last_error_time) }}
                </template>
              </el-table-column>
              <el-table-column prop="id" label="题号" min-width="80"></el-table-column>
              <el-table-column prop="problem_title" label="题目名称" min-width="150"></el-table-column>
              <el-table-column prop="creator" label="上传者" min-width="100"></el-table-column>
              <el-table-column prop="problem_group_title" label="所属题单" min-width="150"></el-table-column>
              <el-table-column label="标签" min-width="150">
                <template #default="scope">
                  <el-tag v-for="tag in scope.row.tags" :key="tag" size="small" class="tag">
                    {{ tag }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="accuracy" label="正确率" min-width="100">
                <template #default="scope">
                  <el-tag :type="getAccuracyColor(scope.row.accuracy)" size="small">
                    {{ (scope.row.accuracy * 100).toFixed(2) }}%
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" min-width="80">
                <template #default="scope">
                  <el-button type="text" size="small" @click="jumpToQuestion(scope.row)">解题</el-button>
                </template>
              </el-table-column>
            </el-table>

            <el-pagination
                class="pagination"
                @size-change="handleSizeChange"
                @current-change="handleCurrentChange"
                :current-page="currentPage"
                :page-sizes="[10, 20, 50, 100]"
                :page-size="pageSize"
                layout="total, sizes, prev, pager, next, jumper"
                :total="total">
            </el-pagination>
          </div>
        </el-main>
      </el-container>
    </el-container>

    <!-- 标签选择对话框 -->
    <el-dialog v-model="tagDialogVisible" title="选择标签" width="50%">
      <el-tabs type="border-card">
        <el-tab-pane v-for="category in tagCategories" :key="category.name" :label="category.name">
          <el-checkbox-group v-model="searchForm.tags">
            <el-checkbox v-for="tag in category.tags" :key="tag" :label="tag">{{ tag }}</el-checkbox>
          </el-checkbox-group>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="tagDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="confirmTagSelection">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.main-container {
  height: 100vh;
}

.sidebar {
  flex-shrink: 0;
  z-index: 1001; /* 增加此行 */
}

.content-container {
  flex-grow: 1;
  overflow-x: hidden;
}

.main-content {
  padding: 20px;
}

.problem-list {
  max-width: 1200px;
  margin: 0 auto;
}

.search-card {
  margin-bottom: 20px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 10px;
}

.search-input {
  flex-grow: 1;
  min-width: 200px;
}

.button-group {
  display: flex;
  align-items: center;
  gap: 10px;
}

.selected-tags {
  margin-top: 10px;
}

.tag {
  margin-right: 5px;
  margin-bottom: 5px;
}

.problem-table {
  margin-bottom: 20px;
}

.pagination {
  display: flex;
  justify-content: center;
}

.group-dropdown {
  margin-left: 10px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
  display: flex;
  align-items: center;
}

@media (max-width: 768px) {
  .search-form {
    flex-direction: column;
    align-items: stretch;
  }

  .search-input {
    width: 100%;
  }

  .button-group {
    flex-direction: column;
    align-items: stretch;
  }

  .group-dropdown {
    margin-left: 0;
    margin-top: 10px;
  }
}
</style>
