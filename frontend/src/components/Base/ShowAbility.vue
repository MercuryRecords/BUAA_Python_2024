<template>
  <div class="profile-container">
    <div class="avatar-section">
      <img :src="avatarUrl" alt="User Avatar" class="avatar-image"/>
      <h2>{{ props.username }}</h2>
      <p>最擅长的tag：
        <template v-if="bestTags.length > 0">
          <span v-for="tag in bestTags" :key="tag" class="tag" @click="updateChart(tag)">{{ tag }}</span>
        </template>
        <span v-else class="no-tag">暂无</span>
      </p>
      <p>最薄弱的tag：
        <template v-if="weakestTags.length > 0">
          <span v-for="tag in weakestTags" :key="tag" class="tag" @click="updateChart(tag)">{{ tag }}</span>
        </template>
        <span v-else class="no-tag">暂无</span>
      </p>
    </div>
    <div class="ability-section">
      <h2>用户{{filterTag}}能力值随时间变化</h2>
      <div class="filter-container">
        <label for="filterTag">标签筛选器：{{filterTag}}</label>
      </div>
      <v-chart class="chart" :option="chartOption" :key="chartKey" autoresize/>
    </div>
  </div>
</template>

<script setup>
import {ref, onMounted} from 'vue'
import {use} from 'echarts/core'
import {CanvasRenderer} from 'echarts/renderers'
import {LineChart} from 'echarts/charts'
import {GridComponent, TooltipComponent, LegendComponent, TitleComponent} from 'echarts/components'
import VChart from 'vue-echarts'
import API from "@/plugins/axios";

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, TitleComponent])

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
    const response = await API.post('/get_ability_trace', {
      username: props.username,
      during_interval: duringInterval.value,
      during_num: duringNum.value,
      filter_tag: tag
    }, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    })
    console.log('API Response:', response.data);
    if (response.data.code === 200) {
      const data = response.data.data;
      console.log('Original data:', data);

      // 生成时间戳
      const currentTime = new Date().getTime();
      const interval = duringInterval.value * 1000; // 转换为毫秒

      chartOption.value.series[0].data = data.map((value, index) => {
        const timestamp = currentTime - (data.length - 1 - index) * interval;
        console.log(`Mapped data point: [${new Date(timestamp).toISOString()}, ${value}]`);
        return [timestamp, value];
      });

      console.log('Processed chart data:', chartOption.value.series[0].data);

      const times = chartOption.value.series[0].data.map(item => item[0]);
      chartOption.value.xAxis.min = Math.min(...times);
      chartOption.value.xAxis.max = Math.max(...times);
      console.log('X-axis range:', [new Date(chartOption.value.xAxis.min).toISOString(), new Date(chartOption.value.xAxis.max).toISOString()]);

      // 强制图表重新渲染
      chartKey.value += 1;
    } else {
      console.error('获取数据失败：', response.data.message);
    }
  } catch (error) {
    console.error('请求出错：', error);
  }
}

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

const updateChart = (tag) => {
  filterTag.value = tag
  fetchData(tag)
}


onMounted(() => {
  fetchAvatar()
  fetchBestTags()
  fetchWeakestTags()
  fetchData()
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
  margin-left: -20px;
}

.avatar-image {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
}

.tag {
  cursor: pointer;
  color: #1890ff;
  text-decoration: underline;
}

.ability-section {
  flex: 1;
  padding-top: 20px;
}

.ability-title {
  margin-bottom: 20px;
}

.filter-container {
  margin-bottom: 20px;
}

.chart {
  height: 400px;
  width: 100%;
  margin-top: 20px;
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

/* New styles to keep tags on the same line */
.avatar-section p {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.avatar-section p span {
  display: inline;
}
</style>