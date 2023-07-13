<script setup lang="ts">

import type { Query } from "~/types";

const { state } = useStore();

const namespace = computed(() => state.user!.ref);

const message = ref("");

const thisQuery = computed(() => ({
  text: message.value,
  namespace: namespace.value!,
}));

const objDownload = ref()

const srcObj = ref("");

const loading = ref(false);

const getAudio = async (query: Query) => {
  loading.value = true;
  const { data } = await useFetch("/api/chatbot/chat?audio=true", {
    method: "POST",
    body: JSON.stringify(query),
  }).arrayBuffer();
  message.value = "";
  const blob = new Blob([unref(data)!], { type: "audio/mp3" });
  const url = URL.createObjectURL(blob);
  srcObj.value = url
  objDownload.value = blob
  loading.value = false;
  const audio = new Audio(url);
  audio.play();
};

const downloadAudio = () => {
  const url = URL.createObjectURL(objDownload.value);
  const a = document.createElement("a");
  a.href = url;
  a.download = "audio.mp3";
  a.click();
  URL.revokeObjectURL(url);
};
</script>
<template>
  <div class="m-12">
    <div class="row center">
      <div class="text-center text-lg font-bold col center  bg-light px-4 py-2 rounded-lg sh">
        <h1 class="text-lg text-accent font-sans drop-shadow-color-primary drop-shadow-sm">
          Audio Chatbot
        </h1>
        <input class="input text-center" type="text" placeholder="Enter your question" v-model="message"
          @keyup.enter="getAudio(thisQuery)" />
        <Icon class="text-4xl text-accent m-4 cp scale animate-spin" icon="mdi-loading" v-if="loading" />
        <Icon class="text-4xl text-accent m-4 cp scale" icon="mdi-download" @click="downloadAudio" v-if="objDownload" />
      </div>

    </div>
  </div>
</template>