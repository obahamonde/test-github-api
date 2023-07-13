<template>
  <textarea class="input" v-model="content"></textarea>
  <input class="input" type="text" v-model="title">
  <button @click="save">Save</button>
</template>

<script setup lang="ts">
const content = ref('')
const title = ref('')

const save = async () => {
  const { data } = await useFetch("/api/data/ingest",
    {
      method: "POST",
      body: JSON.stringify({ text: content.value, namespace: title.value }),
    }
  ).json();

  console.log(unref(data));

  content.value = "";
  title.value = "";

}
</script>
