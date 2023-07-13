<script setup lang="ts">
const { state } = useStore();
const text = ref<string>("");
let wsRef = ref<WebSocket>();
const show = ref<boolean>(false);
</script>

<template>
          <div class="bg-white z-50 rounded-lg text-black sh br fixed w-96 overflow-y-scroll h-1/2 mb-32 col center m-4"
            v-if="show">
                                        <WebSocket ref="wsRef" :url="'wss://www.aiofauna.com/api/chatbot/infer' + (state.user ? '?user=' + state.user.ref : '')">
                        <template #default="{ messages, status }">
                          <div v-if="messages && status == 'OPEN'" class="h-full p-4">
                            <div class="chat__messages">
                              <div v-for="(message, index) in messages" :key="index" :class="{
                                'chat__message--left': index % 2 == 0,
                                'chat__message--right': index % 2 !== 0,
                              }" class="chat__message">
                                <div class="chat__message__content">
                                  <p class="chat__message__text">
                                    {{ index % 2 == 0 ? "🤖" : "🙂" }}
                                  </p>
                                  <p class="chat__message__text">{{ message }}</p>
                                </div>
                              </div>
                            </div>
                          </div>
                          <div v-else>
                            <Icon class="animate-spin text-primary x4" icon="loading" />
                          </div>
                        </template>
                      </WebSocket>
                      <input class="input bottom-0 fixed mb-20" v-model="text" @keyup.enter="
                        wsRef!.send(text);
                      text = '';
                      " />
                    </div>
                    <Icon class="cp scale br x3 fixed m-8 text-primary" icon="logos:openai" @click="show = !show" />
</template>

<style>
.chat__message--left {
  @apply rounded-lg bg-gray-200 p-1 m-1;
}

.chat__message--right {
  @apply rounded-lg bg-primary p-1 m-1;
  color: white;
}

.chat__message__content {
  @apply col center;
}

.chat__message__text {
  @apply m-1;
}
</style>
