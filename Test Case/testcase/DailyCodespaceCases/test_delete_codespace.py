import pytest
import string
from asyncio import sleep
from playwright.sync_api import Page, Playwright, expect
import re
import getpass
from test_commonmethod import test_open_page_sso,test_open_page_sso

#Do not run this case directly, beacase many cases called this method.
@pytest.mark.delete
def test_deleteAllCodespace(playwright: Playwright):
    tempurl="https://github.com/codespaces"
    page=test_open_page_sso(playwright, tempurl)
    try:
        page.context.pages[-2].close()
        page.reload()
        listcount=page.get_by_role("button", name="Codespace configuration").count()
        if  listcount>0:
            for i in range(listcount):
                page.get_by_role("button", name="Codespace configuration").nth(0).click()
                page.get_by_role("menuitem", name="Delete").click()
                page.on("dialog", lambda dialog: dialog.accept())
                page.keyboard.press("Enter")
                page.wait_for_timeout(3000)
                page.reload()
    finally:
        page.wait_for_timeout(1500)
        page.close()
