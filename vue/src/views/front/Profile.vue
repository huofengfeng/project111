<template>
  <div class="profile-page">
    <!-- 顶部导航 -->
    <header class="profile-header">
      <div class="nav-inner">
        <div class="nav-brand">
          <div class="brand-icon-wrap">
            <img src="../../assets/imgs/logo2.png" alt="" class="brand-icon">
          </div>
          <div class="brand-text-wrap">
            <span class="brand-subtitle">个人中心</span>
            <span class="brand-text">我的</span>
          </div>
        </div>
        <div class="nav-actions">
          <router-link to="/" class="nav-btn">
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </router-link>
        </div>
      </div>
    </header>

    <main class="profile-main">
      <!-- 左侧：用户名片 -->
      <aside class="profile-sidebar">
        <div class="identity-card">
          <div class="card-pattern"></div>
          <div class="avatar-frame" @click="triggerUpload">
            <div class="avatar-ring"></div>
            <img v-if="profile.avatar" :src="profile.avatar" class="avatar-img" />
            <div v-else class="avatar-fallback">
              <el-icon :size="48"><UserFilled /></el-icon>
            </div>
            <div class="avatar-mask">
              <el-icon><Camera /></el-icon>
              <span>更换头像</span>
            </div>
            <input ref="fileInput" type="file" accept="image/*" style="display:none" @change="handleFileChange">
          </div>
          <h2 class="identity-name">{{ profile.name || profile.username || '未命名用户' }}</h2>
          <p class="identity-role">
            <span class="role-badge">{{ profile.role === 'Admin' ? '管理员' : 'User' }}</span>
          </p>
          <div class="identity-meta">
            <div class="meta-item">
              <span class="meta-label">账号</span>
              <span class="meta-value">{{ profile.username || '-' }}</span>
            </div>
            <div class="meta-item">
              <span class="meta-label">昵称</span>
              <span class="meta-value">{{ profile.name || '未设置' }}</span>
            </div>
          </div>
        </div>
      </aside>

      <!-- 右侧：编辑表单 -->
      <section class="profile-content">
        <div class="content-card">
          <div class="card-header" @click="profileExpanded = !profileExpanded">
            <div class="header-icon">
              <el-icon><EditPen /></el-icon>
            </div>
            <div class="header-text">
              <h3>编辑资料</h3>
              <p>完善你的个人信息</p>
            </div>
            <div class="header-arrow" :class="{ expanded: profileExpanded }">
              <el-icon><ArrowDown /></el-icon>
            </div>
          </div>

          <div class="card-body-collapse" :class="{ expanded: profileExpanded }">
            <div class="card-body-inner">

          <el-form ref="formRef" :model="profile" :rules="rules" label-position="top" class="profile-form">
            <div class="form-row">
              <el-form-item label="账号" prop="username" class="form-item-half">
                <el-input v-model="profile.username" disabled>
                  <template #prefix>
                    <el-icon><User /></el-icon>
                  </template>
                </el-input>
              </el-form-item>

              <el-form-item label="昵称" prop="name" class="form-item-half">
                <el-input v-model="profile.name" placeholder="请输入你的昵称" maxlength="20" show-word-limit>
                  <template #prefix>
                    <el-icon><EditPen /></el-icon>
                  </template>
                </el-input>
              </el-form-item>
            </div>

            <el-form-item label="头像链接" prop="avatar">
              <el-input v-model="profile.avatar" placeholder="可输入图片地址或点击左侧头像上传">
                <template #prefix>
                  <el-icon><Picture /></el-icon>
                </template>
              </el-input>
            </el-form-item>

            <el-form-item>
              <div class="form-actions">
                <el-button type="primary" size="large" @click="save" :loading="saving">
                  <el-icon><Check /></el-icon>
                  保存修改
                </el-button>
                <el-button size="large" @click="logout">
                  <el-icon><SwitchButton /></el-icon>
                  退出登录
                </el-button>
              </div>
            </el-form-item>
          </el-form>
          </div>
          </div>
        </div>

        <!-- 我的收藏 -->
        <div class="content-card">
          <div class="card-header" @click="favExpanded = !favExpanded">
            <div class="header-icon fav-icon">
              <el-icon><StarFilled /></el-icon>
            </div>
            <div class="header-text">
              <h3>我的收藏</h3>
              <p>{{ favorites.length > 0 ? `共收藏 ${favorites.length} 件文物` : '还没有收藏过文物' }}</p>
            </div>
            <div class="header-arrow" :class="{ expanded: favExpanded }">
              <el-icon><ArrowDown /></el-icon>
            </div>
          </div>

          <div class="card-body-collapse" :class="{ expanded: favExpanded }">
            <div class="card-body-inner">

          <div v-if="favLoading" class="fav-loading">
            <div class="loading-dot"></div>
            <span>加载中...</span>
          </div>

          <div v-else-if="favorites.length === 0" class="fav-empty">
            <el-icon :size="40"><Collection /></el-icon>
            <p>去文物鉴赏页面发现你喜欢的文物，点击星标即可收藏</p>
            <router-link to="/appreciation" class="fav-empty-link">前往鉴赏</router-link>
          </div>

          <div v-else class="fav-grid">
            <div
              v-for="item in favorites"
              :key="item.id"
              class="fav-card"
              @click="goArtifactDetail(item.id)"
            >
              <div class="fav-card-img">
                <img v-if="item.image_url" :src="getImageUrl(item.image_url)" :alt="item.name" />
                <div v-else class="fav-card-placeholder">
                  <el-icon :size="28"><Collection /></el-icon>
                </div>
                <button
                  class="fav-remove-btn"
                  @click.stop="removeFavorite(item.id)"
                  title="取消收藏"
                >
                  <el-icon :size="14"><Close /></el-icon>
                </button>
              </div>
              <div class="fav-card-body">
                <span class="fav-card-era">{{ item.era }}</span>
                <h4 class="fav-card-name">{{ item.name }}</h4>
                <span class="fav-card-type">{{ item.type }}</span>
              </div>
            </div>
          </div>
          </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { ArrowLeft, ArrowDown, UserFilled, Camera, EditPen, User, Picture, Check, SwitchButton, StarFilled, Collection, Close } from "@element-plus/icons-vue"
