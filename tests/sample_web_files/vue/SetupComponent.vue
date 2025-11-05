<script setup>
<!-- File: tests/sample_web_files/vue/SetupComponent.vue -->

import { ref, onMounted } from 'vue'

const count = ref(0)
const message = ref('Hello Vue 3!')

onMounted(() => {
  console.log('Component mounted')
})
</script>

<template>
  <div class="container">
    <h1>{{ message }}</h1>
    <button @click="count++">Count: {{ count }}</button>
  </div>
</template>

<style scoped>
.container {
  text-align: center;
  margin-top: 60px;
}
</style>
