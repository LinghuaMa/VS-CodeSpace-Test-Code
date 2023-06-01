import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace,test_createAndinstall
from test_delete_codespace import test_deleteAllCodespace 


@pytest.mark.exportChanges
def test_delete_all_codespaces(playwright: Playwright):
    test_deleteAllCodespace(playwright)


@pytest.mark.exportChanges
def test_export_changes_to_fork(playwright: Playwright):
    pageurl="https://github.com/codespaces/new?location=EastUs"
    page=test_open_page_sso(playwright,pageurl)
    try:
        page.context.pages[-2].close()
        test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-node")
        test_createAndinstall(page, "4-core")
    
        page.goto("https://github.com/codespaces")
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Export changes to a fork").click()
        # page.get_by_role("menuitem", name="Open in browser").click()
        page.on("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Create branch").click()
        page.wait_for_timeout(45000)
        page.get_by_text("See branch").click()
        assert "forked from" in page.locator("#repository-container-header").inner_text()
        page.go_back()
        page.reload()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        if "Codespace is stopped" in page.text_content("h4"):
            page.get_by_text("Restart codespace").click()
        page.wait_for_timeout(30000) 
        page.get_by_role("tab", name="Explorer").click()
        page.mouse.click(x=150, y=500, delay=0, button="left")  
        test_addnewfile(page,"htmltest.html")
        page.goto("https://github.com/codespaces")
        page.wait_for_timeout(3000)
    finally:
        page.close()


@pytest.mark.exportChanges
def test_export_changes_branch_active(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()    
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        assert page.get_by_role("menuitem", name="Stop codespace").is_visible()
        page.get_by_role("menuitem", name="Export changes to a branch").click()
        page.on("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Create branch").click()
        page.wait_for_timeout(45000)
        page.get_by_text("See branch").click()
        assert "forked from" in page.locator("#repository-container-header").inner_text()
        page.wait_for_timeout(3000)
    finally:
        page.close()


@pytest.mark.exportChanges
def test_export_changes_branch_available_stopped(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()    
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(30000)
        # if 
        test_addnewfile(page,"htmltest01.html")
        page.go_back()
        page.wait_for_timeout(900)
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        if page.get_by_role("menuitem", name="Stop codespace").is_visible():
            test_export_changes(page)
            page.wait_for_timeout(1000)
            page.go_back()
            page.reload()
            page.wait_for_timeout(900)
            page.get_by_role("button", name="Codespace configuration").nth(0).click()
            page.wait_for_timeout(900)
        test_export_changes(page)
        page.wait_for_timeout(3000)
    finally:
        page.close()


@pytest.mark.exportChanges
def test_export_changes_branch_being_connected(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close() 
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        if "Codespace is stopped" in page.text_content("h4"):
            page.get_by_text("Restart codespace").click()
        page.wait_for_timeout(30000)
        # if 
        test_addnewfile(page,"htmltest02.html")
        page.go_back()
        page.reload()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Open in ...").click()
        page.get_by_role("menuitem", name="Open in browser").click()
        page.wait_for_timeout(1000)
        page.go_back()
        page.get_by_role("button", name="Codespace configuration").nth(0).click()
        page.get_by_role("menuitem", name="Export changes to a branch").click()
        page.on("dialog", lambda dialog: dialog.accept())
        page.get_by_role("button", name="Create branch").click()
        page.wait_for_timeout(45000)
        page.get_by_text("See branch").click()
        assert "forked from" in page.locator("#repository-container-header").inner_text()
        page.wait_for_timeout(3000)
    finally:
        page.close()

def test_export_changes(page:Page):
    page.get_by_role("menuitem", name="Export changes to a branch").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Create branch").click()
    page.wait_for_timeout(60000)
    page.get_by_text("See branch").click()
    assert "forked from" in page.locator("#repository-container-header").inner_text()

def test_addnewfile(page:Page, filename:string):
    page.keyboard.press("Control+Shift+E")
    page.get_by_role("button",name="New File...").click()
    page.keyboard.type(filename)
    page.keyboard.press("Enter")
    page.wait_for_timeout(1500)
    page.keyboard.press("Enter")
    page.keyboard.type("<html>htmltest</html>")
    page.wait_for_timeout(2000)