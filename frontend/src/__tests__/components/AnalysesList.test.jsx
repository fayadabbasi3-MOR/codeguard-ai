import { describe, it, expect } from 'vitest'
import { render, screen } from '../test-utils'
import AnalysesList from '../../components/AnalysesList'

describe('AnalysesList', () => {
  const mockAnalyses = [
    {
      id: 'analysis-1',
      repo: 'owner/repo',
      pr_number: 42,
      pr_title: 'Add new feature',
      author: 'developer',
      status: 'completed',
      analyzed_at: new Date().toISOString(),
      summary: {
        critical: 1,
        warnings: 2,
        suggestions: 3,
        total_issues: 6,
      },
    },
    {
      id: 'analysis-2',
      repo: 'owner/repo',
      pr_number: 43,
      pr_title: 'Fix bug',
      author: 'developer',
      status: 'processing',
      analyzed_at: new Date().toISOString(),
      summary: {
        critical: 0,
        warnings: 0,
        suggestions: 0,
        total_issues: 0,
      },
    },
  ]

  it('renders loading state', () => {
    render(<AnalysesList analyses={null} isLoading={true} />)

    const skeletons = document.querySelectorAll('.animate-pulse')
    expect(skeletons.length).toBeGreaterThan(0)
  })

  it('renders empty state when no analyses', () => {
    render(<AnalysesList analyses={[]} isLoading={false} />)

    expect(screen.getByText('No analyses yet.')).toBeInTheDocument()
  })

  it('renders list of analyses', () => {
    render(<AnalysesList analyses={mockAnalyses} isLoading={false} />)

    expect(screen.getByText('Add new feature')).toBeInTheDocument()
    expect(screen.getByText('Fix bug')).toBeInTheDocument()
  })

  it('shows PR number and repo', () => {
    render(<AnalysesList analyses={mockAnalyses} isLoading={false} />)

    expect(screen.getAllByText('owner/repo')).toHaveLength(2)
    expect(screen.getByText('#42')).toBeInTheDocument()
    expect(screen.getByText('#43')).toBeInTheDocument()
  })

  it('shows author name', () => {
    render(<AnalysesList analyses={mockAnalyses} isLoading={false} />)

    expect(screen.getAllByText('by developer')).toHaveLength(2)
  })

  it('shows status badges', () => {
    render(<AnalysesList analyses={mockAnalyses} isLoading={false} />)

    expect(screen.getByText('completed')).toBeInTheDocument()
    expect(screen.getByText('processing')).toBeInTheDocument()
  })

  it('shows no issues message for clean PR', () => {
    const cleanAnalyses = [
      {
        ...mockAnalyses[0],
        summary: { critical: 0, warnings: 0, suggestions: 0, total_issues: 0 },
      },
    ]

    render(<AnalysesList analyses={cleanAnalyses} isLoading={false} />)

    expect(screen.getByText('✅ No issues')).toBeInTheDocument()
  })
})
