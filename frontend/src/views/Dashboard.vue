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
          <div class="card-date" v-if="item.latest_date">
            <span>最新数据: {{ item.latest_date }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <div v-if="loading" class="loading-container">
      <el-icon class="is-loading"><Loading /></el-icon>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from 'vue';
import { Loading } from '@element-plus/icons-vue';
import { useIndicatorStore } from '../stores';
import { storeToRefs } from 'pinia';

const indicatorStore = useIndicatorStore();
const { summary, loading } = storeToRefs(indicatorStore);

onMounted(async () => {
  await indicatorStore.fetchSummary();
});

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

.card-date {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
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
