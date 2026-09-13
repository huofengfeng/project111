<template>
  <header class="front-nav" :class="{ 'nav-scrolled': isScrolled }">
    <div class="nav-inner">
      <div class="nav-brand">
        <img src="../../../assets/imgs/logo2.png" alt="" class="brand-icon">
        <span class="brand-text">唐三彩文物系统</span>
      </div>
      <nav class="nav-links">
        <a href="#hero" class="nav-link active">首页</a>
        <router-link to="/appreciation" class="nav-link">文物鉴赏</router-link>
        <router-link to="/quiz" class="nav-link">文物猜谜</router-link>
        <router-link to="/profile" class="nav-link">我的</router-link>
        <a href="#about" class="nav-link">关于</a>
      </nav>
      <div class="nav-actions">
        <template v-if="user">
          <div class="user-menu" @click="showDropdown = !showDropdown">
            <img v-if="user.avatar" :src="user.avatar" class="user-avatar" />
            <el-icon v-else :size="20" class="user-avatar-placeholder"><UserFilled /></el-icon>
            <span class="user-name">{{ user.name || user.username }}</span>
            <el-icon :size="12"><ArrowDown /></el-icon>
          </div>
          <div v-if="showDropdown" class="user-dropdown">
            <div class="dropdown-item" @click="showDropdown = false; router.push('/profile')">我的</div>
            <div class="dropdown-item" @click="emit('logout')">退出登录</div>
          </div>
        </template>
        <router-link v-else to="/login" class="nav-btn">登录</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { UserFilled, ArrowDown } from '@element-plus/icons-vue'

const router = useRouter()

defineProps({
  user: {
    type: Object,
    default: null,
  },
  isScrolled: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['logout'])

const showDropdown = ref(false)
</script>

<style scoped>
.front-nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  padding: 0 40px;
}

.front-nav.nav-scrolled {
  background: rgba(44, 36, 27, 0.95);
  backdrop-filter: blur(12px);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.2);
}

.nav-inner {
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-icon {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid rgba(201, 168, 76, 0.4);
  padding: 2px;
}

.brand-text {
  color: #e8dcc8;
  font-size: 18px;
  font-weight: 700;
  letter-spacing: 2px;
}

.nav-links {
  display: flex;
  gap: 36px;
}

.nav-link {
  color: rgba(232, 220, 200, 0.7);
  text-decoration: none;
  font-size: 15px;
  letter-spacing: 1px;
  transition: color 0.3s;
  position: relative;
}

.nav-link:hover,
.nav-link.active {
  color: #c9a84c;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -6px;
  left: 50%;
  width: 0;
  height: 2px;
  background: #c9a84c;
  transition: all 0.3s;
  transform: translateX(-50%);
}

.nav-link:hover::after,
.nav-link.active::after {
  width: 100%;
}

.nav-actions {
  display: flex;
  gap: 16px;
  position: relative;
}

.nav-btn {
  padding: 8px 24px;
  border: 1px solid rgba(201, 168, 76, 0.5);
  color: #c9a84c;
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 1px;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-btn:hover {
  background: rgba(201, 168, 76, 0.15);
  border-color: #c9a84c;
}

/* 用户菜单 */
.user-menu {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 6px 12px;
  border-radius: 6px;
  transition: background 0.3s;
  position: relative;
}

.user-menu:hover {
  background: rgba(201, 168, 76, 0.1);
}

.user-avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  object-fit: cover;
  border: 1px solid rgba(201, 168, 76, 0.4);
}

.user-avatar-placeholder {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: linear-gradient(135deg, #c9a84c, #a08040);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.user-name {
  font-size: 14px;
  color: #e8dcc8;
  letter-spacing: 1px;
}

.user-dropdown {
  position: absolute;
  top: 100%;
  right: 40px;
  margin-top: 8px;
  background: #2c241b;
  border: 1px solid rgba(201, 168, 76, 0.3);
  border-radius: 6px;
  padding: 4px 0;
  min-width: 120px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
  z-index: 1001;
}

.dropdown-item {
  padding: 10px 16px;
  font-size: 13px;
  color: #e8dcc8;
  cursor: pointer;
  transition: all 0.2s;
  letter-spacing: 1px;
}

.dropdown-item:hover {
  background: rgba(201, 168, 76, 0.15);
  color: #c9a84c;
}
</style>