<script setup lang="ts">
const wsRef = ref();
const message = ref("");
const send = computed(() => wsRef.value?.send);
const { state } = useStore();
</script>
<template>
  <div class="col center p-4 m-4 bg-gray-300"></div>
  <div>
    <Ws
      :url="'ws://localhost:8080/api/docker/build/' + state.user!.ref"
      :keep-alive="true"
      :chunked="true"
      :progress="true"
      ref="wsRef"
      @send="message = ''"
    >
      <template #outter="{ json }">
        <div v-for="j in json">
          {{ j.status }}
          {{ j.id }}
          <ProgressBar
            :completed="
              (j.progressDetail.current * 100) / j.progressDetail.total
            "
            bgcolor="#000000"
            v-if="j.progressDetail"
          />
        </div>
      </template>
      <template #="{ json }">
        <input
          type="text"
          v-model="message"
          placeholder="repo"
          @keyup.enter="send(message)"
        />
        <br />
      </template>
      <template #closed="{ json }">
        <p>Connection closed</p>
      </template>
      <template #actions>
        <button class="btn-del" @click="wsRef.value?.clear">Clear</button>
      </template>

      <template #waiting="{ json }">
        <div class="text-center text-gray-500 text-sm">
          <p>Waiting for data</p>
        </div>
        {{ json }}
      </template>
    </Ws>
  </div>
</template>
