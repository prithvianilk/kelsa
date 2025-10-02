import { useEffect, useMemo, useState } from 'react'

import {
  KelsaWorkServiceClient,
  type MainPageDataSuccess,
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
              <span>{item.application}</span>
              <span>{Math.round(item.seconds / 60)} min</span>
            </li>
          ))}
        </ul>
      </section>
    </div>
  )
}

export default MyWorkPage
