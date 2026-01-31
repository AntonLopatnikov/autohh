import pytest
from playwright.sync_api import sync_playwright
from data.data import profile_google


@pytest.fixture(scope="session")
def browser_context():
    with sync_playwright() as p:
        profile_path = profile_google
        context = p.chromium.launch_persistent_context(
            user_data_dir=profile_path,
            headless=False,
            channel="chrome",
            no_viewport=True,
            args=[
                "--start-maximized",
                "--disable-blink-features=AutomationControlled",  # Скрывает флаг робота
                "--exclude-switches=enable-automation",  # Убирает инфо-панель сверху
                "--use-fake-ui-for-media-stream",  # На всякий случай для обхода медиа-запросов
            ]
        )

        yield context
        context.close()


@pytest.fixture()
def page(browser_context):
    if len(browser_context.pages) > 0:
        page = browser_context.pages[0]
    else:
        page = browser_context.new_page()

    yield page