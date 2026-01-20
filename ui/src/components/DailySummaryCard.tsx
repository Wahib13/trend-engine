import { useState } from 'react';
import type { DailySummary } from '../data-model/daily-summary';
import './DailySummaryCard.css';

interface Props {
  summary: DailySummary;
}

export function DailySummaryCard({ summary }: Props) {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggle = () => setIsExpanded(prev => !prev);

  return (
    <div className="daily-summary-card">
      <button
        className="daily-summary-header"
        onClick={toggle}
        aria-expanded={isExpanded}
      >
        <div className="header-content">
          <div className="topic-info">
            <span className="topic-badge">{summary.topic.name}</span>
            <h2 className="topic-title">{summary.topic.name.charAt(0).toUpperCase() + summary.topic.name.slice(1)}</h2>
          </div>
          <span className="expand-icon">{isExpanded ? '−' : '+'}</span>
        </div>
        {summary.summary && (
          <p className="summary-text">{summary.summary}</p>
        )}
      </button>

      {isExpanded && (
        <div className="articles-container">
          <div className="articles-header">
            <span className="articles-count">
              {summary.articles.length} {summary.articles.length === 1 ? 'article' : 'articles'}
            </span>
          </div>
          <ul className="articles-list">
            {summary.articles.map(article => (
              <li key={article.id} className="article-item">
                <a
                  href={article.url}
                  target="_blank"
                  rel="noreferrer"
                  className="article-link"
                >
                  <span className="article-title">{article.title}</span>
                  <svg
                    className="external-link-icon"
                    width="16"
                    height="16"
                    viewBox="0 0 16 16"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <path
                      d="M12 8.66667V12.6667C12 13.0203 11.8595 13.3594 11.6095 13.6095C11.3594 13.8595 11.0203 14 10.6667 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V5.33333C2 4.97971 2.14048 4.64057 2.39052 4.39052C2.64057 4.14048 2.97971 4 3.33333 4H7.33333M10 2H14M14 2V6M14 2L6.66667 9.33333"
                      stroke="currentColor"
                      strokeWidth="1.5"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                    />
                  </svg>
                </a>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}