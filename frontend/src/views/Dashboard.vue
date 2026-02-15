<template>
  <div class="dashboard">
    <el-row :gutter="24" class="summary-cards">
      <el-col :span="8" v-for="item in summary" :key="item.code">
        <el-card class="summary-card" shadow="hover">
          <div class="card-header">
            <span class="card-title">{{ item.name }}</span>
            <el-tag :type="getTrendType(item.trend)" size="small" effect="plain">{{ getTrendText(item.trend) }}</el-tag>
          </div>
          <div class="card-value">
            <span class="value">{{ formatValue(item.value) }}</span>
            <span class="unit">{{ item.unit }}</span>
          </div>
          <div class="card-change" :class="getChangeClass(item.change)">
            <span>{{ formatChange(item.change) }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="12">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <div class="card-header">
              <span class="chart-title">GDP走势</span>
              <el-button type="primary" size="small" @click="refreshData('gdp')">刷新</el-button>
            </div>
          </template>
          <v-chart :option="gdpChartOption" :autoresize="true" style="height: 350px;" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span class="chart-title">CPI走势</span>
          </template>
          <v-chart :option="cpiChartOption" :autoresize="true" style="height: 350px;" />
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="chart-card" shadow="never">
          <template #header>
            <span class="chart-title">PMI走势</span>
          </template>
          <v-chart :option="pmiChartOption" :autoresize="true" style="height: 350px;" />
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart, BarChart, PieChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { useIndicatorStore } from '../stores';
import { storeToRefs } from 'pinia';

use([CanvasRenderer, LineChart, BarChart, PieChart, GridComponent, TooltipComponent, LegendComponent]);

const indicatorStore = useIndicatorStore();
const { summary, loading } = storeToRefs(indicatorStore);

const gdpData = ref<{ date: string; value: number }[]>([]);
const cpiData = ref<{ date: string; value: number }[]>([]);
const pmiData = ref<{ date: string; value: number }[]>([]);

onMounted(async () => {
  await indicatorStore.fetchSummary();
  await loadChartData();
});

const loadChartData = async () => {
  try {
    const [gdp, cpi, pmi] = await Promise.all([
      indicatorStore.fetchIndicatorData('gdp'),
      indicatorStore.fetchIndicatorData('cpi'),
      indicatorStore.fetchIndicatorData('pmi')
    ]);
    
    if (gdp?.data?.data) {
      gdpData.value = gdp.data.data.map((d: any) => ({
        date: new Date(d.date).toLocaleDateString('zh-CN'),
        value: d.value
      })).reverse();
    }
    if (cpi?.data?.data) {
      cpiData.value = cpi.data.data.map((d: any) => ({
        date: new Date(d.date).toLocaleDateString('zh-CN'),
        value: d.value
      })).reverse();
    }
    if (pmi?.data?.data) {
      pmiData.value = pmi.data.data.map((d: any) => ({
        date: new Date(d.date).toLocaleDateString('zh-CN'),
        value: d.value
      })).reverse();
    }
  } catch (e) {
    console.error('加载图表数据失败:', e);
  }
};

const refreshData = async (code: string) => {
  await indicatorStore.fetchIndicatorData(code, true);
  await loadChartData();
};

const formatValue = (val?: number) => {
  if (val === undefined || val === null) return '--';
  return val.toFixed(2);
};

const formatChange = (change?: number) => {
  if (change === undefined || change === null) return '';
  return (change > 0 ? '+' : '') + change.toFixed(2) + '%';
};

const getTrendType = (trend: string) => {
  if (trend === 'uptrend') return 'success';
  if (trend === 'downtrend') return 'danger';
  return 'info';
};

const getTrendText = (trend: string) => {
  if (trend === 'uptrend') return '↑ 上升';
  if (trend === 'downtrend') return '↓ 下降';
  return '→ 平稳';
};

const getChangeClass = (change?: number) => {
  if (change === undefined || change === null) return '';
  return change >= 0 ? 'positive' : 'negative';
};

const gdpChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: gdpData.value.map(d => d.date), axisLabel: { color: '#606266' } },
  yAxis: { type: 'value', axisLabel: { color: '#606266' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
  series: [{
    data: gdpData.value.map(d => d.value),
    type: 'line',
    smooth: true,
    lineStyle: { color: '#409eff', width: 3 },
    areaStyle: { color: 'rgba(64, 158, 255, 0.1)' },
    itemStyle: { color: '#409eff' }
  }]
}));

const cpiChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: cpiData.value.map(d => d.date), axisLabel: { color: '#606266' } },
  yAxis: { type: 'value', axisLabel: { color: '#606266' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
  series: [{
    data: cpiData.value.map(d => d.value),
    type: 'bar',
    barWidth: '50%',
    itemStyle: { color: '#e6a23c', borderRadius: [4, 4, 0, 0] }
  }]
}));

const pmiChartOption = computed(() => ({
  tooltip: { trigger: 'axis' },
  grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
  xAxis: { type: 'category', data: pmiData.value.map(d => d.date), axisLabel: { color: '#606266' } },
  yAxis: { type: 'value', axisLabel: { color: '#606266' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
  series: [{
    data: pmiData.value.map(d => d.value),
    type: 'line',
    smooth: true,
    lineStyle: { color: '#67c23a', width: 3 },
    itemStyle: { color: '#67c23a' },
    markLine: {
      data: [{ yAxis: 50, name: '荣枯线' }],
      lineStyle: { color: '#909399', type: 'dashed' },
      label: { color: '#909399' }
    }
  }]
}));
</script>

<style scoped>
.dashboard {
  padding: 0;
}

.summary-cards {
  margin-left: 0 !important;
  margin-right: 0 !important;
}

.summary-card {
  transition: all 0.3s;
}

.summary-card:hover {
  transform: translateY(-4px);
}

.summary-card :deep(.el-card__body) {
  padding: 24px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-title {
  color: #909399;
  font-size: 14px;
}

.card-value {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.value {
  font-size: 32px;
  font-weight: 600;
  color: #303133;
}

.unit {
  color: #909399;
  font-size: 14px;
}

.card-change {
  margin-top: 12px;
  font-size: 14px;
  font-weight: 500;
}

.card-change.positive {
  color: #67c23a;
}

.card-change.negative {
  color: #f56c6c;
}

.chart-card :deep(.el-card__header) {
  padding: 16px 20px;
  border-bottom: 1px solid #f0f0f0;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
</style>
