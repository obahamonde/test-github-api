<script setup lang="ts">
import { useSSE } from "~/composables/sse";
const emit = defineEmits(["closed"]);
const props = defineProps({
  url: {
    type: String,
    required: false,
    default: "/api/sse",
  },
});

const rxProps = reactive(props);

const { messages, eventSource, status: thisStatus } = useSSE(rxProps);
const status = computed<"OPEN" | "CLOSED" | "CONNECTING">(
  () => thisStatus.value
);
watch(eventSource, (newVal, oldVal) => {
  if (oldVal) {
    oldVal.close();
  }
  eventSource.value = newVal;
});
watch(
  () => status.value,
  (newVal, oldVal) => {
    if (newVal === "CLOSED") {
      emit("closed");
    }
  }
);
</script>
<template>
  <div v-if="status === 'OPEN'">
    <div>
      <slot :sse="messages"></slot>
    </div>
  </div>
  <div v-else-if="status === 'CONNECTING'">
    <slot name="loading">
      <Icon icon="mdi-loading" animate-spin x2 />
    </slot>
  </div>
  <div v-else-if="status === 'CLOSED'">
    <slot name="error" :sse="messages">
      <p class="text-error">Connection closed</p>
    </slot>
    <slot name="actions"> </slot>
  </div>
</template>
