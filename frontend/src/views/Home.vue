<template>
  <div class="loginContainer">
    <el-button plain type="text" style="position:absolute;left:20px;top:20px;font-size:18px;"
               @click="back">返回
    </el-button>
    <div class="box">
      <div class="itemBox">
        <div style="display:flex;flex-direction:row;justify-content:space-between;">
          <el-upload class="upload-demo" ref="upload" accept=".png,.jpeg,.gif,.jpg"
                     action="https://run.mocky.io/v3/9d059bf9-4660-45f2-925d-ce80ad6c4d15" :on-change="uploadImg"
                     :show-file-list="false" :auto-upload="false">
            <el-button slot="trigger">上传图片</el-button>
          </el-upload>
          <el-select v-model="langChosed" placeholder="请选择识别语言" style="min-width:100px;margin-left:20px;">
            <el-option v-for="item in langSelect" :key="item.val" :label="item.name" :value="item.val"/>
          </el-select>
          <el-button plain type="text" @click="defaultUSe" style="margin-left:20px;">使用默认图片</el-button>
        </div>
      </div>
      <div class="itemBox">
        <div style="with:120px;text-align:left;">图片：</div>
        <el-image v-if="urlStr" :src="urlStr" style="width:800px;"></el-image>
      </div>
      <div class="itemBox">
        <div style="width:120px;text-align:left;">识别结果：</div>
        <div class="resultBox">
          <pre v-html="ocrStr" class="resultsItem"></pre>
        </div>
      </div>
    </div>

  </div>
</template>
<!-- ocr文字识别 https://github.com/naptha/tesseract.js -->
<script lang="ts" setup>
import {ref} from 'vue'
import Tesseract from 'tesseract.js'
import testocr from '@/assets/img.png'


const ocrStr = ref('')
const urlStr = ref('')
const langChosed = ref('chi_sim')
const langSelect = ref([{
  name: '中文（简体）',
  val: 'chi_sim'
},
  {
    name: '俄文',
    val: 'rus'
  },
  {
    name: '英文',
    val: 'eng'
  },
  {
    name: '日文',
    val: 'jpn'
  }])


const uploadImg = (file: any) => {
  console.log(file)
  // 参数： 第一个参数：图像，第二个：语种
  urlStr.value = file.raw ? URL.createObjectURL(file.raw) : testocr
  console.log(Tesseract)
  Tesseract.recognize(
      urlStr.value,
      langChosed.value,
      {logger: m => console.log(m)}
  ).then((d: any) => {
    console.log(d);

    ocrStr.value = d.data.text
  }).catch((err: any) => {
    console.log(err);
  })
}

const defaultUSe = () => {
  uploadImg(testocr)
}

const back = () => {
  window.history.back()
}
</script>
<style lang="scss" scoped>
.loginContainer {
  height: 100vh;
  width: 100vw;
  padding: 60px;
  margin-bottom: 10px;
  cursor: pointer;
}

.box {
  margin-top: 30px;

}

.itemBox {
  display: flex;
  flex-direction: row;
  margin: 20px auto;
}

.resultsBox {
  width: 800px;
}

.resultsItem {
  text-align: left;
  white-space: pre-wrap;
  line-height: 30px;
}

.resultBox {
  width: 800px;
}
</style>




