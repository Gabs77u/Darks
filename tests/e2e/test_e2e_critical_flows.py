import pytest
from playwright.sync_api import sync_playwright


@pytest.mark.usefixtures("playwright_server")
def test_abre_gui_e_verifica_titulo():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("http://localhost:8000")
        assert "VPN" in page.title() or "Proxy" in page.title() or "Log" in page.title()
        browser.close()
