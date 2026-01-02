export interface Article {
  id: string;
  title: string;
  url: string;
  source: string;

  topicId: string | null;
  topicName?: string;
}
