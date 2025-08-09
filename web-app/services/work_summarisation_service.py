from abc import abstractmethod
from common.logger import Logger
from openai import OpenAI


class Llm:
    def __init__(self, logger: Logger):
        self.logger = logger

    @abstractmethod
    def call(self, system_prompt: str, user_prompt: str) -> str:
        pass

class OpenAIGpt4oMiniLlm(Llm):
    def __init__(self, logger: Logger, openai_client: OpenAI):
        super().__init__(logger)
        self.openai_client = openai_client

    def call(self, system_prompt: str, user_prompt: str) -> str:
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            store=True,
        )
        return response.choices[0].message.content.strip()

class SummarisationService:
    def __init__(self, logger: Logger):
        self.logger = logger

    @abstractmethod
    def summarise_work(self, work) -> str:
        pass

class ArcWorkSummarisationService(SummarisationService):
    def __init__(self, logger: Logger, llm: Llm):
        super().__init__(logger)
        self.llm = llm

    def summarise_work(self, work) -> str:
        self.logger.debug(f"{work}")
        
        system_prompt = """
        You are a helpful assistant that summarises time spent on Arc (a web browser) by responding with 
        what are the major things that the user has done since the start time.
        Keep it brief, only mention the top 2-3 things the user has done per day.

        The input is in the following format:
        [   
            [12, 'EC2 Instance Connect | ap-south-1', '2025-08-03 08:00:00'], 
            [12, '404 Not Found', '2025-08-03 08:00:00']
        ]
        where the first element is the time spent (in seconds) on the thing, the second element is the thing, and the third element is the hour of the day.
        For example, I spent 12 seconds on "EC2 Instance Connect | ap-south-1" at anytime from 8:00 AM to 8:59 AM.
        Remember, the time spent is in seconds, not minutes or hours. So convert it to minutes or hours.

        The response should be in the following format:
        - Date: <date>
        - Total time spent: <total time spent> (in minutes or hours. Don't include time spent in seconds ever)
        - Things done:
            - <thing 1> - <time spent on thing 1>
            - <thing 2> - <time spent on thing 2>
            - <thing 3> - <time spent on thing 3>

        If the total time spent is less than 1 minute, then ignore it.
        thing 1 and thing 2 should never be the same. Always merge all work.
        Categorise the thing being done. For example, "EC2 Instance Connect | ap-south-1" is a "AWS" thing.
        You should expect a lot of youtube, tv shows, etc. All of these should be categoried into a general category, but not too generic that youtube and tv shows are both "Entertainment".
        For ex, "Silicon valley SE1E4" should be categoried "Silicon valley" and not "Entertainment".
        So if I have 30 minutes of "Silicon valley E1" and 10 minutes of "Silicon valley E2", then the summary should be "Silicon valley" with 40 minutes of time spent.
        """

        user_prompt = f"""
        Please summarise the following time spent on Arc in a few paragraphs:
        {work}
        """
        
        return self.llm.call(system_prompt, user_prompt)