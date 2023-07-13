<script setup lang="ts">
const { state } = useStore();
const { loads } = useJson()
const query = ref("");
const q = computed(() => query.value);
const handleUpload = async (repo: string) => {
  alert(repo)
};
</script>
<template>
  <main class="container">
    <input type="text" v-model="query" class="input top-12 absolute" placeholder="Search for your repositories" />
    <Request :url="`/api/github/repos?token=${state.githubToken}&query=${q}&login=${state.user!.name}`" v-if="q">
      <template #default="{ json }">
        <div class="grid3 mt-16">
          <div class="card" v-for="repo in json">
            <GithubRepository :repo="loads(repo)" @upload="handleUpload($event)" />
          </div>
        </div>
      </template>
    </Request>
  </main>
</template>