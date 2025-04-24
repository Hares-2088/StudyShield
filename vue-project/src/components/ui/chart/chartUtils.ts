// src/components/ui/chart/chartUtils.ts
export const formatTooltipDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      weekday: 'short', 
      month: 'short', 
      day: 'numeric'
    });
  };