<template>
  <div class="app-container">
    <el-container v-if="isLoggedIn">
      <el-aside width="240px" class="sidebar">
        <div class="logo">
          <el-icon :size="26" color="#409eff"><TrendCharts /></el-icon>
          <span>宏观分析</span>
        </div>
        <el-menu
          :default-active="currentRoute"
          router
          class="sidebar-menu"
          background-color="#ffffff"
          text-color="#606266"
          active-text-color="#409eff"
          :collapse="false"
        >
          <el-menu-item index="/">
            <el-icon><DataBoard /></el-icon>
            <span>仪表盘</span>
          </el-menu-item>
          <el-menu-item index="/indicators">
            <el-icon><TrendCharts /></el-icon>
            <span>经济指标</span>
          </el-menu-item>
          <el-menu-item index="/analysis">
            <el-icon><Analysis /></el-icon>
            <span>多维分析</span>
          </el-menu-item>
          <el-menu-item index="/alerts">
            <el-icon><Bell /></el-icon>
            <span>预警中心</span>
          </el-menu-item>
          <el-menu-item index="/decision">
            <el-icon><Coin /></el-icon>
            <span>投资决策</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-container>
        <el-header class="header">
          <div class="header-left">
            <h2>{{ pageTitle }}</h2>
          </div>
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <el-avatar :size="32" style="background: #409eff;">
                  <el-icon><User /></el-icon>
                </el-avatar>
                <span class="username">{{ username }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        <el-main class="main-content">
          <router-view />
        </el-main>
      </el-container>
    </el-container>
    <router-view v-else />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useUserStore } from './stores';
import { storeToRefs } from 'pinia';

const route = useRoute();
const router = useRouter();
const userStore = useUserStore();
const { isLoggedIn, token } = storeToRefs(userStore);

const username = computed(() => {
  const stored = localStorage.getItem('username');
  return stored || '用户';
});

const currentRoute = computed(() => route.path);

const pageTitle = computed(() => {
  return (route.meta?.title as string) || '宏观经济分析平台';
});

const handleCommand = (command: string) => {
  if (command === 'logout') {
    userStore.logout();
    router.push('/login');
  }
};
</script>

<style scoped>
.app-container {
  height: 100vh;
  background-color: #f5f7fa;
}

.sidebar {
  background-color: #ffffff;
  height: 100vh;
  overflow: hidden;
  box-shadow: 2px 0 8px rgba(0, 0, 0, 0.04);
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 24px 20px;
  color: #303133;
  font-size: 18px;
  font-weight: 600;
  border-bottom: 1px solid #ebeef5;
}

.sidebar-menu {
  background-color: transparent !important;
  padding: 12px 8px;
}

.sidebar-menu .el-menu-item {
  height: 48px;
  line-height: 48px;
  margin: 4px 0;
  border-radius: 10px;
  transition: all 0.3s;
}

.sidebar-menu .el-menu-item:hover {
  background-color: #f0f2f5 !important;
}

.sidebar-menu .el-menu-item.is-active {
  background-color: #ecf5ff !important;
  color: #409eff !important;
}

.header {
  background-color: #ffffff;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 32px;
  border-bottom: 1px solid #ebeef5;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.02);
}

.header h2 {
  color: #303133;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  padding: 4px 12px;
  border-radius: 8px;
  transition: background-color 0.3s;
}

.user-info:hover {
  background-color: #f5f7fa;
}

.username {
  color: #606266;
  font-size: 14px;
}

.main-content {
  background-color: #f5f7fa;
  padding: 24px;
  overflow-y: auto;
}
</style>
