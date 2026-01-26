import { useState } from 'react'
import { useTriggerAnalysis } from '../hooks/useApi'

function TriggerAnalysis() {
  const [repo, setRepo] = useState('')
  const [prNumber, setPrNumber] = useState('')
  const [isOpen, setIsOpen] = useState(false)

  const triggerMutation = useTriggerAnalysis()

  const handleSubmit = (e) => {
    e.preventDefault()
    if (!repo || !prNumber) return

    triggerMutation.mutate(
      { repo, prNumber: parseInt(prNumber, 10) },
      {
        onSuccess: () => {
          setRepo('')
          setPrNumber('')
          setIsOpen(false)
        },
      }
    )
  }

  if (!isOpen) {
    return (
      <button
        onClick={() => setIsOpen(true)}
        className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
      >
        + Analyze PR
      </button>
    )
  }

  return (
    <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
      <div className="flex items-center justify-between mb-3">
        <h4 className="text-sm font-medium text-gray-900">Trigger Manual Analysis</h4>
        <button
          onClick={() => setIsOpen(false)}
          className="text-gray-400 hover:text-gray-500"
        >
          ✕
        </button>
      </div>
      <form onSubmit={handleSubmit} className="space-y-3">
        <div>
          <label htmlFor="repo" className="block text-xs font-medium text-gray-700">
            Repository (owner/repo)
          </label>
          <input
            type="text"
            id="repo"
            value={repo}
            onChange={(e) => setRepo(e.target.value)}
            placeholder="facebook/react"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 text-sm px-3 py-2 border"
          />
        </div>
        <div>
          <label htmlFor="prNumber" className="block text-xs font-medium text-gray-700">
            PR Number
          </label>
          <input
            type="number"
            id="prNumber"
            value={prNumber}
            onChange={(e) => setPrNumber(e.target.value)}
            placeholder="123"
            className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-gray-500 focus:ring-gray-500 text-sm px-3 py-2 border"
          />
        </div>
        <div className="flex space-x-2">
          <button
            type="submit"
            disabled={triggerMutation.isPending || !repo || !prNumber}
            className="flex-1 inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-black hover:bg-gray-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {triggerMutation.isPending ? 'Analyzing...' : 'Analyze'}
          </button>
          <button
            type="button"
            onClick={() => setIsOpen(false)}
            className="px-3 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
          >
            Cancel
          </button>
        </div>
        {triggerMutation.isError && (
          <p className="text-sm text-gray-700">
            Error: {triggerMutation.error?.message || 'Failed to trigger analysis'}
          </p>
        )}
        {triggerMutation.isSuccess && (
          <p className="text-sm text-gray-600">
            Analysis queued! ID: {triggerMutation.data?.analysis_id}
          </p>
        )}
      </form>
    </div>
  )
}

export default TriggerAnalysis
