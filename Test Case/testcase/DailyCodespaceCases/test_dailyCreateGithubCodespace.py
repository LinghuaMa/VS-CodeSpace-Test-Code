import pytest
import string
from playwright.sync_api import Page, Playwright, sync_playwright
import re
import autoit
from test_commonmethod import test_newtemplatepage

def test_createPublicGithubRepo(playwright:Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    page.locator('a',has_text="New codespace").nth(1).click()
    create_page=page.wait_for_event('popup')
    assert "Create a new codespace" in create_page.text_content('h2')
    create_page.wait_for_timeout(1000)
    create_page.get_by_role("button", name="Select a repository").click()
    create_page.keyboard.type("microsoft/vscode-remote-try-node")
    create_page.wait_for_timeout(2000)
    create_page.keyboard.press("ArrowDown")
    create_page.keyboard.press("Enter")
    vscstargetselector="div.Box-body.p-0 > form > div:nth-child(5) > div > details > summary"
    create_page.locator(vscstargetselector).click()
    for i in range(3):
        create_page.keyboard.press("ArrowDown")
    create_page.keyboard.press("Enter")
    create_page.wait_for_timeout(1000)
    assert  create_page.locator(vscstargetselector).inner_text()=="pre-production"
    create_page.wait_for_timeout(3000)

@pytest.mark.rename
def test_rename_codespace(playwright : Playwright):
    tempurl="https://github.com/codespaces"
    codespacerename="CodeSpace-RenamedTesting01"
    page=test_newtemplatepage(playwright, tempurl)
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.wait_for_timeout(1000)
    page.get_by_role("menuitem", name="Rename",exact=True).click()
    page.wait_for_timeout(300)
    page.on("dialog", lambda dialog:dialog.accept(codespacerename))
    page.wait_for_timeout(1000)
    page.keyboard.press("Enter")
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert codespacerename in page.get_by_role("alert").inner_text()
    page.wait_for_timeout(1000)