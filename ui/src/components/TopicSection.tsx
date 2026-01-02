import { useState } from "react";
import type { Topic } from "../data-model/topic";
import { useArticles } from "../hooks/articles";

interface Props {
  topic: Topic
}

export function TopicSection({ topic }: Props) {
  const { data: articles, isLoading } = useArticles(topic.id);

  const [isOpen, setIsOpen] = useState(false);

  const toggle = () => setIsOpen(prev => !prev);

  return (
    <>
      <h2
        onClick={toggle}
      >
        {topic.name}
        <span>{isOpen ? "-" : "+"}</span>
      </h2>

      {isOpen && (
        <div>
          {isLoading && <div>Loading articles...</div>}
          {!isLoading && articles?.length === 0 && <div>No articles</div>}

          <ul>
            {articles?.map(article => (
              <li key={article.id}>
                {article.url ? (
                  <a href={article.url} target="_blank" rel="noreferrer">
                    {article.title}
                  </a>
                ) : (
                  article.title
                )}
              </li>
            ))}
          </ul>
        </div>
      )}
    </>
  );
}
