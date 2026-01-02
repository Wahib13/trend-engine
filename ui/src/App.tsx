import { TopicSection } from './components/TopicSection';
import { useTopics } from './hooks/topics';

function App() {
const { data: topics, isLoading, error } = useTopics();

  if (isLoading) return <div>Loading topics...</div>;
  if (error) return <div>Failed to load topics</div>;

  return (
    <>
    <h1>Today's Articles</h1>
    <div>
      {topics?.map(topic => (
        <TopicSection key={topic.id} topic={topic} />
      ))}
    </div>
    </>
  )
}

export default App
