<script setup lang="ts">
const filesData = ref<
  { name: string; size: number; contentType: string; lastModified: number }[]
>([]);
function onDrop(files: File[] | null) {
  filesData.value = [];
  if (files) {
    filesData.value = files.map((file) => ({
      name: file.name,
      size: file.size,
      contentType: file.type,
      lastModified: file.lastModified,
    }));
  }
}
const dropZoneRef = ref<HTMLElement>();

const handleInput = () => {
  const input = document.createElement("input");
  input.type = "file";
  input.multiple = true;
  input.onchange = () => {
    onDrop(Array.from(input.files as FileList));
  };
  input.click();
};

const totalSize = computed(() => {
  if (filesData.value.length === 0) return 0;
  return filesData.value.reduce((acc, file) => acc + file.size, 0);
});
const { isOverDropZone } = useDropZone(dropZoneRef, onDrop);
</script>

<template>
  <div ref="dropZoneRef" class="dropzone" dropzone @click="handleInput">
    <div>{{ isOverDropZone ? "Drop Files" : "Drag Files" }}</div>
    <div>
      <div>
        <small
          >{{ filesData.length }} file
          {{ filesData.length > 1 ? "s" : "" }} selected
          {{ (totalSize / 1000).toFixed(2) }} KB</small
        >
      </div>
    </div>
  </div>
</template>
