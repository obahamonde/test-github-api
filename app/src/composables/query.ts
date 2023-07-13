const useQuery = () => {
  const query = ref({});
  const setQuery = (obj: Object) => {
    query.value = obj;
  };
  const queryString = computed(() => {
    if (!query.value) return "";
    return Object.entries(query.value)
      .map(([key, value]) => `${key}=${value}`)
      .join("&");
  });
  return {
    query,
    setQuery,
    queryString,
  };
};
