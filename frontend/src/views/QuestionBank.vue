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
  id: string,
  problem_title: string,
  creator: string,
  problem_group_title: string,
  tags: string[],
  all_count: number,
  all_right_count: number,
  user_count: number,
  user_right_count: number,
  accuracy: number
}

const allProblems = ref<data[]>([
  // ... 其他问题数据
])

const currentPage = ref(1)
const pageSize = ref(20)

const tagDialogVisible = ref(false)
const tagCategories = ref([
  {name: '数学', tags:['多项式','矩阵','行列式','线性代数']},
  {name: '算法', tags: ['动态规划', '贪心', '搜索', '图论', '数论', '字符串']},
  {name: '数据结构', tags: ['栈', '队列', '链表', '树', '图', '堆']},
  {name: '题目类型', tags: ['选择题', '填空题']},
])

const filterProblems = computed(() => {
  return allProblems.value.filter(problem => {
    const matchKeyword = searchForm.keyword === '' ||
        problem.problem_title.toLowerCase().includes(searchForm.keyword.toLowerCase()) ||
        problem.id.toLowerCase().includes(searchForm.keyword.toLowerCase()) ||
        problem.creator.toLowerCase().includes(searchForm.keyword.toLowerCase()) ||
        problem.problem_group_title.toLowerCase().includes(searchForm.keyword.toLowerCase())
    const matchTags = searchForm.selectedTags.length === 0 || searchForm.selectedTags.every(tag => problem.tags.includes(tag))
    return matchKeyword && matchTags
  })
})

const problems = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filterProblems.value.slice(start, end)
})

const total = computed(() => filterProblems.value.length)

const onSearch = () => {
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

const handleSolve = (problem: data) => {
  ElMessage.success(`准备解决题目: ${problem.problem_title}`)
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

function getProblems(page: number) {
  API.post('/get_problems',
      {
        username: route.query.username,
        page: page,
        number_per_page: 10
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
      function (response) {
        if (response.data.code === 200) { // 成功接收
          // for (let i = 0; i < response.data.groups.length; i++) {
          //   if (response.data.groups[i].creator == data.username) {
          //     tableData.push(response.data.groups[i]) //将群组加入tableData，准备在挂载的时候显示出来
          //   }
          // }
          for (let i = 0; i < response.data.data.length; i++) {
            console.log(response.data.data[i]);
            allProblems.value[i] = response.data.data[i];
            allProblems.value[i].accuracy = response.data.data[i].all_right_count / response.data.data[i].all_count
          }
        } else { // 接收失败
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      })
}

function getProblemsNumber() {
  let number = 0;
  console.log(route.query.username)
  API.post('/get_problems_num',
      {
        username: route.query.username,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
      function (response) {
        if (response.data.code === 200) { // 成功接收
          number = response.data;
          console.log(number);
        } else { // 接收失败
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      })
  return number;
}

const fetchProblems = async () => {
  // let number = getProblemsNumber();
  let number = 20;
  for (let i = 1; i <= Math.floor(number/10)+1; i++) {
    getProblems(i);
  }
}

onMounted(() => {
  fetchProblems()
})

// ----------------------测试----------------
// TODO 实现下拉选择用户组
// 定义用户组数据
const userGroups = ref([
  "第一个组",
  "第二个组",
  "第三个组",
  // 可以根据需要添加更多组
])

const selectedGroup = ref('')

const handleCommand = (command: any) => {
  selectedGroup.value = command
  if (command !== '') {
    // 路由跳转到指定组件，并传递选中的标签
    router.push({
      name: 'QuestionBank4SpecificGroup', // 替换为你要跳转的组件名称
      query: {
        username: route.query.username,
        groupLabel: command,
      }
    })
  } else {
    // 无需处理
  }
}
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <h1>题目列表</h1>
      </el-header>

      <el-container>
        <el-aside width="200px">
          <Navigator :username="$route.query.username"></Navigator>
        </el-aside>

        <el-container>
          <el-main class="shifted-content">
            <div class="problem-list">
              <el-card>
                <el-form :inline="true" :model="searchForm" class="demo-form-inline">
                  <el-form-item>
                    <el-input v-model="searchForm.keyword" placeholder="搜索关键词（题号、标题、上传者、所属题单）"
                              style="width: 310px"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button @click="openTagDialog">选择标签</el-button>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="clearFilters">清除所有筛选条件</el-button>
                  </el-form-item>
                  <el-dropdown @command="handleCommand">
                      <span class="el-dropdown-link">
                        {{ selectedGroup || '选择用户组' }}
                        <el-icon class="el-icon--right"></el-icon>
                      </span>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="">全部用户组</el-dropdown-item>
                        <el-dropdown-item v-for="group in userGroups" :key="group" :command="group">
                          {{ group }}
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </el-form>
                <!-- 显示选中标签的区域 -->
                <div v-if="searchForm.selectedTags.length > 0" style="margin-top: 10px;">
                  <el-tag
                      v-for="tag in searchForm.selectedTags"
                      :key="tag"
                      closable
                      @close="removeTag(tag)"
                      style="margin-right: 5px;"
                  >
                    {{ tag }}
                  </el-tag>
                </div>
              </el-card>

              <el-table :data="problems" style="width: 100%">
                <el-table-column prop="id" label="题号" width="100"></el-table-column>
                <el-table-column prop="problem_title" label="题目名称"></el-table-column>
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
                <el-table-column label="操作" width="100">
                  <template #default="scope">
                    <el-button type="text" size="small" @click="handleSolve(scope.row)">解题</el-button>
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
                  layout="total, sizes, prev, pager, next, jumper"
                  :total="total">
              </el-pagination>
            </div>
          </el-main>
        </el-container>
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
.shifted-content {
  margin-left: 80px;
  margin-right: 80px;
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
</style>