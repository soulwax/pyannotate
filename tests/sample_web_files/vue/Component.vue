<template>
<!-- File: tests/sample_web_files/vue/Component.vue -->

  <div class="hello">
    <h1>{{ msg }}</h1>
    <p>
      Welcome to your Vue.js application
    </p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  props: {
    msg: String
  }
}
</script>

<style scoped>
h1 {
  margin: 40px 0 0;
  color: #42b983;
}
</style>