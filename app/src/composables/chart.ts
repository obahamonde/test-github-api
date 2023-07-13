import { Chart, registerables, ChartData, ChartOptions } from "chart.js";

export const useChart = () => {
  Chart.register(...registerables);
  const chartRef = ref<HTMLCanvasElement | null>(null);
  const chart = ref<Chart | null>(null);
  const data = ref<ChartData | null>(null);
  const options = ref<ChartOptions | null>(null);
  const charType: Ref<
    | "line"
    | "bar"
    | "pie"
    | "doughnut"
    | "radar"
    | "polarArea"
    | "bubble"
    | "scatter"
  > = ref<
    | "line"
    | "bar"
    | "pie"
    | "doughnut"
    | "radar"
    | "polarArea"
    | "bubble"
    | "scatter"
  >("line");
  const createChart = () => {
    if (chartRef.value) {
      chart.value = new Chart(chartRef.value, {
        type: charType.value,
        data: data.value!,
        options: options.value!,
      });
    }
  };

  const updateChart = () => {
    if (chart.value) {
      chart.value.data = data.value!;
      chart.value.update();
    }
  };

  const destroy = () => {
    if (chart.value) {
      chart.value.destroy();
      chart.value = null;
    }
  };

  const render = () => {
    if (chart.value) {
      updateChart();
    } else {
      createChart();
    }
  };

  return {
    chartRef,
    chart,
    data,
    options,
    charType,
    render,
    destroy,
  };
};