import { ElMessage, ElMessageBox } from "element-plus"
import request from "@/utils/request"
import { getImageUrl } from "@/utils/imageUrl"

const router = useRouter()
const fileInput = ref(null)
const formRef = ref()
const saving = ref(false)
const favorites = ref([])
const favLoading = ref(false)
const profileExpanded = ref(true)
const favExpanded = ref(true)

const profile = reactive({
  id: null,
  username: '',
  name: '',
  avatar: null,
  role: null,
})

const rules = {
  name: [
    { required: true, message: '请输入昵称', trigger: 'blur' }
  ],
}

const loadProfile = () => {
  request.get('/profile').then(res => {
    if (res.code === '200') {
      Object.assign(profile, res.data)
    }
  }).catch(() => {
    ElMessage.error('加载个人信息失败，请重新登录')
    router.push('/login')
  })
}

const triggerUpload = () => {
  fileInput.value?.click()
}

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (!file) return

  const ext = file.name.slice(file.name.lastIndexOf('.')).toLowerCase()
  if (!['.jpg', '.jpeg', '.png', '.gif', '.webp'].includes(ext)) {
    ElMessage.error('仅支持 jpg、png、gif、webp 格式的图片')
    return
  }

  const formData = new FormData()
  formData.append('file', file)

  request.post('/profile/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }).then(res => {
    if (res.code === '200') {
      profile.avatar = res.data
      ElMessage.success('头像上传成功')
      syncStorage()
    } else {
      ElMessage.error(res.msg || '上传失败')
    }
  }).catch(err => {
    console.error(err)
    ElMessage.error('头像上传失败')
  })
}

const syncStorage = () => {
  const stored = JSON.parse(sessionStorage.getItem('system-user') || '{}')
  stored.name = profile.name
  stored.avatar = profile.avatar
  sessionStorage.setItem('system-user', JSON.stringify(stored))
}

const save = () => {
  formRef.value.validate(valid => {
    if (!valid) return

    saving.value = true
    request.put('/profile', {
      name: profile.name,
      avatar: profile.avatar
    }).then(res => {
      if (res.code === '200') {
        ElMessage.success('保存成功')
        syncStorage()
      } else {
        ElMessage.error(res.msg)
      }
    }).catch(err => {
      console.error(err)
    }).finally(() => {
      saving.value = false
    })
  })
}

const logout = () => {
  ElMessageBox.confirm('确定要退出登录吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  }).then(() => {
    sessionStorage.removeItem('access_token')
    sessionStorage.removeItem('system-user')
    ElMessage.success('已退出登录')
    router.push('/')
  }).catch(() => {})
}

const loadFavorites = () => {
  favLoading.value = true
  request.get('/favorites/items').then(res => {
    if (res.code === '200') {
      favorites.value = res.data || []
    }
  }).catch(() => {}).finally(() => {
    favLoading.value = false
  })
}

const removeFavorite = (artifactId) => {
  request.post('/favorites/toggle', { artifact_id: artifactId }).then(res => {
    if (res.code === '200') {
      favorites.value = favorites.value.filter(f => f.id !== artifactId)
      ElMessage.success('已取消收藏')
    }
  }).catch(() => {})
}

const goArtifactDetail = (id) => {
  router.push(`/artifact/${id}`)
}

