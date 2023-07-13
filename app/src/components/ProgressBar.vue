<script setup lang="ts">
import { CSSProperties } from "vue";

const props = defineProps({
  completed: {
    type: Number,
    required: true,
  },
  bgcolor: {
    type: String,
    required: true,
  },
});

const fillerStyles = computed<CSSProperties>(() => {
  return {
    width: `${props.completed}%`,
    backgroundColor: props.bgcolor,
    transition: "width 0.2s ease-in",
    height: "2rem",
    borderRadius: "inherit",
    textAlign: "right",
  };
});
</script>
<template>
  <main class="container">
    <h1 class="title">
      Your website is being saved to your chatbot's memory. This might take a
      while.
    </h1>
    <div class="bar">
      <div :style="fillerStyles">
        <span class="label">{{ `${completed}%` }}</span>
      </div>
    </div>
  </main>
</template>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.bar {
  height: 2rem;
  width: 40rem;
  background-color: #b5b8bf;
  @apply row start rounded-lg w-full;
}

.label {
  padding: 5px;
  font-weight: bold;
  @apply row center text-white text-xs px-4 py-2;
}

.title {
  @apply font-script py-4 px-2;
  color: #008080;
}
</style>
