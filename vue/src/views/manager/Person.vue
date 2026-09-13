<template>
  <div class="person-page">
    <div class="profile-card">
      <!-- 四角装饰 -->
      <div class="corner corner-tl"></div>
      <div class="corner corner-tr"></div>
      <div class="corner corner-bl"></div>
      <div class="corner corner-br"></div>

      <!-- 左侧竖排标题 -->
      <div class="card-side-label">
        <div class="side-line"></div>
        <span class="side-text">个人资料</span>
        <div class="side-line"></div>
      </div>

      <!-- 主体表单 -->
      <div class="card-body">
        <div class="card-header">
          <h2 class="card-title">「 用户信息 」</h2>
          <p class="card-subtitle">维护管理员账号基本信息与头像</p>
        </div>

        <el-form
          ref="formRef"
          :model="data.user"
          :rules="data.rules"
          label-position="top"
          class="heritage-form"
        >
          <div class="avatar-section">
            <el-upload
              :show-file-list="false"
              class="avatar-uploader"
              :action="uploadUrl"
              :headers="uploadHeaders"
              :on-success="handleFileUpload"
            >
              <div class="avatar-wrap">
                <img v-if="data.user.avatar" :src="data.user.avatar" class="avatar" />
                <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                <div class="avatar-overlay">
                  <span>更换头像</span>
                </div>
              </div>
            </el-upload>
            <span class="avatar-hint">点击更换头像</span>
          </div>

          <div class="form-grid">
            <el-form-item label="登录账号" prop="username">
              <el-input disabled v-model="data.user.username" autocomplete="off" />
            </el-form-item>
            <el-form-item label="显示名称" prop="name">
              <el-input v-model="data.user.name" autocomplete="off" placeholder="请输入显示名称" />
            </el-form-item>
          </div>

          <div class="form-actions">
            <button type="button" class="heritage-btn" @click="save">
              <span class="btn-text">保存修改</span>
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
import { Plus } from "@element-plus/icons-vue";

// 文件上传的接口地址
const uploadUrl = import.meta.env.VITE_BASE_URL + '/files/upload'
// 上传请求需要携带 JWT token
const uploadHeaders = {
  Authorization: 'Bearer ' + sessionStorage.getItem('access_token')
}

const formRef = ref()
const data = reactive({
  user: JSON.parse(sessionStorage.getItem('system-user') || '{}'),
  rules: {
    username: [
      { required: true, message: '请输入账号', trigger: 'blur' }
    ],
    name: [
      { required: true, message: '请输入名称', trigger: 'blur' }
    ],
  }
})

const handleFileUpload = (file) => {
  data.user.avatar = file.data
}

const emit = defineEmits(["updateUser"])

const save = () => {
  formRef.value.validate(valid => {
    if (valid) {
      if (data.user.role === 'Admin') {
        request.put('/admin/update', data.user).then(res => {
          if (res.code === '200') {
            ElMessage.success('更新成功')
            sessionStorage.setItem('system-user', JSON.stringify(data.user))
            emit('updateUser')
          } else {
            ElMessage.error(res.msg)
          }
        })
      } else {
        request.put('/user/update', data.user).then(res => {
          if (res.code === '200') {
            ElMessage.success('更新成功')
            sessionStorage.setItem('system-user', JSON.stringify(data.user))
            emit('updateUser')
          } else {
            ElMessage.error(res.msg)
          }
        })
      }
    }
  })
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@300;400;500;600;700&display=swap');

.person-page {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  padding: 24px;
  min-height: 100%;
  display: flex;
  justify-content: center;
  align-items: flex-start;
}

.profile-card {
  position: relative;
  width: 100%;
  max-width: 720px;
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

/* 头像区域 */
.avatar-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  margin-bottom: 28px;
}

.avatar-wrap {
  position: relative;
  width: 120px;
  height: 120px;
  border-radius: 50%;
  overflow: hidden;
  border: 2px solid rgba(201, 168, 76, 0.35);
  cursor: pointer;
  background: #f5f0e8;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.avatar-uploader-icon {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  color: #8b7355;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(26, 21, 16, 0.55);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.avatar-overlay span {
  color: #e8dcc8;
  font-size: 13px;
  letter-spacing: 2px;
}

.avatar-wrap:hover .avatar-overlay {
  opacity: 1;
}

.avatar-hint {
  font-size: 12px;
  color: #a09080;
  letter-spacing: 1px;
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

/* 禁用态 */
.heritage-form :deep(.el-input.is-disabled .el-input__wrapper) {
  background: rgba(232, 224, 212, 0.4);
}

.heritage-form :deep(.el-input.is-disabled .el-input__inner) {
  color: #8b7355;
}

.form-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-actions {
  display: flex;
  justify-content: center;
  margin-top: 32px;
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
  .person-page {
    padding: 16px;
  }

  .profile-card {
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

  .form-grid {
    grid-template-columns: 1fr;
  }
}
</style>