import { ChartOptions, ChartData } from "chart.js";

export interface ChartJS {
  type: string;
  data: ChartData;
  options: ChartOptions;
}
