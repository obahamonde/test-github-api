import { acceptHMRUpdate, defineStore } from "pinia";
import { User, Notification, Message } from "../types";

export const useStore = defineStore("state", () => {
  const state = reactive({
    notifications: [] as Notification[],
    user: null as User | null,
    token: null as string | null,
    githubToken: null as string | null,
  });

  const setState = (newState: any) => {
    Object.assign(state, newState);
  };

  return {
    state,
    setState,
  };
});

if (import.meta.hot)
  import.meta.hot.accept(acceptHMRUpdate(useStore as any, import.meta.hot));
