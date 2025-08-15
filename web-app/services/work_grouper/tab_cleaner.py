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

tab_cleaners = [
    ConfluenceTabCleaner(),
    DatabricksTabCleaner(),
    JenkinsTabCleaner(),
    DatadogTabCleaner(),
    YoutubeTabCleaner(),
]

def get_tab_cleaner(tab) -> TabCleaner:
    for cleaner in tab_cleaners:
        if cleaner.matches(tab):
            return cleaner
    return YoutubeTabCleaner()