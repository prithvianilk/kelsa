export interface WorkByApp {
  seconds: number
  application: string
}

export interface WorkByAppAndTime {
  seconds: number
  application: string
  done_at: string
}

export type MainPageData = MainPageDataSuccess | ApiError

export interface MainPageDataSuccess {
  total_time_spent_seconds: number
  work_by_app: WorkByApp[]
  work_by_app_and_time: WorkByAppAndTime[]
}

export interface GetMainPageDataParams {
  sinceTime: number
  tillTime?: number
  onlyActiveWork?: boolean
}

export interface WorkByGroup {
  seconds: number
  group: string
}

export interface WorkByGroupAndTime {
  seconds: number
  group: string
  done_at: string
}

export interface ByAppData {
  total_time_spent_seconds: number
  work_by_group: WorkByGroup[]
  work_by_group_and_time: WorkByGroupAndTime[]
  app_name: string
  group_key: string
}

export interface GetByAppDataParams {
  app: string
  sinceTime: number
  tillTime?: number
  onlyActiveWork?: boolean
}

export interface ApiError {
  message: string
}

export class KelsaWorkServiceClient {
  private readonly baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  async getMainPageData({
    sinceTime,
    tillTime,
    onlyActiveWork = false,
  }: GetMainPageDataParams): Promise<MainPageData> {
    const searchParams = new URLSearchParams({
      since_time: sinceTime.toString(),
      only_active_work: String(onlyActiveWork),
    })

    if (tillTime !== undefined) {
      searchParams.append('till_time', tillTime.toString())
    }

    try {
      const response = await fetch(
        `${this.baseUrl}/api/v1/main-page-data?${searchParams.toString()}`
      )

      if (!response.ok) {
        return await this.buildErrorMessage(response)
      }

      return (await response.json()) as MainPageData
    } catch (error) {
      console.error(error)
      return { message: 'Failed to fetch main page data' }
    }
  }

  async getByAppData({ app, sinceTime, tillTime, onlyActiveWork = false }: GetByAppDataParams): Promise<ByAppData | ApiError> {
    const searchParams = new URLSearchParams({
      app,
      since_time: sinceTime.toString(),
      only_active_work: String(onlyActiveWork),
    })

    if (tillTime !== undefined) {
      searchParams.append('till_time', tillTime.toString())
    }

    try {
      const response = await fetch(
        `${this.baseUrl}/api/v1/by-app-data?${searchParams.toString()}`
      )

      if (!response.ok) {
        return await this.buildErrorMessage(response)
      }

      return (await response.json()) as ByAppData
    } catch (error) {
      console.error(error)
      return { message: 'Failed to fetch by-app data' };
    }
  }

  private async buildErrorMessage(response: Response): Promise<ApiError> {
    return (await response.json()) as ApiError
  }
}
