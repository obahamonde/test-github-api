<script setup lang="ts">
const { loginWithGithub, signinWithPopup } = useAuth();
const { query } = useRoute();

const authCode = computed(() => query?.code?.toString());

const { state } = useStore();
const githubhook = async (code: string) => {
  const res = await loginWithGithub(code);
  const { user, token } = res;
  state.user = user;
  state.githubToken = token;
  state.notifications.push({
    message: `Welcome ${state.user!.name}`,
    status: "success",
  });
};
onMounted(async () => {
  if (authCode.value) {
    await githubhook(authCode.value);
  }
});
</script>
<template>
  <div class="row center my-8" v-if="!state.githubToken">
    <button
      class="row center gap-4 sh px-8 rounded-lg text-gray-500 hover:text-black scale cp"
      @click.prevent="signinWithPopup()"
    >
      <Icon class="rf x2 cp scale" icon="mdi-github" />
      <p class="row center w-full">Login with Github</p>
    </button>
  </div>
  <div v-else>
    <RouterLink to="/platform">
      <Icon class="rf x2 cp scale sh" icon="mdi-cloud" />
    </RouterLink>
    <RouterLink to="/repositories">
      <Icon class="rf x2 cp scale sh" icon="mdi-git" />
    </RouterLink>
  </div>
</template>
