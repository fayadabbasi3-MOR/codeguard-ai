import Tooltip from './Tooltip'

function StatsCard({ title, value, subtitle, icon, trend, trendUp, tooltip }) {
  return (
    <div className="bg-white rounded-lg shadow p-6 border border-gray-200">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-1">
          <h3 className="text-sm font-medium text-gray-500">{title}</h3>
          {tooltip && (
            <Tooltip content={tooltip}>
              <span className="text-gray-400 text-xs">ⓘ</span>
            </Tooltip>
          )}
        </div>
        {icon && <span className="text-2xl">{icon}</span>}
      </div>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
      {subtitle && (
        <p className="text-sm text-gray-500 mt-1">{subtitle}</p>
      )}
      {trend !== undefined && (
        <div className={`flex items-center mt-2 text-sm ${trendUp ? 'text-gray-900' : 'text-gray-600'}`}>
          <span>{trendUp ? '↑' : '↓'}</span>
          <span className="ml-1">{trend}</span>
        </div>
      )}
    </div>
  )
}

export default StatsCard
