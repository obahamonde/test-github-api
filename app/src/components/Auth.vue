<script setup lang="ts">
import { useAuth0 } from "@auth0/auth0-vue";
const { state } = useStore();
const { isAuthenticated, loginWithRedirect, getAccessTokenSilently, user } =
  useAuth0();

watch(user, async () => {
  user.value ? (state.user = await authorize()) : (state.user = null);
});

const authorize = async () => {
  const token = await getAccessTokenSilently();
  state.token = token;
  const res = await fetch("/api/auth", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  const data = await res.json();
  state.notifications.push({
    message: "Welcome " + user.value.name,
    status: "success",
  });
  return data;
};
</script>
<template>
  <Notifier />
  <div v-if="(state.user && isAuthenticated) || state.githubToken">
    <slot />
  </div>
  <div v-else>
    <div class="container">
      <button class="btn-get" @click.prevent="loginWithRedirect()">
        Login
      </button>
    </div>
  </div>
</template>
