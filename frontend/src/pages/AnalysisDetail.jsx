import { useParams, Link } from 'react-router-dom'
import { formatDistanceToNow, format } from 'date-fns'
import { useAnalysis, useFeedback } from '../hooks/useApi'
import StatusBadge from '../components/StatusBadge'
import SeverityBadge from '../components/SeverityBadge'
import CategoryBadge from '../components/CategoryBadge'

function IssueCard({ issue }) {
  const feedbackMutation = useFeedback()

  const handleFeedback = (isHelpful) => {
    feedbackMutation.mutate({
      issue_id: issue.id,
      is_helpful: isHelpful,
    })
  }

  return (
    <div className="border border-gray-200 rounded-lg p-4 hover:border-gray-400 transition-colors">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <div className="flex items-center space-x-2 mb-2">
            <SeverityBadge severity={issue.severity} />
            <CategoryBadge category={issue.category} />
          </div>
          <h4 className="text-sm font-medium text-gray-900">{issue.title}</h4>
          <p className="text-sm text-gray-600 mt-1">{issue.message}</p>

          <div className="mt-3 text-sm">
            <p className="text-gray-500">
              <span className="font-medium">File:</span> {issue.file_path}
              {issue.line_number && ` (line ${issue.line_number})`}
            </p>
          </div>

          {issue.explanation && (
            <div className="mt-3 p-3 bg-gray-100 rounded-md border border-gray-200">
              <p className="text-sm text-gray-700">
                <span className="font-medium">Why this matters:</span> {issue.explanation}
              </p>
            </div>
          )}

          {issue.suggestion && (
            <div className="mt-3 p-3 bg-gray-50 rounded-md border border-gray-200">
              <p className="text-sm text-gray-700">
                <span className="font-medium">Suggestion:</span> {issue.suggestion}
              </p>
            </div>
          )}
        </div>
      </div>

      <div className="mt-4 pt-3 border-t border-gray-200 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <span className="text-xs text-gray-500">Was this helpful?</span>
          <button
            onClick={() => handleFeedback(true)}
            disabled={feedbackMutation.isPending || issue.is_helpful !== null}
            className={`px-2 py-1 text-xs rounded ${
              issue.is_helpful === true
                ? 'bg-black text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            } disabled:opacity-50`}
          >
            + Yes
          </button>
          <button
            onClick={() => handleFeedback(false)}
            disabled={feedbackMutation.isPending || issue.is_helpful !== null}
            className={`px-2 py-1 text-xs rounded ${
              issue.is_helpful === false
                ? 'bg-gray-600 text-white'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            } disabled:opacity-50`}
          >
            - No
          </button>
        </div>
        {issue.is_helpful !== null && (
          <span className="text-xs text-gray-400">Feedback recorded</span>
        )}
      </div>
    </div>
  )
}

function AnalysisDetail() {
  const { id } = useParams()
  const { data: analysis, isLoading, error } = useAnalysis(id)

  if (isLoading) {
    return (
      <div className="animate-pulse">
        <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
        <div className="h-4 bg-gray-200 rounded w-1/2 mb-8"></div>
        <div className="space-y-4">
          {[...Array(3)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-100 rounded"></div>
          ))}
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <h2 className="text-lg font-medium text-gray-900">Error loading analysis</h2>
        <p className="text-gray-500 mt-2">{error.message}</p>
        <Link to="/" className="text-gray-900 hover:text-gray-600 mt-4 inline-block underline">
          ← Back to Dashboard
        </Link>
      </div>
    )
  }

  if (!analysis) {
    return (
      <div className="text-center py-12">
        <h2 className="text-lg font-medium text-gray-900">Analysis not found</h2>
        <Link to="/" className="text-gray-900 hover:text-gray-600 mt-4 inline-block underline">
          ← Back to Dashboard
        </Link>
      </div>
    )
  }

  const { summary, issues, metadata } = analysis

  return (
    <div>
      {/* Header */}
      <div className="mb-6">
        <Link to="/" className="text-sm text-gray-900 hover:text-gray-600 underline">
          ← Back to Dashboard
        </Link>
      </div>

      <div className="bg-white rounded-lg shadow p-6 mb-6 border border-gray-200">
        <div className="flex items-start justify-between">
          <div>
            <div className="flex items-center space-x-3">
              <h1 className="text-2xl font-bold text-gray-900">
                {analysis.pr_title || `PR #${analysis.pr_number}`}
              </h1>
              <StatusBadge status={analysis.status} />
            </div>
            <div className="mt-2 flex items-center space-x-2 text-sm text-gray-500">
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
            {analysis.pr_url && (
              <a
                href={analysis.pr_url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-sm text-gray-900 hover:text-gray-600 mt-2 inline-block underline"
              >
                View on GitHub →
              </a>
            )}
          </div>
        </div>

        {/* Stats */}
        <div className="mt-6 grid grid-cols-2 md:grid-cols-5 gap-4">
          <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
            <p className="text-xs text-gray-500">Total Issues</p>
            <p className="text-xl font-bold text-gray-900">{summary.total_issues}</p>
          </div>
          <div className="bg-black rounded-lg p-3">
            <p className="text-xs text-gray-300">Critical</p>
            <p className="text-xl font-bold text-white">{summary.critical}</p>
          </div>
          <div className="bg-gray-600 rounded-lg p-3">
            <p className="text-xs text-gray-300">Warnings</p>
            <p className="text-xl font-bold text-white">{summary.warnings}</p>
          </div>
          <div className="bg-gray-300 rounded-lg p-3">
            <p className="text-xs text-gray-600">Suggestions</p>
            <p className="text-xl font-bold text-gray-800">{summary.suggestions}</p>
          </div>
          <div className="bg-gray-50 rounded-lg p-3 border border-gray-200">
            <p className="text-xs text-gray-500">Analysis Time</p>
            <p className="text-xl font-bold text-gray-900">{(metadata.analysis_time_ms / 1000).toFixed(1)}s</p>
          </div>
        </div>

        {/* Metadata */}
        <div className="mt-4 pt-4 border-t border-gray-200 text-sm text-gray-500">
          <span>Analyzed {formatDistanceToNow(new Date(metadata.analyzed_at), { addSuffix: true })}</span>
          <span className="mx-2">•</span>
          <span>{metadata.files_changed} files changed</span>
          <span className="mx-2">•</span>
          <span>+{metadata.lines_added} -{metadata.lines_removed} lines</span>
          <span className="mx-2">•</span>
          <span>{metadata.tokens_used} tokens used</span>
        </div>
      </div>

      {/* Issues */}
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <h2 className="text-lg font-medium text-gray-900 mb-4">
          Issues ({issues.length})
        </h2>

        {issues.length === 0 ? (
          <div className="text-center py-8">
            <span className="text-4xl">●</span>
            <p className="text-gray-600 mt-2">No issues found! Great job!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {/* Group by severity */}
            {['critical', 'warning', 'suggestion'].map((severity) => {
              const severityIssues = issues.filter((i) => i.severity === severity)
              if (severityIssues.length === 0) return null

              return (
                <div key={severity}>
                  <h3 className="text-sm font-medium text-gray-700 mb-3 capitalize">
                    {severity === 'critical' && '● '}
                    {severity === 'warning' && '◐ '}
                    {severity === 'suggestion' && '○ '}
                    {severity} ({severityIssues.length})
                  </h3>
                  <div className="space-y-3">
                    {severityIssues.map((issue) => (
                      <IssueCard key={issue.id} issue={issue} />
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}

export default AnalysisDetail
