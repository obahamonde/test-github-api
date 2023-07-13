<script setup lang="ts">
const show = ref(false);
const isSecret = ref(true);
const { state } = useStore();
const copy = (text: string) => {
  navigator.clipboard.writeText(text);
};
</script>
<template>
  <Auth>
    <Icon
      icon="mdi-database-lock"
      class="x2 text-purple-800 m-4 mt-4 dark:invert cp scale"
      @click="show = !show"
    />
    <Request :url="'/api/db/' + state.user!.ref">
      <template #default="{ json }">
        <div class="row start text-xs gap-4" v-if="show">
          {{ isSecret ? "********" : json.secret }}
          <Icon
            icon="mdi-clipboard"
            @click="copy(json.secret)"
            class="text-primary hover:text-cyan cp scale"
          />
          <Icon
            icon="mdi-eye"
            class="text-primary hover:text-cyan cp scale"
            @click="isSecret = !isSecret"
          />
        </div>
      </template>
    </Request>
  </Auth>

  <br />
  <br />
</template>
