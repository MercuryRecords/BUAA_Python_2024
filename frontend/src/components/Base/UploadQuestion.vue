<template>
  <div class="upload-problem-container">
    <div class="left-panel">
      <div style="text-align: center;">
        <h2>OCR识别结果</h2>
      </div>
      <el-input
          type="textarea"
          v-model="ocrResult"
          :rows="32"
          placeholder="OCR识别结果将显示在这里，处理会有点慢，请耐心等候~"
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
    </div>
    <div class="right-panel">
      <div style="text-align: center;">
        <h2>题目信息</h2>
      </div>
      <el-form :model="problemForm" label-width="120px">
        <el-form-item label="题目名称">
          <el-input v-model="problemForm.title" placeholder="请输入题目名称"></el-input>
        </el-form-item>
        <el-form-item label="题目类型">
          <el-select v-model="problemForm.type" placeholder="请选择题目类型" @change="handleTypeChange">
            <el-option label="选择题" value="c"></el-option>
            <el-option label="填空题" value="b"></el-option>
          </el-select>
        </el-form-item>
        <el-form-item label="题目内容">
          <el-input type="textarea" v-model="problemForm.content" :rows="6" placeholder="请输入题目内容"></el-input>
        </el-form-item>
        <el-form-item v-if="problemForm.type === 'c'" label="正确答案">
          <el-input v-model="problemForm.answer" placeholder="请输入正确答案（如：A）"></el-input>
        </el-form-item>
        <el-form-item :label="problemForm.type === 'c' ? '选项数量' : '答案数量'">
          <div class="answer-count-controls">
            <el-button @click="decreaseAnswerCount" :disabled="problemForm.ans_count <= 1">-</el-button>
            <span>{{ problemForm.ans_count }}</span>
            <el-button @click="increaseAnswerCount" :disabled="problemForm.ans_count >= 7">+</el-button>
          </div>
        </el-form-item>
        <el-form-item
            v-for="(answer, index) in problemForm.answers"
            :key="index"
            :label="problemForm.type === 'c' ? `选项${String.fromCharCode(65 + index)}` : `答案 ${index + 1}`"
        >
          <el-input v-model="problemForm.answers[index]"></el-input>
        </el-form-item>
        <el-form-item label="题目标签">
          <div class="tags-container">
            <el-tag
                v-for="tag in problemForm.tags"
                :key="tag"
                closable
                @close="handleClose(tag)"
            >
              {{ tag }}
            </el-tag>
            <el-button class="button-new-tag" size="small" @click="showInput">
              + 新标签
            </el-button>
          </div>
        </el-form-item>
        <el-dialog v-model="inputVisible" title="添加新标签" width="30%">
          <el-input
              v-model="inputValue"
              ref="inputRef"
              placeholder="请输入标签名称"
          ></el-input>
          <template #footer>
            <span class="dialog-footer">
              <el-button @click="inputVisible = false">取消</el-button>
              <el-button type="primary" @click="handleInputConfirm">
                确定
              </el-button>
            </span>
          </template>
        </el-dialog>
        <el-form-item>
          <el-button type="primary" @click="submitProblem">提交题目</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive, nextTick} from 'vue'
import {ElMessage} from 'element-plus'
import API from '@/plugins/axios'

interface TreeNode {
  id: number
  label: string
  children?: TreeNode[]
  type: 'group' | 'problem'
}

const groupTree = ref<TreeNode[]>([])
const defaultProps = {
  children: 'children',
  label: 'label',
}

const problemForm = reactive({
  username: '',
  title: '',
  problem_group_id: 0,
  type: '',
  content: '',
  ans_count: 1,
  answer: '',
  field1: '',
  field2: '',
  field3: '',
  field4: '',
  field5: '',
  field6: '',
  field7: '',
  tags: [] as string[],
  answers: [''] // 用于显示多个答案输入框
})

