<script lang="ts" setup>
import { ref, reactive, onMounted, computed, type FormInstance, type FormRules } from 'vue';
import {
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
  ElTable,
  ElTableColumn,
  ElCard,
  ElPopconfirm,
  ElTag,
  ElTooltip
} from 'element-plus';
import 'element-plus/dist/index.css';
import API from '@/plugins/axios';
import Navigator from "@/components/Base/Navigator.vue";

const data = defineProps(['username'])
const dialogVisible = ref(false);
const form = reactive({
  name: '',
  description: ''
});
let editVisible = ref(false);
let descriptionDialogVisible = ref(false);
let edit_loading = ref(true);
let currentGroupName = ref('');
let currentDescription = ref('');

interface Group {
  id: number
  name: string
  description: string
  created_by_id: number
  created_at: string
  creator: string
  number: number
}

interface Member {
  username: string
}

interface GroupMembersDict {
  [group_name: string]: Member[];
}

const tableData = ref<Group[]>([]);
const allGroupMembers = ref<GroupMembersDict>({});
const search = ref('');

const filterTableData = computed(() =>
    tableData.value.filter(
        (data) =>
            !search.value ||
            data.name.toLowerCase().includes(search.value.toLowerCase())
    )
);

const ruleFormRef = ref<FormInstance>();
const validateName = (rule: any, value: any, callback: any) => {
  if (value === '') {
    callback(new Error('请输入群组名称'));
  } else {
    callback();
  }
};
const rules = reactive<FormRules>({
  name: [{validator: validateName, trigger: 'blur'}]
});

const resetForm = () => {
  form.name = '';
  form.description = '';
};

onMounted(async () => showData());

async function showData() {
  try {
    const response = await API.post('/group_get_groups',
        { username: data.username },
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
    );
    if (response.data.code === 200) {
      tableData.value = response.data.groups.filter(group => group.creator === data.username);
      await getGroupMembers();
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error('Error fetching data:', error);
    ElMessage.error('Failed to fetch data');
  }
}

const handleSubmit = async (formEl: FormInstance | undefined) => {
  if (!formEl) return;
  await formEl.validate(async (valid) => {
    if (valid) {
      dialogVisible.value = false;
      try {
        const response = await API.post('/group_create',
            {
              username: data.username,
              group_name: form.name,
              group_description: form.description,
            },
            { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
        );
        if (response.data.code === 200) {
          ElMessage.success(response.data.message);
          await showData();
          resetForm();
        } else {
          ElMessage.error(response.data.message);
        }
      } catch (error) {
        console.error('Error creating group:', error);
        ElMessage.error('Failed to create group');
      }
    } else {
      console.log("submit error");
    }
  });
};

function handleClick() {
  dialogVisible.value = true;
}

function handleClose() {
  dialogVisible.value = false;
  resetForm();
}

function handleEdit(row: Group) {
  currentGroupName.value = row.name;
  editVisible.value = true;
}

async function handleDelete(row: Group) {
  try {
    const response = await API.post('/group_delete_all',
        {
          group_name: row.name,
          username: data.username
        },
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
    );
    if (response.data.code === 200) {
      ElMessage.success(response.data.message);
      await showData();
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error('Error deleting group:', error);
    ElMessage.error('Failed to delete group');
  }
}

async function handleDeleteMember(row: Member) {
  try {
    const response = await API.post('/group_delete_member',
        {
          to_deleter: row.username,
          group_name: currentGroupName.value,
          username: data.username
        },
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
    );
    if (response.data.code === 200) {
      editVisible.value = false;
      ElMessage.success(response.data.message);
      await showData();
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    console.error('Error deleting member:', error);
    ElMessage.error('Failed to delete member');
  }
}

async function getGroupMembers() {
  for (const group of tableData.value) {
    try {
      const response = await API.post('/group_get_members',
          {
            group_name: group.name,
            username: data.username
          },
          { headers: { 'Content-Type': 'application/x-www-form-urlencoded' }}
      );
      if (response.data.code === 200) {
        allGroupMembers.value[group.name] = response.data.members.map(username => ({ username }));
      } else {
        ElMessage.error(response.data.message);
      }
    } catch (error) {
      console.error('Error fetching group members:', error);
      ElMessage.error('Failed to fetch group members');
    }
  }
  edit_loading.value = false;
}

function getMember(groupName: string): Member[] {
  return allGroupMembers.value[groupName] || [];
}

function isCreator(name: string) {
  return name === data.username;
}

function openDescriptionDialog(group: Group) {
  currentDescription.value = group.description;
  currentGroupName.value = group.name;
  descriptionDialogVisible.value = true;
}

</script>

<template>
  <div class="group-management">
    <el-card class="group-card">
      <template #header>
        <div class="card-header">
          <span>我创建的群组</span>
          <el-button type="primary" @click="handleClick">新建群组</el-button>
        </div>
      </template>

      <el-input
          v-model="search"
          placeholder="搜索群组"
          prefix-icon="el-icon-search"
          clearable
          class="search-input"
      />

      <el-table :data="filterTableData" style="width: 100%" class="group-table">
        <el-table-column label="群组名称" prop="name" />
        <el-table-column label="创建者" prop="creator">
          <template #default="{ row }">
            <el-tag size="small" :type="row.creator === data.username ? 'success' : 'info'">
              {{ row.creator }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="人数" prop="number" width="80" />
        <el-table-column label="操作" align="center" width="280">
          <template #default="{ row }">
            <el-button type="" size="small" @click="openDescriptionDialog(row)">
              详情
            </el-button>
            <el-button type="" size="small" @click="handleEdit(row)">
              管理群组
            </el-button>
            <el-popconfirm
                title="确定要删除该群组吗？"
                @confirm="handleDelete(row)"
            >
              <template #reference>
                <el-button type="danger" size="small">
                  删除群组
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog v-model="dialogVisible" title="新建群组" width="30%">
      <el-form :model="form" label-width="80px" :rules="rules" ref="ruleFormRef">
        <el-form-item label="群组名称" prop="name">
          <el-input v-model="form.name" autocomplete="off" clearable />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
              v-model="form.description"
              type="textarea"
              :rows="3"
              placeholder="请输入群组描述"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="handleClose">取 消</el-button>
          <el-button type="primary" @click="handleSubmit(ruleFormRef)">确 定</el-button>
        </span>
      </template>
    </el-dialog>

    <el-dialog v-model="descriptionDialogVisible"
               title="群组详情"
               width="30%"
               align-center>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="群组名称">{{ currentGroupName }}</el-descriptions-item>
        <el-descriptions-item label="描述">{{ currentDescription }}</el-descriptions-item>
      </el-descriptions>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="descriptionDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="editVisible" title="群组成员管理" width="50%">
      <el-table :data="getMember(currentGroupName)" v-loading="edit_loading">
        <el-table-column prop="username" label="名称"></el-table-column>
        <el-table-column label="操作" width="120" align="center">
          <template #default="{ row }">
            <el-tooltip
                :content="isCreator(row.username) ? '无法移除创建者' : '移除成员'"
                placement="top"
                :disabled="!isCreator(row.username)"
            >
              <el-button
                  size="small"
                  type="danger"
                  @click="handleDeleteMember(row)"
                  :disabled="isCreator(row.username)"
              >
                移除
              </el-button>
            </el-tooltip>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="editVisible = false">关闭</el-button>
        </span>
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