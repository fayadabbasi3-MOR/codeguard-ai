import { describe, it, expect } from 'vitest'
import { render, screen } from '../test-utils'
import CategoryBadge from '../../components/CategoryBadge'

describe('CategoryBadge', () => {
  it('renders security category with icon', () => {
    render(<CategoryBadge category="security" />)

    expect(screen.getByText('security')).toBeInTheDocument()
    expect(screen.getByText('▲')).toBeInTheDocument()
  })

  it('renders quality category with icon', () => {
    render(<CategoryBadge category="quality" />)

    expect(screen.getByText('quality')).toBeInTheDocument()
    expect(screen.getByText('◆')).toBeInTheDocument()
  })

  it('renders testing category with icon', () => {
    render(<CategoryBadge category="testing" />)

    expect(screen.getByText('testing')).toBeInTheDocument()
    expect(screen.getByText('■')).toBeInTheDocument()
  })

  it('renders docs category with icon', () => {
    render(<CategoryBadge category="docs" />)

    expect(screen.getByText('docs')).toBeInTheDocument()
    expect(screen.getByText('●')).toBeInTheDocument()
  })

  it('renders performance category with icon', () => {
    render(<CategoryBadge category="performance" />)

    expect(screen.getByText('performance')).toBeInTheDocument()
    expect(screen.getByText('★')).toBeInTheDocument()
  })

  it('renders without icon when showIcon is false', () => {
    render(<CategoryBadge category="security" showIcon={false} />)

    expect(screen.getByText('security')).toBeInTheDocument()
    expect(screen.queryByText('▲')).not.toBeInTheDocument()
  })
})
