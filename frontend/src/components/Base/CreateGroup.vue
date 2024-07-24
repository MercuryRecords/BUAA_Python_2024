<script lang="ts" setup>
import {ref, reactive, onMounted, computed, type ComputedRef, toRef, watch, type Ref} from 'vue';
import {
  ElButton,
  ElDialog,
  ElForm,
  ElFormItem,
  ElInput,
  ElMessage,
  type FormInstance,
  type FormRules
} from 'element-plus';
  import 'element-plus/dist/index.css';
  import API from '@/plugins/axios';
  import Navigator from "@/components/Base/Navigator.vue";
import {all} from "axios";

  const data = defineProps(['username']) //从Navigator拿到的username
  const dialogVisible = ref(false);
  const form = reactive({
    name: '',
    description: ''
  });
  let editVisible = ref(false);
  let deleteVisible = ref(false);
  let centerDialogVisible = ref(false)
  let edit_loading = true
  let currentGroupName = '' // 用于在编辑时记录当前点击了哪一个群组的编辑键
  let currentDescription = ref('')

  interface Group {
    id: number
    name: string
    description: string
    created_by_id: number
    created_at: string
  }

  interface Member {
    username: string
  }

  interface GroupMembersDict {
    [group_name: string]: Member[];
  }

  // let tableData: Group[] = []
  const tableData: Group[] = reactive([]) //存储这个人所在的组
  let membersInGroup: Member[] = reactive([]) // 待定
  let allGroupMembers: Ref<GroupMembersDict> = ref({})
  const filterTableData = computed(() =>
      tableData.filter(
          (data) =>
              !search.value ||
              data.name.toLowerCase().includes(search.value.toLowerCase())
      )
  )
  let search = ref('')

  // 必须输入群名称
  const ruleFormRef = ref<FormInstance>()
  const validateName = (rule: any, value: any, callback: any) => {
    console.log("value:",value)
    if (value === '') {
      callback(new Error('Please input the name'))
    } else {
      callback()
    }
  }
  const rules = reactive<FormRules<typeof form>>({
    name: [{validator: validateName, trigger: 'blur'}]
  })


  onMounted(async()=>showData());

    function showData() {
      console.log("showing data");
      console.log(data.username)
      API.post('/group_get_groups',
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
                if (response.data.groups[i].creator == data.username) {
                  tableData.push(response.data.groups[i]) //将群组加入tableData，准备在挂载的时候显示出来
                }
              }
              console.log(response.data.groups[0])
              getGroupMembers();
            } else { // 接收失败
              ElMessage.error(response.data.message);
            }
          }
      ).catch(
          function () {
            console.log('error submit!')
          })
    }

    const handleSubmit = (formEl: FormInstance | undefined) => {
      if (!formEl) return;
      formEl.validate((valid) => {
        if (valid) {
          dialogVisible.value = false;
          // console.log(data.username)
          // console.log(form.name)
          // console.log(form.description)
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
                  showData();
                  window.location.reload();
                } else {
                  ElMessage.error(response.data.message);
                }
              }
          ).catch(
              function () {
                console.log('error submit!')
              })
        }
        else {
          console.log("submit error")
        }
      })
    }

  function handleClick() {
    dialogVisible.value = true;
  }

  function handleClose() {
    dialogVisible.value = false;
  }


  function handleEdit(row:Group) {
    currentGroupName = row.name;
    editVisible.value = true;
  }

  function handleDelete(row: Group) {
    deleteVisible.value = true;
    API.post('/group_delete_all', {
      group_name: row.name,
      username: data.username
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(
        function (response) {
          if (response.data.code === 200) {
            ElMessage.success(response.data.message); //成功删除
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

  const saveChanges = () => {
    // 这里添加保存更改的逻辑
    console.log('保存的数据：', tableData)
    // ElMessage.success('保存成功')
    editVisible.value = false;
  }

  function handleDeleteMember(row: Member) {
    console.log("Here we are going to delete a member from the group");
    API.post('/group_delete_member', {
      to_deleter: row.username,
      group_name: currentGroupName,
      username: data.username
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    }).then(
        function (response) {
          if (response.data.code === 200) {
            // TODO 能不能窗口停留一会再刷新？
            editVisible.value = false;
            window.location.reload();
            showData();
            ElMessage.success(response.data.message);
          } else {
            ElMessage.error(response.data.message);
          }
        }
    ).catch(
        function () {
          console.log('error delete!')
        })

  }

  function getGroupMembers() {
      for (let i = 0; i < tableData.length; i++) {
        const group_name = tableData[i].name;
        API.post('/group_get_members', {
          group_name: group_name,
          username: data.username
        }, {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }).then(
            function (response) {
              if (response.data.code === 200) {
                const members: Member[] = []
                // 成功拿到对应组的成员名单
                for (let i = 0; i < response.data.members.length; i++) {
                  members.push({username: response.data.members[i]});
                }
                allGroupMembers.value[group_name] = members;
                // allGroupMembers.value.push({group_name: members});
                console.log(66666, allGroupMembers)
              } else {
                ElMessage.error(response.data.message);
              }
              // window.location.reload(); // 在点击确定之后刷新页面，更新所加入的群组，即重新挂载一下
              // showData();
            }
        ).catch(
            function () {
              console.log('error delete!')
            }).finally(()=>{
          console.log("不是哥们！！！！！！！！！！！！！")
          console.log(membersInGroup)
          edit_loading = false;
        })
      }
  }

  const fetchData = async () => {
      getGroupMembers();
  }

  watch(editVisible,(newValue) => {
    if (newValue) {
      fetchData();
    }
  })

  const getMember = (groupName: string): Member[] => {
    return allGroupMembers.value[groupName] || []
  }

  function isCreator(name: string) {
      return name == data.username
  }

  function openDescriptionDialog(group_name:string) {
    console.log("我到底打没打开啊！")
    centerDialogVisible = true;
    currentDescription.value = tableData.find(group => group.name === group_name).description;
  }

</script>



<template>

  <div>
    <el-button type="primary" @click="handleClick">新建群组</el-button>

    <el-dialog title="新建" v-model="dialogVisible" width="30%">
      <el-form :model="form" label-width="80px" :rules="rules" ref="ruleFormRef">

        <el-form-item label="群组名称">
          <el-input v-model="form.name" autocomplete="off" clearable/>
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
        <el-button type="primary" @click="handleSubmit(ruleFormRef)">确 定</el-button>
      </span>
    </el-dialog>
  </div>

  <!--  展示所有的群组-->
  <div>
    <el-table :data="filterTableData" style="width: 100%">
      <el-table-column label="群组名称" prop="name" />
      <el-table-column label="创建者" prop="creator" />
      <el-table-column label="人数" prop="number" />
      <el-table-column label="详情">

        <template #default="scope">
          <div>
            <el-button size="large" @click="openDescriptionDialog(scope.row.name)">
              详情
            </el-button>

          <el-dialog
              v-model="centerDialogVisible"
              width="50%"
          >
            <span>群组描述：{{ currentDescription }}</span>
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
          </template>

      </el-table-column>
      <el-table-column align="center">
        <template #header>
          <el-input v-model="search" size="large" placeholder="Type to search" clearable/>
        </template>
        <template #default="scope">
          <div style="all: unset">
            <el-button size="large" @click="handleEdit(scope.row)" style="margin-right: 10px">
              管理群组
            </el-button>

            <!--    编辑对话框弹出      -->

            <el-dialog
                v-model="editVisible"
                title="编辑信息"
                width="50%"
                style=""
            >
              <el-table :data="getMember(currentGroupName)">
                <el-table-column prop="username" label="名称"></el-table-column>
                <el-table-column label="操作">
                  <template #default="scope">
                    <el-button
                        size="large"
                        type="danger"
                        @click="handleDeleteMember(scope.row)"
                        :disabled="isCreator(scope.row.username)"
                    >踢出群组</el-button>
                  </template>
                </el-table-column>
              </el-table>

              <template #footer>
        <span class="dialog-footer">
          <el-button @click="editVisible = false">取消</el-button>
          <el-button type="primary" @click="saveChanges">
            确定
          </el-button>
        </span>
              </template>
            </el-dialog>

            <!--          -->

          </div>


          <el-button
              size="large"
              type="danger"
              @click="handleDelete(scope.row)"
          >
            删除群组
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>


</template>


