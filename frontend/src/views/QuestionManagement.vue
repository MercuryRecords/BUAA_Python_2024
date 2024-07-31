<script lang="ts" setup>
import { ref, reactive, computed, onMounted } from 'vue'
import {ElMessage, ElMessageBox} from 'element-plus'
import axios from 'axios'
import Navigator from "@/components/Base/Navigator.vue";
import router from "@/router";
import { useRoute } from 'vue-router'
import API from "@/plugins/axios";
import NavigatorM from "@/components/Base/NavigatorM.vue";

const route = useRoute()

const searchForm = reactive({
  keyword: '',
  tags: [] as string[],
  selectedTags: [] as string[],
  searchType: 'key',
})

interface data {
  id: number;
  type: 'c' | 'b';
  problem_title: string;
  content: string;
  ans_count: number;
  field1: string;
  field2: string;
  field3: string;
  field4: string;
  field5: string;
  field6: string;
  field7: string;
  tags: string[];
  creator: string;
  problem_group_id: number;
  problem_group_title: string;
  user_right_count: number;
  user_count: number;
  all_right_count: number;
  all_count: number;
  accuracy: number;
}

const allProblems = ref<data[]>([
  // ... 其他问题数据
])

const currentPage = ref(1)
const pageSize = ref(20)
const tagDialogVisible = ref(false)
const user_tags = ref<string[]>([])
const tagCategories = ref<{ name: string; tags: string[] }[]>([])

