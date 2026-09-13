<template>
  <div></div>
</template>

<script setup>
  import { onMounted } from "vue";
  import router from "@/router";

  onMounted(() => {
    router.replace('/login')
  })
</script>