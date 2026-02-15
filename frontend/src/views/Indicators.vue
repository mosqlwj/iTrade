<template>
  <div class="indicators-page">
    <el-card class="filter-card">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input v-model="searchKeyword" placeholder="搜索指标..." prefix-icon="Search" clearable />
        </el-col>
        <el-col :span="6">
          <el-select v-model="categoryFilter" placeholder="选择分类" clearable style="width: 100%;">
            <el-option label="全部" value="" />
            <el-option label="经济增长" value="经济增长" />
            <el-option label="物价水平" value="物价水平" />
            <el-option label="经济景气" value="经济景气" />
            <el-option label="货币金融" value="货币金融" />
          </el-select>
        </el-col>
      </el-row>
    </el-card>

    <el-row :gutter="24" style="margin-top: 24px;">
      <el-col :span="8" v-for="indicator in filteredIndicators" :key="indicator.code">
        <el-card class="indicator-card" shadow="hover" @click="goToDetail(indicator.code)">
          <div class="indicator-header">
            <div class="indicator-icon" :style="{ background: getCategoryBg(indicator.category) }">
              <el-icon :size="20" :color="getCategoryColor(indicator.category)">
                <TrendCharts v-if="indicator.category === '经济增长'" />
                <Money v-else-if="indicator.category === '货币金融'" />
                <DataLine v-else-if="indicator.category === '物价水平'" />
                <PieChart v-else />
              </el-icon>
            </div>
            <el-tag size="small" :type="getCategoryType(indicator.category)" effect="plain">
              {{ indicator.category }}
            </el-tag>
          </div>
          <h3 class="indicator-name">{{ indicator.name }}</h3>
          <p class="indicator-desc">{{ indicator.description }}</p>
          <div class="indicator-meta">
            <span><el-icon><Refresh /></el-icon> {{ indicator.update_frequency }}</span>
            <span><el-icon><Coordinate /></el-icon> {{ indicator.unit }}</span>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { indicatorApi } from '../api';
import type { Indicator } from '../types';

const router = useRouter();

const searchKeyword = ref('');
const categoryFilter = ref('');
const indicators = ref<Indicator[]>([]);

onMounted(async () => {
  try {
    const res = await indicatorApi.getIndicators();
    indicators.value = res.data.items;
  } catch (e) {
    console.error('获取指标列表失败:', e);
  }
});

const filteredIndicators = computed(() => {
  return indicators.value.filter(item => {
    const matchKeyword = !searchKeyword.value || 
      item.name.includes(searchKeyword.value) || 
      item.code.includes(searchKeyword.value);
    const matchCategory = !categoryFilter.value || item.category === categoryFilter.value;
    return matchKeyword && matchCategory;
  });
});

const goToDetail = (code: string) => {
  router.push(`/indicators/${code}`);
};

const getCategoryColor = (category: string) => {
  const colors: Record<string, string> = {
    '经济增长': '#409eff',
    '物价水平': '#e6a23c',
    '经济景气': '#67c23a',
    '货币金融': '#f56c6c',
  };
  return colors[category] || '#409eff';
};

const getCategoryBg = (category: string) => {
  const bgs: Record<string, string> = {
    '经济增长': '#ecf5ff',
    '物价水平': '#fdf6ec',
    '经济景气': '#f0f9eb',
    '货币金融': '#fef0f0',
  };
  return bgs[category] || '#f5f7fa';
};

const getCategoryType = (category: string) => {
  const types: Record<string, string> = {
    '经济增长': 'primary',
    '物价水平': 'warning',
    '经济景气': 'success',
    '货币金融': 'danger',
  };
  return types[category] || 'primary';
};
</script>

<style scoped>
.indicators-page {
  padding: 0;
}

.filter-card {
  margin-bottom: 0;
}

.indicator-card {
  margin-bottom: 24px;
  cursor: pointer;
  transition: all 0.3s;
  border-color: #ebeef5;
}

.indicator-card:hover {
  transform: translateY(-4px);
  border-color: #409eff;
}

.indicator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.indicator-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.indicator-name {
  margin: 0 0 10px;
  font-size: 17px;
  font-weight: 600;
  color: #303133;
}

.indicator-desc {
  margin: 0 0 16px;
  font-size: 14px;
  color: #909399;
  line-height: 1.6;
  min-height: 44px;
}

.indicator-meta {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  color: #c0c4cc;
}

.indicator-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}
</style>
