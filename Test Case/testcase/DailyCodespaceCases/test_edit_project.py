import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall

@pytest.mark.editproject
def test_debug_project(playwright: Playwright):
    pageurl="https://github.com/codespaces/new?location=SouthEastAsia"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-dotnet")
        test_createAndinstall(page, "2-core")
        
        page.keyboard.press("Control+Shift+P")
        page.keyboard.type("Tasks: Run Build Task")
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
        page.wait_for_timeout(5000)
        assert page.locator(".codicon-terminal-decoration-success").is_visible()
        page.wait_for_timeout(1500)

        page.keyboard.press("F5")
        page.wait_for_timeout(9000)
        assert page.locator("div[class=debug-toolbar]").is_visible()
        page.keyboard.press("Shift+F5")
        page.wait_for_timeout(2000)
    finally:
        page.close()


@pytest.mark.editproject
def test_edit_project(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.mouse.click(x=150, y=500, delay=0, button="left")
        page.get_by_role("button",name="New Folder...").click()
        page.keyboard.type("TestFolder")
        page.keyboard.press("Enter")
        page.get_by_role("button",name="New File...").click()
        page.keyboard.type("htmltest.html")
        page.keyboard.press("Enter")
        page.wait_for_timeout(1500)
        page.keyboard.press("Enter")
        page.keyboard.type("<html>htmltest</html>")
        page.keyboard.press("Control+F")
        assert page.get_by_placeholder("Find").is_visible()
        page.get_by_placeholder("Find").fill("htmltest")
        assert '1 of 1' in page.locator(".matchesCount").inner_text()

        page.keyboard.press("Control+P")
        assert page.get_by_placeholder("Search files").is_visible()
        page.get_by_placeholder("Search files").fill("README")
        page.keyboard.press("Tab")
        page.keyboard.press("Enter")
        assert page.get_by_role("list").get_by_title("/workspaces/vscode-remote-try-dotnet/README.md").is_visible()
    
        page.get_by_role("treeitem", name="TestFolder").locator("a").click()
        page.keyboard.press("F2")
        page.keyboard.type("TestAddedFolder")
        page.keyboard.press("Enter")
        page.wait_for_timeout(2500)
        assert page.get_by_role("treeitem", name="TestAddedFolder").locator("a").is_visible()

        page.keyboard.press("Delete")
        page.on("dialog", lambda dialog: dialog.accept())
        page.keyboard.press("Enter")
        page.wait_for_timeout(2000)
        assert not page.get_by_role("treeitem", name="TestAddedFolder").locator("a").is_visible()
    finally:
        page.close()

@pytest.mark.editproject
def test_edit_project(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.get_by_role("treeitem", name="Program.cs").locator("a").dblclick()
        page.get_by_text("Run").first.click(button="right")
        page.get_by_text("Go to Definition").click()
        page.wait_for_timeout(3000)
    finally:
        page.close()

@pytest.mark.editproject
def test_install_extension_from_market(playwright: Playwright):
    pageurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        page.get_by_role("tab", name="Extensions").click()
        if not page.get_by_label("Search Extensions in Marketplace").is_visible():
            page.get_by_role("tab", name="Extensions").click()
        page.get_by_label("Search Extensions in Marketplace").fill("C# XML Documentation Comments")
        page.locator("div[class=extension-list-item]").filter(has_text="C# XML Documentation Comments").nth(0).click()
        page.locator("a", has_text="Install in Codespaces").click()
        page.wait_for_timeout(5000)
        assert page.get_by_label("Uninstall").is_visible()
    finally:
        page.close()




