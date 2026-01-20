import { apiFetch } from './client';
import type { DailySummary } from '../data-model/daily-summary';

interface GetDailySummariesParams {
  date?: string;
  topic_id?: number;
  skip?: number;
  limit?: number;
}

export async function getDailySummaries(
  params?: GetDailySummariesParams
): Promise<DailySummary[]> {
  const searchParams = new URLSearchParams();

  if (params?.date) searchParams.append('date', params.date);
  if (params?.topic_id) searchParams.append('topic_id', String(params.topic_id));
  if (params?.skip !== undefined) searchParams.append('skip', String(params.skip));
  if (params?.limit !== undefined) searchParams.append('limit', String(params.limit));

  const queryString = searchParams.toString();
  const path = `/daily-summaries/${queryString ? `?${queryString}` : ''}`;

  return apiFetch<DailySummary[]>(path);
}