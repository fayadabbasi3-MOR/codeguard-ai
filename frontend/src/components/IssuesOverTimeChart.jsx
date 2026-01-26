import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts'
import ChartHeader from './ChartHeader'

const CHART_TOOLTIP = "Tracks the daily trend of issues found and PRs analyzed over the selected time period. Use this to identify patterns in code quality and review activity."

function IssuesOverTimeChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <div className="h-4 bg-gray-200 rounded w-1/4 mb-4 animate-pulse"></div>
        <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
      </div>
    )
  }

  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <ChartHeader title="Issues Over Time" tooltip={CHART_TOOLTIP} />
        <div className="h-64 flex items-center justify-center text-gray-500">
          No data available yet
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
      <ChartHeader title="Issues Over Time" tooltip={CHART_TOOLTIP} />
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
            <XAxis
              dataKey="date"
              tick={{ fontSize: 12, fill: '#666' }}
              tickFormatter={(value) => {
                const date = new Date(value)
                return `${date.getMonth() + 1}/${date.getDate()}`
              }}
            />
            <YAxis tick={{ fontSize: 12, fill: '#666' }} />
            <Tooltip
              labelFormatter={(value) => new Date(value).toLocaleDateString()}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
            />
            <Legend />
            <Line
              type="monotone"
              dataKey="issues_found"
              name="Total Issues"
              stroke="#000000"
              strokeWidth={2}
              dot={{ r: 3, fill: '#000' }}
              activeDot={{ r: 5 }}
            />
            <Line
              type="monotone"
              dataKey="critical_issues"
              name="Critical"
              stroke="#666666"
              strokeWidth={2}
              strokeDasharray="5 5"
              dot={{ r: 3, fill: '#666' }}
              activeDot={{ r: 5 }}
            />
            <Line
              type="monotone"
              dataKey="prs_analyzed"
              name="PRs Analyzed"
              stroke="#999999"
              strokeWidth={2}
              dot={{ r: 3, fill: '#999' }}
              activeDot={{ r: 5 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default IssuesOverTimeChart
