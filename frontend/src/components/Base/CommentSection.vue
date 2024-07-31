<template>
  <h3>讨论区</h3>
  <div class="comment-section">
    <!-- 评论列表 -->
    <div v-if="comments.length > 0" class="comment-list">
      <div v-for="comment in comments" :key="comment.id" class="comment">
        <div class="comment-header">
          <img :src="comment.avatar" class="avatar" alt="User Avatar">
          <div class="user-info">
            <span class="username">{{ comment.user.username }}</span>
            <span class="content">{{ comment.content }}</span>
          </div>
        </div>
        <div class="comment-footer">
          <span class="timestamp">{{ formatDate(comment.create_time) }}</span>
          <el-button @click="showReplyForm(comment.id)" size="small">回复</el-button>
          <el-button v-if="comment.replies && comment.replies.length > 0" @click="toggleReplies(comment.id)" size="small">
            {{ comment.showReplies ? '收起回复' : `展开回复 (${comment.replies.length})` }}
          </el-button>
        </div>

        <!-- 回复表单 -->
        <div v-if="replyingTo === comment.id" class="reply-form">
          <el-input
              v-model="replyContent"
              type="textarea"
              :rows="2"
              placeholder="请输入您的回复"
          />
          <el-button @click="submitReply(comment.id)" type="primary" size="small" class="submit_reply">提交回复</el-button>
        </div>

        <!-- 子评论列表 -->
        <div v-if="comment.showReplies && comment.replies && comment.replies.length > 0" class="replies">
          <div v-for="reply in comment.replies" :key="reply.id" class="reply">
            <div class="reply-header">
              <img :src="reply.avatar" class="avatar small" alt="User Avatar">
              <div class="user-info">
                <span class="username">{{ reply.user.username }}</span>
                <span class="content">{{ reply.content }}</span>
              </div>
            </div>
            <div class="reply-footer">
              <span class="timestamp">{{ formatDate(reply.create_time) }}</span>
            </div>
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

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import API from "@/plugins/axios";

interface User {
  username: string;
}

interface Comment {
  id: number;
  user: User;
  content: string;
  create_time: string;
  avatar?: string;
  replies?: Comment[];
  showReplies?: boolean;
}

const props = defineProps(['username', 'questionId']);
const comments = ref<Comment[]>([]);
const newComment = ref('');
const replyingTo = ref<number | null>(null);
const replyContent = ref('');

const getReply = async (parent_id: number, is_sub_comment: string) => {
  try {
    const response = await API.post('/comment_get_comments_from_id', {
      username: props.username,
      parent_id: parent_id,
      is_sub_comment: is_sub_comment
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      return Promise.all(response.data.data.map(async (reply:any) => {
        const avatar = await getAvatar(reply.user.username);
        return { ...reply, avatar };
      }));
    } else {
      ElMessage.error(response.data.message);
      return [];
    }
  } catch (error) {
    ElMessage.error('获取回复失败');
  }
};

const getComments = async (parent_id:number, is_sub_comment:string) => {
  try {
    const response = await API.post('/comment_get_comments_from_id', {
      username: props.username,
      parent_id: parent_id,
      is_sub_comment: is_sub_comment
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      comments.value = await Promise.all(response.data.data.map(async (comment:any) => {
        const avatar = await getAvatar(comment.user.username);
        const replies = await getReply(comment.id, 'y');
        return { ...comment, avatar, replies, showReplies: false };
      }));
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error('获取评论失败');
  }
};

const getAvatar = async (username:string) => {
  try {
    const response = await API.post('/get_avatar', { username }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      return response.data.avatar;
    }
  } catch (error) {
    console.error('获取头像失败', error);
  }
  return ''; // 返回默认头像或空字符串
};

const submitComment = async () => {
  if (!newComment.value.trim()) {
    ElMessage.warning('评论内容不能为空');
    return;
  }
  try {
    const response = await API.post('/comment_add', {
      username: props.username,
      parent_id: props.questionId,
      content: newComment.value,
      is_sub_comment: 'n'
    }, {
      headers: {'Content-Type': 'application/x-www-form-urlencoded'}
    });
    if (response.data.code === 200) {
      ElMessage.success('评论发表成功');
      newComment.value = '';
      await getComments(props.questionId, 'n');
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error('评论发表失败');
  }
};

const showReplyForm = (commentId:number) => {
  replyingTo.value = commentId;
  replyContent.value = '';
};

const submitReply = async (commentId:number) => {
  if (!replyContent.value.trim()) {
    ElMessage.warning('回复内容不能为空');
    return;
  }
  try {
    const response = await API.post('/comment_add', {
      username: props.username,
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
      await getComments(props.questionId, 'n');
    } else {
      ElMessage.error(response.data.message);
    }
  } catch (error) {
    ElMessage.error('回复发表失败');
  }
};

const toggleReplies = (commentId:number) => {
  const comment = comments.value.find(c => c.id === commentId);
  if (comment) {
    comment.showReplies = !comment.showReplies;
  }
};

const formatDate = (timestamp:string) => {
  const date = new Date(timestamp);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  return `${year}年${month}月${day}日`;
};

onMounted(() => {
  getComments(props.questionId, 'n');
});
</script>

<style scoped>
.comment-section {
  max-width: 100%;
  margin: 0 auto;
}

.comment-list {
  margin-bottom: 20px;
}

.comment {
  border-bottom: 1px solid #e0e0e0;
  padding: 15px 0;
}

.comment-header, .reply-header {
  display: flex;
  align-items: flex-start;
  margin-bottom: 10px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  margin-right: 10px;
}

.avatar.small {
  width: 30px;
  height: 30px;
}

.user-info {
  display: flex;
  flex-direction: column;
}

.username {
  font-weight: bold;
  margin-bottom: 5px;
}

.content {
  font-size: 14px;
  line-height: 1.4;
}

.comment-footer, .reply-footer {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  font-size: 12px;
  color: #888;
  gap: 10px;
}

.reply-form {
  margin-top: 10px;
  margin-bottom: 10px;
}

.replies {
  margin-top: 10px;
  margin-left: 50px;
}

.reply {
  background-color: #f9f9f9;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 4px;
}

.add-comment {
  margin-top: 20px;
}

.add-comment .el-button {
  margin-top: 10px;
}

.submit_reply {
  margin-top: 10px;
}
</style>