from abc import abstractmethod
from common import logger
from common.logger import Logger
from openai import OpenAI


class SummarisationService:
    def __init__(self, logger: Logger):
        self.logger = logger

    @abstractmethod
    def summarise_work(self, work) -> str:
        pass

class OpenAIGpt5NanoSummarisationService(SummarisationService):
    def __init__(self, logger: Logger, openai_client: OpenAI):
        super().__init__(logger)
        self.openai_client = openai_client

    def summarise_work(self, work) -> str:
        self.logger.debug(f"{work}")
        
        system_prompt = """
        You are a helpful assistant that summarises work by responding with 
        what are the major things that the user has done since the start time.
        Keep it brief, only mention the top 2-3 things the user has done per day.

        The input is in the following format:
        [   
            [12, 'vscode', '2025-08-03 08:00:00'], 
            [12, '404 Not Found', '2025-08-03 08:00:00']
        ]
        where the first element is the time spent (in seconds) on the thing, the second element is the thing, and the third element is the hour of the day.
        For example, I spent 12 seconds on "vscode" at anytime from 8:00 AM to 8:59 AM.

        The response should be in the following format:
        - Date: <date>
        - Total time spent: <total time spent> (in minutes or hours)
        - Things done:
            - <thing 1> - <time spent on thing 1>
            - <thing 2> - <time spent on thing 2>
            - <thing 3> - <time spent on thing 3>

        If the total time spent is less than 1 minute, then ignore it.
        thing 1 and thing 2 should never be the same. Always merge all work.
        """

        user_prompt = f"""
        Please summarise the following work in a few paragraphs:
        {work}
        """
        
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            store=True,
        )

        return response.choices[0].message.content.strip()