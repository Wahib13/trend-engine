import { useQuery } from "@tanstack/react-query";
import { fetchTopics } from "../api/topics";
import type { Topic } from "../data-model/topic";

export function useTopics() {
  return useQuery<Topic[]>({
    queryKey: ["topics"],
    queryFn: fetchTopics,
    staleTime: 1000 * 60 * 5, // 5 minutes
  });
}