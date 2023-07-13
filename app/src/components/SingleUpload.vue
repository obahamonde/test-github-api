<script setup lang="ts">
const { state } = useStore();

const props = defineProps({
  multiple: {
    type: Boolean,
    default: false,
  },
  accept: {
    type: String,
    default: "*/*",
  },
});

const fileData = ref<{
  name: string;
  size: number;
  contentType: string;
  lastModified: number;
  url: string;
  file: File;
}>();

function onDrop(file: File | null) {
  if (!file) return;
  if (file) {
    fileData.value = {
      name: file.name,
      size: file.size,
      contentType: file.type,
      lastModified: file.lastModified,
      url: URL.createObjectURL(file),
      file: file,
    };
  }
}

const handleInput = () => {
  const input = document.createElement("input");
  input.type = "file";
  input.multiple = false;
  input.onchange = () => {
    onDrop(input.files![0]);
  };
  input.click();
};

const upload = async (file: {
  name: string;
  size: number;
  contentType: string;
  lastModified: number;
  url: string;
  file: File;
}) => {
  const formData = new FormData();
  formData.append("file", file.file);
  const res = await fetch(
    `/api/upload?user=${state.user!.ref}&key=assets/${file.name}&size=${
      file.size
    }`,
    {
      method: "POST",
      body: formData,
    }
  );
  const data = await res.json();
  state.user!.picture = data.url;
  state.notifications.push({
    message: "File uploaded",
    status: "success",
  });
  const url = encodeURIComponent(data.url);
  await fetch(`/api/user/${state.user!.ref}?picture=${url}`, {
    method: "PUT",
  });
};
</script>
<template>
  <div class="col center">
    <label for="singleFile" name="file" class="dropzone" @click="handleInput">
      <div v-if="fileData">
        <slot :data="fileData"></slot>
      </div>
      <div v-else>Click to upload</div>
      <input
        type="file"
        :multiple="props.multiple"
        id="singleFile"
        class="hidden"
        :accept="props.accept"
      />
    </label>
    <button
      class="btn-get"
      @click="
        upload(fileData!);
        $emit('close');
      "
    >
      Upload
    </button>
  </div>
</template>
