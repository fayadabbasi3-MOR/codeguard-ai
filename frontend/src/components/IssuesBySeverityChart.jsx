import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import ChartHeader from './ChartHeader'

const CHART_TOOLTIP = "Distribution of issues by severity level. Critical issues require immediate attention, Warnings should be reviewed, and Suggestions are optional improvements."

const COLORS = {
  critical: '#000000',
  warning: '#666666',
  suggestion: '#cccccc',
}

const LABELS = {
  critical: '● Critical',
  warning: '◐ Warning',
  suggestion: '○ Suggestion',
}

function IssuesBySeverityChart({ data, isLoading }) {
  if (isLoading) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <div className="h-4 bg-gray-200 rounded w-1/4 mb-4 animate-pulse"></div>
        <div className="h-64 bg-gray-100 rounded animate-pulse"></div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <ChartHeader title="Issues by Severity" tooltip={CHART_TOOLTIP} />
        <div className="h-64 flex items-center justify-center text-gray-500">
          No data available yet
        </div>
      </div>
    )
  }

  const chartData = [
    { name: 'critical', value: data.critical || 0 },
    { name: 'warning', value: data.warning || 0 },
    { name: 'suggestion', value: data.suggestion || 0 },
  ].filter(item => item.value > 0)

  const total = chartData.reduce((sum, item) => sum + item.value, 0)

  if (total === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <ChartHeader title="Issues by Severity" tooltip={CHART_TOOLTIP} />
        <div className="h-64 flex items-center justify-center text-gray-500">
          No issues found yet
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
      <ChartHeader title="Issues by Severity" tooltip={CHART_TOOLTIP} />
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              innerRadius={60}
              outerRadius={80}
              paddingAngle={5}
              dataKey="value"
              label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={COLORS[entry.name]} />
              ))}
            </Pie>
            <Tooltip
              formatter={(value, name) => [value, LABELS[name] || name]}
              contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
            />
            <Legend
              formatter={(value) => LABELS[value] || value}
              wrapperStyle={{ fontSize: '14px' }}
            />
          </PieChart>
        </ResponsiveContainer>
      </div>
      <div className="text-center text-sm text-gray-500 mt-2">
        Total: {total} issues
      </div>
    </div>
  )
}

export default IssuesBySeverityChart
