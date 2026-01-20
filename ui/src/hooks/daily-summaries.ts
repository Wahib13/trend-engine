import { useQuery } from '@tanstack/react-query';
import { getDailySummaries } from '../api/daily-summaries';

interface UseDailySummariesOptions {
  date?: string;
  topic_id?: number;
}

export function useDailySummaries(options?: UseDailySummariesOptions) {
  return useQuery({
    queryKey: ['daily-summaries', options?.date, options?.topic_id],
    queryFn: () => getDailySummaries(options),
  });
}