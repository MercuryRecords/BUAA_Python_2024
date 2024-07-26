<template>
  <div class="do-question">
    <Navigator :username="username" />
    <div class="content-wrapper">
      <div class="question-container" v-if="currentQuestion">
        <h2>题目 {{ currentIndex + 1 }} / {{ totalQuestions }}</h2>
        <p class="question-title">{{ currentQuestion.content }}</p>

        <!-- 选择题 -->
        <div v-if="currentQuestion.type === 'c'" class="options">
          <div v-for="index in currentQuestion.ans_count" :key="index"
               class="option"
               :class="{ 'selected': userAnswer === currentQuestion[`field${index}`] }"
               @click="selectAnswer(currentQuestion[`field${index}`])">
            <span class="option-label">{{ ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1] }}.</span>
            {{ currentQuestion[`field${index}`] }}
          </div>
        </div>

        <!-- 填空题 -->
        <div v-else-if="currentQuestion.type === 'b'" class="fill-in-blank">
          <div v-for="index in currentQuestion.ans_count" :key="index" class="fill-in-blank-item">
<!--            <label>空 {{ index }}:</label>-->
            <el-input v-model="userAnswer[index - 1]" :placeholder="`请输入第${index}空的答案`"></el-input>
          </div>
        </div>

        <div class="navigation">
          <el-button @click="previousQuestion" :disabled="currentIndex === 0">上一题</el-button>
          <el-button @click="submitAnswer" type="primary">提交答案</el-button>
          <el-button @click="nextQuestion" :disabled="currentIndex === totalQuestions - 1">下一题</el-button>
        </div>

        <div v-if="feedback" class="feedback" :class="{ 'is-correct': isCorrect, 'is-incorrect': !isCorrect }">
          {{ feedback }}
        </div>

        <div v-if="showStatistics" class="statistics">
          <p>总尝试次数: {{ currentQuestion.all_count }}</p>
          <p>总正确次数: {{ currentQuestion.all_right_count }}</p>
          <p>您的尝试次数: {{ currentQuestion.user_count }}</p>
          <p>您的正确次数: {{ currentQuestion.user_right_count }}</p>
          <p>正确率:
            <el-tag :type="getAccuracyColor(accuracy)">
              {{ (accuracy * 100).toFixed(2) }}%
            </el-tag>
          </p>
        </div>
      </div>

      <div class="question-selector">
        <el-button class="selector-button" @click="showQuestionList = true">
          选择题目
        </el-button>
      </div>
    </div>

    <!-- 题目列表弹出框 -->
    <el-dialog
        title="题目列表"
        v-model="showQuestionList"
        width="30%"
        :before-close="handleCloseDialog"
    >
      <el-menu
          :default-active="currentIndex.toString()"
          @select="handleSelect"
      >
        <el-menu-item v-for="(question, index) in problems" :key="index" :index="index.toString()">
          {{ index + 1 }}  {{ question.problem_title }}
        </el-menu-item>
      </el-menu>
    </el-dialog>
  </div>
</template>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import Navigator from "@/components/Base/Navigator.vue";
import API from "@/plugins/axios";

interface Question {
  id: number;
  type: 'c' | 'b';
  problem_title: string;
  content: string;
  ans_count: number;
  field1: string;
  field2: string;
  field3: string;
  field4: string;
  field5: string;
  field6: string;
  field7: string;
  tags: string[];
  creator: string;
  problem_group_id: number;
  problem_group_title: string;
  user_right_count: number;
  user_count: number;
  all_right_count: number;
  all_count: number;
}

const route = useRoute();

const username = ref(route.query.username as string || '测试用户');
const problems = ref<Question[]>([]);
const currentIndex = ref(parseInt(route.query.index as string, 10) || 0);
const totalQuestions = computed(() => problems.value.length);
const currentQuestion = computed(() => problems.value[currentIndex.value]);

const userAnswer = ref<string | string[]>('');
const feedback = ref('');
const isCorrect = ref(false);
const showStatistics = ref(false);
const showQuestionList = ref(false);

const accuracy = computed(() => {
  if (currentQuestion.value) {
    return currentQuestion.value.all_right_count / currentQuestion.value.all_count;
  }
  return 0;
});

