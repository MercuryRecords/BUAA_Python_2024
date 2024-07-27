<script lang="ts" setup>
import {ref, reactive, onMounted, computed, type ComputedRef, toRef, watch, type Ref} from 'vue';
import {
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
  ElTable,
  ElTableColumn,
  type FormInstance,
  type FormRules
} from 'element-plus';
import 'element-plus/dist/index.css';
import API from '@/plugins/axios';
import Navigator from "@/components/Base/Navigator.vue";

const data = defineProps(['username']) //从Navigator拿到的username
const dialogVisible = ref(false);
const form = reactive({
  name: '',
  description: ''
});
let editVisible = ref(false);
let deleteVisible = ref(false);
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

// 表单验证规则
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
  <div>
    <el-button type="primary" @click="handleClick">新建群组</el-button>

    <el-dialog title="新建" v-model="dialogVisible" width="30%">
      <el-form :model="form" label-width="80px" :rules="rules" ref="ruleFormRef">
        <el-form-item label="群组名称" prop="name">
          <el-input v-model="form.name" autocomplete="off" clearable />
        </el-form-item>
        <el-form-item label="描述">
          <el-input
              v-model="form.description"
              style="width: 240px"
              autosize
              type="textarea"
              placeholder="Please input"
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
  </div>

  <div>
    <el-table :data="filterTableData" style="width: 100%">
      <el-table-column label="群组名称" prop="name" />
      <el-table-column label="创建者" prop="creator" />
      <el-table-column label="人数" prop="number" />
      <el-table-column label="详情">
        <template #default="{ row }">
          <el-button size="large" @click="openDescriptionDialog(row)">
            详情
          </el-button>
        </template>
      </el-table-column>
      <el-table-column align="center">
        <template #header>
          <el-input v-model="search" size="large" placeholder="Type to search" clearable />
        </template>
        <template #default="{ row }">
          <el-button size="large" @click="handleEdit(row)" style="">
            管理群组
          </el-button>
          <el-button size="large" type="danger" @click="handleDelete(row)">
            删除群组
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="descriptionDialogVisible" title="群组详情" width="50%">
      <p><strong>群组名称：</strong>{{ currentGroupName }}</p>
      <p><strong>描述：</strong>{{ currentDescription }}</p>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="descriptionDialogVisible = false">关闭</el-button>
        </div>
      </template>
    </el-dialog>

    <el-dialog v-model="editVisible" title="编辑信息" width="50%">
      <el-table :data="getMember(currentGroupName)" v-loading="edit_loading">
        <el-table-column prop="username" label="名称"></el-table-column>
        <el-table-column label="操作">
          <template #default="{ row }">
            <el-button
                size="large"
                type="danger"
                @click="handleDeleteMember(row)"
                :disabled="isCreator(row.username)"
            >踢出群组</el-button>
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