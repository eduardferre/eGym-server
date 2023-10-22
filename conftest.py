import asyncio
import textwrap
import pytest


def pytest_emoji_passed(config):
    return "✅ ", "PASSED ✅ "


def pytest_emoji_failed(config):
    return "❌ ", "FAILED ❌ "


def pytest_emoji_skipped(config):
    return "⚠️ ", "SKIPPED ⚠️ "


def pytest_emoji_error(config):
    return "‼️ ", "ERROR ‼️ "


def pytest_emoji_xfailed(config):
    return "🤓 ", "XFAIL 🤓 "


def pytest_emoji_xpassed(config):
    return "😜 ", "XPASS 😜 "


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()
