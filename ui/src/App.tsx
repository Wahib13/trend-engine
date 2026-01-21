import { useMemo } from 'react';
import { DailySummaryCard } from './components/DailySummaryCard';
import { useDailySummaries } from './hooks/daily-summaries';
import type { DailySummary } from './data-model/daily-summary';
import './App.css';

function App() {
  const { data: dailySummaries, isLoading, error } = useDailySummaries();

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const summaryDate = new Date(date);
    summaryDate.setHours(0, 0, 0, 0);

    if (summaryDate.getTime() === today.getTime()) {
      return 'Today';
    }

    return date.toLocaleDateString('en-US', {
      weekday: 'long',
      month: 'long',
      day: 'numeric'
    });
  };

  const summariesByDate = useMemo(() => {
    if (!dailySummaries || dailySummaries.length === 0) {
      return [];
    }

    // Group summaries by date
    const grouped = dailySummaries.reduce((acc, summary) => {
      const dateKey = summary.date;
      if (!acc[dateKey]) {
        acc[dateKey] = [];
      }
      acc[dateKey].push(summary);
      return acc;
    }, {} as Record<string, DailySummary[]>);

    // Convert to array and sort by date (most recent first)
    const sortedDates = Object.keys(grouped).sort((a, b) => {
      return new Date(b).getTime() - new Date(a).getTime();
    });

    return sortedDates.map(date => ({
      date,
      formattedDate: formatDate(date),
      summaries: grouped[date]
    }));
  }, [dailySummaries]);

  if (isLoading) {
    return (
      <div className="app-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p className="loading-text">Loading news...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="app-container">
        <div className="error-container">
          <h2>Failed to load news</h2>
          <p>Please try again later.</p>
        </div>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">Trend Engine</h1>
        <p className="app-subtitle">News Summary</p>
      </header>

      <main className="app-main">
        {summariesByDate.length === 0 ? (
          <div className="empty-state">
            <p>No summaries available.</p>
          </div>
        ) : (
          <div className="date-sections">
            {summariesByDate.map(({ date, formattedDate, summaries }) => (
              <section key={date} className="date-section">
                <h2 className="date-header">{formattedDate}</h2>
                <div className="summaries-grid">
                  {summaries.map(summary => (
                    <DailySummaryCard key={summary.id} summary={summary} />
                  ))}
                </div>
              </section>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App
