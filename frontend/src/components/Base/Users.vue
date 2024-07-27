<template>
  <div class="user-management">
    <div class="table-container">
      <div class="table-header">
        <h2>用户列表</h2>
        <el-button type="primary" @click="showAddUserDialog">新增用户</el-button>
      </div>
      <el-table :data="displayedUsers" style="width: 80%">
        <el-table-column label="序号" width="80">
          <template #default="scope">
            {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="400" />
        <el-table-column label="详细信息" width="140">
          <template #default="scope">
            <el-button type="" @click="showUserDetails(scope.row)">
              详细信息
            </el-button>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="140">
          <template #default="scope">
            <el-button type="danger" @click="deleteUser(scope.row.username)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="totalUsers"
        @current-change="handlePageChange"
        layout="prev, pager, next"
        class="pagination"
    />

    <el-dialog v-model="userDetailsVisible" title="用户详细信息">
      <p><strong>用户名：</strong>{{ selectedUser.username }}</p>
      <p><strong>密码：</strong>{{ selectedUser.password }}</p>
      <p><strong>所属群组：</strong>{{ selectedUser.groups?.join(', ') }}</p>
    </el-dialog>

    <el-dialog v-model="addUserDialogVisible" title="新增用户">
      <el-form :model="newUser" :rules="rules" ref="addUserForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="newUser.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="newUser.password" type="password"></el-input>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="cancelAddUser">取消</el-button>
          <el-button type="primary" @click="addUser">确认</el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import {ElMessage, type FormInstance} from 'element-plus'
import API from "@/plugins/axios"

interface User {
  username: string;
  password: string;
  groups: string[];
}

const users = ref<User[]>([])
const currentPage = ref(1)
const pageSize = 10
const totalUsers = ref(0)
const userDetailsVisible = ref(false)
const selectedUser = ref<User>({} as User)
const addUserDialogVisible = ref(false)
const newUser = ref({ username: '', password: '' })
const addUserForm = ref<FormInstance>()

const rules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
  ],
}

const displayedUsers = computed(() => {
  const start = (currentPage.value - 1) * pageSize
  const end = start + pageSize
  return users.value.slice(start, end)
})

const fetchUsers = async () => {
  try {
    const response = await API.post('/admin_get_user_list', {
      username: 'Admin', // 这里应该使用实际的管理员用户名
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    if (response.data.code === 200) {
      users.value = response.data.data;
      totalUsers.value = response.data.data.length;
    } else {
      console.error('Failed to fetch users:', response.data.message)
      ElMessage.error(response.data.message)
    }
  } catch (error) {
    console.error('Error fetching users:', error)
    ElMessage.error('获取用户列表失败')
  }
}

const showUserDetails = (user: User) => {
  selectedUser.value = user
  userDetailsVisible.value = true
}

const deleteUser = async (username: string) => {
  API.post('/admin_delete_user', {
    username: 'Admin',
    name: username
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          fetchUsers();
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
  currentPage.value = page;
}

const showAddUserDialog = () => {
  addUserDialogVisible.value = true
}

const addUser = async () => {
  if (!addUserForm.value) return
  addUserForm.value.validate((valid) => {
    if (valid) {
      API.post('/admin_register_user', {
        username: 'Admin', // 这里应该使用实际的管理员用户名
        name: newUser.value.username,
        password: newUser.value.password
      }, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
      }).then(
          function (response) {
            if (response.data.code === 200) {
              fetchUsers();
              addUserDialogVisible.value = false;
              resetNewUserForm();
              ElMessage.success('用户添加成功');
            } else {
              ElMessage.error(response.data.message);
            }
          }
      ).catch(
          function () {
            console.log('error submit!')
            ElMessage.error('添加用户失败');
          }
      )
    } else {
      console.log('error submit!')
      return false
    }
  })
}

const cancelAddUser = () => {
  addUserDialogVisible.value = false
  resetNewUserForm()
}

const resetNewUserForm = () => {
  newUser.value = { username: '', password: '' }
  if (addUserForm.value) {
    addUserForm.value.resetFields()
  }
}

onMounted(() => {
  fetchUsers();
})
</script>

<style scoped>
.user-management {
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 16px;
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
  margin-right: 300px;
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
</style>