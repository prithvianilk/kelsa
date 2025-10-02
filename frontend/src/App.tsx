import { useEffect, useMemo, useState } from 'react'

import {
  KelsaWorkServiceClient,
  type MainPageDataSuccess,
  type ByAppData,
} from '@src/api/mainPageClient'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const DEFAULT_LOOKBACK_TIME_IN_MS = 1000 * 60 * 60 * 24

function MyWorkPage() {
  const client = useMemo(() => new KelsaWorkServiceClient(API_BASE_URL), [])
  const [data, setData] = useState<MainPageDataSuccess | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [timestamp, setTimestamp] = useState<number>(
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
    return <div>Loading...</div>
  }

  if (error) {
    return <div>{error}</div>
  }

  if (!data) {
    return <div>No data</div>
  }

  return (
    <div>
      <section>
        <h1>Total Time Spent</h1>
        <p>{Math.round(data.total_time_spent_seconds / 60)} minutes</p>
      </section>

      <section>
        <h2>By Application</h2>
        <ul>
          {data.work_by_app.map((item) => (
            <li key={item.application}>
              <button 
                onClick={() => setSelectedApp(item.application)}
                style={{ 
                  background: selectedApp === item.application ? '#646cff' : 'transparent',
                  color: selectedApp === item.application ? 'white' : 'inherit',
                  border: 'none',
                  cursor: 'pointer',
                  padding: '8px 16px',
                  marginRight: '8px'
                }}
              >
                {item.application}
              </button>
              <span>{Math.round(item.seconds / 60)} min</span>
            </li>
          ))}
        </ul>
      </section>

      {selectedApp && (
        <section>
          <h2>Work in {selectedApp}</h2>
          {byAppLoading && <div>Loading app data...</div>}
          {byAppError && <div>Error: {byAppError}</div>}
          {byAppData && !byAppLoading && (
            <div>
              <p>Total: {Math.floor(byAppData.total_time_spent_seconds / 60)} min ({byAppData.group_key.charAt(0).toUpperCase() + byAppData.group_key.slice(1)}-level)</p>
              <table style={{ width: '100%', borderCollapse: 'collapse', border: '1px solid #ccc' }}>
                <thead>
                  <tr>
                    <th style={{ border: '1px solid #ccc', padding: '8px' }}>{byAppData.group_key.charAt(0).toUpperCase() + byAppData.group_key.slice(1)}</th>
                    <th style={{ border: '1px solid #ccc', padding: '8px' }}>Time</th>
                  </tr>
                </thead>
                <tbody>
                  {byAppData.work_by_group.map((item) => (
                    <tr key={item.group}>
                      <td style={{ border: '1px solid #ccc', padding: '8px' }}>{item.group}</td>
                      <td style={{ border: '1px solid #ccc', padding: '8px' }}>{Math.floor(item.seconds / 60)} min</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>
      )}
    </div>
  )
}

export default MyWorkPage
