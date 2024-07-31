<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, type FormInstance } from 'element-plus'
import API from "@/plugins/axios"

const data = defineProps(['username'])

interface User {
  username: string;
  password: string;
  groups: string[];
}

const users = ref<User[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
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
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return users.value.slice(start, end)
})

const fetchUsers = async () => {
  try {
    const response = await API.post('/admin_get_user_list', {
      username: data.username,
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
    username: data.username,
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

const handleSizeChange = (val: number) => {
  pageSize.value = val
  currentPage.value = 1
}

const handleCurrentChange = (val: number) => {
  currentPage.value = val
}

const showAddUserDialog = () => {
  addUserDialogVisible.value = true
}

const addUser = async () => {
  if (!addUserForm.value) return
  addUserForm.value.validate((valid) => {
    if (valid) {
      API.post('/admin_register_user', {
        username: data.username,
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

<template>
  <div class="user-management">
    <el-card class="table-container">
      <template #header>
        <div class="table-header">
          <h2>用户管理</h2>
          <el-button type="primary" @click="showAddUserDialog" class="add-user-button">
            新增用户
          </el-button>
        </div>
      </template>

      <el-table :data="displayedUsers" style="width: 100%">
        <el-table-column label="序号" width="80" align="center">
          <template #default="scope">
            {{ (currentPage - 1) * pageSize + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" />
        <el-table-column label="操作" width="240" align="center">
          <template #default="scope">
            <el-button @click="showUserDetails(scope.row)">
              详细信息
            </el-button>
            <el-popconfirm
                title="确定要删除该用户吗？"
                @confirm="deleteUser(scope.row.username)"
            >
              <template #reference>
                <el-button type="danger">
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 30, 50]"
          :total="totalUsers"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          layout="total, sizes, jumper, ->, prev, pager, next"
          class="pagination"
      />
    </el-card>

    <el-dialog v-model="userDetailsVisible" title="用户详细信息" width="30%">
      <el-descriptions :column="1" border>
        <el-descriptions-item label="用户名">{{ selectedUser.username }}</el-descriptions-item>
        <el-descriptions-item label="密码">{{ selectedUser.password }}</el-descriptions-item>
        <el-descriptions-item label="所属群组">{{ selectedUser.groups?.join(', ') || '无' }}</el-descriptions-item>
      </el-descriptions>
    </el-dialog>

    <el-dialog v-model="addUserDialogVisible" title="新增用户" width="30%">
      <el-form :model="newUser" :rules="rules" ref="addUserForm" label-width="80px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="newUser.username"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="newUser.password" type="password" show-password></el-input>
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

<style scoped>
.user-management {
  display: flex;
  justify-content: center;
  padding: 20px;
  font-size: 16px;
  height: 100%;
  overflow: visible;
}

.table-container {
  width: 100%;
  max-width: 1200px;
  overflow-y: auto; /* 添加这一行 */
  max-height: calc(100vh - 120px); /* 添加这一行，根据实际情况调整 */
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

:deep(.el-card__header) {
  padding: 15px 20px;
}

:deep(.el-table) {
  margin-top: 20px;
  font-size: 16px;
}

:deep(.el-button) {
  font-size: 14px;
  padding: 10px 16px;
}

:deep(.el-dialog__body) {
  padding: 30px 20px;
  font-size: 16px;
}

:deep(.el-descriptions) {
  margin: 20px 0;
}

:deep(.el-descriptions__label) {
  font-weight: bold;
}

:deep(.el-pagination) {
  font-size: 14px;
}

.add-user-button {
  display: flex;
  align-items: center;
  justify-content: center;
}

:deep(.el-dialog__title) {
  font-size: 20px;
}

:deep(.el-form-item__label) {
  font-size: 16px;
}

:deep(.el-input__inner) {
  font-size: 16px;
}
</style>
