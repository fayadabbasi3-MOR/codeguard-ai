import { useState } from 'react'
import { useMetrics, useAnalyses, useRepos } from '../hooks/useApi'
import MetricsGrid from '../components/MetricsGrid'
import IssuesOverTimeChart from '../components/IssuesOverTimeChart'
import IssuesByCategoryChart from '../components/IssuesByCategoryChart'
import IssuesBySeverityChart from '../components/IssuesBySeverityChart'
import TopIssuesTable from '../components/TopIssuesTable'
import AnalysesList from '../components/AnalysesList'
import TriggerAnalysis from '../components/TriggerAnalysis'

function Dashboard() {
  const [selectedRepo, setSelectedRepo] = useState('')
  const [days, setDays] = useState(30)

  const metricsParams = { days }
  if (selectedRepo) metricsParams.repo = selectedRepo

  const { data: metrics, isLoading: metricsLoading } = useMetrics(metricsParams)
  const { data: analyses, isLoading: analysesLoading } = useAnalyses({
    repo: selectedRepo || undefined,
    limit: 10
  })
  const { data: repos } = useRepos()

  return (
    <div>
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            CodeGuard Dashboard
          </h1>
          <p className="text-sm text-gray-500 mt-1">
            AI-powered PR review assistant
          </p>
        </div>
        <TriggerAnalysis />
      </div>

      {/* Filters */}
      <div className="flex items-center space-x-4 mb-6">
        <div>
          <label htmlFor="repo-filter" className="block text-xs font-medium text-gray-500 mb-1">
            Repository
          </label>
          <select
            id="repo-filter"
            value={selectedRepo}
            onChange={(e) => setSelectedRepo(e.target.value)}
            className="block w-48 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
          >
            <option value="">All Repositories</option>
            {repos?.map((repo) => (
              <option key={repo.repo} value={repo.repo}>
                {repo.repo} ({repo.analysis_count})
              </option>
            ))}
          </select>
        </div>
        <div>
          <label htmlFor="days-filter" className="block text-xs font-medium text-gray-500 mb-1">
            Time Range
          </label>
          <select
            id="days-filter"
            value={days}
            onChange={(e) => setDays(parseInt(e.target.value, 10))}
            className="block w-32 rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm"
          >
            <option value={7}>Last 7 days</option>
            <option value={14}>Last 14 days</option>
            <option value={30}>Last 30 days</option>
            <option value={90}>Last 90 days</option>
          </select>
        </div>
      </div>

      {/* Metrics Grid */}
      <MetricsGrid metrics={metrics} isLoading={metricsLoading} />

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <IssuesOverTimeChart
          data={metrics?.daily_metrics}
          isLoading={metricsLoading}
        />
        <IssuesBySeverityChart
          data={metrics?.issues_by_severity}
          isLoading={metricsLoading}
        />
      </div>

      {/* Category Chart and Top Issues */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6">
        <IssuesByCategoryChart
          data={metrics?.issues_by_category}
          isLoading={metricsLoading}
        />
        <TopIssuesTable
          data={metrics?.top_issues}
          isLoading={metricsLoading}
        />
      </div>

      {/* Recent Analyses */}
      <div className="mt-6">
        <AnalysesList analyses={analyses} isLoading={analysesLoading} />
      </div>
    </div>
  )
}

export default Dashboard
