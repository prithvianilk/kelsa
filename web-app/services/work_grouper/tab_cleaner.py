import re
from abc import abstractmethod

class TabCleaner:
    def __init__(self):
        pass

    @abstractmethod
    def matches(self, tab):
        pass

    @abstractmethod
    def clean_tab(self, tab):
        pass

class ConfluenceTabCleaner(TabCleaner):
    def matches(self, tab):
        return "Confluence" in tab

    def clean_tab(self, tab):
        tab = tab.replace("- Confluence", "")
        tab = tab.replace("Add Page - ", "")
        tab = tab.replace("Edit - ", "")
        splits = tab.split(" - ")
        return " — ".join(splits[:-1])

class DatabricksTabCleaner(TabCleaner):
    def matches(self, tab):
        return tab.endswith("- Databricks")

    def clean_tab(self, tab):
        return "Databricks"

class JenkinsTabCleaner(TabCleaner):
    def matches(self, tab):
        return tab.endswith("- Jenkins")

    def clean_tab(self, tab):
        return "Jenkins"

class DatadogTabCleaner(TabCleaner):
    def matches(self, tab):
        return tab.endswith(" | Datadog")

    def clean_tab(self, tab):
        return "Datadog"

class YoutubeTabCleaner(TabCleaner):
    def matches(self, tab):
        return True

    def clean_tab(self, tab):
        cleaned_tab = re.sub(r"\(([0-9]+)\) ", "", tab, count=1)
        if len(cleaned_tab.replace(" ", "")) == 0:
            return tab
        return cleaned_tab

class JioHotstarTabCleaner(TabCleaner):
    def matches(self, tab):
        return "Watch " in tab and "on JioHotstar" in tab
    
    def clean_tab(self, tab):
        tab = tab.replace("Watch ", "")
        tab = tab.replace(" on JioHotstar", "")
        tab = tab.replace("Episode ", "")
        items = tab.split(" ")
        items_excluding_season_and_episode = items[:-2]
        return " ".join(items_excluding_season_and_episode) + " - JioHotstar"

TAB_CLEANERS = [
    ConfluenceTabCleaner(),
    DatabricksTabCleaner(),
    JenkinsTabCleaner(),
    DatadogTabCleaner(),
    JioHotstarTabCleaner(),
    YoutubeTabCleaner(),
]

def get_tab_cleaner(tab) -> TabCleaner:
    for cleaner in TAB_CLEANERS:
        if cleaner.matches(tab):
            return cleaner
    return YoutubeTabCleaner()