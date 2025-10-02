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
  epochTime: number
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
    epochTime,
    onlyActiveWork = false,
  }: GetMainPageDataParams): Promise<MainPageData> {
    const searchParams = new URLSearchParams({
      epoch_time: epochTime.toString(),
      only_active_work: String(onlyActiveWork),
    })

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

  private async buildErrorMessage(response: Response): Promise<ApiError> {
    return (await response.json()) as ApiError
  }
}
