<template>
  <div class="group-management">
    <div class="search-container">
      <el-input
          v-model="searchQuery"
          placeholder="搜索群组"
          @input="handleSearch"
          clearable
          style="width: 70%;"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>
    </div>

    <div class="table-container">
      <div class="table-header">
        <h2>群组列表</h2>
      </div>
      <div class="table-wrapper">
        <el-table :data="displayedGroups" style="width: 100%">
          <el-table-column prop="name" label="群组名" width="180" />
          <el-table-column prop="creator" label="创建者" width="180" />
          <el-table-column label="详细信息" width="120">
            <template #default="scope">
              <el-button @click="showGroupDetails(scope.row)">详细信息</el-button>
            </template>
          </el-table-column>
          <el-table-column label="成员管理" width="120">
            <template #default="scope">
              <el-button @click="showMemberManagement(scope.row)">管理成员</el-button>
            </template>
          </el-table-column>
          <el-table-column label="删除群组" width="120">
            <template #default="scope">
              <el-button type="danger" @click="deleteGroup(scope.row.name)">删除</el-button>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </div>

    <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="filteredGroups.length"
        @current-change="handlePageChange"
        layout="prev, pager, next"
        class="pagination"
    />

    <el-dialog v-model="groupDetailsVisible" title="详细信息">
      <p><strong>群组名：</strong>{{ selectedGroup.name }}</p>
      <p><strong>创建者：</strong>{{ selectedGroup.creator }}</p>
      <p><strong>创建时间：</strong>{{ selectedGroup.create_time }}</p>
      <div class="description-container">
        <p>
          <strong>描述：</strong>
          <span v-if="!isEditingDescription">{{ selectedGroup.description }}</span>
          <el-input
              v-else
              v-model="editedDescription"
              type="textarea"
              :rows="3"
          ></el-input>
        </p>
        <el-button v-if="!isEditingDescription" @click="startEditingDescription" class="edit-button">编辑描述</el-button>
        <el-button v-else type="primary" @click="saveDescription" class="save-button">保存</el-button>
      </div>
    </el-dialog>

    <el-dialog v-model="memberManagementVisible" title="成员管理">
      <el-button @click="showAddMemberDialog" class="add-member-button">新增成员</el-button>
      <el-table :data="sortedMembers" style="width: 100%">
        <el-table-column label="用户名">
          <template #default="scope">
            {{ scope.row }}
            <el-tag v-if="scope.row === selectedGroup.creator" size="small" type="info" effect="light">群主</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope">
            <el-button type="danger" @click="kickMember(scope.row)">踢出</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-dialog>

    <el-dialog v-model="addMemberDialogVisible" title="新增成员">
      <el-form :model="newMember" :rules="rules" ref="addMemberForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="newMember.username"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelAddMember">取消</el-button>
          <el-button type="primary" @click="addMember">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {ElMessage, ElMessageBox, type FormInstance} from 'element-plus'
import { Search } from '@element-plus/icons-vue'
import API from "@/plugins/axios"

interface Group {
  name: string;
  description: string;
  creator: string;
  create_time: string;
  members: string[];
}
const data = defineProps(['username']) //从Navigator拿到的username
const groups = ref<Group[]>([])
const currentPage = ref(1)
const pageSize = 10
const groupDetailsVisible = ref(false)
const memberManagementVisible = ref(false)
const addMemberDialogVisible = ref(false)
const selectedGroup = ref<Group>({} as Group)
const newMember = ref({ username: '' })
const addMemberForm = ref<FormInstance>()
const searchQuery = ref('')
const isEditingDescription = ref(true)
const editedDescription = ref('')

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
  ],
}

const filteredGroups = computed(() => {
  if (searchQuery.value) {
    return groups.value.filter(group => group.name.toLowerCase().includes(searchQuery.value.toLowerCase()))
  }
  return groups.value
})

const displayedGroups = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return filteredGroups.value.slice(start, end)
})