const selectAnswer = (option: string) => {
  userAnswer.value = option;
};

const submitAnswer = () => {
  if (currentQuestion.value.type === 'c') {
    if (!userAnswer.value) {
      ElMessage.warning('请先选择一个答案');
      return;
    }
    isCorrect.value = userAnswer.value === currentQuestion.value.field1;
  } else if (currentQuestion.value.type === 'b') {
    if (!(userAnswer.value as string[]).every(answer => answer)) {
      ElMessage.warning('请填写所有空格');
      return;
    }
    isCorrect.value = (userAnswer.value as string[]).every((answer, index) =>
        answer === currentQuestion.value[`field${index + 1}` as keyof Question]
    );
  }

  feedback.value = isCorrect.value ? '回答正确！' : '回答错误，请重试。';

  currentQuestion.value.all_count++;
  currentQuestion.value.user_count++;
  if (isCorrect.value) {
    currentQuestion.value.all_right_count++;
    currentQuestion.value.user_right_count++;
  }

  showStatistics.value = true;
};

const previousQuestion = () => {
  if (currentIndex.value > 0) {
    currentIndex.value--;
    resetQuestion();
  }
};

const nextQuestion = () => {
  if (currentIndex.value < totalQuestions.value - 1) {
    currentIndex.value++;
    resetQuestion();
  }
};

const resetQuestion = () => {
  userAnswer.value = currentQuestion.value.type === 'c' ? '' : Array(currentQuestion.value.ans_count).fill('');
  feedback.value = '';
  isCorrect.value = false;
  showStatistics.value = false;
};

const getAccuracyColor = (accuracy: number) => {
  if (accuracy >= 0.7) return 'success';
  if (accuracy < 0.3) return 'danger';
  return 'warning';
};

const handleSelect = (index: string) => {
  currentIndex.value = parseInt(index);
  resetQuestion();
  showQuestionList.value = false;
};

const handleCloseDialog = () => {
  showQuestionList.value = false;
};

const getTemporaryQuestion = () => {
  API.post('/get_problem_group_content', {
    username: route.query.username,
    problem_group_id: route.query.problem_group_id,
    is_temporary: 'y'
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          problems.value = response.data.data;
          console.log(problems.value)
          resetQuestion();
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
};

onMounted(() => {
  getTemporaryQuestion();
});
</script>

<style scoped>
.do-question {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.content-wrapper {
  display: flex;
  gap: 20px;
}

.question-container {
  flex: 1;
  background-color: #ffffff;
  border-radius: 8px;
  padding: 30px;
  margin-top: 20px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.question-selector {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

h2, h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 20px;
}

.question-title {
  font-size: 20px;
  font-weight: bold;
  margin-bottom: 30px;
  color: #333;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.option {
  padding: 15px 20px;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  background-color: #f5f5f5;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
}

.option:hover {
  background-color: #e8e8e8;
}

.option.selected {
  background-color: #e1f5fe;
  border-color: #03a9f4;
}

.option-label {
  font-weight: bold;
  margin-right: 10px;
}

.fill-in-blank {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 30px;
}

.fill-in-blank-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.navigation {
  display: flex;
  justify-content: space-between;
  margin-top: 30px;
}

.navigation .el-button {
  min-width: 100px;
}

.el-button--primary {
  background-color: #1976d2;
  border-color: #1976d2;
}

.el-button--primary:hover,
.el-button--primary:focus {
  background-color: #1565c0;
  border-color: #1565c0;
}

.feedback {
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  text-align: center;
}

.feedback.is-correct {
  background-color: #e8f5e9;
  color: #4caf50;
}

.feedback.is-incorrect {
  background-color: #fbe9e7;
  color: #f44336;
}

.statistics {
  margin-top: 20px;
  padding: 10px;
  background-color: #f4f4f5;
  border-radius: 4px;
}

.selector-button {
  width: 120px;
}

/* 弹出框样式 */
:deep(.el-dialog__body) {
  padding: 0;
}

:deep(.el-menu) {
  border-right: none;
}

:deep(.el-menu-item) {
  height: 50px;
  line-height: 50px;
}
</style>