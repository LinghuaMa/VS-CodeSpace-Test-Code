import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall,test_upload_install_vsix

def test_valid_devcontainer(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-cpp")
        test_createAndinstall(page, "4-core")
        
        page.get_by_role("button", name="remote Codespaces").click()
        page.locator("a", has_text="Add Dev Container Configuration Files...").click()
        page.locator("a", has_text="Modify your active configuration...").click()
        page.get_by_label("1Password CLI, flexwie, 1Password CLI").check()
        page.get_by_label("act, dhoeric, Install act - run github action locally").check()
        page.get_by_role("button", name="OK").click()
        page.locator("a", has_text="Keep Defaults").click()
        page.get_by_title("Rebuild Now").click()
        page.get_by_role("button", name="Rebuild").click()
        page.wait_for_timeout(500)
        page.get_by_title("expand panel").click()
        page.locator(".cs-dev-panel-section__title").get_by_text("Codespace Commands").click()
        page.locator("button", has_text="😴  Stop").click()
        page.wait_for_timeout(8000)
        page.locator("button", has_text="Restart codespace").click()
        page.wait_for_timeout(99000)
        assert page.get_by_role("dialog").is_visible() and page.get_by_title("View Creation Log").is_visible()
    finally:
        page.close()

def test_rebuild_codespace(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.get_by_role("button", name="remote Codespaces").click()
        page.locator("a", has_text="Add Dev Container Configuration Files...").click()
        page.locator("#list_id_3_0").click()
        page.get_by_label("1Password CLI, flexwie, 1Password CLI").check()
        page.get_by_label("act, dhoeric, Install act - run github action locally").check()
        page.get_by_role("button", name="OK").click()
        page.locator("a", has_text="Keep Defaults").click()
        page.get_by_title("Rebuild Now").click()
        page.get_by_role("button", name="Rebuild").click()
        page.wait_for_timeout(30000)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Rebuild Container")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(300)
        page.locator(".cs-dev-panel-section__title").get_by_text("Codespace Commands").click()
        page.locator("button", has_text="😴  Stop").click()
        page.wait_for_timeout(1500)
        page.locator("button", has_text="Restart codespace").click()
    finally:
        page.close()


@pytest.mark.devcontainer   
def test_create_with_broken_devcontainer(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?location=EastUs"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "broken")
        page.get_by_role("button", name="Create codespace").click()
        page.wait_for_timeout(135000)
        assert page.get_by_role("dialog").is_visible() and page.get_by_title("View Creation Log").is_visible()

        page.get_by_title("View Creation Log").click()
        page.wait_for_timeout(800)
        test_upload_install_vsix(page)
        if page.get_by_title("View Creation Log").is_visible():
            page.get_by_title("View Creation Log").click()
            page.wait_for_timeout(900)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Rebuild Container")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(999)
        page.get_by_role("button", name="Rebuild").click()
        page.wait_for_timeout(500)
        page.get_by_title("expand panel").click()
        page.locator(".cs-dev-panel-section__title").get_by_text("Codespace Commands").click()
        page.locator("button", has_text="😴  Stop").click()
        page.wait_for_timeout(8000)
        page.locator("button", has_text="Restart codespace").click()
        page.wait_for_timeout(135000)
        assert page.get_by_role("dialog").is_visible() and page.get_by_title("View Creation Log").is_visible()
        page.get_by_title("View Creation Log").click()
        page.wait_for_timeout(800)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Rebuild Container")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(999)
        page.get_by_role("button", name="Rebuild").click()
        page.wait_for_timeout(135000)
        assert page.get_by_role("dialog").is_visible() and page.get_by_title("View Creation Log").is_visible()
        page.get_by_title("View Creation Log").click()
        page.wait_for_timeout(800)
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Codespaces: Full Rebuild Container")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(999)
        page.get_by_role("button", name="Rebuild").click()
        page.wait_for_timeout(135000)
        assert page.get_by_role("dialog").is_visible() and page.get_by_title("View Creation Log").is_visible()
    finally:
        page.close()