from durov_agents.ids import MVP_AGENT_IDS, AgentId
from durov_agents.passport import load_roster


def test_eight_mvp_agents():
    roster = load_roster()
    assert set(roster) == set(MVP_AGENT_IDS)
    assert len(roster) == 8


def test_passports_have_zones_and_forbidden():
    for passport in load_roster().values():
        assert passport.owns
        assert passport.does_not_own
        assert passport.daily_question
        assert passport.forbidden
        assert passport.vault_paths or passport.id == AgentId.LAWYER


def test_lawyer_owns_the_gate():
    lawyer = load_roster()[AgentId.LAWYER]
    assert any("фильтр" in item.lower() or "вердикт" in item.lower() for item in lawyer.owns)
    assert "ворован" in lawyer.purpose
