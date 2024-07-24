<template>
  <div class="upload-problem-container">
    <div class="upload-problem">
      <el-form :model="problemForm" label-width="120px">
        <el-form-item label="题目名称">
          <el-input
              type="textarea"
              v-model="problemForm.title"
              :rows="1"
              placeholder="请输入题目名称"
          ></el-input>
        </el-form-item>
        <el-form-item label="题目类型">
          <el-select v-model="problemForm.type" placeholder="请选择题目类型">
            <el-option label="填空题" value="fill"></el-option>
            <el-option label="选择题" value="choice"></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="题目内容">
          <el-input
              type="textarea"
              v-model="problemForm.content"
              :rows="6"
              placeholder="请输入题目内容"
          ></el-input>
          <el-upload
              class="upload-demo"
              action="#"
              :http-request="customUpload"
              :show-file-list="false"
          >
            <el-button type="primary">上传题目文件</el-button>
            <template #tip>
              <div class="el-upload__tip">
                支持jpg/png/pdf文件，大小不超过5MB
              </div>
            </template>
          </el-upload>
        </el-form-item>

        <el-form-item label="答案数量">
          <div class="answer-count-controls">
            <el-button @click="decreaseAnswerCount" :disabled="problemForm.answers.length <= 1">-</el-button>
            <span>{{ problemForm.answers.length }}</span>
            <el-button @click="increaseAnswerCount" :disabled="problemForm.answers.length >= 7">+</el-button>
          </div>
        </el-form-item>

        <el-form-item
            v-for="(answer, index) in problemForm.answers"
            :key="index"
            :label="`答案 ${index + 1}`"
        >
          <el-input v-model="problemForm.answers[index]"></el-input>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitProblem">提交题目</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive} from 'vue'
import {ElMessage} from 'element-plus'
import API from '@/plugins/axios'

const problemForm = reactive({
  title: '',
  type: '',
  content: '',
  answers: ['']
})
const data = defineProps(['username'])
const customUpload = async (options: any) => {
  const {file} = options
  const formData = new FormData()
  formData.append('username', data.username)
  formData.append('file', file)

  try {
    const response = await API.post('/ocr', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })
    console.log(response.data.code)
    // 假设后端返回的响应中包含识别后的文本在 response.data.text 中
    problemForm.content = response.data.text
    ElMessage.success('文件上传成功，题目内容已更新')
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('文件上传失败，请重试')
  }
}

const increaseAnswerCount = () => {
  if (problemForm.answers.length < 7) {
    problemForm.answers.push('')
  }
}

const decreaseAnswerCount = () => {
  if (problemForm.answers.length > 1) {
    problemForm.answers.pop()
  }
}

const submitProblem = () => {
  // 这里添加提交题目到后端的逻辑
  console.log('提交的题目数据:', problemForm)
  ElMessage.success('题目提交成功')
}
</script>

<style scoped>
.upload-problem-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
}

.upload-problem {
  width: 100%;
  max-width: 600px;
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.upload-demo {
  margin-top: 10px;
}

.answer-count-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.answer-count-controls span {
  font-size: 16px;
  font-weight: bold;
}
</style>