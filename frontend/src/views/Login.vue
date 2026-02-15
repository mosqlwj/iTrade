<template>
  <div class="login-container">
    <div class="login-box">
      <div class="login-header">
        <div class="logo-icon">
          <el-icon :size="36"><TrendCharts /></el-icon>
        </div>
        <h1>iTrade 投资分析平台</h1>
        <p class="subtitle">Investment Analysis Platform</p>
      </div>
      <el-form :model="loginForm" :rules="rules" ref="formRef" class="login-form">
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="请输入用户名"
            prefix-icon="User"
            size="large"
            clearable
          />
        </el-form-item>
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="请输入密码"
            prefix-icon="Lock"
            size="large"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="loading"
            @click="handleLogin"
            class="login-button"
          >
            登 录
          </el-button>
        </el-form-item>
        <div class="login-footer">
          <span>还没有账号？</span>
          <el-link type="primary" @click="showRegister = true">立即注册</el-link>
        </div>
      </el-form>
    </div>

    <el-dialog v-model="showRegister" title="注册账号" width="420px" center>
      <el-form :model="registerForm" :rules="registerRules" ref="registerFormRef">
        <el-form-item prop="username">
          <el-input v-model="registerForm.username" placeholder="请输入用户名" prefix-icon="User" />
        </el-form-item>
        <el-form-item prop="email">
          <el-input v-model="registerForm.email" placeholder="请输入邮箱（可选）" prefix-icon="Message" />
        </el-form-item>
        <el-form-item prop="password">
          <el-input v-model="registerForm.password" type="password" placeholder="请输入密码" prefix-icon="Lock" show-password />
        </el-form-item>
        <el-form-item prop="confirmPassword">
          <el-input v-model="registerForm.confirmPassword" type="password" placeholder="请确认密码" prefix-icon="Lock" show-password />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRegister = false">取 消</el-button>
        <el-button type="primary" @click="handleRegister" :loading="registerLoading">注 册</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { useUserStore } from '../stores';

const router = useRouter();
const userStore = useUserStore();

const formRef = ref();
const registerFormRef = ref();
const loading = ref(false);
const registerLoading = ref(false);
const showRegister = ref(false);

const loginForm = reactive({
  username: '',
  password: ''
});

const registerForm = reactive({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
});

const validatePassword = (rule: any, value: any, callback: any) => {
  if (value !== registerForm.password) {
    callback(new Error('两次输入密码不一致'));
  } else {
    callback();
  }
};

const rules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
};

const registerRules = {
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  confirmPassword: [{ required: true, validator: validatePassword, trigger: 'blur' }]
};

const handleLogin = async () => {
  await formRef.value.validate(async (valid: boolean) => {
    if (valid) {
      loading.value = true;
      try {
        await userStore.login(loginForm.username, loginForm.password);
        localStorage.setItem('username', loginForm.username);
        ElMessage.success('登录成功');
        router.push('/');
      } catch (e: any) {
        ElMessage.error(e.response?.data?.detail || '登录失败');
      } finally {
        loading.value = false;
      }
    }
  });
};

const handleRegister = async () => {
  await registerFormRef.value.validate(async (valid: boolean) => {
    if (valid) {
      registerLoading.value = true;
      try {
        await userStore.register(registerForm.username, registerForm.password, registerForm.email);
        ElMessage.success('注册成功，请登录');
        showRegister.value = false;
        loginForm.username = registerForm.username;
      } catch (e: any) {
        ElMessage.error(e.response?.data?.detail || '注册失败');
      } finally {
        registerLoading.value = false;
      }
    }
  });
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  width: 420px;
  padding: 48px 40px;
  background: #ffffff;
  border-radius: 20px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  width: 72px;
  height: 72px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
  color: #fff;
}

.login-header h1 {
  font-size: 24px;
  font-weight: 600;
  color: #303133;
  margin: 0 0 8px;
}

.subtitle {
  font-size: 13px;
  color: #909399;
  margin: 0;
  letter-spacing: 1px;
}

.login-form {
  margin-top: 20px;
}

.login-form :deep(.el-input__wrapper) {
  padding: 4px 12px;
  border-radius: 10px;
}

.login-form :deep(.el-input__inner) {
  height: 44px;
}

.login-button {
  width: 100%;
  height: 44px;
  font-size: 16px;
  font-weight: 500;
  border-radius: 10px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  transition: all 0.3s;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

.login-footer {
  display: flex;
  justify-content: center;
  gap: 8px;
  color: #909399;
  font-size: 14px;
}

.login-footer .el-link {
  font-size: 14px;
}
</style>
