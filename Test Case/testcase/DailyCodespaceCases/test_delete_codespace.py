import pytest
import string
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re
from test_commonmethod import test_newtemplatepage

@pytest.mark.delete
def test_deleteAllUnpublish_codespace(playwright: Playwright):
    tempurl="https://github.com/codespaces?unpublished=true"
    page=test_newtemplatepage(playwright, tempurl)
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
    page.get_by_role("menuitem", name="Delete").click()
    page.on("dialog", lambda dialog: dialog.accept())
    page.keyboard.press("Enter")
    page.wait_for_timeout(3000)
    page.reload()
    if page.locator(codespaceactionselector).count()>0:  
        codespaceconfigurAfterdelete=page.locator(codespaceconfigureselector).inner_text()
        assert codespaceconfigurBeforedelete not in codespaceconfigurAfterdelete

@pytest.mark.delete
def test_deleteAllPublishedCodespace(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_newtemplatepage(playwright, tempurl)
    publishedlist=page.locator("body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(4) > div>div")
    publishedlistcount=publishedlist.count()
    if  publishedlistcount>1:
        for i in range(publishedlistcount):
            if(i<publishedlistcount-1):
                page.get_by_role("button", name="Codespace configuration").nth(0).click()
                page.get_by_role("menuitem", name="Delete").click()
                page.on("dialog", lambda dialog: dialog.accept())
                page.keyboard.press("Enter")
                page.wait_for_timeout(3000)
                page.reload()

