import { describe, it, expect } from 'vitest'
import { render, screen } from '../test-utils'
import StatusBadge from '../../components/StatusBadge'

describe('StatusBadge', () => {
  it('renders pending status', () => {
    render(<StatusBadge status="pending" />)

    expect(screen.getByText('pending')).toBeInTheDocument()
    expect(screen.getByText('○')).toBeInTheDocument()
  })

  it('renders processing status', () => {
    render(<StatusBadge status="processing" />)

    expect(screen.getByText('processing')).toBeInTheDocument()
    expect(screen.getByText('◐')).toBeInTheDocument()
  })

  it('renders completed status', () => {
    render(<StatusBadge status="completed" />)

    expect(screen.getByText('completed')).toBeInTheDocument()
    expect(screen.getByText('●')).toBeInTheDocument()
  })

  it('renders failed status', () => {
    render(<StatusBadge status="failed" />)

    expect(screen.getByText('failed')).toBeInTheDocument()
    expect(screen.getByText('✕')).toBeInTheDocument()
  })
})
