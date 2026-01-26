import { describe, it, expect } from 'vitest'
import { render, screen } from '../test-utils'
import StatsCard from '../../components/StatsCard'

describe('StatsCard', () => {
  it('renders title and value', () => {
    render(<StatsCard title="PRs Analyzed" value={42} />)

    expect(screen.getByText('PRs Analyzed')).toBeInTheDocument()
    expect(screen.getByText('42')).toBeInTheDocument()
  })

  it('renders subtitle when provided', () => {
    render(
      <StatsCard title="Issues" value={10} subtitle="Last 30 days" />
    )

    expect(screen.getByText('Last 30 days')).toBeInTheDocument()
  })

  it('renders icon when provided', () => {
    render(<StatsCard title="Time Saved" value="5h" icon="⏱️" />)

    expect(screen.getByText('⏱️')).toBeInTheDocument()
  })

  it('renders upward trend indicator', () => {
    render(
      <StatsCard title="PRs" value={100} trend="+20%" trendUp={true} />
    )

    expect(screen.getByText('↑')).toBeInTheDocument()
    expect(screen.getByText('+20%')).toBeInTheDocument()
  })

  it('renders downward trend indicator', () => {
    render(
      <StatsCard title="Issues" value={50} trend="-10%" trendUp={false} />
    )

    expect(screen.getByText('↓')).toBeInTheDocument()
    expect(screen.getByText('-10%')).toBeInTheDocument()
  })
})
