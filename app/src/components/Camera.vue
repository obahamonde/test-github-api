<script setup lang="ts">
const { state, setState } = useStore();

const currentCamera = ref<string>();

const { videoInputs: cameras } = useDevicesList({
  requestPermissions: true,
  onUpdated() {
    if (!cameras.value.find((i) => i.deviceId === currentCamera.value)) {
      currentCamera.value = cameras.value[0].deviceId;
    }
  },
});
const video = ref<HTMLVideoElement>();

const { stream, enabled } = useUserMedia({ videoDeviceId: currentCamera });

watchEffect(() => {
  if (video.value && enabled.value) video.value.srcObject = stream.value!;
});

const recorder = ref<MediaRecorder>();

watchEffect(() => {
  if (stream.value && enabled.value) {
    recorder.value?.stop();
    recorder.value = new MediaRecorder(stream.value);
    recorder.value.start();
  } else {
    recorder.value?.stop();
  }
});

const videoBlob = ref<Blob[]>([]);

watchEffect(() => {
  if (recorder.value) {
    recorder.value.ondataavailable = (e) => {
      videoBlob.value.push(e.data);
    };
  }
  state.currentVideo = new File(
    videoBlob.value,
    state.currentVideoName as string,
    {
      type: "video/webm",
    }
  );
  watchEffect(() => {
    if (state.currentVideo) {
      setState({ currentVideoUrl: URL.createObjectURL(state.currentVideo) });
    }
  });
});
</script>
<template>
  <button
    icon
    @click="enabled = !enabled"
    v-if="!enabled"
    class="br text-white bg-primary fixed m-4 hover:bg-secondary scale"
    title="Record Video"
  >
    <Icon icon="mdi-video" />
  </button>
  <video
    ref="video"
    style="z-index: 9999"
    muted
    autoplay
    controls
    class="w-48 sh bl fixed m-4 mb-20"
    :hidden="!enabled"
    @click="enabled = !enabled"
  />
</template>
