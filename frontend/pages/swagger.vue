<template>
  <div>
    <h1 class="text-2xl font-bold mb-6">API Dokumentation</h1>
    <iframe
      src="http://localhost:8000/docs"
      width="100%"
      height="800px"
      style="border: none;"
    ></iframe>
  </div>
</template>

<script setup lang="ts">
definePageMeta({
  layout: 'default'
});
</script>
