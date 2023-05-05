import pytest
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re
import string
from test_commonmethod import test_newtemplatepage

@pytest.mark.daily
@pytest.mark.stop
def test_codespace_auto_stop(playwright : Playwright):
    tempurl="https://github.com/settings/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    test_update_idle_timeout(page,"5")

    page.goto("https://github.com/codespaces/new")
    page.get_by_role("button", name="Select a repository").click()
    page.keyboard.type("VSLSTest2/BookShop")
    page.wait_for_timeout(2000)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    
    page.get_by_role("button", name="production").click()
    page.get_by_role("menuitemradio", name="pre-production").check()
    page.wait_for_timeout(1000)
    assert  page.get_by_role("button", name="pre-production").is_visible()     
    page.wait_for_timeout(2000)
    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(200*1000)
    page.locator(".monaco-button.monaco-text-button", has_text="Stop Now").click()
    page.wait_for_timeout(5000)
    assert "Codespace is stopped" in page.text_content("h4")
    page.wait_for_timeout(1000)
    page.goto("https://github.com/codespaces")
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(200*1000)
    page.locator(".monaco-button.monaco-text-button", has_text="Keep Working").click()
    page.wait_for_timeout(200*1000)
    page.keyboard.press("Control+Shift+E")
    page.get_by_role("button",name="New File...").click()
    page.keyboard.type("htmltest.html")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    page.keyboard.press("Enter")
    page.keyboard.type("<html>htmltest</html>")
    page.wait_for_timeout(160*1000)
    assert "Codespace is stopped" in page.text_content('h4')

    page.goto("https://github.com/settings/codespaces")
    test_update_idle_timeout(page,"30")

def test_update_idle_timeout(page:Page, timeout: string):
    page.wait_for_timeout(2000)
    page.locator("#default-idle-timeout-minutes").fill(timeout)
    page.locator("#default-idle-timeout-header").get_by_role("button",name="Save").click()
    assert "Your Codespaces idle timeout has been updated" in page.get_by_role("alert").inner_text()
    page.wait_for_timeout(1000)

@pytest.mark.daily
@pytest.mark.stop
def test_stop_codespace_from_index_page(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    codeSpaceStatusBefore = page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(4) > div > div.Box-row > div > div:nth-child(2) > div")
    codeSpaceStatustxtBefore = list(filter(None, codeSpaceStatusBefore.nth(0).text_content().replace("\n","").split(" ")))
    
    if "Active" not in codeSpaceStatustxtBefore:
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(3000)
        page.goto("https://github.com/codespaces")

    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Stop codespace").click()
    page.wait_for_timeout(1000)
    page.reload()
    codeSpaceStatusAfter = page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(4) > div > div.Box-row > div > div:nth-child(2) > div")
    codeSpaceStatustxtAfter = list(filter(None, codeSpaceStatusAfter.nth(0).text_content().replace("\n","").split(" ")))
    assert "Active" not in codeSpaceStatustxtAfter

@pytest.mark.stop
def test_stop_current_codespace(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)
    page.get_by_role("button", name="remote Codespaces").click()
    page.get_by_placeholder("Select an option to open a Remote Window").click()
    page.wait_for_timeout(10000)
    page.get_by_placeholder("Select an option to open a Remote Window").fill("stop current codespace")
    page.keyboard.press("Enter")
    page.wait_for_load_state()
    stop_text = page.get_by_role("heading", name="Codespace is stopped").inner_text()
    assert "Codespace is stopped" in stop_text
    

@pytest.mark.stop
def test_stop_current_codespace_F1(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)
    page.locator(".monaco-list > .monaco-scrollable-element").nth(0).click()
    page.keyboard.press("F1")
    page.get_by_placeholder("Type the name of a command to run.").fill(">Codespaces: stop current codespace")
    page.wait_for_timeout(20000)
    page.keyboard.press("Enter")
    page.wait_for_load_state()
    stop_text = page.get_by_role("heading", name="Codespace is stopped").inner_text()
    assert "Codespace is stopped" in stop_text

@pytest.mark.stop
def test_stopcodespace_DevPanel(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)
    page.get_by_title("expand panel").click()
    page.locator(".cs-dev-panel-section__title", has_text="Codespace Commands").click()
    page.wait_for_timeout(1000)
    page.locator(".cs-dev-panel__input.cs-dev-panel__input--button.one").click()
    page.wait_for_timeout(5000)
    assert "Codespace is stopped" in page.text_content("h4")