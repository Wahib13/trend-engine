import { DailySummaryCard } from './components/DailySummaryCard';
import { useDailySummaries } from './hooks/daily-summaries';
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

  if (isLoading) {
    return (
      <div className="app-container">
        <div className="loading-container">
          <div className="loading-spinner"></div>
          <p className="loading-text">Loading today's news...</p>
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

  const summaryDate = dailySummaries && dailySummaries.length > 0
    ? formatDate(dailySummaries[0].date)
    : 'Today';

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">Trend Engine</h1>
        <p className="app-subtitle">{summaryDate}'s News Summary</p>
      </header>

      <main className="app-main">
        {!dailySummaries || dailySummaries.length === 0 ? (
          <div className="empty-state">
            <p>No summaries available for today.</p>
          </div>
        ) : (
          <div className="summaries-grid">
            {dailySummaries.map(summary => (
              <DailySummaryCard key={summary.id} summary={summary} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App
