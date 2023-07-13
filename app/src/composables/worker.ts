import * as monaco from "monaco-editor";

export const useWorker = (worker: Worker, model: monaco.editor.ITextModel) => {
  const { uri } = model;
  const workerProxy = ref<monaco.languages.typescript.TypeScriptWorker>();
  const workerModel = ref<monaco.languages.typescript.TypeScriptWorker>();
  const workerModelUri = ref<string>();
  const workerModelVersion = ref<number>();
  const workerModelVersionId = ref<number>();
  const workerModelVersionIdDisposer = ref<() => void>();
  const workerModelDisposer = ref<() => void>();

  const disposeWorkerModel = () => {
    if (workerModelDisposer.value) {
      workerModelDisposer.value();
      workerModelDisposer.value = undefined;
    }
  };

  const disposeWorkerModelVersionId = () => {
    if (workerModelVersionIdDisposer.value) {
      workerModelVersionIdDisposer.value();
      workerModelVersionIdDisposer.value = undefined;
    }
  };

  const disposeWorker = () => {
    disposeWorkerModel();
    disposeWorkerModelVersionId();
    workerProxy.value = undefined;
    workerModel.value = undefined;
    workerModelUri.value = undefined;
    workerModelVersion.value = undefined;
    workerModelVersionId.value = undefined;
  };

  const updateWorkerModel = () => {
    if (workerModelUri.value !== uri.toString()) {
      disposeWorkerModel();
      workerModel.value = workerProxy.value.getEagerModel(uri.toString());
      workerModelUri.value = uri.toString();
    }
  };

  const updateWorkerModelVersionId = () => {
    if (workerModelVersion.value !== model.getVersionId()) {
      disposeWorkerModelVersionId();
      workerModelVersionId.value = model.onDidChangeContent(() => {
        workerModel.value.updateVersion();
      });
      workerModelVersion.value = model.getVersionId();
    }
  };

  const updateWorker = () => {
    if (!workerProxy.value) {
      workerProxy.value = monaco.languages.typescript.getTypeScriptWorker();
    }

    updateWorkerModel();
    updateWorkerModelVersionId();
  };

  const dispose = () => {
    disposeWorker();
    worker.terminate();
  };

  watch(model, () => {
    updateWorker();
  });

  return {
    workerProxy,
    workerModel,
    dispose,
  };
};
