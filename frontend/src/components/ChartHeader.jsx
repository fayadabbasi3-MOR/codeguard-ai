import Tooltip from './Tooltip'

function ChartHeader({ title, tooltip }) {
  return (
    <div className="flex items-center space-x-1 mb-4">
      <h3 className="text-lg font-medium text-gray-900">{title}</h3>
      {tooltip && (
        <Tooltip content={tooltip}>
          <span className="text-gray-400 text-sm cursor-help">ⓘ</span>
        </Tooltip>
      )}
    </div>
  )
}

export default ChartHeader
