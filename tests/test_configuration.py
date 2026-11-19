import json

import pytest

from research_council.configuration import Settings


def test_empty_configuration_is_valid_offline(workspace):
    settings = Settings.load(workspace, environ={})
    assert not settings.status()["model_configured"]
    with pytest.raises(ValueError, match="not implemented"):
        settings.require_live()


def test_env_precedence_and_no_secret_output(workspace):
    (workspace / ".env").write_text(
        "COUNCIL_MODEL_PROVIDER=deepseek\nCOUNCIL_MODEL_NAME=example\n"
        "DEEPSEEK_API_KEY=private-value\nTIDB_PASSWORD=database-secret\n"
    )
    settings = Settings.load(workspace, environ={"COUNCIL_MODEL_NAME": "override"})
    assert settings.model_name == "override"
    assert settings.status()["model_configured"]
    assert "private-value" not in json.dumps(settings.status()) + repr(settings)
    assert "database-secret" not in json.dumps(settings.status()) + repr(settings)


def test_dotenv_does_not_expand_or_execute(workspace):
    (workspace / ".env").write_text("DEEPSEEK_API_KEY=${HOME}-$(touch should-not-exist)\n")
    settings = Settings.load(workspace, environ={})
    assert settings.values["DEEPSEEK_API_KEY"] == "${HOME}-$(touch should-not-exist)"
    assert not (workspace / "should-not-exist").exists()
