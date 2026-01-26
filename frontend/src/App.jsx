import { BrowserRouter, Routes, Route } from 'react-router-dom'
import Dashboard from './pages/Dashboard'
import AnalysisDetail from './pages/AnalysisDetail'
import Layout from './components/Layout'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Dashboard />} />
          <Route path="analysis/:id" element={<AnalysisDetail />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
