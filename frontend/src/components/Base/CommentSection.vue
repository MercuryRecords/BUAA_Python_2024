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

        <!-- 回复按钮 -->
        <el-button @click="showReplyForm(comment.id)" size="small">回复</el-button>

        <!-- 回复表单 -->
        <div v-if="replyingTo === comment.id" class="reply-form">
          <el-input
              v-model="replyContent"
              type="textarea"
              :rows="2"
              placeholder="请输入您的回复"
          />
          <el-button @click="submitReply(comment.id)" type="primary" size="small">提交回复</el-button>
        </div>

        <!-- 子评论列表 -->
        <div v-if="comment.replies && comment.replies.length > 0" class="replies">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply">
            <div class="reply-header">
              <span class="username">{{ reply.username }}</span>
              <span class="timestamp">{{ formatDate(reply.timestamp) }}</span>
            </div>
            <div class="reply-content">{{ reply.content }}</div>
          </div>
        </div>
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
import { useRoute } from "vue-router";

const data = defineProps(['username', 'questionId'])
const comments = ref([]);
const newComment = ref('');
const replyingTo = ref(null);
const replyContent = ref('');

const getComments = async () => {
  try {
    const response = await API.post('/comment_get_comments_from_id', {
      username: data.username,
      problem_id: data.questionId,
      is_sub_comment: 'n'
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      console.log(response.data)
      comments.value = response.data.data;
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error('获取评论失败');
  }
};

const submitComment = async () => {
  console.log(newComment.value, data.username,data.questionId);
  if (!newComment.value.trim()) {
    ElMessage.warning('评论内容不能为空');
    return;
  }
  try {
    const response = await API.post('/comment_add', {
      username: data.username,
      parent_id: data.questionId,
      content: newComment.value,
      is_sub_comment: 'n'
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      console.log(newComment.value);
      ElMessage.success('评论发表成功');
      newComment.value = '';
      await getComments(); // 重新加载评论
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error('评论发表失败');
  }
};

const showReplyForm = (commentId) => {
  replyingTo.value = commentId;
  replyContent.value = '';
};

const submitReply = async (commentId) => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('回复内容不能为空');
    return;
  }
  try {
    const response = await API.post('/comment_add', {
      username: route.query.username,
      parent_id: commentId,
      content: replyContent.value,
      is_sub_comment: 'y'
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      ElMessage.success('回复发表成功');
      replyContent.value = '';
      replyingTo.value = null;
      await getComments(); // 重新加载评论
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error('回复发表失败');
  }
};

const formatDate = (timestamp) => {
  return new Date(timestamp).toLocaleString();
};

onMounted(() => {
  getComments();
});
</script>

<style scoped>
/* 保留原有的样式 */

.reply-form {
  margin-top: 10px;
  margin-bottom: 10px;
}

.replies {
  margin-top: 10px;
  margin-left: 20px;
}

.reply {
  background-color: #f9f9f9;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.reply-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 5px;
  font-size: 12px;
}

.reply-content {
  font-size: 14px;
}
</style>