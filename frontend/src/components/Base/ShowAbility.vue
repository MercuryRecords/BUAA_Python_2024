<template>
  <div class="profile-container">
    <div class="avatar-section">
      <img :src="avatarUrl" alt="User Avatar" class="avatar-image"/>
      <h2>{{ props.username }}</h2>
      <p>最擅长的标签：
        <template v-if="bestTags.length > 0">
          <span v-for="tag in bestTags" :key="tag" class="tag" @click="updateChart(tag)">{{ tag }}</span>
        </template>
        <span v-else class="no-tag">暂无</span>
      </p>
      <p>最薄弱的标签：
        <template v-if="weakestTags.length > 0">
          <span v-for="tag in weakestTags" :key="tag" class="tag" @click="updateChart(tag)">{{ tag }}</span>
        </template>
        <span v-else class="no-tag">暂无</span>
      </p>
    </div>
    <div class="ability-section">
      <h2>{{ props.username }}的{{ filterTag }}能力值</h2>
      <div class="chart-header">
        <div class="filter-container">
          <label for="filterTag">标签筛选器：{{ filterTag }}</label>
        </div>
        <el-select v-model="timeUnit" @change="updateChart(filterTag)" class="time-unit-select">
          <el-option value="" label="默认"></el-option>
          <el-option value="minute" label="分钟"></el-option>
          <el-option value="hour" label="小时"></el-option>
          <el-option value="day" label="天"></el-option>
        </el-select>
      </div>
      <v-chart class="chart" :option="chartOption" :key="chartKey" autoresize/>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted, watch} from 'vue'
import {use} from 'echarts/core'
import {CanvasRenderer} from 'echarts/renderers'
import {LineChart} from 'echarts/charts'
import {GridComponent, TooltipComponent, LegendComponent, TitleComponent} from 'echarts/components'
import VChart from 'vue-echarts'
import API from "@/plugins/axios";

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

const timeUnit = ref('')
const props = defineProps(['username'])
const duringInterval = ref(60)
const duringNum = ref(10)
const filterTag = ref('')
const chartKey = ref(0)
const avatarUrl = ref('')
const bestTags = ref([])
const weakestTags = ref([])

const chartOption = ref({
  title: {
    text: '趋势图'
  },
  tooltip: {
    trigger: 'axis',
    formatter: function (params) {
      const date = new Date(params[0].value[0]);
      return `时间: ${date.toLocaleString()}<br/>能力值: ${params[0].value[1]}`;
    }
  },
  xAxis: {
    type: 'time',
    name: '时间',
    axisLabel: {
      formatter: function (value) {
        return new Date(value).toLocaleTimeString();
      }
    }
  },
  yAxis: {
    type: 'value',
    name: '能力值',
    nameLocation: 'middle',
    nameGap: 40,
    nameRotate: 90,
    axisLabel: {
      formatter: '{value}'
    }
  },
  series: [{
    name: '能力值',
    type: 'line',
    data: [],
    symbolSize: 8,
    itemStyle: {
      color: '#1890ff'
    }
  }]
})

