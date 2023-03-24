import pytest
import string
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re

@pytest.mark.delete
def test_deleteAllUnpublish_codespace(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cwayma")
    page = context.new_page()
    page.goto("https://github.com/codespaces?unpublished=true")
    codespaceactionselector="body > div.logged-in.env-production.page-responsive > div.application-main > main>div>div:nth-child(2)>div>div>div.Box-row> div > div:nth-child(2) > div"
    if page.locator(codespaceactionselector).count()>0:
        for i in range(page.locator(codespaceactionselector).count()):
            if(i<page.locator(codespaceactionselector).count()):
                delete_codespace(page, codespaceactionselector)
            else:
                return

def delete_codespace(page:Page, codespaceactionselector: string):
    codespaceconfigureselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(1)"
    codespaceconfigurBeforedelete=page.locator(codespaceconfigureselector).inner_text()
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    if "Active" in page.locator(codespaceactionselector).nth(0).text_content():
        page.keyboard.press("ArrowDown")  
    for i in range(5):
        page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.on("dialog", lambda dialog: dialog.accept())
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)
    page.reload()
    if page.locator(codespaceactionselector).count()>0:  
        codespaceconfigurAfterdelete=page.locator(codespaceconfigureselector).inner_text()
        assert codespaceconfigurBeforedelete not in codespaceconfigurAfterdelete