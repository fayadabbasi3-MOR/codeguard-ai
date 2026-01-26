import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import api from '../api/client'

// Query keys
export const queryKeys = {
  metrics: (params) => ['metrics', params],
  analyses: (params) => ['analyses', params],
  analysis: (id) => ['analysis', id],
  repos: ['repos'],
}

// Metrics hooks
export function useMetrics(params = {}) {
  return useQuery({
    queryKey: queryKeys.metrics(params),
    queryFn: () => api.getMetrics(params),
    refetchInterval: 30000, // Refresh every 30 seconds
  })
}

// Analyses hooks
export function useAnalyses(params = {}) {
  return useQuery({
    queryKey: queryKeys.analyses(params),
    queryFn: () => api.getAnalyses(params),
    refetchInterval: 10000, // Refresh every 10 seconds
  })
}

export function useAnalysis(id) {
  return useQuery({
    queryKey: queryKeys.analysis(id),
    queryFn: () => api.getAnalysis(id),
    enabled: !!id,
  })
}

// Repos hook
export function useRepos() {
  return useQuery({
    queryKey: queryKeys.repos,
    queryFn: api.getRepos,
  })
}

// Feedback mutation
export function useFeedback() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: api.submitFeedback,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['analyses'] })
      queryClient.invalidateQueries({ queryKey: ['analysis'] })
    },
  })
}

// Trigger analysis mutation
export function useTriggerAnalysis() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: ({ repo, prNumber }) => api.triggerAnalysis(repo, prNumber),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['analyses'] })
    },
  })
}
