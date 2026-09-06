from durov_agents.cli import main


def test_roster_cli(capsys):
    assert main(["roster"]) == 0
    out = capsys.readouterr().out
    assert "координатор" in out
    assert "юрист" in out


def test_run_cli_block(capsys):
    assert main(["run", "ворованная информация конкурентов"]) == 0
    out = capsys.readouterr().out
    assert "block" in out.lower() or "блок" in out.lower()


def test_label_plan_cli(capsys):
    assert main(["label", "plan"]) == 0
    assert "domain_legal" in capsys.readouterr().out
