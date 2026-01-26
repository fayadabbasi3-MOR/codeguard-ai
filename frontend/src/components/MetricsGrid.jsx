import StatsCard from './StatsCard'

const TOOLTIPS = {
  prsAnalyzed: "Total number of pull requests that have been analyzed by CodeGuard within the selected time period.",
  issuesFound: "Total number of code issues identified across all analyzed PRs. Issues are categorized by severity (critical, warning, suggestion) and type (security, quality, testing, docs, performance).",
  criticalIssues: "High-priority issues that should be addressed before merging. These typically include security vulnerabilities, hardcoded secrets, or code that could cause production failures.",
  timeSaved: "Estimated review time saved by catching issues automatically. Calculated as 3 minutes per issue found, based on average time engineers spend identifying and commenting on similar issues during manual review.",
}

function MetricsGrid({ metrics, isLoading }) {
  if (isLoading) {
    return (
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[...Array(4)].map((_, i) => (
          <div key={i} className="bg-white rounded-lg shadow p-6 animate-pulse border border-gray-200">
            <div className="h-4 bg-gray-200 rounded w-1/2 mb-4"></div>
            <div className="h-8 bg-gray-200 rounded w-1/3"></div>
          </div>
        ))}
      </div>
    )
  }

  if (!metrics) {
    return null
  }

  const { issues_by_severity } = metrics

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <StatsCard
        title="PRs Analyzed"
        value={metrics.total_prs_analyzed}
        icon="◆"
        subtitle="Total pull requests"
        tooltip={TOOLTIPS.prsAnalyzed}
      />
      <StatsCard
        title="Issues Found"
        value={metrics.total_issues_found}
        icon="●"
        subtitle={`${metrics.avg_issues_per_pr.toFixed(1)} per PR avg`}
        tooltip={TOOLTIPS.issuesFound}
      />
      <StatsCard
        title="Critical Issues"
        value={issues_by_severity?.critical || 0}
        icon="▲"
        subtitle="Security & blocking issues"
        tooltip={TOOLTIPS.criticalIssues}
      />
      <StatsCard
        title="Time Saved"
        value={`${metrics.estimated_time_saved_hours.toFixed(1)}h`}
        icon="○"
        subtitle="Estimated review time"
        tooltip={TOOLTIPS.timeSaved}
      />
    </div>
  )
}

export default MetricsGrid
