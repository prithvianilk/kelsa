import re
from abc import abstractmethod

class TabCleaner:
    def __init__(self):
        pass

    @abstractmethod
    def matches(self, tab: str) -> bool:
        pass

    @abstractmethod
    def clean_tab(self, tab: str) -> str:
        pass

class ConfluenceTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        return "Confluence" in tab

    def clean_tab(self, tab: str) -> str:
        tab = tab.replace("- Confluence", "")
        tab = tab.replace("Add Page - ", "")
        tab = tab.replace("Edit - ", "")
        splits = tab.split(" - ")
        return " — ".join(splits[:-1]) + " - Confluence"

class DatabricksTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        return tab.endswith("- Databricks")

    def clean_tab(self, tab: str) -> str:
        return "Databricks"

class JenkinsTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        return tab.endswith("- Jenkins")

    def clean_tab(self, tab: str) -> str:
        return "Jenkins"

class DatadogTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        return tab.endswith(" | Datadog")

    def clean_tab(self, tab: str) -> str:
        return "Datadog"

class YoutubeTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        return True

    def clean_tab(self, tab: str) -> str:
        cleaned_tab = re.sub(r"\(([0-9]+)\) ", "", tab, count=1)
        if len(cleaned_tab.replace(" ", "")) == 0:
            return tab
        return cleaned_tab

class JioHotstarTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        return "Watch " in tab and "on JioHotstar" in tab
    
    def clean_tab(self, tab: str) -> str:
        """
        Matches any tab that looks like:

        Watch Succession S2 Episode 9 on JioHotstar

        Watch Silicon Valley S2 Episode 9 on JioHotstar
        """
        tab = tab.replace("Watch ", "")
        tab = tab.replace(" on JioHotstar", "")
        tab = tab.replace("Episode ", "")
        items = tab.split(" ")
        items_excluding_season_and_episode = items[:-2]
        return " ".join(items_excluding_season_and_episode) + " - JioHotstar"

class GoogleMeetTabCleaner(TabCleaner):
    def matches(self, tab: str) -> bool:
        """
        Matches any tab that looks like: umb-oqqa-xqf
        """
        return re.search(r"[a-z]{3}-[a-z]{4}-[a-z]{3}", tab) is not None
    
    def clean_tab(self, tab: str) -> str:
        return "Google Meet"

TAB_CLEANERS: list[TabCleaner] = [
    ConfluenceTabCleaner(),
    GoogleMeetTabCleaner(),
    DatabricksTabCleaner(),
    JenkinsTabCleaner(),
    DatadogTabCleaner(),
    JioHotstarTabCleaner(),
    YoutubeTabCleaner(),
]

def get_tab_cleaner(tab: str) -> TabCleaner:
    for cleaner in TAB_CLEANERS:
        if cleaner.matches(tab):
            return cleaner
    return YoutubeTabCleaner()