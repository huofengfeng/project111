<template>
  <div class="manager-container">
    <!-- 左侧侧边栏 -->
    <aside class="sidebar">
      <!-- 品牌区 -->
      <div class="sidebar-brand">
        <img src="@/assets/imgs/logo2.png" alt="" class="brand-logo">
        <div class="brand-text">
          <div class="brand-title">唐三彩文物系统</div>
          <div class="brand-sub">数字化管理平台</div>
        </div>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar-nav">
        <div class="nav-group">
          <div class="nav-label">概览</div>
          <router-link
            to="/manager/home"
            class="nav-item"
            :class="{ active: isActive('/manager/home') }"
          >
            <el-icon><HomeFilled /></el-icon>
            <span>系统首页</span>
          </router-link>
        </div>

        <div class="nav-group">
          <div class="nav-label">文物管理</div>
          <router-link
            to="/manager/artifact"
            class="nav-item"
            :class="{ active: isActive('/manager/artifact') }"
          >
            <el-icon><Collection /></el-icon>
            <span>文物信息</span>
          </router-link>
          <router-link
            to="/manager/tombsMap"
            class="nav-item"
            :class="{ active: isActive('/manager/tombsMap') }"
          >
            <el-icon><MapLocation /></el-icon>
            <span>出土分布</span>
          </router-link>
          <router-link
            to="/manager/timeline"
            class="nav-item"
            :class="{ active: isActive('/manager/timeline') }"
          >
            <el-icon><Timer /></el-icon>
            <span>年代演变</span>
          </router-link>
          <router-link
            to="/manager/knowledge-graph"
            class="nav-item"
            :class="{ active: isActive('/manager/knowledge-graph') }"
          >
            <el-icon><Connection /></el-icon>
            <span>知识图谱</span>
          </router-link>
        </div>

        <div class="nav-group">
          <div class="nav-label">系统</div>
          <router-link
            to="/manager/admin"
            class="nav-item"
            :class="{ active: isActive('/manager/admin') }"
          >
            <el-icon><User /></el-icon>
            <span>管理员信息</span>
          </router-link>
          <router-link
            to="/manager/user"
            class="nav-item"
            :class="{ active: isActive('/manager/user') }"
          >
            <el-icon><UserFilled /></el-icon>
            <span>用户信息</span>
          </router-link>
        </div>
      </nav>

      <!-- 底部用户信息 -->
      <div class="sidebar-footer">
        <div class="footer-user">
          <img
            class="footer-avatar"
            :src="data.user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'"
            alt=""
          >
          <div class="footer-info">
            <div class="footer-name">{{ data.user.name }}</div>
            <div class="footer-role">{{ data.user.role || 'Admin' }}</div>
          </div>
        </div>
        <el-tooltip content="退出系统" placement="top">
          <div class="footer-logout" @click="logout">
            <el-icon><SwitchButton /></el-icon>
          </div>
        </el-tooltip>
      </div>
    </aside>

    <!-- 右侧主区域 -->
    <main class="main">
      <!-- 顶部标题栏 -->
      <header class="main-header">
        <div class="header-left">
          <!-- 面包屑 -->
          <div class="breadcrumb">
            <span class="bc-root">唐三彩文物系统</span>
            <span class="bc-sep">/</span>
            <span class="bc-current">{{ currentTitle }}</span>
          </div>
        </div>
        <div class="header-right">
          <span class="header-time">{{ currentTime }}</span>
          <div class="header-divider"></div>
          <el-dropdown trigger="click" @command="handleCommand">
            <div class="header-user-trigger">
              <img
                class="header-avatar"
                :src="data.user.avatar || 'https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png'"
                alt=""
              >
              <span class="header-user-name">{{ data.user.name }}</span>
              <el-icon class="header-arrow"><ArrowDown /></el-icon>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="person">
                  <el-icon><User /></el-icon> 个人资料
                </el-dropdown-item>
                <el-dropdown-item command="password">
                  <el-icon><Lock /></el-icon> 修改密码
                </el-dropdown-item>
                <el-dropdown-item command="logout" divided>
                  <el-icon><SwitchButton /></el-icon> 退出系统
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <!-- 内容区 -->
      <div class="main-content">
        <router-view v-slot="{ Component }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" @updateUser="updateUser" />
          </transition>
        </router-view>
      </div>
    </main>
  </div>
</template>

<script setup>
import { reactive, computed, ref, onMounted, onUnmounted } from "vue";
import router from "@/router";
import { ElMessage } from "element-plus";
import {
  HomeFilled,
  User,
  UserFilled,
  Collection,
  Lock,
  SwitchButton,
  MapLocation,
  Timer,
  ArrowDown,
  Connection,
} from "@element-plus/icons-vue";

const data = reactive({
  user: JSON.parse(sessionStorage.getItem('system-user') || '{}')
})

if (!data.user?.id) {
  ElMessage.error('请登录！')
  router.push('/login')
} else if (data.user.role !== 'Admin') {
  ElMessage.error('请使用管理员账号登录！')
  router.push('/')
}

const currentRoute = computed(() => router.currentRoute.value.path)

function isActive(path) {
  return currentRoute.value === path
}

const currentTitle = computed(() => {
  const path = currentRoute.value
  const map = {
    '/manager/home': '系统首页',
    '/manager/admin': '管理员信息',
    '/manager/user': '用户信息',
    '/manager/artifact': '文物信息',
    '/manager/tombsMap': '出土分布',
    '/manager/timeline': '年代演变',
    '/manager/knowledge-graph': '知识图谱',
    '/manager/person': '个人资料',
    '/manager/password': '修改密码'
  }
  return map[path] || ''
})

