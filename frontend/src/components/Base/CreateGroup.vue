<script lang="ts" setup>
import {ref, reactive, onMounted, computed} from 'vue';
import {ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElMessage} from 'element-plus';
import 'element-plus/dist/index.css';
import API from '@/plugins/axios';

const data = defineProps(['username']) //从Navigator拿到的username
const dialogVisible = ref(false);
const form = reactive({
  name: '',
  description: ''
});
let editVisible = ref(false);
let deleteVisible = ref(false);
let centerDialogVisible = ref(false)

interface Group {
  name: string
  creator: string
  number: number
}

const tableData: Group[] = reactive([])
const search = ref('')
const searchData: Group[] = reactive([])
onMounted(async () => showData());

function showData() {
  console.log("showing data");
  console.log(data.username)
  API.post('/group_get_groups_created',
      {
        username: data.username,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
      function (response) {
        if (response.data.code === 200) { // 成功接收
          for (let i = 0; i < response.data.groups.length; i++) {
            tableData.push(response.data.groups[i]) //将群组加入tableData，准备在挂载的时候显示出来
          }
        } else if (response.data.code === 401) { // 用户不存在的情况，才会报错
          ElMessage.error("CG showData " + response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      })
}

function handleSubmit() {
  dialogVisible.value = false;
  API.post('/group_create',
      {
        username: data.username,
        group_name: form.name,
        group_description: form.description,
      }, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      }).then(
      function (response) {
        if (response.data.code === 200) {
          ElMessage.success(response.data.message);
        } else {
          ElMessage.error("CG handleSubmit" + response.data.message);
        }
        window.location.reload(); // 在点击确定之后刷新页面，更新所创建的群组
        showData();
      }
  ).catch(
      function () {
        console.log('error submit!')
      })
}

function handleClick() {
  dialogVisible.value = true;
}

function handleClose() {
  dialogVisible.value = false;
}


function handleEdit() {
  editVisible.value = true;
}

function handleDelete(row: Group) {
  deleteVisible.value = true;
  API.post('/group_delete_all', {
    username: data.username,
    group_name: row.name,
  }, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          ElMessage.success(response.data.message); //成功退出
        } else {
          ElMessage.error(response.data.message);
        }
        window.location.reload(); // 在点击确定之后刷新页面，更新所加入的群组，即重新挂载一下
        showData();
      }
  ).catch(
      function () {
        console.log('error delete!')
      })
}
</script>


<template>

  <div>
    <el-button type="primary" @click="handleClick">新建群组</el-button>

    <el-dialog title="新建" v-model="dialogVisible" width="30%">
      <el-form :model="form" label-width="80px">

        <el-form-item label="群组名称">
          <el-input v-model="form.name" autocomplete="off"/>
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
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
        <el-button @click="handleClose">取 消</el-button>
      </span>
    </el-dialog>
  </div>

  <!--  展示所有的群组-->
  <div>
    <el-table :data="search.length===0?tableData:searchData" style="width: 100%">
      <el-table-column label="群组名称" prop="name"/>
      <el-table-column label="创建者" prop="creator"/>
      <el-table-column label="人数" prop="number"/>
      <el-table-column label="详情">

        <div> <!--对话框-->
          <el-button size="large" @click="centerDialogVisible = true">
            Click to open the Dialog
          </el-button>

          <el-dialog
              v-model="centerDialogVisible"

              width="500"
              align-center
          >
            <span>Open the dialog from the center from the screen</span>
            <template #footer>
              <div class="dialog-footer">
                <el-button @click="centerDialogVisible = false">Cancel</el-button>
                <el-button type="primary" @click="centerDialogVisible = false">
                  Confirm
                </el-button>
              </div>
            </template>
          </el-dialog>
        </div>

      </el-table-column>
      <el-table-column align="center">
<!--        <template #header>-->
<!--          <el-input v-model="search" @keyup.enter="handleSearch" size="large" placeholder="输入完毕请按回车！"/>-->
<!--        </template>-->
        <template #default="scope">
          <el-button size="large" @click="handleEdit()">
            Edit
          </el-button>
          <el-button
              size="large"
              type="danger"
              @click="handleDelete(scope.row)"
          >
            Delete
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>


</template>


