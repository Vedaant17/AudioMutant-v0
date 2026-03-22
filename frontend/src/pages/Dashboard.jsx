import ResultsPanel from "../components/ResultsPanel";

function Dashboard({ result, file, audioUrl }) {
  return (
    <div>
      <ResultsPanel result={result} file={file} />
    </div>
  );
}

export default Dashboard;