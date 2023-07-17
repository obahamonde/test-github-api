<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { state } = useStore();
const { logout } = useAuth0();
const showModal = ref(false);
</script>
<template>
  <div class="col center p-12 gap-4">
    <img
      :src="state.user!.picture"
      class="rf sh cp scale"
      @click="showModal = !showModal"
    />
    <h1 class="font-sans">{{ state.user!.name }}</h1>
    <h2 class="font-sans">{{ state.user!.email }}</h2>
    <button class="btn-del" @click="logout()">Logout</button>
  </div>
  <Modal v-if="showModal" @close="showModal = false">
    <template #header>
      <p class="drop-shadow drop-shadow-color-blueGray font-sans text-center">
        Upload a File
      </p>
    </template>
    <template #body>
      <SingleUpload accepts="image/*">
        <template #default="{ data }">
          <img :src="data.url" class="rf sh x6" />
        </template>
      </SingleUpload>
    </template>
  </Modal>
</template>
<route lang="yaml">
meta:
  layout: app
</route>
