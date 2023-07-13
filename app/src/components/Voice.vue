<script setup lang="ts">
//Importing dependencies
import { useSpeech } from "~/composables/speech";
import { useSynthesis } from "~/composables/synthesis";
const { text, voices, voice, pickVoice, pause, stop } = useSynthesis();
const { isListening, result, speech } = useSpeech();
const voicesLength = computed(() => voices.value.length);
const currentVoice = ref<string>("");
const toggle = ref<boolean>(false);
</script>
<template>
  <div v-if="speech.isSupported">
    <div v-if="voicesLength > 0 && toggle">
      <select
        class="input"
        v-model="currentVoice"
        @change="pickVoice(currentVoice)"
      >
        <option v-for="v in voices" :value="v">
          {{ v }}
        </option>
      </select>
      <p>
        Selected voice: <strong>{{ voice.name }}</strong>
      </p>
    </div>
    <div v-if="isListening">
      <Icon
        v-if="isListening"
        class="btn-icon"
        icon="mdi-pause"
        @click="pause()"
      />
      <Icon
        v-if="isListening"
        class="btn-icon"
        icon="mdi-stop"
        @click="stop()"
      />
    </div>
    <div v-else>
      <Icon class="btn-icon" icon="mdi-translate" @click="toggle = !toggle" />
      <Icon class="btn-icon" icon="mdi-microphone" @click="speech.start()" />
    </div>
    <slot :output="result"> </slot>
    <slot :input="text"> </slot>
  </div>
  <div v-else>Speech recognition is not supported in your browser.</div>
</template>
