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
               :class="{
                 'selected': userAnswer === ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1],
                 'correct': !isCorrect && correctAnswer === ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1]
               }"
               @click="selectAnswer(index - 1)">
            <span class="option-label">{{ ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1] }}.</span>
            {{ currentQuestion[`field${index}`] }}
          </div>
        </div>

        <!-- 填空题 -->
        <div v-else-if="currentQuestion.type === 'b'" class="fill-in-blank">
          <div v-for="index in currentQuestion.ans_count" :key="index" class="fill-in-blank-item">
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

        <!-- 填空题错误答案展示 -->
        <div v-if="!isCorrect && currentQuestion.type === 'b'" class="correct-answers">
          <h3>正确答案：</h3>
          <div v-for="(answer, index) in correctAnswers" :key="index" class="correct-answer-item">
            <span>第{{ index + 1 }}空：{{ answer }}</span>
          </div>
        </div>

        <div v-if="showStatistics" class="statistics">
          <p>您的尝试次数: {{ currentQuestion.user_count }}</p>
          <p>您的正确次数: {{ currentQuestion.user_right_count }}</p>
          <p>您的正确率:
            <el-tag :type="getAccuracyColor(accuracy)">
              {{ (accuracy * 100).toFixed(2) }}%
            </el-tag>
          </p>
          <p>
            总正确率：
            <el-tag :type="getAccuracyColor(accuracy)">
              {{ (total_accuracy * 100).toFixed(2) }}%
            </el-tag>
          </p>
        </div>
      </div>

      <div class="question-selector">
        <el-button class="selector-button" @click="showQuestionDrawer = true">
          选择题目
        </el-button>
      </div>
    </div>

    <!-- 题目列表抽屉 -->
    <el-drawer
        title="题目列表"
        v-model="showQuestionDrawer"
        direction="rtl"
        size="300px"
    >
      <el-scrollbar height="calc(100vh - 60px)">
        <el-menu
            :default-active="currentIndex.toString()"
            @select="handleSelect"
        >
          <el-menu-item v-for="(question, index) in problems" :key="index" :index="index.toString()">
            <span class="question-item">
              <span class="question-title">{{ question.problem_title }}</span>
            </span>
          </el-menu-item>
        </el-menu>
      </el-scrollbar>
    </el-drawer>
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
const correctAnswer = ref('');
const correctAnswers = ref<string[]>([]);

const userAnswer = ref<string | string[]>('');
const feedback = ref('');
const isCorrect = ref(false);
const showStatistics = ref(false);
const showQuestionDrawer = ref(false);

const accuracy = computed(() => {
  if (currentQuestion.value) {
    if (currentQuestion.value.user_count == 0) {
      return 0;
    }
    return currentQuestion.value.user_right_count / currentQuestion.value.user_count;
  }
  return 0;
});

const total_accuracy = computed(() => {
  if (currentQuestion.value) {
    if (currentQuestion.value.all_count == 0) {
      return 0;
    }
    return currentQuestion.value.all_right_count / currentQuestion.value.all_count;
  }
  return 0;
});

const selectAnswer = (index: number) => {
  userAnswer.value = ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index];
};

const checkAnswer = () => {
  API.post('/problem_check', {
    username: route.query.username,
    problem_id: currentQuestion.value.id,
    user_answer: userAnswer.value,
    user_field1: Array.isArray(userAnswer.value) ? userAnswer.value[0] : '',
    user_field2: Array.isArray(userAnswer.value) ? userAnswer.value[1] : '',
    user_field3: Array.isArray(userAnswer.value) ? userAnswer.value[2] : '',
    user_field4: Array.isArray(userAnswer.value) ? userAnswer.value[3] : '',
    user_field5: Array.isArray(userAnswer.value) ? userAnswer.value[4] : '',
    user_field6: Array.isArray(userAnswer.value) ? userAnswer.value[5] : '',
    user_field7: Array.isArray(userAnswer.value) ? userAnswer.value[6] : ''
  }, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  }).then(
      function (response) {
        if (response.data.code === 200) {
          isCorrect.value = (response.data.data.correct == 'T');
          currentQuestion.value.user_right_count = response.data.data.user_right_count;
          currentQuestion.value.user_count = response.data.data.user_count;
          currentQuestion.value.all_count = response.data.data.all_count;
          currentQuestion.value.all_right_count = response.data.data.all_right_count;

          // 存储正确答案
          if (currentQuestion.value.type === 'c') {
            correctAnswer.value = response.data.data.answer;
          } else if (currentQuestion.value.type === 'b') {

          }

          feedback.value = isCorrect.value ? '回答正确！' : '回答错误，请查看正确答案。';
          showStatistics.value = true;
        } else {
          ElMessage.error(response.data.message);
        }
      }
  ).catch(
      function () {
        console.log('error submit!')
      }
  )
}

const submitAnswer = () => {
  if (currentQuestion.value.type === 'c') {
    if (!userAnswer.value) {
      ElMessage.warning('请先选择一个答案');
      return;
    }
  } else if (currentQuestion.value.type === 'b') {
    if (!(userAnswer.value as string[]).every(answer => answer)) {
      ElMessage.warning('请填写所有空格');
      return;
    }
  }
  checkAnswer();
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
  correctAnswer.value = '';
  correctAnswers.value = [];
};

const getAccuracyColor = (accuracy: number) => {
  if (accuracy >= 0.7) return 'success';
  if (accuracy < 0.3) return 'danger';
  return 'warning';
};

const handleSelect = (index: string) => {
  currentIndex.value = parseInt(index);
  resetQuestion();
  showQuestionDrawer.value = false;
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
  margin-left: 220px;
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

.option.correct {
  background-color: #e8f5e9;
  border-color: #4caf50;
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

.question-item {
  display: flex;
  align-items: center;
}

.question-number {
  width: 30px;
  text-align: right;
  margin-right: 10px;
  font-weight: bold;
}

.question-title {
  flex: 1;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>