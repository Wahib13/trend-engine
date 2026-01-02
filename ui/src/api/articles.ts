import { apiFetch } from "./client";
import type { Article } from "../data-model/article";

export async function fetchArticlesByTopic(topicId: number): Promise<Article[]> {
  return apiFetch<Article[]>("/articles/?topic_id=" + topicId);
}
