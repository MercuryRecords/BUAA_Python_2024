<template>
  <div class="common-layout">
    <el-container>
      <el-header>
      </el-header>

      <el-container>
        <el-aside width="200px">
          <NavigatorM :username="$route.query.username"></NavigatorM>
        </el-aside>

        <el-container>
          <el-main class="shifted-content">
            <div class="sensitive-words-manager">
              <el-card class="box-card">
                <template #header>
                  <div class="card-header">
                    <span>敏感词管理</span>
                  </div>
                </template>

                <el-tabs type="border-card">
                  <el-tab-pane label="添加敏感词">
                    <el-input
                        v-model="wordsToAdd"
                        type="textarea"
                        :rows="5"
                        placeholder="请输入敏感词,每行一个"
                    />
                    <el-button type="primary" @click="addSensitiveWords" class="mt-3">添加敏感词</el-button>

                    <el-divider content-position="center">或</el-divider>

                    <el-upload
                        class="upload-demo"
                        action="#"
                        :on-change="handleFileUpload"
                        :auto-upload="false"
                        accept=".txt"
                    >
                      <template #trigger>
                        <el-button type="primary">选择文件</el-button>
                      </template>
                      <el-button class="ml-3" type="success" @click="addSensitiveWordsFromFile">
                        上传并添加
                      </el-button>
                    </el-upload>
                  </el-tab-pane>

                  <el-tab-pane label="管理敏感词">
                    <el-input
                        v-model="wordToDelete"
                        placeholder="请输入要删除的敏感词"
                        class="mb-3"
                    >
                      <template #append>
                        <el-button type="danger" @click="deleteSensitiveWord(wordToDelete)">删除敏感词</el-button>
                      </template>
                    </el-input>

                    <el-table :data="sensitiveWords" style="width: 100%" max-height="400">
                      <el-table-column prop="word" label="敏感词"/>
                      <el-table-column fixed="right" label="操作" width="120">
                        <template #default="scope">
                          <el-button
                              type="danger"
                              size="small"
                              @click="deleteSensitiveWord(scope.row.word)"
                          >
                            删除
                          </el-button>
                        </template>
                      </el-table-column>
                    </el-table>
                  </el-tab-pane>

                  <el-tab-pane label="清除所有敏感词">
                    <el-button type="danger" @click="clearAllSensitiveWords">清除所有敏感词</el-button>
                  </el-tab-pane>
                </el-tabs>
              </el-card>
            </div>
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {ElMessage, ElMessageBox, type UploadFile} from 'element-plus'
import axios from 'axios'
import API from "@/plugins/axios";
import {useRoute} from "vue-router";
import NavigatorM from "@/components/Base/NavigatorM.vue";

const route = useRoute()
const wordsToAdd = ref('')
const wordToDelete = ref('')
const message = ref('')
const dialogVisible = ref(false)
const file = ref<File | null | undefined>(null)
const sensitiveWords = ref([])

const fetchSensitiveWords = async () => {
  API.post('/admin_get_sensitive_word_list', {
    username: route.query.username,
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      function (response) {
        if (response.data.code === 200) {
          console.log(response.data.data);
          sensitiveWords.value = response.data.data.map((word:string) => ({word}))
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

onMounted(fetchSensitiveWords)

const addSensitiveWords = async () => {
  API.post('/admin_add_sensitive_words_by_list', {
    username: route.query.username,
    words: wordsToAdd.value.split('\n').filter(word => word.trim())
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      async function (response) {
        if (response.data.code === 200) {
          dialogVisible.value = true
          wordsToAdd.value = ''
          await fetchSensitiveWords()
          ElMessage.success(response.data.message);
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

const handleFileUpload = (uploadFile: UploadFile) => {
  if (uploadFile.raw) {
    file.value = uploadFile.raw
  } else {
    file.value = null
  }
}

const addSensitiveWordsFromFile = async () => {
  // TODO 修改bug
  if (!file.value) {
    ElMessage.warning('请选择文件')
    return
  }
  const formData = new FormData()
  formData.append('username', (route.query.username as string))
  formData.append('file', file.value)

  API.post('/admin_add_sensitive_words_by_txt_file', formData, {
    headers: {'Content-Type': 'multipart/form-data'}
  }).then(
      async function (response) {
        if (response.data.code === 200) {
          dialogVisible.value = true
          file.value = null
          await fetchSensitiveWords()
          ElMessage.success(response.data.message);
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

const deleteSensitiveWord = async (word = wordToDelete.value) => {
  await ElMessageBox.confirm('确定要删除这个关键词吗？', '警告', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  });
  API.post('/admin_delete_sensitive_word', {
    username: route.query.username,
    word: word
  }, {
    headers: {'Content-Type': 'application/x-www-form-urlencoded'}
  }).then(
      async function (response) {
        if (response.data.code === 200) {
          dialogVisible.value = true
          wordToDelete.value = ''
          await fetchSensitiveWords()
          ElMessage.success(response.data.message);
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

const clearAllSensitiveWords = async () => {
  try {
    await ElMessageBox.confirm('确定要清除所有敏感词吗？', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    API.post('/admin_clear_sensitive_word', {
      username: route.query.username,
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    }).then(
        async function (response) {
          if (response.data.code === 200) {
            dialogVisible.value = true
            wordToDelete.value = ''
            await fetchSensitiveWords()
            ElMessage.success(response.data.message);
          } else {
            ElMessage.error(response.data.message);
          }
        }
    ).catch(
        function () {
          console.log('error submit!')
        }
    )
  } catch (error) {

  }
}
</script>

<style scoped>
.sensitive-words-manager {
  max-width: 800px;
  margin: 20px auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.mt-3 {
  margin-top: 12px;
}

.mb-3 {
  margin-bottom: 12px;
}

.ml-3 {
  margin-left: 12px;
}
</style>