const categoryStyles = {
  security: 'bg-black text-white border-black',
  quality: 'bg-gray-700 text-white border-gray-700',
  testing: 'bg-gray-500 text-white border-gray-500',
  docs: 'bg-gray-300 text-gray-800 border-gray-300',
  performance: 'bg-gray-400 text-gray-900 border-gray-400',
}

const categoryIcons = {
  security: '▲',
  quality: '◆',
  testing: '■',
  docs: '●',
  performance: '★',
}

function CategoryBadge({ category, showIcon = true }) {
  const style = categoryStyles[category] || 'bg-gray-50 text-gray-700 border-gray-200'
  const icon = categoryIcons[category] || ''

  return (
    <span className={`inline-flex items-center px-2 py-0.5 rounded text-xs font-medium border ${style}`}>
      {showIcon && icon && <span className="mr-1">{icon}</span>}
      {category}
    </span>
  )
}

export default CategoryBadge
