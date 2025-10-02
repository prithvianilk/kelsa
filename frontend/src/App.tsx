import { useEffect, useMemo, useState } from 'react'

import {
  KelsaWorkServiceClient,
  type MainPageDataSuccess,
  type ByAppData,
} from '@src/api/workServiceClient'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const DEFAULT_LOOKBACK_TIME_IN_MS = 1000 * 60 * 60 * 24

function MyWorkPage() {
  const client = useMemo(() => new KelsaWorkServiceClient(API_BASE_URL), [])
  const [data, setData] = useState<MainPageDataSuccess | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [timestamp] = useState<number>(
    Date.now() - DEFAULT_LOOKBACK_TIME_IN_MS
  )
  const [error, setError] = useState<string | null>(null)
  
  const [selectedApp, setSelectedApp] = useState<string | null>(null)
  const [byAppData, setByAppData] = useState<ByAppData | null>(null)
  const [byAppLoading, setByAppLoading] = useState(false)
  const [byAppError, setByAppError] = useState<string | null>(null)

  useEffect(() => {
    async function getMainPageData() {
      setIsLoading(true)
      setError(null)

      try {
        const response = await client.getMainPageData({
          epochTime: timestamp,
          onlyActiveWork: false,
        })

        console.log(response)

        if ('message' in response) {
          setError(response.message)
          return
        }

        setData(response)
      } finally {
        setIsLoading(false)
      }
    }

    void getMainPageData()

    return () => {}
  }, [client])

  useEffect(() => {
    async function getByAppData() {
      if (!selectedApp) return

      setByAppLoading(true)
      setByAppError(null)

      try {
        const response = await client.getByAppData({
          app: selectedApp,
          epochTime: timestamp,
          onlyActiveWork: false,
        })

        console.log('By-app response:', response)

        if ('message' in response) {
          setByAppError(response.message)
          return
        }

        setByAppData(response)
      } finally {
        setByAppLoading(false)
      }
    }

    void getByAppData()
  }, [client, selectedApp, timestamp])

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600 text-lg">Loading your work data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-red-50 to-pink-50 flex items-center justify-center">
        <div className="bg-white rounded-lg shadow-lg p-8 max-w-md mx-auto">
          <div className="text-red-600 text-6xl mb-4 text-center">⚠️</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">Something went wrong</h2>
          <p className="text-gray-600">{error}</p>
        </div>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-yellow-50 to-orange-50 flex items-center justify-center">
        <div className="text-center">
          <div className="text-yellow-600 text-6xl mb-4">📊</div>
          <h2 className="text-xl font-semibold text-gray-800 mb-2">No data available</h2>
          <p className="text-gray-600">Try refreshing the page or check your connection.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-blue-50">
      <div className="container mx-auto px-6 py-8">
        <div className="max-w-6xl mx-auto">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-4xl font-bold text-gray-800 mb-2">Work Dashboard</h1>
            <p className="text-gray-600">Track your productivity across applications</p>
          </div>

          {/* Total Time Card */}
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8 border border-gray-100">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">Total Time Spent</h2>
                <div className="text-4xl font-bold text-blue-600">
                  {Math.round(data.total_time_spent_seconds / 60)}
                  <span className="text-lg font-normal text-gray-600 ml-2">minutes</span>
                </div>
              </div>
              <div className="text-blue-500 text-6xl">⏱️</div>
            </div>
          </div>

          {/* Apps Grid */}
          <div className="bg-white rounded-xl shadow-lg p-8 mb-8 border border-gray-100">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">By Application</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {data.work_by_app.map((item) => (
                <button
                  key={item.application}
                  onClick={() => setSelectedApp(item.application)}
                  className={`p-4 rounded-lg border-2 transition-all duration-200 ${
                    selectedApp === item.application
                      ? 'border-blue-500 bg-blue-50 shadow-md'
                      : 'border-gray-200 hover:border-gray-300 hover:shadow-sm'
                  }`}
                >
                  <div className="flex items-center justify-between">
                    <div className="text-left">
                      <h3 className="font-medium text-gray-800">{item.application}</h3>
                      <p className="text-gray-600 text-sm">Last 24 hours</p>
                    </div>
                    <div className="text-right">
                      <div className="text-xl font-bold text-blue-600">
                        {Math.round(item.seconds / 60)}
                      </div>
                      <div className="text-sm text-gray-500">min</div>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Selected App Details */}
          {selectedApp && (
            <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-2xl font-semibold text-gray-800">
                  Work in {selectedApp}
                </h2>
                <button
                  onClick={() => setSelectedApp(null)}
                  className="text-gray-400 hover:text-gray-600 transition-colors"
                >
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              {byAppLoading && (
                <div className="flex items-center justify-center py-12">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
                  <span className="ml-3 text-gray-600">Loading app data...</span>
                </div>
              )}

              {byAppError && (
                <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                  <div className="flex items-center">
                    <div className="text-red-500 text-xl mr-3">⚠️</div>
                    <div>
                      <h3 className="font-medium text-red-800">Error loading data</h3>
                      <p className="text-red-600 text-sm">{byAppError}</p>
                    </div>
                  </div>
                </div>
              )}

              {byAppData && !byAppLoading && (
                <div>
                  <div className="mb-6 p-4 bg-blue-50 rounded-lg">
                    <div className="flex items-center justify-between">
                      <div>
                        <span className="text-sm text-blue-600 font-medium">Total in {selectedApp}</span>
                        <div className="text-2xl font-bold text-blue-800">
                          {Math.floor(byAppData.total_time_spent_seconds / 60)} minutes
                        </div>
                      </div>
                      <div className="text-blue-200 text-sm">
                        {byAppData.group_key.charAt(0).toUpperCase() + byAppData.group_key.slice(1)}-level grouping
                      </div>
                    </div>
                  </div>

                  <div className="overflow-hidden rounded-lg border border-gray-200">
                    <table className="min-w-full divide-y divide-gray-200">
                      <thead className="bg-gray-50">
                        <tr>
                          <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                            {byAppData.group_key.charAt(0).toUpperCase() + byAppData.group_key.slice(1)}
                          </th>
                          <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
                            Time Spent
                          </th>
                        </tr>
                      </thead>
                      <tbody className="bg-white divide-y divide-gray-200">
                        {byAppData.work_by_group.map((item) => (
                          <tr key={item.group} className="hover:bg-gray-50">
                            <td className="px-6 py-4 whitespace-nowrap font-medium text-gray-900">
                              {item.group}
                            </td>
                            <td className="px-6 py-4 whitespace-nowrap text-right">
                              <span className="text-gray-900 font-medium">
                                {Math.floor(item.seconds / 60)} min
                              </span>
                              <span className="ml-2 text-gray-500 text-sm">
                                ({Math.floor(item.seconds / 3600 * 100) / 100}h)
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default MyWorkPage