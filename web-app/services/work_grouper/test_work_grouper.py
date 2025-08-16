from .work_grouper import (
    ArcProjectNameApplicationWorkGrouper,
    IdeaProjectNameApplicationWorkGrouper,
    NoOpApplicationWorkGrouper,
    SlackTabApplicationWorkGrouper
)


def test_arc_youtube_project_name_application_work_grouper():
    arc_project_name_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "Arc", "2025-01-01 00:00:00"],
        [200, "(1) Arc", "2025-01-01 00:00:00"],
        [300, "(1) (2) Arc", "2025-01-01 00:00:00"],
        [400, "(1)", "2025-01-01 00:00:00"],
    ]
    expected_regrouped_work = [[400, "(1)"], [300, "Arc"], [300, "(2) Arc"]]
    assert expected_regrouped_work == arc_project_name_application_work_grouper.regroup_work_by_tab(work)

def test_arc_confluence_project_name_application_work_grouper():
    arc_project_name_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "Add Page - page - TECH - Confluence", "2025-01-01 00:00:00"],
        [200, "Edit - page - TECH - Confluence", "2025-01-01 00:00:00"],
        [300, "page - TECH - Confluence", "2025-01-01 00:00:00"],
        [400, "page-2 - TECH - Confluence", "2025-01-01 00:00:00"],
    ]
    expected_regrouped_work = [
        [600, "page"],
        [400, "page-2"],
    ]
    assert expected_regrouped_work == arc_project_name_application_work_grouper.regroup_work_by_tab(work)

def test_arc_datadog_date_hour_application_work_grouper():
    arc_date_hour_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "Editing Resource post_/api has a high error rate on env:prod | Datadog", "2025-01-01 00:00:00"],
        [100, "service-stage (env:stage) | Datadog", "2025-01-01 00:00:00"],
        [100, "service-prod service.process (env:prod) | Datadog", "2025-01-01 00:00:00"],
        [100, "APM Home (env:dtplcat1) | Datadog", "2025-01-01 00:00:00"],
    ]
    expected_regrouped_work = [[400, "Datadog"]]
    assert expected_regrouped_work == arc_date_hour_application_work_grouper.regroup_work_by_tab(work)

def test_arc_databricks_date_hour_application_work_grouper():
    arc_date_hour_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "New Query 2025-08-06 8:56pm - Databricks", "2025-01-01 00:00:00"],
        [100, "New Query 2025-07-21 5:54pm - Databricks", "2025-01-01 00:00:00"]
    ]
    expected_regrouped_work = [[200, "Databricks"]]
    assert expected_regrouped_work == arc_date_hour_application_work_grouper.regroup_work_by_tab(work)

def test_arc_jenkins_date_hour_application_work_grouper():
    arc_date_hour_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "service-1 - Jenkins", "2025-01-01 00:00:00"],
        [100, "service-2 - Jenkins", "2025-01-01 00:00:00"]
    ]
    expected_regrouped_work = [[200, "Jenkins"]]
    assert expected_regrouped_work == arc_date_hour_application_work_grouper.regroup_work_by_tab(work)

def test_idea_project_name_application_work_grouper():
    idea_project_name_application_work_grouper = IdeaProjectNameApplicationWorkGrouper()

    work = [
        [
            100,
            "mistletoe – MerchantLogoService.java [mistletoe.application.main]",
            "2025-01-01 00:00:00",
        ],
        [
            200,
            "mistletoe – MerchantLogoService.java [mistletoe.application.main]",
            "2025-01-01 00:00:00",
        ],
    ]
    expected_regrouped_work = [
        [300, "mistletoe"],
    ]
    assert (
        expected_regrouped_work
        == idea_project_name_application_work_grouper.regroup_work_by_tab(work)
    )


def test_slack_tab_application_work_grouper_with_date_hour():
    slack_tab_application_work_grouper = SlackTabApplicationWorkGrouper()
    work = [
        [100, "Person 1 (DM) - Company - 16 new items - Slack", "2025-01-01 00:00:00"],
        [200, "Person 1 (DM) - Company - 16 new items - Slack", "2025-01-01 00:00:00"],
        [
            200,
            "Person1, Person 2, Person 3, Person 4 (DM) - Company - 12 new items - Slack",
            "2025-01-01 00:00:00",
        ],
        [
            300,
            "Person1, Person 2, Person 3, Person 4 (DM) - Company - 13 new items - Slack",
            "2025-01-01 00:00:00",
        ],
        [400, "Activity - Company - Slack", "2025-01-01 00:00:00"],
        [500, "Activity - Company - Slack", "2025-01-01 00:00:00"],
        [600, "kelsa-alerts (Channel) - Dreamplug - Slack", "2025-01-01 00:00:00"],
    ]
    expected_regrouped_work = [
        [900, "Activity"],
        [600, "kelsa-alerts (Channel)"],
        [500, "Person1, Person 2, Person 3, Person 4 (DM)"],
        [300, "Person 1 (DM)"]
    ]
    assert expected_regrouped_work == slack_tab_application_work_grouper.regroup_work_by_tab(work)

def test_jio_hotstar_tab_application_work_grouper():
    jio_hotstar_tab_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "Watch Succession S2 Episode 9 on JioHotstar", "2025-01-01 00:00:00"],
        [100, "Watch Succession S1 Episode 10 on JioHotstar", "2025-01-01 00:00:00"],
    ]
    expected_regrouped_work = [[200, "Succession - JioHotstar"]]
    assert expected_regrouped_work == jio_hotstar_tab_application_work_grouper.regroup_work_by_tab(work)


def test_work_grouper_limit():
    work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "1", "2025-01-01 00:00:00"],
        [200, "2", "2025-01-01 00:00:00"],
        [300, "3", "2025-01-01 00:00:00"],
    ]
    assert work_grouper.regroup_work_by_tab(work, limit=1) == [[300, "3"]]
    assert work_grouper.regroup_work_by_tab(work, limit=2) == [[300, "3"], [200, "2"]]
    assert work_grouper.regroup_work_by_tab(work) == [[300, "3"], [200, "2"], [100, "1"]]

def test_work_grouping_by_tab_and_date_hour():
    work_grouper = NoOpApplicationWorkGrouper()
    work = [
        [100, "1", "2025-01-01 00:00:00"],
        [150, "1", "2025-01-01 00:00:00"],
        [200, "2", "2025-01-01 00:00:00"],
        [300, "3", "2025-01-01 00:00:00"],
    ]
    assert work_grouper.regroup_work_by_tab_and_date_hour(work, limit=2) == [[250, "1", "2025-01-01 00:00:00"], [300, "3", "2025-01-01 00:00:00"]]
