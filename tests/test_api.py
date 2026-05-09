"""Tests for the Throughline API."""

from fastapi.testclient import TestClient

from throughline.api import app

client = TestClient(app)


def test_health_endpoint_returns_ok() -> None:
    """The health endpoint responds with status ok and the current version."""
    response = client.get("/health")

    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "ok"
    assert body["version"] == "0.1.0"
    assert "anthropic_key_loaded" in body


def test_health_endpoint_reports_anthropic_key_status() -> None:
    """The health endpoint reports whether the Anthropic key was loaded.

    The actual value depends on whether .env is loaded in the test environment;
    we only check that the field is present and is a boolean.
    """
    response = client.get("/health")

    body = response.json()
    assert isinstance(body["anthropic_key_loaded"], bool)