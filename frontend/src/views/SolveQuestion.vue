<template>
  <div class="do-question">
    <Navigator :username="username" />
    <div class="content-wrapper">
      <div class="question-container" v-if="currentQuestion">
        <h2>题目 {{ currentIndex + 1 }} / {{ totalQuestions }}</h2>
        <p class="question-title">{{ currentQuestion.contents }}</p>

        <!-- 选择题 -->
        <div v-if="currentQuestion.type === 'c'" class="options">
          <div v-for="(option, index) in currentQuestion.options" :key="index"
               class="option"
               :class="{ 'selected': userAnswer === option }"
               @click="selectAnswer(option)">
            <span class="option-label">{{ ['A', 'B', 'C', 'D'][index] }}.</span>
            {{ option }}
          </div>
        </div>

        <!-- 填空题 -->
        <div v-else-if="currentQuestion.type === 'b'" class="fill-in-blank">
          <el-input v-model="userAnswer" placeholder="请输入您的答案"></el-input>
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
            <el-tag :type="getAccuracyColor(currentQuestion.accuracy)">
              {{ (currentQuestion.accuracy * 100).toFixed(2) }}%
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
import { ref, computed } from 'vue';
import { useRoute } from 'vue-router';
import { ElMessage } from 'element-plus';
import Navigator from "@/components/Base/Navigator.vue";

interface Question {
  id: string,
  problem_title: string,
  creator: string,
  problem_group_title: string,
  tags: string[],
  all_count: number,
  all_right_count: number,
  user_count: number,
  user_right_count: number,
  accuracy: number,
  type: 'b' | 'c',
  contents: string
  options?: string[];
  correct_answer: string;
}

const route = useRoute();

const username = ref(route.query.username as string || '测试用户');
const problems = ref<Question[]>([
  {
    id: "Q001",
    problem_title: "vue的核心特性",
    creator: "Admin",
    problem_group_title: "Vue基础",
    tags: ["Vue.js", "前端框架"],
    all_count: 100,
    all_right_count: 80,
    user_count: 2,
    user_right_count: 1,
    accuracy: 0.8,
    type: 'c',
    contents: "下列哪项不是Vue.js的核心特性?",
    options: ["响应式数据绑定", "组件化开发", "虚拟DOM", "原生移动应用开发"],
    correct_answer: "原生移动应用开发"
  },
  {
    id: "Q002",
    problem_title: "组合式API",
    creator: "Vue专家",
    problem_group_title: "Vue3新特性",
    tags: ["Vue3", "组合式API"],
    all_count: 50,
    all_right_count: 40,
    user_count: 1,
    user_right_count: 1,
    accuracy: 0.8,
    type: 'c',
    contents: "Vue.js中用于声明响应式状态的组合式API是?",
    options: ["useState", "useEffect", "ref", "useState"],
    correct_answer: "ref"
  },
  {
    id: "Q003",
    problem_title: "Vue实例的生命周期钩子",
    creator: "Vue专家",
    problem_group_title: "Vue生命周期",
    tags: ["Vue", "生命周期"],
    all_count: 30,
    all_right_count: 25,
    user_count: 1,
    user_right_count: 1,
    accuracy: 0.833,
    type: 'b',
    contents: "Vue实例被创建后，第一个被调用的生命周期钩子是 ______。",
    correct_answer: "created"
  },
]);

const currentIndex = ref(0);
const totalQuestions = computed(() => problems.value.length);
const currentQuestion = computed(() => problems.value[currentIndex.value]);

const userAnswer = ref('');
const feedback = ref('');
const isCorrect = ref(false);
const showStatistics = ref(false);
const showQuestionList = ref(false);

const selectAnswer = (option: string) => {
  userAnswer.value = option;
};

const submitAnswer = () => {
  if (!userAnswer.value) {
    ElMessage.warning('请先选择或输入一个答案');
    return;
  }

  isCorrect.value = userAnswer.value === currentQuestion.value.correct_answer;
  feedback.value = isCorrect.value ? '回答正确！' : '回答错误，请重试。';

  currentQuestion.value.all_count++;
  currentQuestion.value.user_count++;
  if (isCorrect.value) {
    currentQuestion.value.all_right_count++;
    currentQuestion.value.user_right_count++;
  }
  currentQuestion.value.accuracy = currentQuestion.value.all_right_count / currentQuestion.value.all_count;

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
  userAnswer.value = '';
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