import { describe, it, expect } from 'vitest'
import { render, screen } from '../test-utils'
import MetricsGrid from '../../components/MetricsGrid'

describe('MetricsGrid', () => {
  const mockMetrics = {
    total_prs_analyzed: 100,
    total_issues_found: 250,
    avg_issues_per_pr: 2.5,
    estimated_time_saved_hours: 12.5,
    issues_by_severity: {
      critical: 10,
      warning: 90,
      suggestion: 150,
    },
  }

  it('renders loading state', () => {
    render(<MetricsGrid metrics={null} isLoading={true} />)

    // Should show loading skeleton (animated divs)
    const skeletons = document.querySelectorAll('.animate-pulse')
    expect(skeletons.length).toBeGreaterThan(0)
  })

  it('renders nothing when metrics is null and not loading', () => {
    const { container } = render(<MetricsGrid metrics={null} isLoading={false} />)

    expect(container.firstChild).toBeNull()
  })

  it('renders PRs analyzed', () => {
    render(<MetricsGrid metrics={mockMetrics} isLoading={false} />)

    expect(screen.getByText('PRs Analyzed')).toBeInTheDocument()
    expect(screen.getByText('100')).toBeInTheDocument()
  })

  it('renders issues found with average', () => {
    render(<MetricsGrid metrics={mockMetrics} isLoading={false} />)

    expect(screen.getByText('Issues Found')).toBeInTheDocument()
    expect(screen.getByText('250')).toBeInTheDocument()
    expect(screen.getByText('2.5 per PR avg')).toBeInTheDocument()
  })

  it('renders critical issues count', () => {
    render(<MetricsGrid metrics={mockMetrics} isLoading={false} />)

    expect(screen.getByText('Critical Issues')).toBeInTheDocument()
    expect(screen.getByText('10')).toBeInTheDocument()
  })

  it('renders time saved', () => {
    render(<MetricsGrid metrics={mockMetrics} isLoading={false} />)

    expect(screen.getByText('Time Saved')).toBeInTheDocument()
    expect(screen.getByText('12.5h')).toBeInTheDocument()
  })
})
