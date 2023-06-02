import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 

@pytest.mark.daily
@pytest.mark.disconnect
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)

@pytest.mark.daily
@pytest.mark.disconnect
def test_disconnect_ViewCreationLog_codespace(playwright: Playwright):
    pageurl="https://github.com/codespaces/new?location=EastUs"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-python")
        test_createAndinstall(page, "16-core")
        #View Creation Log command
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("View Creation Log")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        assert page.get_by_role("tab").get_by_title("/workspaces/.codespaces/.persistedshare/creation.log").is_visible()
        #disconnect codespace
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: details")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        page.get_by_role("tree").nth(0).hover()
        page.get_by_title("Disconnect").click()
        page.wait_for_timeout(1500)
        assert 'Codespaces' in page.title()
    finally:
        page.close()


