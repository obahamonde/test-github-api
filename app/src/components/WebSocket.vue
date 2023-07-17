<script setup lang="ts">
import type { Message } from "~/types";

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
});
const { data, open, close, status, send } = useWebSocket(props.url, {
  autoReconnect: true,
});

onMounted(() => {
  open();
});

onUnmounted(() => {
  close();
});

const messages = ref<Message[]>([]);

watch(data, (newData) => {
  messages.value.push({
    message: newData,
    author: "bot",
  });
});

const sendJson = (json: any) => {
  send(JSON.stringify(json));
};

const sendMessage = (message: string) => {
  send(message);
  messages.value.push({
    message,
    author: "user",
  }); 
};

defineExpose({
  send: sendMessage,
  sendJson,
});
</script>
<template>
  <slot :data="data" :messages="messages" :status="status" />
</template>
