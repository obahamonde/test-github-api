<script setup lang="ts">
import { useRequest } from "~/composables/request";

const { request, response, iserror, isloading, lastResponseTime } =
  useRequest();

const allowed = computed(() => {
  const now = Number(useNow().value);
  const last = Number(lastResponseTime.value);
  return now - last > props.debounce * 1000;
});

const props = defineProps({
  url: {
    type: String,
    required: true,
  },
  options: {
    type: Object,
    required: false,
    default: () => ({
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    }),
  },
  refetch: {
    type: Boolean,
    required: false,
    default: true,
  },
  debounce: {
    type: Number,
    required: false,
    default: 2,
  },
});

const rxProps = reactive(props);

const fetchData = async () => {
  if (!allowed.value) return;
  if (rxProps.refetch) {
    await request(rxProps.url, rxProps.options);
  }
};

const { state } = useStore();

onMounted(async () => {
  await request(props.url, props.options);
});

watch(rxProps, fetchData);

watchEffect(() => {
  if (iserror.value) {
    state.notifications.push({
      status: "error",
      message:
        typeof iserror.value === "string"
          ? iserror.value
          : JSON.stringify(iserror.value),
    });
  }
});

const loaderActive = computed(() => isloading.value);
</script>

<template>
  <div v-if="!iserror && !loaderActive && response">
    <slot :json="response"></slot>
  </div>
  <div v-else-if="iserror">
    <slot name="error" :error="iserror">
      <!-- Add default error handling UI here -->
      <p class="text-error">
        An error occurred:
        {{ typeof iserror === "string" ? iserror : JSON.stringify(iserror) }}
      </p>
    </slot>
  </div>
  <div v-else-if="loaderActive">
    <slot name="loading">
      <Icon icon="mdi-loading" animate-spin x2 />
    </slot>
  </div>
</template>
