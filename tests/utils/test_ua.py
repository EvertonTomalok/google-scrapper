from src.utils.ua import build_user_agents


def test_ua_normal_instance(snapshot):
    all_user_agents = build_user_agents()
    snapshot.assert_match(all_user_agents)


def test_ua_filtered_instance(snapshot):
    all_user_agents = build_user_agents(min_version=65)
    snapshot.assert_match(all_user_agents)

    assert all([
        True if ua["version"] >= 65 else False
        for ua in all_user_agents
    ])
