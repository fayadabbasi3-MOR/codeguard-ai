import { describe, it, expect } from 'vitest'
import { render, screen } from '../test-utils'
import SeverityBadge from '../../components/SeverityBadge'

describe('SeverityBadge', () => {
  it('renders critical severity with icon', () => {
    render(<SeverityBadge severity="critical" />)

    expect(screen.getByText('critical')).toBeInTheDocument()
    expect(screen.getByText('●')).toBeInTheDocument()
  })

  it('renders warning severity with icon', () => {
    render(<SeverityBadge severity="warning" />)

    expect(screen.getByText('warning')).toBeInTheDocument()
    expect(screen.getByText('◐')).toBeInTheDocument()
  })

  it('renders suggestion severity with icon', () => {
    render(<SeverityBadge severity="suggestion" />)

    expect(screen.getByText('suggestion')).toBeInTheDocument()
    expect(screen.getByText('○')).toBeInTheDocument()
  })

  it('renders without icon when showIcon is false', () => {
    render(<SeverityBadge severity="critical" showIcon={false} />)

    expect(screen.getByText('critical')).toBeInTheDocument()
    expect(screen.queryByText('●')).not.toBeInTheDocument()
  })

  it('handles unknown severity gracefully', () => {
    render(<SeverityBadge severity="unknown" />)

    expect(screen.getByText('unknown')).toBeInTheDocument()
  })
})
