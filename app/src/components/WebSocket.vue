<script setup lang="ts">
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

const messages = ref<string[]>([]);

watch(data, (newData) => {
  messages.value.push(newData);
});

const sendJson = (json: any) => {
  send(JSON.stringify(json));
};

const sendMessage = (message: string) => {
  send(message);
  messages.value.push(message);
};

defineExpose({
  send: sendMessage,
  sendJson,
});
</script>
<template>
  <slot :data="data" :messages="messages" :status="status" />
</template>
