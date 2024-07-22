<template>

  <div>
    <el-button type="primary" @click="handleClick">新建群组</el-button>

    <el-dialog title="新建" v-model="dialogVisible" width="30%">
      <el-form ref="form" :model="form" label-width="80px">
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



</template>

<script>
import { ref, reactive } from 'vue';
import 'element-plus/dist/index.css';
import { ElButton, ElDialog, ElForm, ElFormItem, ElInput, ElMessage } from 'element-plus';

export default {
  data() {
    return {
      dialogVisible: false,
      form: {
        name: '',
        description: ''
      }

    }
  },
  methods: {
    handleSubmit() {
      ElMessage({
        type: 'success',
        message: `群组名称: ${this.form.name} 已创建`,
      });
      this.dialogVisible = false;
      console.log(this.form);
      this.form.name = '';
      this.form.description = '';

      // TODO 向后端发送对应的信息

    },
    handleClick() {
      this.dialogVisible = true;
    },
    handleClose() {
      this.dialogVisible = false;
    }
  }
}
</script>
