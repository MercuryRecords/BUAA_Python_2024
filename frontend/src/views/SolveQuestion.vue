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
                 'selected': !submitted && userAnswer === ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1],
                 'correct': submitted && correctAnswer === ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1],
                 'incorrect': submitted && userAnswer === ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1] && userAnswer !== correctAnswer
               }"
               @click="selectAnswer(index - 1)">
            <span class="option-label">{{ ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index - 1] }}.</span>
            {{ currentQuestion[`field${index}`] }}
          </div>
        </div>

        <!-- 填空题 -->
        <div v-else-if="currentQuestion.type === 'b'" class="fill-in-blank">
          <div v-for="index in currentQuestion.ans_count" :key="index" class="fill-in-blank-item">
            <el-input
                v-model="userAnswer[index - 1]"
                :placeholder="`请输入第${index}空的答案`"
                :class="{
                'correct-input': submitted && isCorrect4Blank[index - 1],
                'incorrect-input': submitted && !isCorrect4Blank[index - 1]
              }"
            ></el-input>
          </div>
        </div>

        <div class="navigation">
          <el-button @click="previousQuestion" :disabled="currentIndex === 0">上一题</el-button>
          <el-button @click="submitAnswer" type="primary" :disabled="submitted">提交答案</el-button>
          <el-button @click="nextQuestion" :disabled="currentIndex === totalQuestions - 1">下一题</el-button>
        </div>

        <div v-if="submitted" class="result-and-comments">
          <div class="result-container">
            <h3>做题统计</h3>
            <p class="stat-line">
              本题你做过 {{ currentQuestion.user_count }} 次，错了 <span class="red">{{ currentQuestion.user_count - currentQuestion.user_right_count }}</span> 次
            </p>
            <div class="stat-line">
              题库正确率：
              <div class="progress-bar">
                <div class="progress" :style="{ width: `${(total_accuracy * 100).toFixed(2)}%` }"></div>
              </div>
              <span class="percentage">{{ (total_accuracy * 100).toFixed(2) }}%</span>
            </div>

            <el-button @click="toggleAnswers" class="show-answer-button">
              {{ showAnswers ? '隐藏答案' : '显示答案' }}
            </el-button>
            <div v-if="showAnswers" class="correct-answers">
              <h3>正确答案：</h3>
              <p v-if="currentQuestion.type === 'c'">{{ correctAnswer }}</p>
              <div v-else-if="currentQuestion.type === 'b'">
                <p v-for="(answer, index) in correctAnswers.slice(0, currentQuestion.ans_count)" :key="index">
                  第{{ index + 1 }}空：{{ answer }}
                </p>
              </div>
            </div>
          </div>

          <div class="result-container">
            <CommentSection
                :questionId="currentQuestion.id"
                :username="username"
            />
          </div>
        </div>

        <div v-if="feedback" class="feedback" :class="{ 'is-correct': isCorrect, 'is-incorrect': !isCorrect }">
          {{ feedback }}
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
            class="question-menu"
        >
          <el-menu-item v-for="(question, index) in problems" :key="index" :index="index.toString()" class="question-menu-item">
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
import CommentSection from "@/components/Base/CommentSection.vue";

// ... (保持原有的接口定义和其他导入不变)

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
const isCorrect4Blank = ref<boolean[]>([]);

const userAnswer = ref<string | string[]>('');
const feedback = ref('');
const isCorrect = ref(false);
const showQuestionDrawer = ref(false);
const showAnswers = ref(false);
const submitted = ref(false);

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
  if (!submitted.value) {
    userAnswer.value = ['A', 'B', 'C', 'D', 'E', 'F', 'G'][index];
  }
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
            correctAnswers.value = [response.data.data.field1, response.data.data.field2, response.data.data.field3,
              response.data.data.field4, response.data.data.field5, response.data.data.field6, response.data.data.field7];
            isCorrect4Blank.value = [response.data.data.correct1 == 'T', response.data.data.correct2 == 'T', response.data.data.correct3 == 'T',
              response.data.data.correct4 == 'T', response.data.data.correct5 == 'T', response.data.data.correct6 == 'T',
              response.data.data.correct7 == 'T'];
          }
          // feedback.value = isCorrect.value ? '回答正确！' : '回答错误，请查看正确答案。';
          submitted.value = true;
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
  correctAnswer.value = '';
  correctAnswers.value = [];
  showAnswers.value = false;
  submitted.value = false;
  isCorrect4Blank.value = [];
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

const toggleAnswers = () => {
  showAnswers.value = !showAnswers.value;
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
  font-size: 15px;
  font-weight: bold;
  margin-bottom: 10px;
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

.option.incorrect {
  background-color: #ffebee;
  border-color: #f44336;
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

.result-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.comments-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.correct-answers {
  margin-top: 20px;
}

.score {
  font-size: 16px;
  margin-top: 10px;
}

.feedback {
  margin-top: 20px;
  padding: 10px;
  border-radius: 4px;
  font-weight: bold;
}

.is-correct {
  background-color: #e8f5e9;
  color: #4caf50;
}

.is-incorrect {
  background-color: #ffebee;
  color: #f44336;
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

.selector-button {
  margin-top: 20px;
}

.correct-input :deep(.el-input__wrapper) {
  background-color: #e8f5e9;
  box-shadow: 0 0 0 1px #4caf50 inset;
}

.incorrect-input :deep(.el-input__wrapper) {
  background-color: #ffebee;
  box-shadow: 0 0 0 1px #f44336 inset;
}

/* 确保输入框内的文字颜色保持可读 */
.correct-input :deep(.el-input__inner),
.incorrect-input :deep(.el-input__inner) {
  background-color: transparent;
  color: #333;
}

.result-container {
  margin-top: 30px;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 4px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.stat-line {
  margin-bottom: 10px;
  font-size: 14px;
  color: #333;

}

.red {
  color: red;
  font-weight: bold;
}

.progress-bar {
  background-color: #f0f0f0;
  height: 10px;
  width: 200px;
  border-radius: 5px;
  overflow: hidden;
  display: inline-block;
  vertical-align: middle;
}

.progress {
  background-color: #4CAF50;
  height: 100%;
}

.percentage {
  margin-left: 10px;
  font-size: 14px;
  color: #666;
}

.question-menu {
  padding: 10px;
  background-color: transparent;
  border-right: none;
}

.question-menu-item {
  border-radius: 8px;
  margin-bottom: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.question-menu-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
}

.question-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  padding: 10px;
}

.question-title {
  font-size: 14px;
  color: #333;
  line-height: 1.4;
}

/* 覆盖 Element Plus 的默认样式 */
.el-menu-item {
  height: auto;
  line-height: 1.5;
  padding: 0;
}

.el-menu-item.is-active {
  background-color: #e6f7ff;
}

.el-menu-item:hover {
  background-color: #f5f5f5;
}
</style>