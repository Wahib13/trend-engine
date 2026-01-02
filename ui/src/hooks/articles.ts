import { useQuery } from "@tanstack/react-query";
import { fetchArticlesByTopic } from "../api/articles";

export function useArticles(topicId: number) {
  return useQuery({
    queryKey: ["articles", topicId],
    queryFn: () => fetchArticlesByTopic(topicId),
  });
}
