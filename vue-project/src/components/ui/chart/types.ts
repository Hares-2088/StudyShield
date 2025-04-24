// src/components/ui/chart/types.ts
export interface ChartConfig {
    [key: string]: {
      label: string;
      color?: string;
    };
  }
  
  export interface ChartTooltipContentProps {
    active?: boolean;
    payload?: any[];
    label?: string;
    nameKey?: string;
    labelFormatter?: (value: any) => string;
    hideLabel?: boolean;
  }