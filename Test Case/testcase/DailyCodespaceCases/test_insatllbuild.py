import pytest
import string
from playwright.sync_api import Page, Playwright, sync_playwright
import re
import autoit
from test_commonmethod import test_newtemplatepage,test_create_ppe_codespace,test_upload_install_vsix

# 4-core;US West
@pytest.mark.createcodespace   
def test_newBookShop_codespace(playwright: Playwright):
    tempurl="https://github.com/codespaces/new"
    page=test_newtemplatepage(playwright, tempurl)
    test_create_ppe_codespace(page, "VSLSTest2/BookShop")
    #4-core
    page.get_by_role("button", name="2-core").click()
    page.wait_for_timeout(500)
    page.keyboard.press("Tab")
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    assert page.get_by_role("button", name="4-core").count()==1

    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(15000)
    test_upload_install_vsix(page)
