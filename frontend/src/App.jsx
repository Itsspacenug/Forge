import { useState } from 'react'
import OptimizerPage from './pages/OptimizerPage'
import ResultsPage from './pages/ResultsPage'

export default function App() {
  const [selectedSchedule, setSelectedSchedule] = useState(null)

  if(selectedSchedule){
      return ( 
      <ResultsPage
        schedule={selectedSchedule}
        onBack={() => setSelectedSchedule(null)} 
        />
      )
  }

  return <OptimizerPage onSelectSchedule={setSelectedSchedule} />
}