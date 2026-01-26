const statusStyles = {
  pending: 'bg-gray-200 text-gray-700',
  processing: 'bg-gray-400 text-white',
  completed: 'bg-black text-white',
  failed: 'bg-gray-600 text-white',
}

const statusIcons = {
  pending: '○',
  processing: '◐',
  completed: '●',
  failed: '✕',
}

function StatusBadge({ status }) {
  const style = statusStyles[status] || 'bg-gray-100 text-gray-800'
  const icon = statusIcons[status] || ''

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${style}`}>
      <span className="mr-1">{icon}</span>
      {status}
    </span>
  )
}

export default StatusBadge
