<script setup lang="ts">
const url = ref("");
const { state } = useStore();
const urlTriggered = ref(false);
const route = useRoute();
</script>
<template>
  <div class="container" v-show="route.fullPath == '/app/settings'">
    <h1 class="text-title m-8">Create a new Website Chatbot</h1>
    <p class="text-subtitle m-8">
      Enter the URL of your website to create a new chatbot.
    </p>
    <input class="input" v-model="url" placeholder="Enter your URL" @keyup.enter="urlTriggered = true" />

    <div class="row gap-8 center" v-if="urlTriggered && state.user">
      <WebSocket :url="'wss://www.aiofauna.com/api/chatbot/ingest?namespace=' + url + '&ref=' + state.user!.ref">
        <template #default="{ data }">
          <div v-if="data">
            <ProgressBar :completed="Number(Number(data).toFixed(2))" bgcolor="#008080" />
          </div>  
        </template>
      </WebSocket>
    </div>
  </div>
</template>
<route lang="yaml">
meta:
  layout: app
</route>