const ocrResult = ref('')
const inputVisible = ref(false)
const inputValue = ref('')
const inputRef = ref<HTMLInputElement | null>(null)

const data = defineProps(['username', 'sheetId'])

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
    ocrResult.value = response.data.text
    ElMessage.success('文件上传成功，OCR识别结果已更新')
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('文件上传失败，请重试')
  }
}

const handleNodeClick = (data: TreeNode) => {
  if (data.type === 'group') {
    problemForm.problem_group_id = data.id
  }
}

const append = (data: TreeNode) => {
  const newChild: TreeNode = {id: Date.now(), label: 'new node', type: 'group'}
  if (!data.children) {
    data.children = []
  }
  data.children.push(newChild)
}

const handleClose = (tag: string) => {
  problemForm.tags = problemForm.tags.filter((t) => t !== tag)
}

const showInput = () => {
  inputVisible.value = true
  nextTick(() => {
    if (inputRef.value) {
      inputRef.value.focus()
    }
  })
}

const handleInputConfirm = () => {
  if (inputValue.value) {
    problemForm.tags.push(inputValue.value)
  }
  inputVisible.value = false
  inputValue.value = ''
}

const handleTypeChange = () => {
  // 重置答案相关字段
  problemForm.ans_count = 1
  problemForm.answer = ''
  problemForm.answers = ['']
}

const increaseAnswerCount = () => {
  if (problemForm.ans_count < 7) {
    problemForm.ans_count++
    problemForm.answers.push('')
  }
}

const decreaseAnswerCount = () => {
  if (problemForm.ans_count > 1) {
    problemForm.ans_count--
    problemForm.answers.pop()
  }
}

const submitProblem = () => {
  // 准备提交数据
  console.log(data.username)
  const submitData: Record<string, any> = {
    username: data.username,
    title: problemForm.title,
    problem_group_id: data.sheetId,
    type: problemForm.type,
    content: problemForm.content,
    ans_count: problemForm.ans_count,
    answer: problemForm.answer,
    field1: problemForm.field1,
    field2: problemForm.field2,
    field3: problemForm.field3,
    field4: problemForm.field4,
    field5: problemForm.field5,
    field6: problemForm.field6,
    field7: problemForm.field7,
    tags: problemForm.tags
  }

  // 根据ans_count设置答案
  for (let i = 0; i < problemForm.ans_count; i++) {
    submitData[`field${i + 1}`] = problemForm.answers[i]
  }

  // 发送请求到后端
  API.post('/api/problem_create', submitData)
      .then(response => {
        if (response.data.code === 200) {
          console.log('提交成功:', response.data)
          ElMessage.success('题目提交成功')
        } else {
          console.log('提交失败:',response.data)
          ElMessage.error('题目提交失败')
        }
      })
      .catch(error => {
        console.error('提交失败:', error)
        ElMessage.error('题目提交失败，请重试')
      })
}

// 初始化函数，用于获取题目组树
const initGroupTree = () => {
  API.get('/api/problem_groups')
      .then(response => {
        groupTree.value = response.data
      })
      .catch(error => {
        console.error('获取题目组失败:', error)
        ElMessage.error('获取题目组失败，请刷新页面重试')
      })
}

// 在组件挂载时调用初始化函数
initGroupTree()
</script>

<style scoped>
.upload-problem-container {
  display: flex;
  height: 100vh;
}

.left-panel {
  width: 300px;
  padding: 0 20px 0 20px;
  border-right: 1px solid #dcdfe6;
}

.right-panel {
  flex: 1;
  padding: 20px;
}

.custom-tree-node {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}

.answer-count-controls {
  display: flex;
  align-items: center;
}

.answer-count-controls span {
  margin: 0 10px;
}

.el-tag {
  margin-right: 10px;
  margin-bottom: 10px;
}

.button-new-tag {
  margin-bottom: 10px;
}

.input-new-tag {
  width: 90px;
  margin-bottom: 10px;
  vertical-align: bottom;
}
</style>