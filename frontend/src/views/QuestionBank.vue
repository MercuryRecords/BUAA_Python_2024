<script lang="ts" setup>
import {ref, reactive} from 'vue'
import {ElMessage} from 'element-plus'
import Navigator from "@/components/Base/Navigator.vue";

const searchForm = reactive({
  difficulty: '',
  keyword: ''
})

const problems = ref([
  {id: 'P1000', title: '超级玛丽游戏', difficulty: '入门'},
  {id: 'P1001', title: 'A+B Problem', difficulty: '入门'},
  {id: 'P1002', title: '[NOIP2002 普及组] 过河卒', source: 'NOIP普及组', year: '2002', difficulty: '普及'},
  // ... 添加更多题目
])

const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(10243)

const onSearch = () => {
  // 实现搜索逻辑
  ElMessage.success('搜索功能待实现')
}

const handleSizeChange = (val: any) => {
  pageSize.value = val
  // 重新加载数据
}

const handleCurrentChange = (val: any) => {
  currentPage.value = val
  // 重新加载数据
}

const getDifficultyType = (difficulty: any) => {
  switch (difficulty) {
    case '入门':
      return 'success'
    case '普及':
      return 'warning'
    case '提高':
      return 'danger'
    default:
      return 'info'
  }
}

const handleSolve = (problem: any) => {
  ElMessage.success(`准备解决题目: ${problem.title}`)
}
</script>

<template>
  <div class="common-layout">
    <el-container>
      <el-header>
        <!--          <h1>Shared Platform</h1>-->
      </el-header>

      <el-container>
        <el-aside width="200px">
          <!--            导航栏-->
          <Navigator :username="$route.query.username"></Navigator> <!--挂上导航栏，点击即可跳转,现在的位置是home/username=?-->
        </el-aside>

        <el-container>
          <el-main class="shifted-content">
            <!--            <h1>我创建的群组</h1>-->
            <!--              主体内容-->
            <!--            <CreateGroup :username="$route.query.username"></CreateGroup>-->
            <div class="problem-list">
              <el-card>
                <el-form :inline="true" :model="searchForm" class="demo-form-inline">
                  <el-form-item label="筛选条件">
                    <el-select v-model="searchForm.difficulty" placeholder="难度">
                      <el-option label="全部难度" value=""></el-option>
                      <el-option label="入门" value="入门"></el-option>
                      <el-option label="普及" value="普及"></el-option>
                      <el-option label="提高" value="提高"></el-option>
                    </el-select>
                  </el-form-item>
                  <el-form-item>
                    <el-input v-model="searchForm.keyword" placeholder="搜索关键词"></el-input>
                  </el-form-item>
                  <el-form-item>
                    <el-button type="primary" @click="onSearch">搜索</el-button>
                  </el-form-item>
                </el-form>
              </el-card>

              <el-table :data="problems" style="width: 100%">
                <el-table-column prop="id" label="题号" width="100"></el-table-column>
                <el-table-column prop="title" label="题目名称"></el-table-column>
                <el-table-column label="来源" width="180">
                  <template #default="scope">
                    <el-tag v-if="scope.row.source" size="small">{{ scope.row.source }}</el-tag>
                    <el-tag v-if="scope.row.year" size="small" type="info">{{ scope.row.year }}</el-tag>
                  </template>
                </el-table-column>
                <el-table-column label="难度" width="100">
                  <template #default="scope">
                    <el-tag :type="getDifficultyType(scope.row.difficulty)" size="small">{{
                        scope.row.difficulty
                      }}
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
  </div>
</template>

<style scoped>
.problem-list {
  padding: 20px;
}
</style>