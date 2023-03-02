from asyncio import sleep
from lib2to3.pgen2 import pgen
from multiprocessing import context
from pydoc import pager
from re import T
import pytest
from playwright.async_api import Page, expect, Playwright, Browser, BrowserContext

@pytest.mark.usereacttemplatecreatecodespace
def test_use_react_template_create_codespace(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    assert 'Your codespaces' in page.text_content('h2')

    #see all template
    templatemaindiv="body > div.logged-in.env-production.page-responsive > div.application-main > main > div"
    showallbuttonselector=templatemaindiv+"> div.Layout-sidebar.p-2 > ul > li:nth-child(1) > nav-list > ul > li > ul > li:nth-child(2)"
    page.locator(showallbuttonselector).click()
    assert 'Choose a template' in page.text_content('h1')
    
    sleep(1500)
    reacttemplateselector=templatemaindiv+" > div.Layout-main > codespace-zero-config > ol > li:nth-child(3) > div > div:nth-child(3) > form > button"
    page.locator(reacttemplateselector).click()
    page.wait_for_timeout(20000)
