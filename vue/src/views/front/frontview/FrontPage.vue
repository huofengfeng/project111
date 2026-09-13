<template>
  <div class="front-page">
    <FrontNav :user="user" :isScrolled="isScrolled" @logout="logout" />
    <FrontHero />
    <FrontTimeline />
    <FrontMap />
    <FrontAbout />
    <FrontFooter />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import FrontNav from './FrontNav.vue'
import FrontHero from './FrontHero.vue'
import FrontTimeline from './FrontTimeline.vue'
import FrontMap from './FrontMap.vue'
import FrontAbout from './FrontAbout.vue'
import FrontFooter from './FrontFooter.vue'

const isScrolled = ref(false)
const user = ref(null)

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const loadUser = () => {
  const token = sessionStorage.getItem('access_token')
  const u = sessionStorage.getItem('system-user')
  if (u && token) {
    try { user.value = JSON.parse(u) } catch {}
  } else {
    user.value = null
  }
}

const logout = () => {
  sessionStorage.removeItem('access_token')
  sessionStorage.removeItem('system-user')
  user.value = null
  ElMessage.success('已退出登录')
}

onMounted(() => {
  loadUser()
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;500;600;700&display=swap');

.front-page {
  font-family: 'Noto Serif SC', 'SimSun', '宋体', serif;
  background: #f5f0e8;
  min-height: 100vh;
  overflow-x: hidden;
}
</style>