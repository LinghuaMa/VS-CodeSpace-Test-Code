import pytest
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re
import string
from test_commonmethod import test_newtemplatepage,test_create_ppe_codespace,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_codespace_auto_stop_then_start(playwright : Playwright):
    tempurl="https://github.com/settings/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    test_update_idle_timeout(page,"5")
    try:
        page.goto("https://github.com/codespaces/new?location=SouthEastAsia")
        test_create_ppe_codespace(page, "VSLSTest2/BookShop")
            
        test_createAndinstall(page, "4-core")
        page.wait_for_timeout(100000)
        page.get_by_role("button", name="Notifications", exact=True).click()
        for i in range(30):
            if not page.get_by_role("button", name="Stop Now").is_visible():
                page.wait_for_timeout(15000)
            else:
                break
        page.get_by_role("button", name="Stop Now").click()
        page.wait_for_timeout(20000)
        assert "Codespace is stopped" in page.text_content("h4")
        page.wait_for_timeout(1000)
        page.locator("button", has_text="Restart codespace").click()
        page.wait_for_timeout(100000)
        page.get_by_role("button", name="Notifications", exact=True).click()
        for i in range(30):
            if not page.get_by_role("button", name="Keep Working").is_visible():
                page.wait_for_timeout(15000)
            else:
                break
        page.get_by_role("button", name="Keep Working").click()
        page.wait_for_timeout(5000)
        page.keyboard.press("Control+Shift+E")
        page.get_by_role("button",name="New File...").click()
        page.wait_for_timeout(1000)
        page.keyboard.type("htmltest.html")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        page.keyboard.press("Enter")
        page.keyboard.type("<html>htmltest</html>")
        page.wait_for_timeout(3000)
        page.keyboard.press("Control+Shift+G")
        page.wait_for_timeout(1000)
        assert page.get_by_label("html, Untracked").is_visible()
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
    try:
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
    finally:
        page.goto("https://github.com/settings/codespaces")
        test_update_idle_timeout(page,"30")
        page.close()

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_stop_current_codespace(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.wait_for_timeout(1500)
        page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
        new_page=page.wait_for_event('popup')
        new_page.wait_for_timeout(30000)
        if new_page.locator("button", has_text="Restart codespace").is_visible():
            new_page.locator("button", has_text="Restart codespace").click()
            new_page.wait_for_timeout(30000)
        new_page.get_by_role("button", name="remote Codespaces").click()
        new_page.get_by_placeholder("Select an option to open a Remote Window").click()
        new_page.wait_for_timeout(800)
        new_page.get_by_placeholder("Select an option to open a Remote Window").fill("stop current codespace")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(20000)
        assert "Codespace is stopped" in new_page.text_content("h4")
        new_page.close()
    finally:
        page.close()
    
@pytest.mark.daily
@pytest.mark.stopandconnect
def test_stop_current_codespace_F1(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
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
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_stopcodespace_DevPanel(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try: 
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
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_connect_lastopened_folder(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.wait_for_timeout(1500)
        page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
        new_page=page.wait_for_event('popup')
        new_page.wait_for_timeout(30000)
        if new_page.locator("button", has_text="Restart codespace").is_visible():
            new_page.locator("button", has_text="Restart codespace").click()
            new_page.wait_for_timeout(30000)
        test_open_folder(new_page, "/workspaces/BookShop/Views/Home/")
        assert "Home [Codespaces]" in new_page.text_content("h3")
        test_open_folder(new_page, "/workspaces/BookShop")
    finally:
        new_page.close()
        page.close()

def test_open_folder(new_page: Page, folderpath: string):
    new_page.get_by_label("Application Menu").click()
    new_page.get_by_role("menuitem", name="File").click()
    new_page.get_by_role("menuitem", name="Open Folder...").click()
    new_page.wait_for_timeout(2000)
    new_page.get_by_role("combobox").fill("/workspaces/BookShop/Views/Home/")
    new_page.wait_for_timeout(1000)
    new_page.get_by_role("button", name="OK",  exact=True).click()
    new_page.wait_for_timeout(35000)

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_connect_stress_testing(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.wait_for_timeout(1500)
        page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
        new_page=page.wait_for_event('popup')
        new_page.wait_for_timeout(30000)
        if new_page.locator("button", has_text="Restart codespace").is_visible():
            new_page.locator("button", has_text="Restart codespace").click()
            new_page.wait_for_timeout(30000)
        new_page.get_by_role("tab", name="Remote Explorer").locator("a").click()
        new_page.get_by_label("Terminal 1, bash Run").type("sudo apt-get update")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(3000)
        new_page.get_by_label("Terminal 1, bash Run").type("sudo apt-get install stress-ng")
        new_page.keyboard.press("Enter")
        new_page.keyboard.press("Y")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(7000)
        new_page.get_by_label("Terminal 1, bash Run").type("stress-ng --cpu 4")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(3000)

        new_page.keyboard.press("Control+Shift+`")
        new_page.wait_for_timeout(8000)
        new_page.get_by_label("Terminal 2, bash Run").type("stress-ng --vm-bytes $(awk '/MemAvailable/{printf '%d\n',$2 * 1;}' < /proc/meminfo)k --vm-keep -m 1")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(99000)
        alertmessage="High codespace CPU (100%) utilization detected. Consider stopping some processes for the best experience., source: GitHub Codespaces (Extension), notification"
        for i in range(10):
            if not new_page.get_by_role("dialog", name=alertmessage).is_visible():
                new_page.wait_for_timeout(9000)
            else:
                break
        assert new_page.get_by_role("dialog", name=alertmessage).is_visible()
    finally:
        new_page.close()

@pytest.mark.ignore
def test_connect_after_deleting_home_directory(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.wait_for_timeout(1500)
        page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
        new_page=page.wait_for_event('popup')
        new_page.wait_for_timeout(40000)
        new_page.get_by_label("Terminal 1, bash Run").type("sudo rm -rf ~")
        new_page.keyboard.press("Enter")
    finally:
        new_page.close()

@pytest.mark.daily
@pytest.mark.stopandconnect
def test_connect_after_renaming_other_directory(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    try:
        page.wait_for_timeout(1500)
        page.locator("a[data-test-selector='codespace-url']", has_text="✨").nth(0).click()
        new_page=page.wait_for_event('popup')
        new_page.wait_for_timeout(40000)
        
        new_page.get_by_label("Application Menu").click()
        new_page.get_by_role("menuitem", name="File").click()
        new_page.get_by_role("menuitem", name="Open Folder...").click()
        new_page.wait_for_timeout(4000)
        new_page.get_by_role("combobox").fill("/workspaces/")
        new_page.wait_for_timeout(2000)
        new_page.get_by_role("button", name="OK",  exact=True).click()
        new_page.wait_for_timeout(35000)
        new_page.get_by_title("/workspaces/BookShop • Contains emphasized items").click(button="right")
        new_page.locator("text=Rename").click()
        new_page.wait_for_timeout(800)
        new_page.keyboard.type("NewBookShop")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(9000)
        new_page.keyboard.press("Control+Shift+P")
        new_page.keyboard.type("Codespace: Stop Current codespace")
        new_page.keyboard.press("ArrowDown")
        new_page.keyboard.press("Enter")
        new_page.wait_for_timeout(20000)
        new_page.get_by_title("expand panel").click()
        new_page.locator(".cs-dev-panel-section__title", has_text="Codespace Commands").click()
        new_page.wait_for_timeout(2000)
        new_page.locator("button", has_text="😴  Stop").click()
        new_page.wait_for_timeout(20000)
        new_page.locator("button", has_text="Restart codespace").click()
        new_page.wait_for_timeout(40000)
        if new_page.get_by_role("button", name="Cancel").is_visible():
            new_page.get_by_role("button", name="Cancel").click()
        new_page.wait_for_timeout(8000)
        assert new_page.get_by_title("/workspaces/BookShop", exact=True).is_visible()
        assert new_page.get_by_title("/workspaces/NewBookShop • Contains emphasized items", exact=True).is_visible()
    finally:
        new_page.close()