async function getUserTags() {
  try {
    const response = await API.post('/get_user_tags', {
      username: route.query.username,
    }, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    if (response.data.code === 200) {
      user_tags.value = response.data.data.filter((tag: string) =>
          !["选择题", "选择", "填空题", "填空"].includes(tag)
      )

      tagCategories.value = [
        { name: '所有标签', tags: user_tags.value },
        { name: '题目类型', tags: ['选择题', '填空题'] },
      ]

      console.log("Get the tags", user_tags.value)
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('Error fetching user tags:', error)
    ElMessage.error('获取标签失败')
  }
}


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
  ElMessage.success(`找到 ${filteredProblems.value.length} 个匹配的题目`)
}

function _onSearch() {
  let search_username = ''
  let search_user_group_name = ''
  let search_keyword = ''

  if (searchForm.searchType == 'key') {
    search_username = searchForm.keyword;
  }
  else if (searchForm.searchType == 'group') {
    search_user_group_name = searchForm.keyword;
  } else if (searchForm.searchType == 'user') {
    search_keyword = searchForm.keyword;
  }
  getProblems(search_username, search_user_group_name, search_keyword);
  onSearch();
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
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
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

function getProblems(search_username:string, search_user_group_name:string, search_keyword:string) {
  API.post('/admin_get_problems', {
    username: route.query.username,
    username_to_search: search_username,
    filter_group: search_user_group_name,
    to_search: search_keyword
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          allProblems.value = []
          for (let i = 0; i < response.data.data.length; i++) {
            console.log(response.data.data[i]);
            allProblems.value[i] = response.data.data[i];
            allProblems.value[i].accuracy = response.data.data[i].all_count == 0 ? 0 :response.data.data[i].all_right_count / response.data.data[i].all_count
            // if (response.data.data[i].type == 'b') {
            //   allProblems.value[i].tags.push("填空题");
            // } else {
            //   allProblems.value[i].tags.push("选择题");
            // }
            console.log(allProblems)
          }
          onSearch();
        } else {
          console.log("Mission failed")
          ElMessage.error(response.data.message);
          allProblems.value = [];
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
}

const fetchProblems = async () => {
  getProblems('','','');
}


function getPlaceholder() {
  switch (searchForm.searchType) {
    case 'key':
      return '输入题目关键字';
    case 'group':
      return '输入用户组名称';
    case 'user':
      return '输入用户名称';
    default:
      return '请选择搜索方式';
  }
}

const updateDialogVisible = ref(false)
const currentProblem = ref<data | null>(null)
const updateForm = reactive({
  problem_title: '',
  type: '',
  content: '',
  ans_count: 0,
  answer: '',
  field1: '',
  field2: '',
  field3: '',
  field4: '',
  field5: '',
  field6: '',
  field7: '',
  tags: [] as string[]
})

// 打开更新对话框
const openUpdateDialog = (problem: data) => {
  currentProblem.value = problem
  updateForm.problem_title = problem.problem_title
  updateForm.type = problem.type
  updateForm.content = problem.content
  updateForm.ans_count = problem.ans_count
  updateForm.field1 = problem.field1
  updateForm.field2 = problem.field2
  updateForm.field3 = problem.field3
  updateForm.field4 = problem.field4
  updateForm.field5 = problem.field5
  updateForm.field6 = problem.field6
  updateForm.field7 = problem.field7
  updateForm.tags = [...problem.tags]
  updateDialogVisible.value = true
}

// 提交更新
const submitUpdate = () => {
  if (!currentProblem.value) return
  console.log(updateForm.tags)
  API.post('/admin_problem_update', {
    username: route.query.username,
    problem_id: currentProblem.value.id,
    ...updateForm
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(response => {
    if (response.data.code === 200) {
      ElMessage.success('题目更新成功')
      updateDialogVisible.value = false
      fetchProblems() // 重新获取题目列表
    } else {
      ElMessage.error(response.data.message)
    }
  }).catch(error => {
    console.error('更新题目失败:', error)
    ElMessage.error('更新题目失败，请稍后重试')
  })
}

// 删除题目
const deleteProblem = (problem: data) => {
  ElMessageBox.confirm(`确定要删除题目 "${problem.problem_title}" 吗？`, '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    API.post('/admin_problem_delete', {
      username: route.query.username,
      problem_id: problem.id
    }, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    }).then(response => {
      if (response.data.code === 200) {
        ElMessage.success('题目删除成功')
        fetchProblems() // 重新获取题目列表
      } else {
        ElMessage.error(response.data.message)
      }
    }).catch(error => {
      console.error('删除题目失败:', error)
      ElMessage.error('删除题目失败，请稍后重试')
    })
  }).catch(() => {
    // 取消删除操作
  })
}

onMounted(async() => {
  await fetchProblems();
})
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
      </el-header>

      <el-container>
        <el-aside width="200px">
          <NavigatorM :username="$route.query.username"></NavigatorM>
        </el-aside>

        <el-container>
          <el-main class="shifted-content">
            <div class="problem-list">
              <el-card>
                <el-form :inline="true" :model="searchForm" class="demo-form-inline">
                  <el-form-item>
                    <el-select v-model="searchForm.searchType" placeholder="搜索方式" style="width: 180px">
                      <el-option label="按题目关键字搜索" value="key"></el-option>
                      <el-option label="按用户组搜索" value="group"></el-option>
                      <el-option label="按用户搜索" value="user"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-input
                        v-model="searchForm.keyword"
                        style="width: 250px"
                        :placeholder="getPlaceholder()"
                        @keyup.enter="onSearch"
                    ></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button @click="onSearch">搜索</el-button>
                  </el-form-item>
                </el-form>
              </el-card>

              <el-table :data="problems" style="width: 100%">
                <el-table-column prop="id" label="题号" width="100"></el-table-column>
                <el-table-column prop="problem_title" label="题目名称" ></el-table-column>
                <el-table-column prop="creator" label="上传者" width="100"></el-table-column>
                <el-table-column prop="problem_group_title" label="所属题单" width="180"></el-table-column>
                <el-table-column label="标签" width="200">
                  <template #default="scope">
                    <el-tag v-for="tag in scope.row.tags" :key="tag" size="small" style="margin-right: 5px;">
                      {{ tag }}
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column prop="accuracy" label="正确率" width="100">
                  <template #default="scope">
                    <el-tag :type="getAccuracyColor(scope.row.accuracy)" size="small">
                      {{ (scope.row.accuracy * 100).toFixed(2) }}%
                    </el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="操作" width="120">
                  <template #default="scope">
                    <el-button type="text" size="default" @click="openUpdateDialog(scope.row)">编辑</el-button>
                    <el-button type="text" size="default" @click="deleteProblem(scope.row)">删除</el-button>
                  </template>
                </el-table-column>
              </el-table>

              <el-pagination
                  class="pages"
                  @size-change="handleSizeChange"
                  @current-change="handleCurrentChange"
                  :current-page="currentPage"
                  :page-sizes="[10, 20, 50, 100]"
                  :page-size="pageSize"
                  layout="total, sizes, jumper, ->, prev, pager, next"
                  :total="total">
              </el-pagination>
            </div>
          </el-main>
        </el-container>
      </el-container>
    </el-container>

    <el-dialog v-model="updateDialogVisible" title="更新题目" width="50%">
      <el-form :model="updateForm" label-width="100px">
        <el-form-item label="题目标题">
          <el-input v-model="updateForm.problem_title"></el-input>
        </el-form-item>
        <el-form-item label="题目类型">
          <el-tag :type="updateForm.type === 'c' ? 'success' : 'warning'">
            {{ updateForm.type === 'c' ? '选择题' : '填空题' }}
          </el-tag>
        </el-form-item>
        <el-form-item label="题目内容">
          <el-input v-model="updateForm.content" type="textarea" :rows="4"></el-input>
        </el-form-item>
        <el-form-item label="答案数量">
          <el-input-number v-model="updateForm.ans_count" :min="0"></el-input-number>
        </el-form-item>

        <!-- 选择题选项 -->
        <template v-if="updateForm.type === 'c'">
          <el-form-item label="选项A">
            <el-input v-model="updateForm.field1"></el-input>
          </el-form-item>
          <el-form-item label="选项B">
            <el-input v-model="updateForm.field2"></el-input>
          </el-form-item>
          <el-form-item label="选项C">
            <el-input v-model="updateForm.field3"></el-input>
          </el-form-item>
          <el-form-item label="选项D">
            <el-input v-model="updateForm.field4"></el-input>
          </el-form-item>
        </template>

        <!-- 填空题答案 -->
        <template v-else>
          <el-form-item v-for="i in updateForm.ans_count" :key="i" :label="`答案${i}`">
            <el-input v-model="updateForm[`field${i}` as keyof typeof updateForm]"></el-input>
          </el-form-item>
        </template>

        <el-form-item label="标签">
          <el-select v-model="updateForm.tags" multiple filterable allow-create>
            <el-option v-for="tag in tagCategories.flatMap(c => c.tags)" :key="tag" :label="tag" :value="tag"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
      <span class="dialog-footer">
        <el-button @click="updateDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitUpdate">确认</el-button>
      </span>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.shifted-content {
  margin-left: 80px;
  margin-right: 225px;
}

.problem-list {
  padding: 20px;
}

.pages {
  margin-top: 10px;
}

.filter-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  margin-bottom: 20px;
}

.el-dropdown-link {
  cursor: pointer;
  color: #409EFF;
  display: flex;
  align-items: center;
}

.selected-filters {
  margin-top: 10px;
  font-size: 14px;
  color: #606266;
}

.total-count {
  margin-left: 10px;
  color: #909399;
}

.groups {
  width: 100px;
}

.user-group-dropdown {
  display: inline-block;
}

.el-dropdown-link {
  cursor: pointer;
  color: #606266;
  font-size: 14px;
  display: flex;
  align-items: center;
  padding: 8px 16px;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  transition: all 0.3s;
}

.el-dropdown-link:hover {
  color: #409EFF;
  border-color: #c6e2ff;
  background-color: #ecf5ff;
}

.el-icon--right {
  margin-left: 5px;
  transition: transform 0.3s;
}

.el-dropdown-link:hover .el-icon--right {
  transform: rotate(180deg);
}

:deep(.el-dropdown-menu) {
  padding: 5px 0;
}

:deep(.el-dropdown-menu__item) {
  padding: 8px 20px;
  font-size: 14px;
  line-height: 1.5;
}

:deep(.el-dropdown-menu__item:hover) {
  background-color: #f5f7fa;
  color: #409EFF;
}

:deep(.el-dropdown-menu__item:focus) {
  background-color: #f5f7fa;
  color: #409EFF;
}

:deep(.el-dropdown-menu__item.is-disabled) {
  color: #c0c4cc;
  cursor: not-allowed;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

:deep(.el-button--text) {
  padding: 2px 0;
  font-size: 12px;
}

:deep(.el-button--text:first-child) {
  margin-right: 8px;
}
</style>