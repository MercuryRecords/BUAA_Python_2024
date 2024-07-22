<script lang="ts" setup>
import {ref, reactive, onMounted} from 'vue';
import {ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElMessage} from 'element-plus';
import 'element-plus/dist/index.css';
import API from '@/plugins/axios';
import Navigator from "@/components/Base/Navigator.vue";

const data = defineProps(['username']) //从Navigator拿到的username
const dialogVisible = ref(false);
const form = reactive({
  name: '',
  description: ''
});

function handleSubmit() {
  dialogVisible.value = false;
  console.log(data.username)
  console.log(form.name)
  console.log(form.description)
  // TODO 向后端发送对应的信息
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
          ElMessage.error(response.data.message);
        }
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
          <Navigator></Navigator> <!--挂上导航栏，点击即可跳转,现在的位置是home/username=?-->
        </el-aside>

        <el-container>
          <el-main>
            <!--              主体内容-->
            <RouterView></RouterView>
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
        <el-button @click="handleClose">取 消</el-button>
        <el-button type="primary" @click="handleSubmit">确 定</el-button>
      </span>
              </el-dialog>
            </div>
          </el-main>
        </el-container>
      </el-container>

    </el-container>
  </div>


</template>

<style>
.el-menu {
  border-right: none;
}

.el-main {
  padding: 0;
}

.toolbar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  right: 20px;
}
</style>
