<template>
  <div class="alerts-page">
    <el-card class="create-card">
      <template #header>
        <span class="card-title">创建预警</span>
      </template>
      <el-form :model="alertForm" inline>
        <el-form-item label="指标">
          <el-select v-model="alertForm.indicator_code" placeholder="选择指标" style="width: 140px;">
            <el-option v-for="ind in indicators" :key="ind.code" :label="ind.name" :value="ind.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="条件">
          <el-select v-model="alertForm.condition" placeholder="选择条件" style="width: 100px;">
            <el-option label="大于" value="above" />
            <el-option label="小于" value="below" />
            <el-option label="等于" value="equals" />
          </el-select>
        </el-form-item>
        <el-form-item label="阈值">
          <el-input-number v-model="alertForm.threshold" :precision="2" :step="0.1" style="width: 120px;" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleCreate">创建预警</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="list-card" style="margin-top: 24px;">
      <template #header>
        <div class="card-header">
          <span class="card-title">我的预警</span>
          <el-button type="success" @click="checkAlerts" :loading="checking">检查预警</el-button>
        </div>
      </template>
      
      <el-table :data="alerts" stripe v-if="alerts.length">
        <el-table-column prop="indicator_code" label="指标" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.indicator_code.toUpperCase() }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="condition" label="条件" width="120">
          <template #default="{ row }">
            <span v-if="row.condition === 'above'">大于</span>
            <span v-else-if="row.condition === 'below'">小于</span>
            <span v-else>等于</span>
          </template>
        </el-table-column>
        <el-table-column prop="threshold" label="阈值" width="100" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
              {{ row.is_active ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_triggered" label="最后触发" width="180">
          <template #default="{ row }">
            {{ row.last_triggered ? new Date(row.last_triggered).toLocaleString('zh-CN') : '未触发' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="{ row }">
            <el-button type="danger" size="small" @click="handleDelete(row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-empty description="暂无预警规则" v-else />
    </el-card>

    <el-dialog v-model="showTriggered" title="触发的预警" width="500px">
      <el-alert v-for="item in triggeredAlerts" :key="item.alert_id" :title="`${item.indicator_code} 达到 ${item.current_value}`" type="warning" style="margin-bottom: 10px;">
        <template #default>
          条件: {{ item.condition === 'above' ? '>' : item.condition === 'below' ? '<' : '=' }} {{ item.threshold }}
        </template>
      </el-alert>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage } from 'element-plus';
import { useAlertStore } from '../stores';
import { storeToRefs } from 'pinia';

const alertStore = useAlertStore();
const { alerts } = storeToRefs(alertStore);

const indicators = ref([
  { code: 'gdp', name: 'GDP' },
  { code: 'cpi', name: 'CPI' },
  { code: 'pmi', name: 'PMI' }
]);

const alertForm = reactive({
  indicator_code: '',
  condition: 'above',
  threshold: 0
});

const checking = ref(false);
const showTriggered = ref(false);
const triggeredAlerts = ref<any[]>([]);

onMounted(() => {
  alertStore.fetchAlerts();
});

const handleCreate = async () => {
  if (!alertForm.indicator_code) {
    ElMessage.warning('请选择指标');
    return;
  }
  try {
    await alertStore.createAlert(alertForm);
    ElMessage.success('创建成功');
    alertForm.indicator_code = '';
    alertForm.threshold = 0;
  } catch (e) {
    ElMessage.error('创建失败');
  }
};

const handleDelete = async (id: number) => {
  try {
    await alertStore.deleteAlert(id);
    ElMessage.success('删除成功');
  } catch (e) {
    ElMessage.error('删除失败');
  }
};

const checkAlerts = async () => {
  checking.value = true;
  try {
    const res = await alertStore.checkAlerts();
    triggeredAlerts.value = res.data || [];
    if (triggeredAlerts.value.length > 0) {
      showTriggered.value = true;
    } else {
      ElMessage.info('暂无触发的预警');
    }
  } catch (e) {
    ElMessage.error('检查失败');
  } finally {
    checking.value = false;
  }
};
</script>

<style scoped>
.alerts-page {
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
</style>