const fetchGroups = async () => {
  try {
    const response = await API.post('/admin_get_group_list', {
      username: data.username, // 这里应该使用实际的管理员用户名
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    if (response.data.code === 200) {
      groups.value = response.data.data
    } else {
      console.error('Failed to fetch groups:', response.data.message)
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('Error fetching groups:', error)
    ElMessage.error('获取群组列表失败')
  }
}

const showGroupDetails = (group: Group) => {
  selectedGroup.value = group
  editedDescription.value = group.description
  groupDetailsVisible.value = true
}

const showMemberManagement = (group: Group) => {
  selectedGroup.value = group
  memberManagementVisible.value = true
}

const deleteGroup = async (groupName: string) => {
  await ElMessageBox.confirm('确定要删除这个群组吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  API.post('/admin_delete_group', {
    username: data.username,
    group_name: groupName
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          ElMessage.success(response.data.message);
          fetchGroups();
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

const handlePageChange = (page: number) => {
  currentPage.value = page
}

const showAddMemberDialog = () => {
  addMemberDialogVisible.value = true
}

const cancelAddMember = () => {
  addMemberDialogVisible.value = false
  newMember.value = { username: '' }
  if (addMemberForm.value) {
    addMemberForm.value.resetFields()
  }
}

const addMember = () => {
  if (addMemberForm.value) {
    addMemberForm.value.validate((valid) => {
      if (valid) {
        API.post('/admin_add_user_to_group', {
          username: data.username, // TODO: 修改为实际的管理员用户名
          name: newMember.value.username,
          group_name: selectedGroup.value.name
        }, {
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
        }).then(response => {
          if (response.data.code === 200) {
            ElMessage.success(response.data.message);
            selectedGroup.value.members.push(newMember.value.username);
            cancelAddMember();
          } else {
            ElMessage.error(response.data.message);
          }
        }).catch(error => {
          console.error('Error adding member:', error);
          ElMessage.error('添加成员失败');
        });
      } else {
        return false;
      }
    });
  }
}

const kickMember = (member: string) => {
  API.post('/admin_remove_user_from_group', {
    username: data.username, // TODO: 修改为实际的管理员用户名
    name: member,
    group_name: selectedGroup.value.name
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(response => {
    if (response.data.code === 200) {
      if (member === selectedGroup.value.creator) {
        ElMessage.warning('踢出群主，已解散该群组');
        memberManagementVisible.value = false;
        fetchGroups(); // 刷新群组列表
      } else {
        ElMessage.success(response.data.message);
        selectedGroup.value.members = selectedGroup.value.members.filter(m => m !== member);
      }
    } else {
      ElMessage.error(response.data.message);
    }
  }).catch(error => {
    console.error('Error kicking member:', error);
    ElMessage.error('踢出成员失败');
  });
}

const handleSearch = () => {
  currentPage.value = 1 // 重置页码
}

const sortedMembers = computed(() => {
  if (!selectedGroup.value || !selectedGroup.value.members) return [];

  return [selectedGroup.value.creator, ...selectedGroup.value.members.filter(member => member !== selectedGroup.value.creator)];
});

const startEditingDescription = () => {
  isEditingDescription.value = true
  editedDescription.value = selectedGroup.value.description
}

const cancelEditingDescription = () => {
  isEditingDescription.value = false
  editedDescription.value = selectedGroup.value.description
}

const saveDescription = async () => {
  try {
    const response = await API.post('/admin_edit_group_info', {
      username: data.username, // TODO: 修改为实际的管理员用户名
      group_name: selectedGroup.value.name,
      new_description: editedDescription.value
    }, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
    })

    if (response.data.code === 200) {
      ElMessage.success('群组描述修改成功')
      selectedGroup.value.description = editedDescription.value
      groupDetailsVisible.value = false
      // isEditingDescription.value = false
      // 更新本地群组列表中的描述
      // const groupIndex = groups.value.findIndex(g => g.name === selectedGroup.value.name)
      // if (groupIndex !== -1) {
      //   groups.value[groupIndex].description = editedDescription.value
      // }
    } else {
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('Error updating group description:', error)
    ElMessage.error('更新群组描述失败')
  }
}

onMounted(() => {
  fetchGroups();
})
</script>

<style scoped>
.group-management {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 16px;
}

.search-container {
  width: 90%;
  max-width: 1000px;
  margin-bottom: 20px;
}

.table-container {
  width: 90%;
  max-width: 1000px;
  margin-bottom: 20px;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
}

:deep(.el-table) {
  font-size: 14px;
}

:deep(.el-button) {
  font-size: 14px;
  padding: 8px 15px;
  width: auto;
  min-width: 90px;
}

:deep(.el-dialog__body) {
  font-size: 16px;
}

:deep(.el-dialog__title) {
  font-size: 20px;
}

:deep(.el-pagination) {
  font-size: 14px;
}

.add-member-button {
  margin-bottom: 20px;
}

:deep(.el-tag) {
  margin-left: 5px;
}

.save-button {
  position: absolute;
  bottom: 0;
  right: 0;
}

.description-container {
  position: relative;
  padding-bottom: 40px; /* Add some space at the bottom for the button */
}

</style>