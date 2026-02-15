<template>
  <div class="indicator-detail">
    <el-button @click="$router.back()" class="back-button">
      <el-icon><ArrowLeft /></el-icon> 返回
    </el-button>

    <el-card class="detail-card" v-if="indicatorData">
      <template #header>
        <div class="card-header">
          <div>
            <h2>{{ indicatorData.indicator_name }}</h2>
            <span class="code">{{ indicatorCode }}</span>
          </div>
          <el-button type="primary" @click="refresh" :loading="loading">刷新数据</el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-item">
            <span class="label">最新值</span>
            <span class="value">{{ formatValue(indicatorData.latest_value) }}</span>
            <span class="unit">{{ indicatorData.unit }}</span>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-item">
            <span class="label">变化率</span>
            <span class="value" :class="getChangeClass(indicatorData.change_percent)">
              {{ formatChange(indicatorData.change_percent) }}
            </span>
          </div>
        </el-col>
        <el-col :span="6" v-if="trendData">
          <div class="stat-item">
            <span class="label">趋势</span>
            <el-tag :type="getTrendType(trendData.trend)">{{ getTrendText(trendData.trend) }}</el-tag>
          </div>
        </el-col>
        <el-col :span="6" v-if="trendData?.prediction">
          <div class="stat-item">
            <span class="label">预测趋势</span>
            <el-tag :type="trendData.prediction.trend === 'up' ? 'success' : 'danger'">
              {{ trendData.prediction.trend === 'up' ? '上升' : '下降' }}
            </el-tag>
          </div>
        </el-col>
      </el-row>

      <div class="chart-container" style="margin-top: 30px;">
        <v-chart :option="chartOption" :autoresize="true" style="height: 400px;" />
      </div>
    </el-card>

    <el-skeleton :rows="10" animated v-else-if="loading" />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent, MarkLineComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { useIndicatorStore } from '../stores';
import { storeToRefs } from 'pinia';

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent, MarkLineComponent]);

const route = useRoute();
const indicatorStore = useIndicatorStore();
const { loading } = storeToRefs(indicatorStore);

const indicatorCode = computed(() => route.params.code as string);
const indicatorData = ref<any>(null);
const trendData = ref<any>(null);

const loadData = async () => {
  try {
    const [data, trend] = await Promise.all([
      indicatorStore.fetchIndicatorData(indicatorCode.value),
      indicatorStore.fetchTrend(indicatorCode.value)
    ]);
    indicatorData.value = data;
    trendData.value = trend;
  } catch (e) {
    console.error('加载数据失败:', e);
  }
};

onMounted(() => {
  loadData();
});

watch(indicatorCode, () => {
  loadData();
});

const refresh = async () => {
  await indicatorStore.fetchIndicatorData(indicatorCode.value, true);
  await loadData();
};

const formatValue = (val?: number) => {
  if (val === undefined || val === null) return '--';
  return val.toFixed(2);
};

const formatChange = (change?: number) => {
  if (change === undefined || change === null) return '--';
  return (change > 0 ? '+' : '') + change.toFixed(2) + '%';
};

const getChangeClass = (change?: number) => {
  if (change === undefined || change === null) return '';
  return change >= 0 ? 'positive' : 'negative';
};

const getTrendType = (trend: string) => {
  if (trend === 'uptrend') return 'success';
  if (trend === 'downtrend') return 'danger';
  return 'info';
};

const getTrendText = (trend: string) => {
  if (trend === 'uptrend') return '上升';
  if (trend === 'downtrend') return '下降';
  return '平稳';
};

const chartOption = computed(() => {
  if (!indicatorData.value?.data) return {};
  
  const data = indicatorData.value.data.map((d: any) => ({
    date: new Date(d.date).toLocaleDateString('zh-CN'),
    value: d.value
  })).reverse();

  return {
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { 
      type: 'category', 
      data: data.map((d: any) => d.date),
      axisLabel: { color: '#a0aec0' }
    },
    yAxis: { 
      type: 'value', 
      axisLabel: { color: '#a0aec0' },
      splitLine: { lineStyle: { color: '#2d2d44' } }
    },
    series: [{
      data: data.map((d: any) => d.value),
      type: 'line',
      smooth: true,
      lineStyle: { color: '#409eff', width: 2 },
      areaStyle: { color: 'rgba(64, 158, 255, 0.15)' },
      markPoint: {
        data: [
          { type: 'max', name: '最大值' },
          { type: 'min', name: '最小值' }
        ]
      }
    }]
  };
});
</script>

<style scoped>
.indicator-detail {
  padding: 0;
}

.back-button {
  margin-bottom: 20px;
  background-color: #1a1a2e;
  border-color: #2d2d44;
  color: #fff;
}

.detail-card {
  background-color: #1a1a2e;
  border: 1px solid #2d2d44;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #fff;
}

.card-header h2 {
  margin: 0;
  font-size: 24px;
}

.code {
  color: #666;
  font-size: 14px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding: 20px;
  background: #0f0f1a;
  border-radius: 8px;
}

.stat-item .label {
  color: #666;
  font-size: 14px;
}

.stat-item .value {
  font-size: 24px;
  font-weight: bold;
  color: #fff;
}

.stat-item .value.positive {
  color: #67c23a;
}

.stat-item .value.negative {
  color: #f56c6c;
}

.stat-item .unit {
  color: #666;
  font-size: 14px;
}
</style>
