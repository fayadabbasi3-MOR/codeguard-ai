const severityStyles = {
  critical: 'bg-black text-white',
  warning: 'bg-gray-600 text-white',
  suggestion: 'bg-gray-300 text-gray-800',
}

const severityIcons = {
  critical: '●',
  warning: '◐',
  suggestion: '○',
}

function SeverityBadge({ severity, showIcon = true }) {
  const style = severityStyles[severity] || 'bg-gray-100 text-gray-800'
  const icon = severityIcons[severity] || ''

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${style}`}>
      {showIcon && icon && <span className="mr-1">{icon}</span>}
      {severity}
    </span>
  )
}

export default SeverityBadge
