import { apiFetch } from "./client";
import type { Topic } from "../data-model/topic";

export function fetchTopics(): Promise<Topic[]> {
  return apiFetch<Topic[]>("/topics/");
}
