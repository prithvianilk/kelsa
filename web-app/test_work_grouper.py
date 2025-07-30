from work_grouper import ArcProjectNameApplicationWorkGrouper, IdeaProjectNameApplicationWorkGrouper, SlackTabApplicationWorkGrouper

def test_arc_project_name_application_work_grouper():
    arc_project_name_application_work_grouper = ArcProjectNameApplicationWorkGrouper()
    work = [
        [100, "Arc", "2025-01-01 00:00:00"],
        [200, "(1) Arc", "2025-01-01 00:00:00"],
        [300, "(1) (2) Arc", "2025-01-01 00:00:00"],
        [400, "(1)"]
    ]
    expected_regrouped_work = [
        [100, "Arc"],
        [200, "Arc"],
        [300, "(2) Arc"],
        [400, "(1)"]
    ]
    assert expected_regrouped_work == arc_project_name_application_work_grouper.regroup_work_by_tab(work)

def test_idea_project_name_application_work_grouper():
    idea_project_name_application_work_grouper = IdeaProjectNameApplicationWorkGrouper()

    work = [
        [100, "mistletoe – MerchantLogoService.java [mistletoe.application.main]", "2025-01-01 00:00:00"],
        [200, "mistletoe – MerchantLogoService.java [mistletoe.application.main]", "2025-01-01 00:00:00"]
    ]
    expected_regrouped_work = [
        [300, "mistletoe"],
    ]
    assert expected_regrouped_work == idea_project_name_application_work_grouper.regroup_work_by_tab(work)


def test_slack_tab_application_work_grouper_with_date_hour():
    slack_tab_application_work_grouper = SlackTabApplicationWorkGrouper()
    work = [
        [100, "Person 1 (DM) - Company - 16 new items - Slack", "2025-01-01 00:00:00"],
        [200, "Person 1 (DM) - Company - 16 new items - Slack", "2025-01-01 00:00:00"],
        [200, "Person1, Person 2, Person 3, Person 4 (DM) - Company - 12 new items - Slack", "2025-01-01 00:00:00"],
        [300, "Person1, Person 2, Person 3, Person 4 (DM) - Company - 13 new items - Slack", "2025-01-01 00:00:00"],
        [400, "Activity - Company - Slack", "2025-01-01 00:00:00"],
        [500, "Activity - Company - Slack", "2025-01-01 00:00:00"],
        [600, "kelsa-alerts (Channel) - Dreamplug - Slack", "2025-01-01 00:00:00"]
    ]
    expected_regrouped_work = [
        [300, "Person 1 (DM)"],
        [500, "Person1, Person 2, Person 3, Person 4 (DM)"],
        [900, "Activity"],
        [600, "kelsa-alerts (Channel)"]
    ]
    assert expected_regrouped_work == slack_tab_application_work_grouper.regroup_work_by_tab(work)