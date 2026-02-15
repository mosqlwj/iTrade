<template>
  <div class="decision-page">
    <el-row :gutter="24">
      <el-col :span="24">
        <el-card class="summary-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">宏观经济环境评估</span>
              <el-button type="primary" size="small" @click="refreshAssessment">重新评估</el-button>
            </div>
          </template>
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="assessment-item">
                <div class="assessment-label">经济增长</div>
                <div class="assessment-value">
                  <el-tag :type="growthStatus.type" size="large" effect="plain">{{ growthStatus.text }}</el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="assessment-item">
                <div class="assessment-label">通胀水平</div>
                <div class="assessment-value">
                  <el-tag :type="inflationStatus.type" size="large" effect="plain">{{ inflationStatus.text }}</el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="assessment-item">
                <div class="assessment-label">经济景气</div>
                <div class="assessment-value">
                  <el-tag :type="monetaryStatus.type" size="large" effect="plain">{{ monetaryStatus.text }}</el-tag>
                </div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="assessment-item">
                <div class="assessment-label">综合评级</div>
                <div class="assessment-value">
                  <el-tag type="primary" size="large">{{ overallRating }}</el-tag>
                </div>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span class="card-title">GDP与CPI对比</span>
          </template>
          <v-chart :option="gdpCpiChartOption" :autoresize="true" style="height: 350px;" />
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <span class="card-title">PMI走势</span>
          </template>
          <v-chart :option="pmiChartOption" :autoresize="true" style="height: 350px;" />
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="24">
        <el-card class="advice-card">
          <template #header>
            <span class="card-title">投资建议</span>
          </template>
          <div class="advice-content">
            <el-alert
              v-for="(advice, index) in investmentAdvices"
              :key="index"
              :title="advice.title"
              :type="advice.type"
              :description="advice.description"
              show-icon
              :closable="false"
              style="margin-bottom: 12px;"
            />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="24">
        <el-card class="scenario-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">情景模拟</span>
              <el-switch v-model="enableSimulation" active-text="启用" inactive-text="关闭" />
            </div>
          </template>
          <el-row :gutter="20" v-if="enableSimulation">
            <el-col :span="8">
              <div class="scenario-item">
                <div class="scenario-title">乐观情景</div>
                <p>GDP增长 +2%，CPI维持当前水平</p>
                <el-tag type="success">建议: 增配权益类资产</el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="scenario-item">
                <div class="scenario-title">基准情景</div>
                <p>GDP增长维持当前，CPI小幅上升</p>
                <el-tag type="warning">建议: 均衡配置</el-tag>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="scenario-item">
                <div class="scenario-title">悲观情景</div>
                <p>GDP增长-1%，CPI上升</p>
                <el-tag type="danger">建议: 增加债券配置</el-tag>
              </div>
            </el-col>
          </el-row>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { use } from 'echarts/core';
import { CanvasRenderer } from 'echarts/renderers';
import { LineChart, BarChart } from 'echarts/charts';
import { GridComponent, TooltipComponent, LegendComponent } from 'echarts/components';
import VChart from 'vue-echarts';
import { useIndicatorStore } from '../stores';
import { storeToRefs } from 'pinia';

use([CanvasRenderer, LineChart, BarChart, GridComponent, TooltipComponent, LegendComponent]);

const indicatorStore = useIndicatorStore();
const { summary } = storeToRefs(indicatorStore);

const enableSimulation = ref(false);
const gdpData = ref<any>(null);
const cpiData = ref<any>(null);
const pmiData = ref<any>(null);

onMounted(async () => {
  await indicatorStore.fetchSummary();
  await loadData();
});

const loadData = async () => {
  try {
    const [gdp, cpi, pmi] = await Promise.all([
      indicatorStore.fetchIndicatorData('gdp'),
      indicatorStore.fetchIndicatorData('cpi'),
      indicatorStore.fetchIndicatorData('pmi')
    ]);
    gdpData.value = gdp?.data;
    cpiData.value = cpi?.data;
    pmiData.value = pmi?.data;
  } catch (e) {
    console.error('加载数据失败:', e);
  }
};

const refreshAssessment = async () => {
  await loadData();
};

const growthStatus = computed(() => {
  const gdp = summary.value.find(s => s.code === 'gdp');
  if (!gdp || gdp.value === null) return { type: 'info', text: '暂无数据' };
  if (gdp.value > 5) return { type: 'success', text: '强劲' };
  if (gdp.value > 0) return { type: 'warning', text: '温和' };
  return { type: 'danger', text: '放缓' };
});

const inflationStatus = computed(() => {
  const cpi = summary.value.find(s => s.code === 'cpi');
  if (!cpi || cpi.value === null) return { type: 'info', text: '暂无数据' };
  if (cpi.value > 3) return { type: 'danger', text: '通胀' };
  if (cpi.value > 0) return { type: 'success', text: '温和' };
  return { type: 'warning', text: '通缩风险' };
});

