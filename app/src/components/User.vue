<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { state } = useStore();
const { isAuthenticated, logout, loginWithRedirect } = useAuth0();
const showModal = ref(false);
</script>
<template>
  <div
    v-if="state.user && isAuthenticated"
    class="x4 scale cp br fixed m-4"
    @click="showModal = !showModal"
  >
    <img :src="state.user.picture" class="rf sh" />
  </div>
  <div v-else class="x4 scale cp br fixed m-4">
    <Icon
      icon="mdi-login"
      class="rf text-error x2"
      @click="loginWithRedirect()"
    />
  </div>

  <Modal v-if="showModal" @close="showModal = false">
    <template #header>
      <p class="drop-shadow drop-shadow-color-blueGray font-sans">
        {{ state.user!.name }}
      </p>
    </template>
    <template #body>
      <p class="drop-shadow drop-shadow-color-blueGray font-sans">
        {{ state.user!.email }}
      </p>
    </template>
    <template #footer>
      <button class="btn-del" @click="logout()">Logout</button>
    </template>
  </Modal>
  <Chatbot />
</template>
