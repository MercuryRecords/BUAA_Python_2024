<template>
  <div class="upload-problem-container">
    <div class="panels-container">
      <div class="panel left-panel">
        <div class="panel-header">
          <h2>OCR识别结果</h2>
        </div>
        <el-input
            type="textarea"
            v-model="ocrResult"
            :rows="32"
            class="ocr-textarea"
            placeholder="OCR识别结果将显示在这里，处理会有点慢，请耐心等候~"
        ></el-input>
        <div class="upload-button-container">
          <el-upload
              class="upload-demo"
              action="#"
              :http-request="customUpload"
              :show-file-list="false"
          >
            <el-button type="primary">上传题目文件</el-button>
          </el-upload>
        </div>
        <div class="el-upload__tip">
          支持jpg/png/pdf文件，大小不超过5MB
        </div>
      </div>
      <div class="panel right-panel">
        <div class="panel-header">
          <h2>题目信息</h2>
        </div>
        <el-form :model="problemForm" label-position="left" label-width="120px">
          <el-form-item label="题目名称">
            <el-input v-model="problemForm.title" placeholder="请输入题目名称"></el-input>
          </el-form-item>
          <el-form-item label="题目类型">
            <el-select v-model="problemForm.type" placeholder="请选择题目类型" @change="handleTypeChange">
              <el-option label="选择题" value="c"></el-option>
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
              v-for="(_, index) in problemForm.answers"
              :key="index"
              :label="`选项${String.fromCharCode(65 + index)}`"
          >
            <el-input v-model="problemForm[`field${index + 1}`]"></el-input>
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
              <el-button class="button-new-tag" size="small" @click="getRecommendedTags" type="danger">
                推荐标签
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
                <el-button type="primary" @click="handleInputConfirm">
                  确定
                </el-button>
                <el-button @click="inputVisible = false">取消</el-button>
              </span>
            </template>
          </el-dialog>
          <el-form-item>
            <div class="submit-buttons">
              <el-button type="primary" @click="submitProblem">提交题目(结束本次上传并返回题单界面)</el-button>
              <el-button type="success" @click="submitAndContinue">提交并继续(继续上传，不会返回)</el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import {ref, reactive, nextTick, watch} from 'vue'
import {ElMessage} from 'element-plus'
import API from '@/plugins/axios'
import router from "@/router";

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
const questions = ref([])
const currentQuestionIndex = ref(0)
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
    console.log(response.data)
    ocrResult.value = response.data.text
    questions.value = response.data.questions || []
    if (questions.value.length > 0) {
      fillProblemForm(questions.value[0])
    }
    ElMessage.success('文件上传成功，OCR识别结果已更新')
  } catch (error) {
    console.error('上传失败:', error)
    ElMessage.error('文件上传失败，请重试')
  }
}

const fillProblemForm = (question: any) => {
  problemForm.tags.length = 0
  problemForm.content = question.content
  problemForm.ans_count = question.choices.length
  problemForm.answers = question.choices.map((choice: string) => {
    const parts = choice.split(' ')
    return parts.slice(1).join(' ') // 去掉选项标识符（如 "A)"），只保留内容
  })
  problemForm.type = 'c' // 假设所有题目都是选择题
  // 填充选项 A, B, C, D
  const optionLabels = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
  question.choices.forEach((choice: string, index: number) => {
    const fieldName = `field${index + 1}` as keyof typeof problemForm
    problemForm[fieldName] = choice
    console.log(fieldName)
    console.log(problemForm[fieldName])
  })
}

const submitAndContinue = () => {
  submitProblem(false)
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

const submitProblem = (shouldReturn = true) => {
  // 准备提交数据

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
  // for (let i = 0; i < problemForm.ans_count; i++) {
  //   submitData[`field${i + 1}`] = problemForm.answers[i]
  // }
  console.log(submitData)
  // 发送请求到后端
  API.post('/problem_create', submitData,
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded'
        }
      })
      .then(response => {
        if (response.data.code === 200) {
          console.log('提交成功:', response.data)
          ElMessage.success('题目提交成功')
          if (shouldReturn) {
            setTimeout(() => {
              router.back()
            }, 1000)
          } else {
            currentQuestionIndex.value++
            if (currentQuestionIndex.value < questions.value.length) {
              fillProblemForm(questions.value[currentQuestionIndex.value])
            } else {
              ElMessage.info('所有题目已提交完毕')
            }
          }
        } else {
          console.log('提交失败:', response.data)
          ElMessage.error('题目提交失败')
        }
      })
      .catch(error => {
        console.error('提交失败:', error)
        ElMessage.error('题目提交失败，请重试')
      })
}

const getRecommendedTags = async () => {
  try {
    console.log(data.username)
    console.log(problemForm.content)
    const response = await API.post('/extract_keywords', {
      username: data.username,
      text: problemForm.content
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });

    if (response.data.code === 200) {
      const recommendedTags = response.data.keywords;
      // 将推荐的标签添加到现有标签中，避免重复
      recommendedTags.forEach(tag => {
        if (!problemForm.tags.includes(tag)) {
          problemForm.tags.push(tag);
        }
      });
      ElMessage.success('已添加推荐标签');
    } else {
      ElMessage.warning('获取推荐标签失败');
    }
  } catch (error) {
    console.error('获取推荐标签出错:', error);
    ElMessage.error('获取推荐标签失败，请重试');
  }
}

// 监听 ocrResult 的变化
watch(ocrResult, (newValue) => {
  if (newValue && questions.value.length > 0) {
    fillProblemForm(questions.value[0])
  }
})
</script>

<style scoped>
.upload-problem-container {
  display: flex;
  height: calc(100vh - 60px); /* 减少高度以消除滚动条 */
  padding: 20px;
  align-items: flex-start;
  overflow: hidden; /* 防止出现滚动条 */
}

.panels-container {
  display: flex;
  width: 100%;
  height: 100%;
}

.panel {
  display: flex;
  flex-direction: column;
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  padding: 20px;
}

.left-panel {
  flex: 1;
  margin-right: 10px;
}

.right-panel {
  flex: 2;
  margin-left: 10px;
  overflow-y: auto;
}

.panel-header {
  text-align: center;
  margin-bottom: 20px;
}

.upload-button-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

.el-upload__tip {
  text-align: center;
  margin-top: 10px;
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

.submit-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

/* 移除右侧面板的滚动条 */
.right-panel::-webkit-scrollbar {
  display: none;
}

.right-panel {
  -ms-overflow-style: none;
  scrollbar-width: none;
}

:deep(.ocr-textarea .el-textarea__inner) {
  height: calc(100vh - 300px);
  max-height: none;
}
</style>