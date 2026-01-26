import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// API functions
export const api = {
  // Metrics
  getMetrics: async (params = {}) => {
    const { data } = await apiClient.get('/api/metrics', { params })
    return data
  },

  // Analyses
  getAnalyses: async (params = {}) => {
    const { data } = await apiClient.get('/api/analyses', { params })
    return data
  },

  getAnalysis: async (id) => {
    const { data } = await apiClient.get(`/api/analysis/${id}`)
    return data
  },

  getPRAnalysis: async (repo, prNumber) => {
    const { data } = await apiClient.get(`/api/pr/${repo}/${prNumber}`)
    return data
  },

  // Repos
  getRepos: async () => {
    const { data } = await apiClient.get('/api/repos')
    return data
  },

  // Feedback
  submitFeedback: async (feedback) => {
    const { data } = await apiClient.post('/api/feedback', feedback)
    return data
  },

  // Test trigger
  triggerAnalysis: async (repo, prNumber) => {
    const { data } = await apiClient.post('/webhook/test', null, {
      params: { repo, pr_number: prNumber },
    })
    return data
  },

  // Health check
  healthCheck: async () => {
    const { data } = await apiClient.get('/health')
    return data
  },
}

export default api
