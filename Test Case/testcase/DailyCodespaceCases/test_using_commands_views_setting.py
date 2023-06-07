import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.daily
@pytest.mark.usingcommands
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.daily
@pytest.mark.usingcommands
def test_open_my_codespace_by_command(playwright: Playwright):
    pageurl="https://github.com/codespaces/new?location=EastUs"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-java")
        test_createAndinstall(page, "4-core")
        page.wait_for_timeout(3000)
        page.get_by_role("button", name="remote Codespaces").click()
        page.get_by_placeholder("Select an option to open a Remote Window").fill("My Codespaces")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1000)
        assert 'https://github.com/codespaces/' in page.context.pages[-1].url
        page.wait_for_timeout(2000)
        page.context.pages[-1].close()
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.usingcommands
def test_kill_vscode_server(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(45000)
        assert page.get_by_role("button", name="Manage").locator("a").is_visible()
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Kill VS Code Server on Host")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(4300)
        assert not page.get_by_role("button", name="Manage").locator("a").is_visible()
        page.wait_for_timeout(10000)
        page.keyboard.press("Control+Shift+E")
        page.wait_for_timeout(1000)
        assert page.get_by_role("button", name="Manage").locator("a").is_visible()
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.usingcommands
def test_download_VSCode(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(45000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Download Visual Studio Code")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert "https://code.visualstudio.com" in page.context.pages[-1].url
        page.context.pages[-1].close()
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.usingcommands
def test_open_close_performance_setting(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(45000)
        page.keyboard.press("Control+,")
        page.wait_for_timeout(1500)
        page.get_by_label("Search settings").fill("Show Performance Explorer")
        if 'No Settings Found' in page.locator(".settings-body").inner_text():
            page.reload()
            page.wait_for_timeout(45000)
            page.keyboard.press("Control+,")
            page.wait_for_timeout(1500)
            page.get_by_label("Search settings").fill("Show Performance Explorer")
        page.get_by_role("checkbox", name="github.codespaces.showPerformanceExplorer").check()
        page.wait_for_timeout(2000)
        assert page.get_by_role("button", name="Codespace Performance Section").is_visible()
        page.get_by_role("checkbox", name="github.codespaces.showPerformanceExplorer").uncheck()
        page.wait_for_timeout(2000)
        assert not page.get_by_role("button", name="Codespace Performance Section").is_visible()
        page.get_by_role("checkbox", name="github.codespaces.showPerformanceExplorer").check()
        page.wait_for_timeout(2000)
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.usingcommands
def test_focus_on_views(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(45000)
        page.get_by_role("tab", name="Remote Explorer").locator("a").click()
        page.wait_for_timeout(1000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Focus on GitHub Codespaces View")
        if page.locator("a", has_text="No matching commands").is_visible():
            page.get_by_role("tab", name="Remote Explorer").locator("a").click()
            page.wait_for_timeout(1000)
            page.keyboard.press("Control+Shift+P")
            page.keyboard.type("Focus on GitHub Codespaces View")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert "VSCS Target: ppe" in page.locator(".last-focused").inner_text()
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Focus on Ports View")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert page.get_by_role("tab", name="Ports", selected=True).is_visible()
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Focus on Codespace Performance View")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert "Codespace ID" in page.locator(".last-focused").inner_text()
    finally:
        page.close()

@pytest.mark.daily
@pytest.mark.usingcommands
def test_show_remote_menu(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(45000)
        page.get_by_role("tab", name="Remote Explorer").locator("a").click()
        page.wait_for_timeout(1000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Show Remote Menu")
        if page.locator("a", has_text="No matching commands").is_visible():
            page.get_by_role("tab", name="Remote Explorer").locator("a").click()
            page.wait_for_timeout(1000)
            page.keyboard.press("Control+Shift+P")
            page.keyboard.type("Show Remote Menu")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert page.get_by_placeholder("Select an option to open a Remote Window").is_visible()
    finally:
        page.close()

    