const fetchAvatar = async () => {
  try {
    const response = await API.post('/get_avatar', {
      username: props.username
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    if (response.data.code === 200) {
      avatarUrl.value = response.data.avatar
    } else {
      console.error('获取头像失败：', response.data.message)
      avatarUrl.value = 'path/to/default/avatar.png' // 设置默认头像
    }
  } catch (error) {
    console.error('请求头像出错：', error)
    avatarUrl.value = 'path/to/default/avatar.png' // 设置默认头像
  }
}

const fetchData = async (tag = '') => {
  try {
    switch (timeUnit.value) {
      case 'minute':
      case '': // 默认情况
        duringInterval.value = 60; // 1分钟
        break;
      case 'hour':
        duringInterval.value = 3600; // 1小时
        break;
      case 'day':
        duringInterval.value = 86400; // 1天
        break;
    }

    const response = await API.post('/get_ability_trace', {
      username: props.username,
      during_interval: duringInterval.value,
      during_num: duringNum.value,
      filter_tag: tag
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });
    console.log('API Response:', response.data);
    if (response.data.code === 200) {
      const data = response.data.data;
      console.log('Original data:', data);

      const currentTime = new Date();
      let timeInterval;

      switch (timeUnit.value) {
        case 'minute':
        case '': // 默认情况
          timeInterval = 60 * 1000; // 1分钟
          break;
        case 'hour':
          timeInterval = 60 * 60 * 1000; // 1小时
          break;
        case 'day':
          timeInterval = 24 * 60 * 60 * 1000; // 1天
          break;
      }

      chartOption.value.series[0].data = data.map((value, index) => {
        const time = new Date(currentTime - (data.length - 1 - index) * timeInterval);
        return [time.getTime(), value];
      });

      console.log('Processed chart data:', chartOption.value.series[0].data);

      // 更新 x 轴配置
      chartOption.value.xAxis.type = 'time';
      chartOption.value.xAxis.min = chartOption.value.series[0].data[0][0];
      chartOption.value.xAxis.max = chartOption.value.series[0].data[data.length - 1][0];

      // 强制图表重新渲染
      chartKey.value += 1;
    } else {
      console.error('获取数据失败：', response.data.message);
    }
  } catch (error) {
    console.error('请求出错：', error);
  }
};


const fetchBestTags = async () => {
  try {
    const response = await API.post('/get_advantaged_tags', {
      username: props.username,
      required_num: 5
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    console.log('哈哈哈哈')
    console.log(response.data)
    if (response.data.code === 200) {
      bestTags.value = response.data.data.map(tag => tag.name)
    } else {
      console.error('获取最擅长标签失败：', response.data.message)
    }
  } catch (error) {
    console.error('请求最擅长标签出错：', error)
  }
}

const fetchWeakestTags = async () => {
  try {
    const response = await API.post('/get_disadvantaged_tags', {
      username: props.username,
      required_num: 5
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    if (response.data.code === 200) {
      weakestTags.value = response.data.data.map(tag => tag.name)
    } else {
      console.error('获取最薄弱标签失败：', response.data.message)
    }
  } catch (error) {
    console.error('请求最薄弱标签出错：', error)
  }
}

const updateChart = async (tag) => {
  filterTag.value = tag
  await fetchData(tag)
  updateChartDisplay()
}

const updateChartDisplay = () => {
  const data = chartOption.value.series[0].data;
  if (data.length === 0) return;

  // 根据时间单位更新 x 轴标签格式
  switch (timeUnit.value) {
    case 'minute':
    case '': // 默认情况
      chartOption.value.xAxis.axisLabel.formatter = (value) => {
        const date = new Date(value);
        return `${date.getHours().toString().padStart(2, '0')}:${date.getMinutes().toString().padStart(2, '0')}`;
      };
      break;
    case 'hour':
      chartOption.value.xAxis.axisLabel.formatter = (value) => {
        const date = new Date(value);
        return `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')} ${date.getHours().toString().padStart(2, '0')}:00`;
      };
      break;
    case 'day':
      chartOption.value.xAxis.axisLabel.formatter = (value) => {
        const date = new Date(value);
        return `${(date.getMonth() + 1).toString().padStart(2, '0')}/${date.getDate().toString().padStart(2, '0')}`;
      };
      break;
  }

  // 设置 x 轴刻度数量
  chartOption.value.xAxis.splitNumber = 10;

  // Force chart to re-render
  chartKey.value += 1;
};

watch(timeUnit, updateChartDisplay)

onMounted(() => {
  fetchAvatar()
  fetchBestTags()
  fetchWeakestTags()
  fetchData().then(updateChartDisplay)
})
</script>

<style scoped>
.profile-container {
  display: flex;
  gap: 40px;
  padding: 20px;
  align-items: flex-start;
}

.avatar-section {
  flex: 0 0 180px;
  text-align: center;
}

.avatar-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.ability-section {
  flex: 1;
}

.chart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-container {
  /* styles for filter container */
}

.time-unit-select {
  width: 120px;
}

.chart {
  height: 400px;
  width: 100%;
}

.tag {
  cursor: pointer;
  color: #1890ff;
  text-decoration: none;
  margin-right: 5px;
  display: inline-block;
}

.no-tag {
  color: #999;
}

.avatar-section p {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.avatar-section p span {
  display: inline;
}
</style>