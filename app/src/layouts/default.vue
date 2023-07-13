<script setup lang="ts">
const { query } = useRoute();
const { code } = query;
const auth = ref(false);
onMounted(() => {
  if (code) {
    auth.value = true;
  }
});
</script>

<template>
  <Auth v-if="auth"></Auth>
  <Dark />
      <SideBar />
    <div class="container">
    
          <Chatbot/>
      <RouterView /></div>
</template>