onMounted(() => {
  loadProfile()
  loadFavorites()
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.profile-page {
  min-height: 100vh;
  background: #f5f0e8;
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  position: relative;
}

/* ========== 导航 ========== */
.profile-header {
  position: relative;
  z-index: 10;
  background: linear-gradient(135deg, #2c241b 0%, #1a1510 100%);
  padding: 0 40px;
  border-bottom: 1px solid rgba(201, 168, 76, 0.25);
}

.nav-inner {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 72px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 16px;
}

.brand-icon-wrap {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  border: 1px solid rgba(201, 168, 76, 0.4);
  padding: 4px;
  background: rgba(255, 255, 255, 0.03);
}

.brand-icon {
  width: 100%;
  height: 100%;
  border-radius: 6px;
  object-fit: cover;
}

.brand-text-wrap {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.brand-subtitle {
  color: rgba(232, 220, 200, 0.5);
  font-size: 12px;
  letter-spacing: 3px;
}

.brand-text {
  color: #e8dcc8;
  font-size: 22px;
  font-weight: 700;
  letter-spacing: 4px;
}

.nav-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 10px 22px;
  border: 1px solid rgba(201, 168, 76, 0.45);
  color: #c9a84c;
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 1px;
  border-radius: 6px;
  transition: all 0.3s;
  background: rgba(201, 168, 76, 0.05);
}

.nav-btn:hover {
  background: rgba(201, 168, 76, 0.15);
  border-color: #c9a84c;
  transform: translateX(-2px);
}

/* ========== 主布局 ========== */
.profile-main {
  position: relative;
  z-index: 1;
  max-width: 1100px;
  margin: 0 auto;
  padding: 48px 24px 80px;
  display: grid;
  grid-template-columns: 340px 1fr;
  gap: 32px;
  align-items: start;
}

/* ========== 侧边身份卡 ========== */
.profile-sidebar {
  position: sticky;
  top: 24px;
}

.identity-card {
  background: #fff;
  border-radius: 16px;
  padding: 40px 28px;
  text-align: center;
  border: 1px solid #e8e0d4;
  box-shadow:
    0 12px 40px rgba(0, 0, 0, 0.06),
    0 1px 0 rgba(201, 168, 76, 0.1) inset;
  position: relative;
  overflow: hidden;
}

.card-pattern {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 110px;
  background: linear-gradient(135deg, #c9a84c 0%, #a08040 100%);
  opacity: 0.12;
  border-radius: 16px 16px 0 0;
}

.avatar-frame {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto 20px;
  cursor: pointer;
}

.avatar-ring {
  position: absolute;
  inset: -6px;
  border: 2px dashed rgba(201, 168, 76, 0.35);
  border-radius: 50%;
  transition: all 0.4s ease;
}

.avatar-frame:hover .avatar-ring {
  transform: rotate(180deg);
  border-color: #c9a84c;
}

.avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: linear-gradient(135deg, #c9a84c, #a08040);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 3px solid #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  position: relative;
  z-index: 1;
}

.avatar-mask {
  position: absolute;
  inset: 0;
  border-radius: 50%;
  background: rgba(26, 21, 16, 0.55);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
  color: #e8dcc8;
  opacity: 0;
  transition: opacity 0.3s;
  z-index: 2;
  border: 3px solid transparent;
}

.avatar-mask .el-icon {
  font-size: 22px;
}

.avatar-mask span {
  font-size: 12px;
  letter-spacing: 1px;
}

.avatar-frame:hover .avatar-mask {
  opacity: 1;
}

.identity-name {
  font-size: 22px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 2px;
  margin: 0 0 10px;
}

.identity-role {
  margin: 0 0 28px;
}

.role-badge {
  display: inline-block;
  padding: 4px 14px;
  background: rgba(201, 168, 76, 0.1);
  color: #a08040;
  font-size: 12px;
  letter-spacing: 2px;
  border-radius: 20px;
  border: 1px solid rgba(201, 168, 76, 0.25);
}

.identity-meta {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.meta-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #f5f0e8;
  border-radius: 8px;
  border: 1px solid #e8e0d4;
}

.meta-label {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 1px;
}

.meta-value {
  font-size: 14px;
  color: #4a3f35;
  font-weight: 500;
}

/* ========== 右侧内容 ========== */
.profile-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.content-card {
  background: #fff;
  border-radius: 16px;
  padding: 36px;
  border: 1px solid #e8e0d4;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.06);
}

.card-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 0;
  padding-bottom: 24px;
  border-bottom: 1px solid #f0ebe3;
  cursor: pointer;
  user-select: none;
}

.card-header:hover .header-arrow {
  color: #c9a84c;
}

.header-arrow {
  margin-left: auto;
  color: #a09080;
  transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  align-items: center;
}

.header-arrow.expanded {
  transform: rotate(180deg);
}

.card-body-collapse {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.card-body-collapse.expanded {
  max-height: 2000px;
}

.card-body-inner {
  padding-top: 24px;
}

.header-icon {
  width: 52px;
  height: 52px;
  background: linear-gradient(135deg, #c9a84c, #a08040);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 24px;
  flex-shrink: 0;
}

.header-text h3 {
  font-size: 22px;
  font-weight: 700;
  color: #4a3f35;
  letter-spacing: 2px;
  margin: 0 0 4px;
}

.header-text p {
  font-size: 13px;
  color: #8b7355;
  margin: 0;
  letter-spacing: 1px;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.form-actions {
  display: flex;
  gap: 16px;
  margin-top: 8px;
}

/* ========== 收藏区域 ========== */
.fav-icon {
  background: linear-gradient(135deg, #e8c84a, #c9a84c);
}

.fav-loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 0;
  color: #8b7355;
  font-size: 13px;
  letter-spacing: 1px;
}

.loading-dot {
  width: 8px;
  height: 8px;
  background: #c9a84c;
  border-radius: 50%;
  animation: pulse 1.2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 0.3; transform: scale(0.8); }
  50% { opacity: 1; transform: scale(1); }
}

.fav-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 48px 20px;
  color: #a09080;
}

.fav-empty p {
  font-size: 13px;
  color: #8b7355;
  letter-spacing: 1px;
  margin: 0;
}

.fav-empty-link {
  display: inline-block;
  padding: 8px 24px;
  color: #c9a84c;
  text-decoration: none;
  border: 1px solid rgba(201, 168, 76, 0.4);
  border-radius: 6px;
  font-size: 13px;
  letter-spacing: 1px;
  transition: all 0.3s;
}

.fav-empty-link:hover {
  background: rgba(201, 168, 76, 0.08);
  border-color: #c9a84c;
}

.fav-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

.fav-card {
  background: #f5f0e8;
  border: 1px solid #e8e0d4;
  border-radius: 10px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.fav-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  border-color: #c9a84c;
}

.fav-card-img {
  position: relative;
  aspect-ratio: 1 / 1;
  overflow: hidden;
  background: #e8e0d4;
}

.fav-card-img img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.fav-card:hover .fav-card-img img {
  transform: scale(1.05);
}

.fav-card-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #c9a84c;
  opacity: 0.35;
}

.fav-remove-btn {
  position: absolute;
  top: 6px;
  right: 6px;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  color: #a09080;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.25s;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
  z-index: 2;
}

.fav-card:hover .fav-remove-btn {
  opacity: 1;
}

.fav-remove-btn:hover {
  background: #e05050;
  color: #fff;
}

.fav-card-body {
  padding: 12px;
}

.fav-card-era {
  font-size: 11px;
  color: #c9a84c;
  letter-spacing: 1.5px;
}

.fav-card-name {
  font-size: 14px;
  font-weight: 600;
  color: #4a3f35;
  margin: 4px 0;
  letter-spacing: 0.5px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.fav-card-type {
  font-size: 11px;
  color: #8b7355;
  letter-spacing: 1px;
}

/* Element Plus 深度覆盖 */
:deep(.el-form-item__label) {
  color: #4a3f35;
  font-weight: 600;
  font-size: 14px;
  padding-bottom: 6px;
}

:deep(.el-input__wrapper) {
  background: #f5f0e8;
  border-radius: 8px;
  box-shadow: 0 0 0 1px #e8e0d4 inset;
  padding: 4px 12px;
}

:deep(.el-input__inner) {
  color: #4a3f35;
}

:deep(.el-input__prefix-inner) {
  color: #a08040;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #c9a84c, #a08040);
  border: none;
  letter-spacing: 1px;
  font-weight: 600;
  padding: 0 28px;
}

:deep(.el-button--primary:hover) {
  background: linear-gradient(135deg, #b89a45, #8f7338);
  transform: translateY(-1px);
  box-shadow: 0 8px 20px rgba(201, 168, 76, 0.25);
}

:deep(.el-button:not(.el-button--primary)) {
  border-color: #d4c5b0;
  color: #6b5d4d;
  letter-spacing: 1px;
}

:deep(.el-button:not(.el-button--primary):hover) {
  border-color: #c9a84c;
  color: #a08040;
  background: rgba(201, 168, 76, 0.05);
}

/* ========== 响应式 ========== */
@media (max-width: 900px) {
  .profile-main {
    grid-template-columns: 1fr;
  }

  .profile-sidebar {
    position: static;
  }

  .form-row {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 480px) {
  .profile-header {
    padding: 0 20px;
  }

  .nav-inner {
    height: 64px;
  }

  .brand-text {
    font-size: 18px;
  }

  .profile-main {
    padding: 28px 16px 60px;
  }

  .content-card {
    padding: 24px;
  }

  .form-actions {
    flex-direction: column;
  }
}
</style>
