<template>
  <div>
    <input type="file" @change="handleFileUpload" accept=".pdf"/>
    <button @click="uploadFile" :disabled="!file">上传PDF文件</button>
    <p v-if="uploadStatus">{{ uploadStatus }}</p>
    <p v-if="extractedText">提取的文本：{{ extractedText }}</p>
  </div>
</template>

<script lang="js" setup>
import {ref} from 'vue'
import API from '@/plugins/axios.ts'

const file = ref(null)
const uploadStatus = ref('')
const extractedText = ref('')

const handleFileUpload = (event) => {
  file.value = event.target.files[0]
  uploadStatus.value = ''
  extractedText.value = ''
}

const uploadFile = async () => {
  if (!file.value) {
    uploadStatus.value = '请先选择PDF文件'
    return
  }

  const formData = new FormData()
  formData.append('file', file.value)

  try {
    console.log(formData)
    uploadStatus.value = '正在上传并处理PDF...'
    const response = await API.post('/pdf/text', formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      }
    })

    if (response.data.code === 200) {
      uploadStatus.value = 'PDF处理成功'
      extractedText.value = response.data.text
    } else {
      uploadStatus.value = '处理失败：服务器返回了非预期的响应'
    }
  } catch (error) {
    console.error('PDF处理失败', error)
    uploadStatus.value = `处理失败: ${error.response?.data?.message || error.message}`
  }
}
</script>