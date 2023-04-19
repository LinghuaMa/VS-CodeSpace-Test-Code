import pytest
import string
import getpass
from playwright.sync_api import Page, Playwright
from test_commonmethod import test_open_page_sso,test_create_ppe_codespace


def test_export_changes_to_fork(playwright: Playwright):
    pageurl="https://github.com/codespaces/new?location=EastUs"
    page=test_open_page_sso(playwright,pageurl)
    test_create_ppe_codespace(page, "Microsoft/vscode-remote-try-node")
    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(75000)
    page.goto("https://github.com/codespaces")
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Export changes to a fork").click()
    # page.get_by_role("menuitem", name="Open in browser").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Create branch").click()
    page.wait_for_timeout(45000)
    page.get_by_text("See branch").click()
    assert "forked from" in page.locator("#repository-container-header").inner_text()

def test_export_changes_branch_available_stopped(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    if page.get_by_role("menuitem", name="Stop codespace").is_visible():
        test_export_changes(page)
        page.wait_for_timeout(1000)
        page.get_by_role("menuitem", name="Stop codespace").click()
        page.wait_for_timeout(9000)
    test_export_changes(page)

def test_export_changes_branch_being_connected(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Open in ...").click()
    page.get_by_role("menuitem", name="Open in browser").click()
    page.wait_for_timeout(3000)
    page.go_back()
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Export changes to a branch").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Create branch").click()
    page.wait_for_timeout(45000)
    page.get_by_text("See branch").click()
    assert "forked from" in page.locator("#repository-container-header").inner_text()

def test_export_changes(page:Page):
    page.get_by_role("menuitem", name="Export changes to a branch").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.get_by_role("button", name="Create branch").click()
    page.wait_for_timeout(60000)
    page.get_by_text("See branch").click()
    assert "forked from" in page.locator("#repository-container-header").inner_text()