// 实时时间
const currentTime = ref('')
let timer = null
const updateTime = () => {
  const now = new Date()
  const y = now.getFullYear()
  const m = String(now.getMonth() + 1).padStart(2, '0')
  const d = String(now.getDate()).padStart(2, '0')
  const h = String(now.getHours()).padStart(2, '0')
  const min = String(now.getMinutes()).padStart(2, '0')
  const weekDays = ['日', '一', '二', '三', '四', '五', '六']
  const w = weekDays[now.getDay()]
  currentTime.value = `${y}年${m}月${d}日 周${w} ${h}:${min}`
}
onMounted(() => {
  updateTime()
  timer = setInterval(updateTime, 30000)
})
onUnmounted(() => {
  clearInterval(timer)
})

const updateUser = () => {
  data.user = JSON.parse(sessionStorage.getItem('system-user') || '{}')
}

const logout = () => {
  ElMessage.success('退出成功')
  sessionStorage.removeItem('system-user')
  sessionStorage.removeItem('access_token')
  router.push('/login')
}

const handleCommand = (command) => {
  if (command === 'person') {
    router.push('/manager/person')
  } else if (command === 'password') {
    router.push('/manager/password')
  } else if (command === 'logout') {
    logout()
  }
}
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.manager-container {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  display: flex;
  min-height: 100vh;
  background: #f7f4ee;
}

/* ========== 左侧侧边栏 ========== */
.sidebar {
  width: 240px;
  background: linear-gradient(180deg, #2c241b 0%, #3a2f24 100%);
  display: flex;
  flex-direction: column;
  height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  z-index: 100;
  flex-shrink: 0;
}

/* 品牌区 */
.sidebar-brand {
  padding: 24px 20px 20px;
  display: flex;
  align-items: center;
  gap: 12px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
  flex-shrink: 0;
}

.brand-logo {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  border: 1px solid rgba(201, 168, 76, 0.3);
  padding: 3px;
  background: rgba(255, 255, 255, 0.05);
  flex-shrink: 0;
}

.brand-title {
  color: #e8dcc8;
  font-size: 16px;
  font-weight: 700;
  letter-spacing: 2px;
  line-height: 1.3;
  white-space: nowrap;
}

.brand-sub {
  color: #8b7355;
  font-size: 11px;
  margin-top: 3px;
  letter-spacing: 1px;
}

/* 导航菜单 */
.sidebar-nav {
  flex: 1;
  overflow-y: auto;
  padding: 16px 14px;
}

.sidebar-nav::-webkit-scrollbar {
  width: 3px;
}

.sidebar-nav::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
}

.nav-group {
  margin-bottom: 20px;
}

.nav-label {
  font-size: 11px;
  font-weight: 600;
  color: #6b5d4d;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  padding: 0 10px 8px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  margin-bottom: 6px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 10px 14px;
  border-radius: 8px;
  color: #a09080;
  font-size: 14px;
  letter-spacing: 0.5px;
  text-decoration: none;
  transition: all 0.2s ease;
  position: relative;
  margin-bottom: 2px;
}

.nav-item:hover {
  background: rgba(255, 255, 255, 0.06);
  color: #d4c5b0;
}

.nav-item.active {
  background: rgba(201, 168, 76, 0.15);
  color: #e8dcc8;
}

.nav-item.active::before {
  content: '';
  position: absolute;
  left: 0;
  top: 8px;
  bottom: 8px;
  width: 3px;
  background: #c9a84c;
  border-radius: 0 2px 2px 0;
}

.nav-item .el-icon {
  font-size: 18px;
  color: inherit;
  flex-shrink: 0;
}

/* 底部用户信息 */
.sidebar-footer {
  padding: 14px 16px;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-shrink: 0;
}

.footer-user {
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-avatar {
  width: 34px;
  height: 34px;
  border-radius: 50%;
  border: 1px solid rgba(201, 168, 76, 0.3);
}

.footer-name {
  font-size: 13px;
  color: #d4c5b0;
  font-weight: 600;
  line-height: 1.3;
}

.footer-role {
  font-size: 11px;
  color: #6b5d4d;
}

.footer-logout {
  width: 32px;
  height: 32px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #8b7355;
  cursor: pointer;
  transition: all 0.2s;
}

.footer-logout:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #c9a84c;
}

/* ========== 右侧主区域 ========== */
.main {
  margin-left: 240px;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* 顶部标题栏 */
.main-header {
  height: 60px;
  background: rgba(247, 244, 238, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(224, 213, 197, 0.6);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 28px;
  position: sticky;
  top: 0;
  z-index: 10;
  flex-shrink: 0;
}

/* 面包屑 */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
}

.bc-root {
  color: #8b7355;
  font-weight: 500;
}

.bc-sep {
  color: #d4c5b0;
}

.bc-current {
  color: #4a3f35;
  font-weight: 600;
  letter-spacing: 1px;
}

/* 右上角区域 */
.header-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-time {
  color: #8b7355;
  font-size: 13px;
  letter-spacing: 0.5px;
  white-space: nowrap;
}

.header-divider {
  width: 1px;
  height: 20px;
  background: #d4c5b0;
}

.header-user-trigger {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 8px;
  transition: background 0.2s;
}

.header-user-trigger:hover {
  background: rgba(0, 0, 0, 0.04);
}

.header-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  border: 1px solid #d4c5b0;
}

.header-user-name {
  color: #5a4d3f;
  font-size: 14px;
  white-space: nowrap;
}

.header-arrow {
  color: #a09080;
  font-size: 12px;
}

/* 内容区 */
.main-content {
  flex: 1;
  padding: 24px 28px;
  overflow: hidden;
  min-height: 0;
}

/* 页面切换动画 */
.page-fade-enter-active,
.page-fade-leave-active {
  transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
}

.page-fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.page-fade-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}
</style>
