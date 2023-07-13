<script setup lang="ts">
const props = defineProps({
  url: {
    type: String,
    required: true,
  },
});
const { data, status, close, eventSource } = useEventSource(props.url);
onUnmounted(() => {
  close();
});
const messages = ref<string[]>([]);
onMounted(() => {
  if (!eventSource.value) return;
  eventSource.value.onmessage = (event: any) => {
    messages.value.push(event.data);
  };
});
const parsedMessages = computed(() => {
  return messages.value.map((message) => JSON.parse(message));
});
</script>
<template>
  <div>{{ data }}</div>
  <div>{{ status }}</div>
  <div>{{ messages }}</div>
</template>
