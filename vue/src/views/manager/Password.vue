<template>
  <div class="password-page">
    <div class="password-card">
      <!-- 四角装饰 -->
      <div class="corner corner-tl"></div>
      <div class="corner corner-tr"></div>
      <div class="corner corner-bl"></div>
      <div class="corner corner-br"></div>

      <!-- 左侧竖排标题 -->
      <div class="card-side-label">
        <div class="side-line"></div>
        <span class="side-text">修改密码</span>
        <div class="side-line"></div>
      </div>

      <!-- 主体表单 -->
      <div class="card-body">
        <div class="card-header">
          <h2 class="card-title">「 安全设置 」</h2>
          <p class="card-subtitle">定期更换密码，保护账号安全</p>
        </div>

        <el-form
          ref="formRef"
          :rules="data.rules"
          :model="data.user"
          label-position="top"
          class="heritage-form"
        >
          <div class="password-fields">
            <el-form-item label="原密码" prop="password">
              <el-input
                v-model="data.user.password"
                show-password
                placeholder="请输入当前密码"
              />
            </el-form-item>

            <el-form-item label="新密码" prop="newPassword">
              <el-input
                v-model="data.user.newPassword"
                show-password
                placeholder="请输入新密码"
              />
            </el-form-item>

            <el-form-item label="确认新密码" prop="confirmPasword">
              <el-input
                v-model="data.user.confirmPasword"
                show-password
                placeholder="请再次输入新密码"
              />
            </el-form-item>
          </div>

          <div class="password-tips">
            <div class="tip-item">
              <span class="tip-dot"></span>
              <span class="tip-text">新密码请勿与原密码相同</span>
            </div>
            <div class="tip-item">
              <span class="tip-dot"></span>
              <span class="tip-text">两次输入的新密码需保持一致</span>
            </div>
          </div>

          <div class="form-actions">
            <button type="button" class="heritage-btn" @click="save">
              <span class="btn-text">确认修改</span>
              <span class="btn-line"></span>
            </button>
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue"
import request from "@/utils/request";
import { ElMessage } from "element-plus";
import router from "@/router";

const formRef = ref()
const data = reactive({
  user: JSON.parse(sessionStorage.getItem('system-user') || '{}'),
  rules: {
    password: [
      { required: true, message: '请输入原密码', trigger: 'blur' }
    ],
    newPassword: [
      { required: true, message: '请输入新密码', trigger: 'blur' }
    ],
    confirmPasword: [
      { required: true, message: '请确认新密码', trigger: 'blur' }
    ],
  }
})

const save = () => {
  formRef.value.validate(valid => {
    if (valid) {
      if (data.user.password === data.user.newPassword) {
        ElMessage.error('新密码不能和原密码一致')
        return
      }
      if (data.user.newPassword !== data.user.confirmPasword) {
        ElMessage.error('确认新密码错误')
        return
      }
      request.put('/updatePassword', data.user).then(res => {
        if (res.code === '200') {
          ElMessage.success('修改密码成功')
          sessionStorage.setItem('system-user', JSON.stringify(data.user))
          router.push('/login')
        } else {
          ElMessage.error(res.msg)
        }
      })
    }
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap');

.password-page {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  padding: 24px;
  min-height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.password-card {
  position: relative;
  width: 100%;
  max-width: 560px;
  display: flex;
  gap: 24px;
  padding: 40px 48px;
  background: linear-gradient(145deg, #fbf7f0 0%, #f2ece0 50%, #e9e0d0 100%);
  border-radius: 8px;
  box-shadow:
    0 16px 48px rgba(0, 0, 0, 0.08),
    inset 0 0 0 1px rgba(201, 168, 76, 0.18);
}

/* 四角装饰 */
.corner {
  position: absolute;
  width: 30px;
  height: 30px;
  border: 2px solid rgba(201, 168, 76, 0.35);
}

.corner-tl {
  top: 12px;
  left: 12px;
  border-right: none;
  border-bottom: none;
  border-top-left-radius: 4px;
}

.corner-tr {
  top: 12px;
  right: 12px;
  border-left: none;
  border-bottom: none;
  border-top-right-radius: 4px;
}

.corner-bl {
  bottom: 12px;
  left: 12px;
  border-right: none;
  border-top: none;
  border-bottom-left-radius: 4px;
}

.corner-br {
  bottom: 12px;
  right: 12px;
  border-left: none;
  border-top: none;
  border-bottom-right-radius: 4px;
}

/* 左侧竖排标签 */
.card-side-label {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 14px;
  padding-top: 8px;
  flex-shrink: 0;
}

.side-line {
  width: 1px;
  height: 40px;
  background: linear-gradient(180deg, transparent, rgba(139, 115, 85, 0.3), transparent);
}

.side-text {
  writing-mode: vertical-rl;
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 6px;
  font-weight: 500;
}

/* 主体内容 */
.card-body {
  flex: 1;
}

.card-header {
  text-align: center;
  margin-bottom: 32px;
}

.card-title {
  font-size: 24px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 3px;
  margin: 0 0 8px;
}

.card-subtitle {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 1px;
  margin: 0;
}

/* 表单 */
.heritage-form :deep(.el-form-item__label) {
  font-size: 12px;
  color: #8b7355;
  letter-spacing: 2px;
  margin-bottom: 6px;
  padding: 0;
  font-weight: 500;
}

.heritage-form :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.6);
  box-shadow: 0 0 0 1px #e8e0d4 inset;
  border-radius: 6px;
  padding: 0 14px;
  transition: all 0.3s;
}

.heritage-form :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 1px rgba(201, 168, 76, 0.6) inset;
  background: #fff;
}

.heritage-form :deep(.el-input__inner) {
  height: 42px;
  color: #4a3f35;
  font-size: 14px;
  letter-spacing: 1px;
}

.heritage-form :deep(.el-input__inner::placeholder) {
  color: #a09080;
}

.password-fields {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

/* 提示信息 */
.password-tips {
  margin-top: 20px;
  padding: 16px 18px;
  background: rgba(201, 168, 76, 0.06);
  border: 1px solid rgba(201, 168, 76, 0.12);
  border-radius: 6px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.tip-dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: #c9a84c;
  opacity: 0.6;
  flex-shrink: 0;
}

.tip-text {
  font-size: 12px;
  color: #8b7355;
  letter-spacing: 0.5px;
}

/* 按钮 */
.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 28px;
}

.heritage-btn {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 11px 36px;
  font-size: 14px;
  letter-spacing: 2px;
  color: #c9a84c;
  background: transparent;
  border: 1px solid rgba(201, 168, 76, 0.45);
  border-radius: 4px;
  cursor: pointer;
  font-family: 'Noto Serif SC', 'SimSun', serif;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  overflow: hidden;
}

.heritage-btn:hover {
  background: rgba(201, 168, 76, 0.08);
  border-color: #c9a84c;
  color: #4a3f35;
}

.btn-text {
  position: relative;
  z-index: 1;
}

.btn-line {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 0%;
  background: rgba(201, 168, 76, 0.12);
  transition: height 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  z-index: 0;
}

.heritage-btn:hover .btn-line {
  height: 100%;
}

/* 响应式 */
@media (max-width: 640px) {
  .password-page {
    padding: 16px;
  }

  .password-card {
    flex-direction: column;
    padding: 32px 24px;
    gap: 16px;
  }

  .card-side-label {
    flex-direction: row;
    gap: 10px;
    padding-top: 0;
  }

  .side-line {
    width: 30px;
    height: 1px;
  }

  .side-text {
    writing-mode: horizontal-tb;
    font-size: 12px;
    letter-spacing: 4px;
  }
}
</style>