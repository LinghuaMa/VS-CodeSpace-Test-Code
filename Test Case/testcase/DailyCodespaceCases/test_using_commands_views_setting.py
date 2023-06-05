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
    finally:
        page.close()


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
        page.wait_for_timeout(5000)
        assert not page.get_by_role("button", name="Manage").locator("a").is_visible()
        page.wait_for_timeout(10000)
        page.keyboard.press("Control+Shift+E")
        page.wait_for_timeout(1000)
        assert page.get_by_role("button", name="Manage").locator("a").is_visible()
    finally:
        page.close()