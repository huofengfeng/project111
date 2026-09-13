<template>
  <div class="login-container">
    <div class="login-wrapper">
            <!-- 左侧面板（登录时显示装饰，注册时显示表单） -->
      <div class="login-panel left-panel" :class="{ 'is-register': isRegister }">
        <!-- 登录状态下的左侧面板内容 -->
        <div class="panel-content panel-decor" v-if="!isRegister">
          <h1 class="panel-title">欢迎回来！</h1>
          <p class="panel-desc">已有账号？<br>请直接登录</p>
          <el-button class="panel-btn" @click="toggleMode">去注册</el-button>
        </div>
        <!-- 注册状态下的左侧表单内容 -->
        <div class="panel-content panel-form" v-else>
          <div class="form-header">
            <h2 class="form-title">注册</h2>
            <div class="title-underline"></div>
          </div>
          <el-form :model="regData.form" ref="regFormRef" :rules="regData.rules" class="login-form">
            <el-form-item prop="username">
              <el-input :prefix-icon="User" size="large" v-model="regData.form.username" placeholder="请输入账号" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input :prefix-icon="Lock" size="large" v-model="regData.form.password" placeholder="请输入密码" show-password />
            </el-form-item>
            <el-form-item prop="confirmPassword">
              <el-input :prefix-icon="Lock" size="large" v-model="regData.form.confirmPassword" placeholder="请确认密码" show-password />
            </el-form-item>
            <el-form-item>
              <el-button size="large" class="login-btn" @click="register">注 册</el-button>
            </el-form-item>
          </el-form>
        </div>
      </div>

      <!-- 右侧面板（登录时显示表单，注册时显示装饰） -->
      <div class="login-panel right-panel" :class="{ 'is-register': isRegister }">
        <!-- 登录状态下的右侧表单内容 -->
        <div class="panel-content panel-form" v-if="!isRegister">
          <div class="form-header">
            <h2 class="form-title">登录</h2>
            <div class="title-underline"></div>
          </div>
          <el-form :model="data.form" ref="formRef" :rules="data.rules" class="login-form">
            <el-form-item prop="username">
              <el-input :prefix-icon="User" size="large" v-model="data.form.username" placeholder="请输入账号" />
            </el-form-item>
            <el-form-item prop="password">
              <el-input :prefix-icon="Lock" size="large" v-model="data.form.password" placeholder="请输入密码" show-password />
            </el-form-item>
            <el-form-item prop="role">
              <el-select size="large" style="width: 100%" v-model="data.form.role">
                <el-option value="Admin" label="管理员"></el-option>
                <el-option value="User" label="用户"></el-option>
              </el-select>
            </el-form-item>
            <el-form-item>
              <el-button size="large" class="login-btn" @click="login">登 录</el-button>
            </el-form-item>
          </el-form>
          <div class="form-footer">
            还没有账号？请 <a href="javascript:void(0)" @click="toggleMode">注册</a>
          </div>
          <div class="back-home">
            <a href="javascript:void(0)" @click="router.push('/')">← 返回前台</a>
          </div>
        </div>
        <!-- 注册状态下的右侧面板装饰内容 -->
        <div class="panel-content panel-decor" v-else>
          <h1 class="panel-title">加入我们！</h1>
          <p class="panel-desc">还没有账号？<br>立即注册开启旅程</p>
          <el-button class="panel-btn" @click="toggleMode">去登录</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
  import { reactive, ref } from "vue";
  import { User, Lock } from "@element-plus/icons-vue";
  import request from "@/utils/request";
  import {ElMessage} from "element-plus";
  import router from "@/router";

  const isRegister = ref(false)

  const data = reactive({
    form: { role: 'Admin' },
    rules: {
      username: [
        { required: true, message: '请输入账号', trigger: 'blur' },
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
    }
  })

  const regData = reactive({
    form: { username: '', password: '', confirmPassword: '' },
    rules: {
      username: [
        { required: true, message: '请输入账号', trigger: 'blur' },
      ],
      password: [
        { required: true, message: '请输入密码', trigger: 'blur' },
      ],
      confirmPassword: [
        { validator: (rule, value, callback) => {
            if (!value) {
              callback(new Error('请确认密码'))
            } else if (value !== regData.form.password) {
              callback(new Error('两次输入密码不一致'))
            } else {
              callback()
            }
          }, trigger: 'blur' },
      ],
    }
  })

  const formRef = ref()
  const regFormRef = ref()

  const toggleMode = () => {
    isRegister.value = !isRegister.value
  }

  const login = () => {
    formRef.value.validate((valid => {
      if (valid) {
        // 调用后台的接口
        request.post('/login', data.form).then(res => {
          if (res.code === '200') {
            ElMessage.success("登录成功")
            // 存储 JWT token
            sessionStorage.setItem('access_token', res.data.access_token)
            // 存储用户信息
            sessionStorage.setItem('system-user', JSON.stringify(res.data.user))
            router.push(res.data.user.role === 'Admin' ? '/manager/home' : '/')
          } else {
            ElMessage.error(res.msg)
          }
        }).catch(err => {
          console.error('登录请求失败:', err)
        })
      }
    })).catch(error => {
      console.error(error)
    })
  }

  const register = () => {
    regFormRef.value.validate((valid => {
      if (valid) {
        request.post('/register', regData.form).then(res => {
          if (res.code === '200') {
            ElMessage.success("注册成功")
            isRegister.value = false
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
    })).catch(error => {
      console.error(error)
    })
  }

</script>

<style scoped>
/* 引入古典衬线字体 */
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&display=swap');

.login-container {
  height: 100vh;
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  /* 深褐色古典背景，带纸质纹理感 */
  background: #2c241b;
  background-image:
    radial-gradient(circle at 20% 50%, rgba(139, 90, 43, 0.15) 0%, transparent 50%),
    radial-gradient(circle at 80% 80%, rgba(160, 82, 45, 0.1) 0%, transparent 50%);
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
}

.login-wrapper {
  display: flex;
  width: 800px;
  height: 520px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
  background: #f5f0e8;
  position: relative;
}

/* 面板基础 */
.login-panel {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

/* 左侧面板 */
.left-panel {
  width: 40%;
  background: #3a4f6a;
  background-image:
    linear-gradient(135deg, rgba(58, 79, 106, 0.95) 0%, rgba(44, 62, 80, 0.95) 100%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e8dcc8;
}

.left-panel.is-register {
  width: 60%;
  background: #faf6f0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
}

/* 右侧面板 */
.right-panel {
  width: 60%;
  padding: 50px 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  background: #faf6f0;
  position: relative;
}

.right-panel::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url("data:image/svg+xml,%3Csvg width='100' height='100' viewBox='0 0 100 100' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.8' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23noise)' opacity='0.03'/%3E%3C/svg%3E");
  pointer-events: none;
}

.right-panel.is-register {
  width: 40%;
  background: #3a4f6a;
  background-image:
    linear-gradient(135deg, rgba(58, 79, 106, 0.95) 0%, rgba(44, 62, 80, 0.95) 100%),
    url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23ffffff' fill-opacity='0.03'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
  padding: 0;
}

/* 装饰边框 */
.left-panel::before,
.right-panel.is-register::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 1px solid rgba(212, 175, 55, 0.2);
  margin: 12px;
  pointer-events: none;
  transition: opacity 0.6s ease;
}

.left-panel.is-register::before {
  display: none;
}

/* 面板内容 */
.panel-content {
  text-align: center;
  padding: 30px;
  width: 100%;
  transition: opacity 0.4s ease, transform 0.4s ease;
}

.panel-decor .panel-title {
  font-size: 32px;
  font-weight: 700;
  margin-bottom: 20px;
  color: #f0e6d3;
  letter-spacing: 4px;
}

.panel-decor .panel-desc {
  font-size: 16px;
  line-height: 1.8;
  margin-bottom: 30px;
  color: #c9b896;
  letter-spacing: 2px;
}

.panel-btn {
  background: transparent !important;
  border: 1px solid #c9a84c !important;
  color: #c9a84c !important;
  padding: 12px 40px !important;
  font-size: 16px !important;
  border-radius: 25px !important;
  transition: all 0.3s ease !important;
  font-family: 'Noto Serif SC', serif !important;
}

.panel-btn:hover {
  background: #c9a84c !important;
  color: #2c3e50 !important;
}

/* 注册状态下右侧面板的装饰文字颜色调整 */
.right-panel.is-register .panel-decor .panel-title {
  color: #f0e6d3;
}

.right-panel.is-register .panel-decor .panel-desc {
  color: #c9b896;
}

/* 表单区域 */
.panel-form {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.left-panel.is-register .panel-form {
  padding: 40px 50px;
}

.form-header {
  text-align: center;
  margin-bottom: 35px;
}

.form-title {
  font-size: 28px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 6px;
  margin-bottom: 10px;
}

.title-underline {
  width: 50px;
  height: 3px;
  background: #8b7355;
  margin: 0 auto;
  border-radius: 2px;
}

.login-form :deep(.el-input__wrapper) {
  background: #f0ebe3;
  box-shadow: inset 0 1px 3px rgba(0,0,0,0.05);
  border: 1px solid #d4c5b0;
  border-radius: 6px;
}

.login-form :deep(.el-input__inner) {
  color: #5a4d3f;
  font-family: 'Noto Serif SC', serif;
}

.login-form :deep(.el-input__inner::placeholder) {
  color: #a89b8c;
}

.login-btn {
  width: 100%;
  background: #6b5b4f !important;
  border: none !important;
  color: #f0e6d3 !important;
  font-size: 16px !important;
  letter-spacing: 4px !important;
  border-radius: 6px !important;
  padding: 12px 0 !important;
  transition: all 0.3s ease !important;
  font-family: 'Noto Serif SC', serif !important;
}

.login-btn:hover {
  background: #5a4a3e !important;
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(107, 91, 79, 0.3);
}

.form-footer {
  text-align: center;
  margin-top: 20px;
  color: #8b7d6b;
  font-size: 14px;
}

.form-footer a {
  color: #6b5b4f;
  text-decoration: none;
  font-weight: 600;
  border-bottom: 1px solid transparent;
  transition: border-color 0.3s;
}

.form-footer a:hover {
  border-bottom-color: #6b5b4f;
}

.back-home {
  text-align: center;
  margin-top: 14px;
}

.back-home a {
  color: #a89b8c;
  font-size: 13px;
  text-decoration: none;
  transition: color 0.3s;
  letter-spacing: 1px;
}

.back-home a:hover {
  color: #6b5b4f;
}

/* 内容切换动画 */
.panel-content {
  animation: fadeIn 0.5s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式 */
@media (max-width: 850px) {
  .login-wrapper {
    width: 90%;
    flex-direction: column;
    height: auto;
  }
  .left-panel, .right-panel,
  .left-panel.is-register, .right-panel.is-register {
    width: 100% !important;
  }
  .left-panel {
    padding: 30px;
    min-height: 180px;
  }
  .left-panel.is-register .panel-form {
    padding: 30px;
  }
}
</style>