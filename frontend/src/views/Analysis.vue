<template>
  <div class="analysis-page">
    <el-card class="config-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-form-item label="选择指标">
            <el-select v-model="selectedIndicators" multiple placeholder="选择指标进行对比" style="width: 100%">
              <el-option
                v-for="ind in availableIndicators"
                :key="ind.code"
                :label="ind.name"
                :value="ind.code"
              />
            </el-select>
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="开始日期">
            <el-date-picker v-model="startDate" type="date" placeholder="选择开始日期" style="width: 100%" />
          </el-form-item>
        </el-col>
        <el-col :span="6">
          <el-form-item label="结束日期">
            <el-date-picker v-model="endDate" type="date" placeholder="选择结束日期" style="width: 100%" />
          </el-form-item>
        </el-col>
        <el-col :span="4">
          <el-button type="primary" @click="compare" :loading="loading" style="margin-top: 4px;">对比分析</el-button>
        </el-col>
      </el-row>
    </el-card>

    <el-card class="result-card" style="margin-top: 24px;" v-if="compareResult">
      <template #header>
        <span class="card-title">对比分析结果</span>
      </template>
      <v-chart :option="compareChartOption" :autoresize="true" style="height: 450px;" />
    </el-card>

    <el-row :gutter="24" style="margin-top: 24px;" v-if="compareResult">
      <el-col :span="12">
        <el-card class="stat-card">
          <template #header>
            <span class="card-title">相关性分析</span>
          </template>
          <div class="correlation-matrix">
            <p style="color: #909399; text-align: center;">多指标相关性矩阵</p>
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="stat-card">
          <template #header>
            <span class="card-title">统计摘要</span>
          </template>
          <el-table :data="statsData" stripe style="width: 100%">
            <el-table-column prop="indicator" label="指标" />
            <el-table-column prop="latest" label="最新值" />
            <el-table-column prop="max" label="最大值" />
            <el-table-column prop="min" label="最小值" />
            <el-table-column prop="avg" label="平均值" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { indicatorApi } from '../api';

use([CanvasRenderer, LineChart, GridComponent, TooltipComponent, LegendComponent]);

const selectedIndicators = ref<string[]>(['gdp', 'cpi']);
const startDate = ref<string>('');
const endDate = ref<string>('');
const loading = ref(false);
const compareResult = ref<any>(null);

const availableIndicators = ref([
  { code: 'gdp', name: 'GDP' },
  { code: 'cpi', name: 'CPI' },
  { code: 'pmi', name: 'PMI' }
]);

const compare = async () => {
  if (selectedIndicators.value.length < 2) {
    return;
  }
  loading.value = true;
  try {
    const res = await indicatorApi.compareIndicators(
      selectedIndicators.value,
      startDate.value ? new Date(startDate.value).toISOString().split('T')[0] : undefined,
      endDate.value ? new Date(endDate.value).toISOString().split('T')[0] : undefined
    );
    compareResult.value = res.data;
  } catch (e) {
    console.error('对比分析失败:', e);
  } finally {
    loading.value = false;
  }
};

const compareChartOption = computed(() => {
  if (!compareResult.value) return {};
  
  const series: any[] = [];
  const legend: string[] = [];
  const colors = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#909399'];
  
  let idx = 0;
  for (const [code, data] of Object.entries(compareResult.value)) {
    const indicator = availableIndicators.value.find(i => i.code === code);
    const name = indicator?.name || code;
    legend.push(name);
    
    const chartData = (data as any).data.reverse().map((d: any) => ({
      date: new Date(d.date).toLocaleDateString('zh-CN'),
      value: d.value
    }));
    
    series.push({
      name,
      type: 'line',
      data: chartData.map((d: any) => d.value),
      smooth: true,
      lineStyle: { color: colors[idx % colors.length], width: 2 },
      yAxisIndex: idx > 2 ? 1 : 0
    });
    idx++;
  }
  
  const dates = series[0]?.data?.map((_: any, i: number) => {
    if (!compareResult.value[selectedIndicators.value[0]]) return '';
    const dataArr = compareResult.value[selectedIndicators.value[0]].data;
    return dataArr[i] ? new Date(dataArr[i].date).toLocaleDateString('zh-CN') : '';
  }) || [];

  return {
    tooltip: { trigger: 'axis' },
    legend: { data: legend, textStyle: { color: '#606266' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: dates, axisLabel: { color: '#606266' } },
    yAxis: [
      { type: 'value', axisLabel: { color: '#606266' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
      { type: 'value', axisLabel: { color: '#606266' }, splitLine: { show: false } }
    ],
    series
  };
});

const statsData = computed(() => {
  if (!compareResult.value) return [];
  
  return Object.entries(compareResult.value).map(([code, data]: [string, any]) => {
    const values = data.data.map((d: any) => d.value);
    return {
      indicator: code.toUpperCase(),
      latest: values[values.length - 1]?.toFixed(2),
      max: Math.max(...values).toFixed(2),
      min: Math.min(...values).toFixed(2),
      avg: (values.reduce((a: number, b: number) => a + b, 0) / values.length).toFixed(2)
    };
  });
});
</script>

<style scoped>
.analysis-page {
  padding: 0;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
</style>
