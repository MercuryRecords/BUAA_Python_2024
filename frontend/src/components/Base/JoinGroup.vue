<script lang="ts" setup>
import { ref, reactive, onMounted, computed } from 'vue';
import { ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElMessage } from 'element-plus';
import type { FormInstance, FormRules } from 'element-plus'
import 'element-plus/dist/index.css';
import API from '@/plugins/axios';

const data = defineProps(['username']);
const dialogVisible = ref(false);
const formRef = ref<FormInstance>();
const form = reactive({
  name: '',
  description: ''
});

// 定义表单验证规则
const rules = reactive<FormRules>({
  name: [
    { required: true, message: '请输入群组名称', trigger: 'blur' },
  ],
  description: [
    { required: true, message: '请输入申请理由', trigger: 'blur' },
  ],
});

let editVisible = ref(false);
let deleteVisible = ref(false);
let centerDialogVisible = ref(false);
let searchVisible = ref(false);

interface Group {
  name: string;
  creator: string;
  number: number;
  description?: string;
}

const tableData: Group[] = reactive([]);
const search = ref('');
const searchData: Group[] = reactive([]);
const dialogTitle = computed(() => search.value.length === 0 ? '加入群组' : '加入搜索到的群组');
const selectedGroup = ref<Group | null>(null);

onMounted(async () => showData());

function showData() {
  console.log("showing data");
  console.log(data.username);
  API.post('/group_get_groups_joined',
      {
        username: data.username,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
      function (response) {
        if (response.data.code === 200) {
          tableData.splice(0, tableData.length, ...response.data.groups);
        } else if (response.data.code === 401) {
          ElMessage.error("JG showData " + response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!');
      });
}

function handleSubmit(formEl: FormInstance | undefined) {
  if (!formEl) return
  formEl.validate((valid) => {
    if (valid) {
      dialogVisible.value = false;
      API.post('/group_join_forced',
          {
            username: data.username,
            group_name: form.name,
          }, {
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded'
            }
          }).then(
          function (response) {
            if (response.data.code === 200) {
              ElMessage.success(response.data.message);
              if (search.value) {
                handleSearch();
              } else {
                showData();
              }
            } else {
              ElMessage.error("handleSubmit " + response.data.message);
            }
            // 清空表单
            form.name = '';
            form.description = '';
          }
      ).catch(
          function () {
            console.log('error submit!');
          });
    } else {
      console.log('error submit!');
      return false
    }
  })
}

function handleClick() {
  dialogVisible.value = true;
}

function handleClose() {
  dialogVisible.value = false;
  // 清空表单
  form.name = '';
  form.description = '';
}

function handleEdit() {
  editVisible.value = true;
}

function handleSearch() {
  searchVisible.value = true;
  searchData.length = 0;
  API.post('/group_search', {
    username: data.username,
    keywords: search.value,
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          console.log(response.data);
          searchData.splice(0, searchData.length, ...response.data.groups);
          ElMessage.success(response.data.message);
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error search!');
      });
}

function handleDelete(row: Group) {
  deleteVisible.value = true;
  API.post('/group_quit', {
    username: data.username,
    group_name: row.name
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          ElMessage.success(response.data.message);
          showData();
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error delete!');
      });
}

function handleJoin(row: Group) {
  form.name = row.name;
  form.description = '';
  dialogVisible.value = true;
}

function showDetails(row: Group) {
  selectedGroup.value = row;
  centerDialogVisible.value = true;
}

</script>


<template>
  <div class="group-management">
    <el-card class="group-card">
      <template #header>
        <div class="card-header">
          <span>我加入的群组</span>
          <el-button type="primary" @click="handleClick">加入群组</el-button>
        </div>
      </template>

      <el-input
          v-model="search"
          placeholder="搜索群组"
          prefix-icon="el-icon-search"
          clearable
          class="search-input"
          @keyup.enter="handleSearch"
      />

      <el-table :data="search.length === 0 ? tableData : searchData" style="width: 100%" class="group-table">
        <el-table-column label="群组名称" prop="name" />
        <el-table-column label="创建者" prop="creator">
          <template #default="{ row }">
            <el-tag size="small" type="info">
              {{ row.creator }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="人数" prop="number" width="80" />
        <el-table-column label="操作" align="center" width="280">
          <template #default="{ row }">
            <el-button type="" size="small" @click="showDetails(row)">
              详情
            </el-button>
            <template v-if="search.length === 0">
              <el-popconfirm
                  title="确定要退出该群组吗？"
                  @confirm="handleDelete(row)"
              >
                <template #reference>
                  <el-button type="danger" size="small">
                    退出群组
                  </el-button>
                </template>
              </el-popconfirm>
            </template>
            <template v-else>
              <el-button type="primary" size="small" @click="handleJoin(row)">
                加入群组
              </el-button>
            </template>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="30%">
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px" status-icon>
        <el-form-item label="群组名称" prop="name">
          <el-input v-model="form.name" autocomplete="off" clearable />
        </el-form-item>
        <el-form-item label="申请理由" prop="description">
          <el-input
              v-model="form.description"
              type="textarea"
              :rows="3"
              placeholder="请输入申请理由"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="handleSubmit(formRef)">确 定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog
        v-model="centerDialogVisible"
        title="群组详情"
        width="30%"
        align-center
    >
      <el-descriptions :column="1" border v-if="selectedGroup">
        <el-descriptions-item label="群组名称">{{ selectedGroup.name }}</el-descriptions-item>
        <el-descriptions-item label="群主">{{ selectedGroup.creator }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ selectedGroup.description || '暂无描述' }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="centerDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.group-management {
  padding: 20px;
}

.group-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.search-input {
  margin-bottom: 20px;
}

.group-table {
  margin-top: 20px;
}

.dialog-footer {
  text-align: right;
  margin-top: 20px;
}
</style>