const monetaryStatus = computed(() => {
  const pmi = summary.value.find(s => s.code === 'pmi');
  if (!pmi || pmi.value === null) return { type: 'info', text: '暂无数据' };
  if (pmi.value > 50) return { type: 'success', text: '扩张' };
  if (pmi.value > 45) return { type: 'warning', text: '收缩' };
  return { type: 'danger', text: '萎缩' };
});

const overallRating = computed(() => {
  const growth = growthStatus.value.text;
  const inflation = inflationStatus.value.text;
  const monetary = monetaryStatus.value.text;
  
  if (growth === '强劲' && inflation === '温和' && monetary === '扩张') return '看好';
  if (growth === '放缓' || inflation === '通胀' || monetary === '萎缩') return '谨慎';
  return '中性';
});

const investmentAdvices = computed(() => {
  const rating = overallRating.value;
  const advices = [];
  
  if (rating === '看好') {
    advices.push(
      { title: '权益市场', type: 'success', description: '经济基本面良好，建议增加股票配置' },
      { title: '行业配置', type: 'success', description: '关注消费、科技、金融等周期板块' },
      { title: '债券配置', type: 'warning', description: '可适当降低债券比例' }
    );
  } else if (rating === '谨慎') {
    advices.push(
      { title: '权益市场', type: 'danger', description: '建议降低股票仓位' },
      { title: '防御板块', type: 'warning', description: '关注公用事业、医药等防御性板块' },
      { title: '债券配置', type: 'success', description: '增加利率债配置' }
    );
  } else {
    advices.push(
      { title: '权益市场', type: 'warning', description: '保持均衡配置' },
      { title: '行业配置', type: 'info', description: '关注结构性机会' },
      { title: '债券配置', type: 'info', description: '维持中性策略' }
    );
  }
  
  return advices;
});

const gdpCpiChartOption = computed(() => {
  if (!gdpData.value?.data || !cpiData.value?.data) return {};
  
  const gdpArr = gdpData.value.data.slice(-8).reverse().map((d: any) => ({
    date: new Date(d.date).toLocaleDateString('zh-CN'),
    value: d.value
  }));
  const cpiArr = cpiData.value.data.slice(-8).reverse().map((d: any) => ({
    date: new Date(d.date).toLocaleDateString('zh-CN'),
    value: d.value
  }));

  return {
    tooltip: { trigger: 'axis' },
    legend: { data: ['GDP', 'CPI'], textStyle: { color: '#606266' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { 
      type: 'category', 
      data: gdpArr.map(d => d.date),
      axisLabel: { color: '#606266' }
    },
    yAxis: [
      { type: 'value', name: 'GDP', axisLabel: { color: '#606266' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
      { type: 'value', name: 'CPI', axisLabel: { color: '#606266' }, splitLine: { show: false } }
    ],
    series: [
      { name: 'GDP', type: 'line', data: gdpArr.map(d => d.value), smooth: true, lineStyle: { color: '#409eff', width: 2 } },
      { name: 'CPI', type: 'line', yAxisIndex: 1, data: cpiArr.map(d => d.value), smooth: true, lineStyle: { color: '#e6a23c', width: 2 } }
    ]
  };
});

const pmiChartOption = computed(() => {
  if (!pmiData.value?.data) return {};
  
  const pmiArr = pmiData.value.data.slice(-12).reverse().map((d: any) => ({
    date: new Date(d.date).toLocaleDateString('zh-CN'),
    value: d.value
  }));

  return {
    tooltip: { trigger: 'axis' },
    legend: { data: ['PMI'], textStyle: { color: '#606266' } },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { 
      type: 'category', 
      data: pmiArr.map(d => d.date),
      axisLabel: { color: '#606266' }
    },
    yAxis: { type: 'value', axisLabel: { color: '#606266' }, splitLine: { lineStyle: { color: '#f0f0f0' } } },
    series: [
      { name: 'PMI', type: 'line', data: pmiArr.map(d => d.value), smooth: true, lineStyle: { color: '#67c23a', width: 2 } }
    ]
  };
});
</script>

<style scoped>
.decision-page {
  padding: 0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.assessment-item {
  text-align: center;
  padding: 24px;
  background: #fafafa;
  border-radius: 12px;
}

.assessment-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 12px;
}

.assessment-value {
  font-size: 18px;
  font-weight: 600;
}

.advice-content {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.scenario-item {
  padding: 24px;
  background: #fafafa;
  border-radius: 12px;
  text-align: center;
}

.scenario-title {
  color: #303133;
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 12px;
}

.scenario-item p {
  color: #909399;
  margin-bottom: 16px;
  font-size: 14px;
}
</style>
