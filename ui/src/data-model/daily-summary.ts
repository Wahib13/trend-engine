import type { Topic } from "./topic";

export interface Article {
  id: number;
  title: string;
  url: string;
  topics: Topic[];
}

export interface DailySummary {
  id: number;
  date: string;
  summary: string | null;
  topic: Topic;
  articles: Article[];
}
