export const useSSE = (props: { url: string }) => {
  const { status, data, eventSource, close } = useEventSource(`${props.url}`);

  const messages = ref<any[]>([]);

  watch(data, (newData) => {
    if (newData) {
      messages.value.unshift(JSON.parse(newData));
    }
  });

  onUnmounted(() => {
    close();
  });

  return {
    messages,
    status,
    eventSource,
  };
};
