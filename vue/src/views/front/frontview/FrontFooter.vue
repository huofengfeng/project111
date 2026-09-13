<template>
  <footer class="front-footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <img src="../../../assets/imgs/logo2.png" alt="" class="footer-logo">
        <span>唐三彩文物数字化管理系统</span>
      </div>
      <div class="footer-links">
        <a href="#hero">首页</a>
        <router-link to="/appreciation">文物鉴赏</router-link>
        <router-link to="/quiz">文物猜谜</router-link>
        <a href="#timeline">年代演变</a>
        <a href="#map">出土分布</a>
      </div>
      <div class="footer-copy">
        <span>唐三彩文物数字化管理系统 v1.0</span>
        <span class="footer-sep">|</span>
        <span>守护千年文明，传承文化瑰宝</span>
      </div>
    </div>
  </footer>
</template>

<script setup>
// 无 props，完全自包含的页脚组件
</script>

<style scoped>
/* ========== 页脚 ========== */
.front-footer {
  background: #1a1510;
  padding: 48px 40px 24px;
}

.footer-inner {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-brand {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  margin-bottom: 24px;
}

.footer-logo {
  width: 32px;
  height: 32px;
  border-radius: 6px;
  border: 1px solid rgba(201, 168, 76, 0.3);
  padding: 2px;
}

.footer-brand span {
  color: #e8dcc8;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 2px;
}

.footer-links {
  display: flex;
  justify-content: center;
  gap: 32px;
  margin-bottom: 24px;
}

.footer-links a {
  color: rgba(232, 220, 200, 0.5);
  text-decoration: none;
  font-size: 14px;
  letter-spacing: 1px;
  transition: color 0.3s;
}

.footer-links a:hover {
  color: #c9a84c;
}

.footer-copy {
  text-align: center;
  color: rgba(232, 220, 200, 0.3);
  font-size: 12px;
  letter-spacing: 1px;
}

.footer-sep {
  margin: 0 12px;
}
</style>