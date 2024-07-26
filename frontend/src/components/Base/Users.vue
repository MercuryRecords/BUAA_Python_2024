<template>
  <div class="user-management">
    <div class="table-container">
      <el-table :data="users" style="width: 90%">
        <el-table-column label="序号" width="80">
          <template #default="scope">
            {{ (currentPage - 1) * 10 + scope.$index + 1 }}
          </template>
        </el-table-column>
        <el-table-column prop="username" label="用户名" width="180" />
        <el-table-column label="详细信息" width="140">
          <template #default="scope">
            <el-button type="primary" @click="showUserDetails(scope.row)">
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
        :page-size="10"
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
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import API from "@/plugins/axios"

interface User {
  username: string;
  password: string;
  groups: string[];
}

const users = ref<User[]>([])
const currentPage = ref(1)
const totalUsers = ref(0)
const userDetailsVisible = ref(false)
const selectedUser = ref<User>({} as User)

const fetchUsers = async () => {
  try {
    const response = await API.post('/admin_get_user_list', {
      username: 'Admin', // 这里应该使用实际的管理员用户名
      page: currentPage.value
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })

    if (response.data.code === 200) {
      users.value = response.data.data
      totalUsers.value = response.data.data.length // 假设后端返回了总用户数
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
  try {
    // 这里应该发送删除用户的请求到后端
    // 现在我们只是从本地数组中删除
    users.value = users.value.filter(user => user.username !== username)
    ElMessage.success('用户删除成功')
  } catch (error) {
    console.error('Error deleting user:', error)
    ElMessage.error('删除用户失败')
  }
}

const handlePageChange = (page: number) => {
  currentPage.value = page
  fetchUsers()
}

onMounted(fetchUsers)
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
  width: 100%;
  display: flex;
  justify-content: center;
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
</style>