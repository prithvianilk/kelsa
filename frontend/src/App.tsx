import { useEffect, useMemo, useState } from 'react'
import { cn } from '@/lib/utils'
import {
  KelsaWorkServiceClient,
  type MainPageDataSuccess,
  type ByAppData,
} from '@src/api/workServiceClient'
import { Button } from '@/components/ui/button'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import {
  ChartContainer,
  ChartTooltip,
  ChartTooltipContent,
} from '@/components/ui/chart'
import { Pie, PieChart } from 'recharts'

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

const DEFAULT_LOOKBACK_TIME_IN_MS = 1000 * 60 * 60 * 24

function formatMinutes(seconds: number) {
  return Math.round(seconds / 60)
}

function formatHours(seconds: number) {
  return Math.floor((seconds / 3600) * 100) / 100
}

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
  }, [client, timestamp])

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
      <div className="flex min-h-screen items-center justify-center bg-background">
        <div className="space-y-4 text-center">
          <div className="mx-auto h-12 w-12 animate-spin rounded-full border-2 border-muted-foreground/40 border-t-primary" />
          <p className="text-muted-foreground">Loading your work data...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <Card className="w-full max-w-md text-center">
          <CardHeader>
            <CardTitle className="text-destructive">Something went wrong</CardTitle>
            <CardDescription>{error}</CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  if (!data) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-background">
        <Card className="w-full max-w-md text-center">
          <CardHeader>
            <CardTitle>No data available</CardTitle>
            <CardDescription>
              Try refreshing the page or check your connection.
            </CardDescription>
          </CardHeader>
        </Card>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-background text-foreground">
      <div className="mx-auto flex w-full max-w-6xl flex-col gap-8 px-6 py-10">
        <header className="flex flex-col gap-2">
          <h1 className="text-3xl font-semibold tracking-tight">Work analytics dashboard</h1>
          <p className="text-muted-foreground">
            Time analytics for your work
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2">
          <div className="flex flex-col gap-6">
            <Card className="bg-card/60 backdrop-blur">
              <CardHeader>
                <CardDescription>Total Time Spent</CardDescription>
                <CardTitle className="text-4xl font-semibold">
                  {formatMinutes(data.total_time_spent_seconds)}
                  <span className="ml-2 text-base font-normal text-muted-foreground">
                    minutes
                  </span>
                </CardTitle>
              </CardHeader>
            </Card>

            {data.work_by_app.length > 0 && (
              <Card className="flex-1 flex flex-col">
                <CardHeader>
                  <CardTitle>Time distribution</CardTitle>
                  <CardDescription>By application</CardDescription>
                </CardHeader>
                <CardContent className="flex-1 flex items-center justify-center">
                  <ChartContainer
                    config={Object.fromEntries(
                      data.work_by_app.map((app, idx) => [
                        app.application,
                        {
                          label: app.application,
                          color: idx === 0 ? 'hsl(210, 100%, 50%)' : `hsl(${210 + (idx * 25) % 180}, ${70 + (idx * 10) % 30}%, ${45 + (idx * 8) % 25}%)`,
                        },
                      ])
                    )}
                    className="aspect-square max-h-[400px] w-full"
                  >
                    <PieChart>
                      <ChartTooltip
                        cursor={false}
                        content={<ChartTooltipContent hideLabel />}
                      />
                      <Pie
                        data={data.work_by_app.map((item) => ({
                          application: item.application,
                          minutes: formatMinutes(item.seconds),
                          fill: `var(--color-${item.application})`,
                        }))}
                        dataKey="minutes"
                        nameKey="application"
                      />
                    </PieChart>
                  </ChartContainer>
                </CardContent>
              </Card>
            )}
          </div>

          <Card className="bg-card/60 backdrop-blur">
            <CardHeader>
              <CardTitle className="text-sm font-medium">By Application</CardTitle>
              <CardDescription>Last 24 hours</CardDescription>
            </CardHeader>
            <CardContent className="grid gap-2">
              {data.work_by_app.map((item) => {
                const minutes = formatMinutes(item.seconds)
                return (
                  <Button
                    key={item.application}
                    variant={selectedApp === item.application ? 'default' : 'ghost'}
                    className={cn(
                      'justify-between text-left bg-transparent hover:bg-accent/40 py-8',
                      selectedApp === item.application && 'bg-primary text-primary-foreground hover:bg-primary'
                    )}
                    onClick={() => setSelectedApp(item.application)}
                  >
                    <span className="flex flex-col">
                      <span className="text-sm font-medium">{item.application}</span>
                      <span className="text-xs text-muted-foreground">
                        Last 24 hours
                      </span>
                    </span>
                    <span className="text-sm font-medium">{minutes} min</span>
                  </Button>
                )
              })}
            </CardContent>
          </Card>
        </div>

        {selectedApp ? (
          <Card>
            <CardHeader className="flex flex-row items-center justify-between">
              <div>
                <CardDescription>Work in</CardDescription>
                <CardTitle>{selectedApp}</CardTitle>
              </div>
              <Button variant="ghost" size="sm" onClick={() => setSelectedApp(null)}>
                Clear
              </Button>
            </CardHeader>
            <CardContent className="space-y-6">
              {byAppLoading && (
                <div className="flex items-center justify-center py-10 text-muted-foreground">
                  Loading app data...
                </div>
              )}

              {byAppError && (
                <div className="rounded-md border border-destructive/30 bg-destructive/10 px-4 py-3 text-sm text-destructive">
                  {byAppError}
                </div>
              )}

              {byAppData && !byAppLoading && !byAppError && (
                <div className="space-y-6">
                  <div className="rounded-md border bg-muted/40 p-4">
                    <p className="text-xs font-medium text-muted-foreground">
                      Total in {selectedApp}
                    </p>
                    <p className="text-2xl font-semibold">
                      {formatMinutes(byAppData.total_time_spent_seconds)} minutes
                    </p>
                  </div>

                  <div className="overflow-hidden rounded-md border">
                    <table className="min-w-full text-sm">
                      <thead className="bg-muted/60 text-left text-xs uppercase text-muted-foreground">
                        <tr>
                          <th className="px-6 py-3 font-medium">
                            {byAppData.group_key.charAt(0).toUpperCase() +
                              byAppData.group_key.slice(1)}
                          </th>
                          <th className="px-6 py-3 text-right font-medium">Time spent</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y">
                        {byAppData.work_by_group.map((item) => (
                          <tr key={item.group} className="hover:bg-muted/40">
                            <td className="px-6 py-4 font-medium">{item.group}</td>
                            <td className="px-6 py-4 text-right">
                              <span className="font-medium">
                                {formatMinutes(item.seconds)} min
                              </span>
                              <span className="ml-2 text-xs text-muted-foreground">
                                ({formatHours(item.seconds)}h)
                              </span>
                            </td>
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        ) : (
          <Card className="border-dashed">
            <CardHeader>
              <CardTitle className="text-base font-medium">
                Select an application
              </CardTitle>
              <CardDescription>
                Choose an app from the list to explore time spent across groups.
              </CardDescription>
            </CardHeader>
          </Card>
        )}
      </div>
    </div>
  )
}

export default MyWorkPage