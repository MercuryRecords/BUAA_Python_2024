<template>
  <div class="comment-section">
    <h3>讨论区</h3>

    <!-- 评论列表 -->
    <div v-if="comments.length > 0" class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-header">
          <span class="username">{{ comment.username }}</span>
          <span class="timestamp">{{ formatDate(comment.timestamp) }}</span>
        </div>
        <div class="comment-content">{{ comment.content }}</div>
      </div>
    </div>
    <div v-else>暂无评论</div>

    <!-- 添加评论表单 -->
    <div class="add-comment">
      <el-input
          v-model="newComment"
          type="textarea"
          :rows="3"
          placeholder="请输入您的评论"
      />
      <el-button @click="submitComment" type="primary">发表评论</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import API from "@/plugins/axios";

const props = defineProps({
  questionId: {
    type: Number,
    required: true
  },
  username: {
    type: String,
    required: true
  }
});

const comments = ref([]);
const newComment = ref('');

const getComments = async () => {
  try {
    const response = await API.get(`/comments/${props.questionId}`);
    comments.value = response.data.comments;
  } catch (error) {
    ElMessage.error('获取评论失败');
  }
};

const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('评论内容不能为空');
    return;
  }

  try {
    await API.post('/comments', {
      questionId: props.questionId,
      username: props.username,
      content: newComment.value
    });
    ElMessage.success('评论发表成功');
    newComment.value = '';
    await getComments(); // 重新加载评论
  } catch (error) {
    ElMessage.error('评论发表失败');
  }
};

const formatDate = (timestamp) => {
  // 实现日期格式化逻辑
  return new Date(timestamp).toLocaleString();
};

onMounted(() => {
  console.log("I'm Done")
  getComments();
});
</script>

<style scoped>
.comment-section {

}

.comment-list {
  margin-bottom: 20px;
}

.comment {
  background-color: #ffffff;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 4px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.comment-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
}

.username {
  font-weight: bold;
  color: #333;
}

.timestamp {
  color: #888;
}

.comment-content {
  font-size: 16px;
}

.add-comment {
  margin-top: 20px;
}

.add-comment .el-button {
  margin-top: 10px;
}

.result-and-comments {
  display: flex;
  gap: 20px;
  margin-top: 30px;
}

.result-container {
  flex: 1;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
}

.comments-container {
  flex: 1;
  background-color: #f5f5f5;
  border-radius: 8px;
  padding: 20px;
}

.progress-bar {
  background-color: #e0e0e0;
  border-radius: 5px;
  height: 10px;
  margin: 10px 0;
}

.progress {
  background-color: #1890ff;
  height: 100%;
  border-radius: 5px;
}

h3 {
  margin-bottom: 10px;
}

</style>