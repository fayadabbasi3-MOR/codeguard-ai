import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from 'recharts'
import ChartHeader from './ChartHeader'

const CHART_TOOLTIP = "Breakdown of issues by category: Security (vulnerabilities, secrets), Quality (code smells, complexity), Testing (missing tests), Docs (documentation gaps), Performance (efficiency issues)."

const COLORS = {
  security: '#000000',
  quality: '#333333',
  testing: '#666666',
  docs: '#999999',
  performance: '#cccccc',
}

function IssuesByCategoryChart({ data, isLoading }) {
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
        <ChartHeader title="Issues by Category" tooltip={CHART_TOOLTIP} />
        <div className="h-64 flex items-center justify-center text-gray-500">
          No data available yet
        </div>
      </div>
    )
  }

  const chartData = [
    { name: 'Security', value: data.security || 0, icon: '▲' },
    { name: 'Quality', value: data.quality || 0, icon: '◆' },
    { name: 'Testing', value: data.testing || 0, icon: '■' },
    { name: 'Docs', value: data.docs || 0, icon: '●' },
    { name: 'Performance', value: data.performance || 0, icon: '★' },
  ].filter(item => item.value > 0)

  if (chartData.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
        <ChartHeader title="Issues by Category" tooltip={CHART_TOOLTIP} />
        <div className="h-64 flex items-center justify-center text-gray-500">
          No issues found yet
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
      <ChartHeader title="Issues by Category" tooltip={CHART_TOOLTIP} />
      <div className="h-64">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData} layout="vertical" margin={{ top: 5, right: 30, left: 80, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
            <XAxis type="number" tick={{ fontSize: 12, fill: '#666' }} />
            <YAxis
              type="category"
              dataKey="name"
              tick={{ fontSize: 12, fill: '#666' }}
              tickFormatter={(value, index) => `${chartData[index]?.icon || ''} ${value}`}
            />
            <Tooltip
              contentStyle={{ borderRadius: '8px', border: '1px solid #e5e7eb' }}
              formatter={(value) => [value, 'Issues']}
            />
            <Bar dataKey="value" radius={[0, 4, 4, 0]}>
              {chartData.map((entry, index) => (
                <Cell
                  key={`cell-${index}`}
                  fill={COLORS[entry.name.toLowerCase()] || '#6b7280'}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  )
}

export default IssuesByCategoryChart
