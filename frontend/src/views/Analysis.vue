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

    <el-divider content-position="left">
      <span class="section-title">📊 经济指标参考指南</span>
    </el-divider>

    <el-tabs v-model="activeTab" class="indicator-tabs">
      <el-tab-pane label="国民经济核算" name="macro">
        <div class="indicator-grid">
          <el-card v-for="item in indicatorData.macro" :key="item.name" class="indicator-card" shadow="hover">
            <template #header>
              <div class="indicator-header">
                <span class="indicator-name">{{ item.name }}</span>
                <el-tag size="small" type="success">宏观经济</el-tag>
              </div>
            </template>
            <div class="indicator-content">
              <div class="indicator-item">
                <span class="label">📖 含义：</span>
                <span class="value">{{ item.meaning }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📡 来源：</span>
                <span class="value">{{ item.source }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📅 频率：</span>
                <span class="value">{{ item.frequency }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📈 范围：</span>
                <span class="value">{{ item.range }}</span>
              </div>
              <div class="indicator-item impact">
                <span class="label">🎯 影响：</span>
                <span class="value">{{ item.impact }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="货币金融" name="finance">
        <div class="indicator-grid">
          <el-card v-for="item in indicatorData.finance" :key="item.name" class="indicator-card" shadow="hover">
            <template #header>
              <div class="indicator-header">
                <span class="indicator-name">{{ item.name }}</span>
                <el-tag size="small" type="warning">货币金融</el-tag>
              </div>
            </template>
            <div class="indicator-content">
              <div class="indicator-item">
                <span class="label">📖 含义：</span>
                <span class="value">{{ item.meaning }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📡 来源：</span>
                <span class="value">{{ item.source }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📅 频率：</span>
                <span class="value">{{ item.frequency }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📈 范围：</span>
                <span class="value">{{ item.range }}</span>
              </div>
              <div class="indicator-item impact">
                <span class="label">🎯 影响：</span>
                <span class="value">{{ item.impact }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="通胀指标" name="inflation">
        <div class="indicator-grid">
          <el-card v-for="item in indicatorData.inflation" :key="item.name" class="indicator-card" shadow="hover">
            <template #header>
              <div class="indicator-header">
                <span class="indicator-name">{{ item.name }}</span>
                <el-tag size="small" type="danger">通胀</el-tag>
              </div>
            </template>
            <div class="indicator-content">
              <div class="indicator-item">
                <span class="label">📖 含义：</span>
                <span class="value">{{ item.meaning }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📡 来源：</span>
                <span class="value">{{ item.source }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📅 频率：</span>
                <span class="value">{{ item.frequency }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📈 范围：</span>
                <span class="value">{{ item.range }}</span>
              </div>
              <div class="indicator-item impact">
                <span class="label">🎯 影响：</span>
                <span class="value">{{ item.impact }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="国际贸易" name="trade">
        <div class="indicator-grid">
          <el-card v-for="item in indicatorData.trade" :key="item.name" class="indicator-card" shadow="hover">
            <template #header>
              <div class="indicator-header">
                <span class="indicator-name">{{ item.name }}</span>
                <el-tag size="small" type="info">国际贸易</el-tag>
              </div>
            </template>
            <div class="indicator-content">
              <div class="indicator-item">
                <span class="label">📖 含义：</span>
                <span class="value">{{ item.meaning }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📡 来源：</span>
                <span class="value">{{ item.source }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📅 频率：</span>
                <span class="value">{{ item.frequency }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📈 范围：</span>
                <span class="value">{{ item.range }}</span>
              </div>
              <div class="indicator-item impact">
                <span class="label">🎯 影响：</span>
                <span class="value">{{ item.impact }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="市场情绪" name="sentiment">
        <div class="indicator-grid">
          <el-card v-for="item in indicatorData.sentiment" :key="item.name" class="indicator-card" shadow="hover">
            <template #header>
              <div class="indicator-header">
                <span class="indicator-name">{{ item.name }}</span>
                <el-tag size="small">市场情绪</el-tag>
              </div>
            </template>
            <div class="indicator-content">
              <div class="indicator-item">
                <span class="label">📖 含义：</span>
                <span class="value">{{ item.meaning }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📡 来源：</span>
                <span class="value">{{ item.source }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📅 频率：</span>
                <span class="value">{{ item.frequency }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📈 范围：</span>
                <span class="value">{{ item.range }}</span>
              </div>
              <div class="indicator-item impact">
                <span class="label">🎯 影响：</span>
                <span class="value">{{ item.impact }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>

      <el-tab-pane label="国际经济" name="global">
        <div class="indicator-grid">
          <el-card v-for="item in indicatorData.global" :key="item.name" class="indicator-card" shadow="hover">
            <template #header>
              <div class="indicator-header">
                <span class="indicator-name">{{ item.name }}</span>
                <el-tag size="small" type="danger">国际</el-tag>
              </div>
            </template>
            <div class="indicator-content">
              <div class="indicator-item">
                <span class="label">📖 含义：</span>
                <span class="value">{{ item.meaning }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📡 来源：</span>
                <span class="value">{{ item.source }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📅 频率：</span>
                <span class="value">{{ item.frequency }}</span>
              </div>
              <div class="indicator-item">
                <span class="label">📈 范围：</span>
                <span class="value">{{ item.range }}</span>
              </div>
              <div class="indicator-item impact">
                <span class="label">🎯 影响：</span>
                <span class="value">{{ item.impact }}</span>
              </div>
            </div>
          </el-card>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-card class="framework-card" style="margin-top: 24px;">
      <template #header>
        <span class="card-title">📈 综合分析框架</span>
      </template>
      <el-row :gutter="20">
        <el-col :span="8">
          <div class="framework-item">
            <div class="framework-title">💧 流动性框架</div>
            <div class="framework-content">
              M2 → 社融 → 利率 → A股估值<br/>
              <span class="highlight">宽松利好A股</span>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="framework-item">
            <div class="framework-title">💰 盈利框架</div>
            <div class="framework-content">
              GDP → 企业利润 → A股盈利<br/>
              <span class="highlight">增长推动上涨</span>
            </div>
          </div>
        </el-col>
        <el-col :span="8">
          <div class="framework-item">
            <div class="framework-title">🌍 风险偏好框架</div>
            <div class="framework-content">
              美元 → 外资 → 北向资金<br/>
              <span class="highlight">外资流入利好</span>
            </div>
          </div>
        </el-col>
      </el-row>
      <el-divider />
      <div class="cycle-tips">
        <el-alert type="info" :closable="false">
          <template #title>
            <span>🔄 经济周期与投资建议</span>
          </template>
          <div class="cycle-content">
            <p><strong>复苏期</strong>：GDP↑ + CPI稳定 + 利率↓ → 增配周期股（金融、地产、有色）</p>
            <p><strong>过热期</strong>：GDP↑ + CPI↑ + 利率↑ → 减配股票，增配商品</p>
            <p><strong>衰退期</strong>：GDP↓ + CPI↓ + 利率↓ → 增配债券，减少股票</p>
            <p><strong>萧条期</strong>：政策刺激 → 逐步增配股票，等待复苏</p>
          </div>
        </el-alert>
      </div>
    </el-card>
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
const activeTab = ref('macro');

const availableIndicators = ref([
  { code: 'gdp', name: 'GDP' },
  { code: 'cpi', name: 'CPI' },
  { code: 'pmi', name: 'PMI' }
]);

const indicatorData = {
  macro: [
    {
      name: 'GDP (国内生产总值)',
      meaning: '衡量一国经济总量的核心指标，反映经济增长速度和总体规模',
      source: '国家统计局',
      frequency: '季度',
      range: '2%-15%',
      impact: 'GDP增长反映经济活力，企业盈利预期上升，A股上涨。2020年Q1 GDP同比-6.8%触底后A股反弹'
    },
    {
      name: 'PMI (采购经理指数)',
      meaning: '制造业景气度先行指标，50为荣枯线，反映企业扩张或收缩',
      source: '中国物流与采购联合会',
      frequency: '月度',
      range: '35-65 (50为荣枯)',
      impact: '>50制造业扩张，利好周期股；<50衰退风险。2024年1月PMI降至49.2，A股回调'
    }
  ],
  finance: [
    {
      name: 'M2 (广义货币)',
      meaning: '货币供应量，反映市场流动性充裕程度',
      source: '央行',
      frequency: '月度',
      range: '年增5%-15%',
      impact: 'M2增速上升提供流动性，利好A股。2020年M2同比增10.1%，A股走牛'
    },
    {
      name: '社融 (社会融资规模)',
      meaning: '实体经济从金融体系获得的资金总量，反映融资需求',
      source: '央行',
      frequency: '月度',
      range: '年增8%-15%',
      impact: '社融回暖反映融资需求旺盛，企业经营改善，利好股市'
    },
    {
      name: 'LPR (贷款市场报价利率)',
      meaning: '贷款利率基准，分为1年期和5年期以上品种',
      source: '央行',
      frequency: '月度',
      range: '1年期3.45%，5年期4.2%',
      impact: '降息降低融资成本，提升企业盈利预期，利好A股'
    },
    {
      name: '存款准备金率',
      meaning: '商业银行必须存放央行的准备金比例',
      source: '央行',
      frequency: '不定期',
      range: '大型机构10.5%-14.5%',
      impact: '降准释放流动性，增加市场资金供应，利好A股'
    }
  ],
  inflation: [
    {
      name: 'CPI (居民消费价格指数)',
      meaning: '衡量居民生活消费品和服务价格变动的指标',
      source: '国家统计局',
      frequency: '月度',
      range: '2%-5%温和通胀',
      impact: '温和上涨利好股市；>5%引发政策收紧担忧'
    },
    {
      name: 'PPI (工业生产者出厂价格指数)',
      meaning: '工业企业产品出厂价格变动，反映工业品价格水平',
      source: '国家统计局',
      frequency: '月度',
      range: '-5%~5%',
      impact: 'PPI上行利好周期股（钢铁、有色），下行利空'
    },
    {
      name: '核心CPI',
      meaning: '剔除食品能源后的通胀，更真实反映潜在通胀压力',
      source: '国家统计局',
      frequency: '月度',
      range: '1%-3%',
      impact: '持续高于2%可能引发央行收紧政策'
    }
  ],
  trade: [
    {
      name: '进出口贸易额',
      meaning: '对外贸易规模，反映国际市场需求和国内经济活力',
      source: '海关总署',
      frequency: '月度',
      range: '贸易顺差/逆差',
      impact: '贸易顺差扩大利好出口型企业'
    },
    {
      name: '人民币汇率',
      meaning: '人民币对外币的价值，反映货币强弱',
      source: '外汇交易中心',
      frequency: '日度',
      range: '6.3-7.5',
      impact: '人民币升值吸引外资流入，利好A股'
    },
    {
      name: '外汇储备',
      meaning: '国家持有的外币资产总额',
      source: '央行',
      frequency: '月度',
      range: '3万亿美元以上',
      impact: '外汇储备稳定支撑人民币，利于外资流入A股'
    }
  ],
  sentiment: [
    {
      name: '沪深300市盈率',
      meaning: '市场整体估值水平，衡量股票贵贱',
      source: '交易所',
      frequency: '日度',
      range: '10-25倍',
      impact: '估值处于历史低位时是抄底机会'
    },
    {
      name: '融资融券余额',
      meaning: '市场杠杆资金规模，反映投资者风险偏好',
      source: '交易所',
      frequency: '日度',
      range: '1-2万亿',
      impact: '融资余额上升反映市场情绪乐观，过高则风险积聚'
    },
    {
      name: '北向资金净流入',
      meaning: '外资通过沪深港通买入A股的金额',
      source: '港交所',
      frequency: '日度',
      range: '-50~200亿/日',
      impact: '外资持续流入反映对A股看好，利好A股'
    },
    {
      name: '股债收益差',
      meaning: '股票收益率与债券收益率的差值',
      source: '估算',
      frequency: '日度',
      range: '-2%~4%',
      impact: '差值扩大时股票相对债券更有配置价值'
    }
  ],
  global: [
    {
      name: '美国非农就业',
      meaning: '美国新增就业人数，反映美国经济状况',
      source: '美国劳工部',
      frequency: '月度',
      range: '新增10-30万人',
      impact: '好于预期利空A股（资本外流），差于预期利好A股'
    },
    {
      name: '美联储利率',
      meaning: '美元利率基准，影响全球资本流动',
      source: '美联储',
      frequency: '不定期',
      range: '0%-5.5%',
      impact: '美元加息资本外流利空A股，降息利好A股'
    },
    {
      name: '美元指数',
      meaning: '美元相对一篮子货币的强弱',
      source: 'ICE',
      frequency: '日度',
      range: '90-110',
      impact: '美元走强利空A股（资本外流），走弱利好A股'
    },
    {
      name: 'VIX恐慌指数',
      meaning: '衡量市场恐慌程度，也称"恐慌指数"',
      source: 'CBOE',
      frequency: '日度',
      range: '10-30',
      impact: 'VIX飙升往往伴随全球股市下跌，A股也可能承压'
    }
  ]
};

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

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.indicator-tabs {
  margin-top: 16px;
}

.indicator-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(400px, 1fr));
  gap: 16px;
  margin-top: 16px;
}

.indicator-card {
  border-radius: 8px;
}

.indicator-card :deep(.el-card__header) {
  padding: 12px 16px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.indicator-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.indicator-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.indicator-content {
  font-size: 13px;
  line-height: 1.8;
}

.indicator-item {
  margin-bottom: 8px;
  display: flex;
  flex-wrap: wrap;
}

.indicator-item .label {
  color: #606266;
  font-weight: 500;
  min-width: 60px;
}

.indicator-item .value {
  color: #303133;
  flex: 1;
}

.indicator-item.impact {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #ebeef5;
  background: #fdf6ec;
  padding: 12px;
  border-radius: 4px;
}

.indicator-item.impact .value {
  color: #e6a23c;
}

.framework-card :deep(.el-card__header) {
  background: #f0f9eb;
}

.framework-item {
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  height: 100%;
}

.framework-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 12px;
}

.framework-content {
  font-size: 13px;
  color: #606266;
  line-height: 1.8;
}

.framework-content .highlight {
  color: #409eff;
  font-weight: 600;
}

.cycle-tips {
  margin-top: 16px;
}

.cycle-content p {
  margin: 8px 0;
  font-size: 13px;
  color: #606266;
}

.cycle-content strong {
  color: #303133;
}
</style>
