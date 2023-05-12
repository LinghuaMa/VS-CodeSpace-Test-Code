import pytest
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re
import string
from test_commonmethod import test_newtemplatepage,test_create_ppe_codespace,test_createAndinstall

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_codespace_auto_stop(playwright : Playwright):
    tempurl="https://github.com/settings/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    test_update_idle_timeout(page,"5")
    try:
        page.goto("https://github.com/codespaces/new?location=SouthEastAsia")
        test_create_ppe_codespace(page, "VSLSTest2/BookShop")
            
        test_createAndinstall(page, "4-core")
        page.wait_for_timeout(150000)
        for i in range(10):
            if not page.get_by_role("button", name="Stop Now").is_visible():
                page.wait_for_timeout(20000)
            else:
                break
        page.get_by_role("button", name="Stop Now").click()
        page.wait_for_timeout(20000)
        assert "Codespace is stopped" in page.text_content("h4")
        page.wait_for_timeout(1000)
        page.get_by_role("button", name="Restart codepsace").click()
        page.wait_for_timeout(150000)
        for i in range(10):
            if not page.get_by_role("button", name="Keep Working").is_visible():
                page.wait_for_timeout(20000)
            else:
                break
        page.get_by_role("button", name="Keep Working").click()
        page.wait_for_timeout(150000)
        page.keyboard.press("Control+Shift+E")
        page.get_by_role("button",name="New File...").click()
        page.keyboard.type("htmltest.html")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        page.keyboard.press("Enter")
        page.keyboard.type("<html>htmltest</html>")
        page.wait_for_timeout(160000)
        assert "Codespace is stopped" in page.text_content('h4')
    finally:
        page.goto("https://github.com/settings/codespaces")
        test_update_idle_timeout(page,"30")
        page.close()

def test_update_idle_timeout(page:Page, timeout: string):
    page.wait_for_timeout(2000)
    page.locator("#default-idle-timeout-minutes").fill(timeout)
    page.locator("#default-idle-timeout-header").get_by_role("button",name="Save").click()
    assert "Your Codespaces idle timeout has been updated" in page.get_by_role("alert").inner_text()
    page.wait_for_timeout(1000)

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_stop_connect_codespace_from_index_page(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    codeSpaceStatusBefore = page.locator("div.Box-row > div > div:nth-child(2) > div")
    codeSpaceStatustxtBefore = list(filter(None, codeSpaceStatusBefore.nth(0).text_content().replace("\n","").split(" ")))
    page.wait_for_timeout(999)
    if "Active" not in codeSpaceStatustxtBefore:
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in JupyterLab").click()
        page.wait_for_timeout(8000)
        page.go_back()
        page.reload()
    page.wait_for_timeout(5000)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Stop codespace").click()
    page.wait_for_timeout(5000)
    page.reload()
    codeSpaceStatusAfter = page.locator("div.Box-row > div > div:nth-child(2) > div")
    codeSpaceStatustxtAfter = list(filter(None, codeSpaceStatusAfter.nth(0).text_content().replace("\n","").split(" ")))
    page.wait_for_timeout(2000)
    assert "Active" not in codeSpaceStatustxtAfter
    page.goto("https://github.com/settings/codespaces")
    test_update_idle_timeout(page,"30")
    page.close()

@pytest.mark.stopandconnect
def test_stop_current_codespace(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.wait_for_timeout(1500)
    page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
    new_page=page.wait_for_event('popup')
    new_page.wait_for_timeout(30000)
    new_page.get_by_role("button", name="remote Codespaces").click()
    new_page.get_by_placeholder("Select an option to open a Remote Window").click()
    new_page.wait_for_timeout(8000)
    new_page.get_by_placeholder("Select an option to open a Remote Window").fill("stop current codespace")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(20000)
    assert "Codespace is stopped" in new_page.text_content("h4")
    new_page.close()
    page.close()
    

@pytest.mark.stopandconnect
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
    page.wait_for_timeout(5000)
    page.keyboard.press("Enter")
    page.wait_for_timeout(20000)
    assert "Codespace is stopped" in page.text_content("h4")
    page.close()

@pytest.mark.stopandconnect
def test_stopcodespace_DevPanel(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(30000)
    page.get_by_title("expand panel").click()
    page.locator(".cs-dev-panel-section__title", has_text="Codespace Commands").click()
    page.wait_for_timeout(2000)
    page.locator("button", has_text="😴  Stop").click()
    page.wait_for_timeout(20000)
    assert "Codespace is stopped" in page.text_content("h4")

@pytest.mark.stopandconnect
def test_connect_lastopened_folder(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.wait_for_timeout(1500)
    page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
    new_page=page.wait_for_event('popup')
    new_page.wait_for_timeout(30000)
    new_page.get_by_label("Application Menu").click()
    new_page.get_by_role("menuitem", name="File").click()
    new_page.get_by_role("menuitem", name="Open Folder...").click()
    new_page.wait_for_timeout(4000)
    new_page.get_by_role("combobox").fill("/workspaces/BookShop/Views/Home/")
    new_page.get_by_role("button", name="OK",  exact=True).click()
    new_page.wait_for_timeout(35000)
    assert "Home [Codespaces]" in new_page.text_content("h3")
    new_page.close()
    page.close()


@pytest.mark.stopandconnect
def test_connect_stress_testing(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.wait_for_timeout(1500)
    page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
    new_page=page.wait_for_event('popup')
    new_page.wait_for_timeout(30000)