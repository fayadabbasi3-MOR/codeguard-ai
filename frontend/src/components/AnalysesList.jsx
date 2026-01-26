import { Link } from 'react-router-dom'
import { formatDistanceToNow } from 'date-fns'
import StatusBadge from './StatusBadge'
import SeverityBadge from './SeverityBadge'

function AnalysesList({ analyses, isLoading }) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <div className="h-6 bg-gray-200 rounded w-1/4 animate-pulse"></div>
        </div>
        <div className="divide-y divide-gray-200">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="px-6 py-4">
              <div className="h-5 bg-gray-200 rounded w-3/4 mb-2 animate-pulse"></div>
              <div className="h-4 bg-gray-100 rounded w-1/2 animate-pulse"></div>
            </div>
          ))}
        </div>
      </div>
    )
  }

  if (!analyses || analyses.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow border border-gray-200">
        <div className="px-6 py-4 border-b border-gray-200">
          <h3 className="text-lg font-medium text-gray-900">Recent Analyses</h3>
        </div>
        <div className="px-6 py-12 text-center">
          <p className="text-gray-500">No analyses yet.</p>
          <p className="text-sm text-gray-400 mt-1">
            Trigger an analysis or connect a GitHub repo to get started.
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow border border-gray-200">
      <div className="px-6 py-4 border-b border-gray-200">
        <h3 className="text-lg font-medium text-gray-900">Recent Analyses</h3>
      </div>
      <div className="divide-y divide-gray-200">
        {analyses.map((analysis) => (
          <Link
            key={analysis.id}
            to={`/analysis/${analysis.id}`}
            className="block px-6 py-4 hover:bg-gray-50 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div className="flex-1 min-w-0">
                <div className="flex items-center space-x-3">
                  <p className="text-sm font-medium text-gray-900 truncate">
                    {analysis.pr_title || `PR #${analysis.pr_number}`}
                  </p>
                  <StatusBadge status={analysis.status} />
                </div>
                <div className="flex items-center mt-1 space-x-2 text-sm text-gray-500">
                  <span>{analysis.repo}</span>
                  <span>•</span>
                  <span>#{analysis.pr_number}</span>
                  {analysis.author && (
                    <>
                      <span>•</span>
                      <span>by {analysis.author}</span>
                    </>
                  )}
                </div>
              </div>
              <div className="flex items-center space-x-4 ml-4">
                {analysis.status === 'completed' && (
                  <div className="flex items-center space-x-2">
                    {analysis.summary.critical > 0 && (
                      <span className="text-sm">
                        <SeverityBadge severity="critical" showIcon={false} />
                        <span className="ml-1">{analysis.summary.critical}</span>
                      </span>
                    )}
                    {analysis.summary.warnings > 0 && (
                      <span className="text-sm">
                        <SeverityBadge severity="warning" showIcon={false} />
                        <span className="ml-1">{analysis.summary.warnings}</span>
                      </span>
                    )}
                    {analysis.summary.suggestions > 0 && (
                      <span className="text-sm">
                        <SeverityBadge severity="suggestion" showIcon={false} />
                        <span className="ml-1">{analysis.summary.suggestions}</span>
                      </span>
                    )}
                    {analysis.summary.total_issues === 0 && (
                      <span className="text-sm text-gray-600">● No issues</span>
                    )}
                  </div>
                )}
                <span className="text-sm text-gray-400">
                  {formatDistanceToNow(new Date(analysis.analyzed_at), { addSuffix: true })}
                </span>
              </div>
            </div>
          </Link>
        ))}
      </div>
    </div>
  )
}

export default AnalysesList
