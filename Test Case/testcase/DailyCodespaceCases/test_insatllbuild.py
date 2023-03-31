import pytest
import string
from playwright.sync_api import Page, Playwright, sync_playwright
import re
import autoit
from test_commonmethod import test_newtemplatepage

@pytest.mark.createcodespace
def test_newBookShop_codespace(playwright: Playwright):
    tempurl="https://github.com/codespaces/new"
    page=test_newtemplatepage(playwright, tempurl)
    create_page.get_by_role("button", name="Select a repository").click()
    page.keyboard.type("VSLSTest2/BookShop")
    page.wait_for_timeout(2000)
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    vscstargetselector="div.Box-body.p-0 > form > div:nth-child(5) > div > details > summary"
    page.locator(vscstargetselector).click()
    for i in range(3):
        page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    assert  page.locator(vscstargetselector).inner_text()=="pre-production"     
    page.wait_for_timeout(2000)

    page.get_by_role("button", name="Create codespace").click()
    page.wait_for_timeout(15000)
    for i in range(10):
        if ".vsix" not in page.locator("#workbench\.view\.explorer > div > div > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div.pane-body").inner_text():
            if not autoit.win_exists("[CLASS:#32770]"):
                page.mouse.click(x=150, y=500, delay=0, button="right")
                page.wait_for_timeout(1000)
                page.click("text=Upload...")
                page.wait_for_timeout(2000)
            else:
                autoit.control_send("[CLASS:#32770]", "Edit1", 'C:\\Users\\v-margema\\Downloads\\Extension\\codespaces-1.13.10.vsix')
                page.wait_for_timeout(5000)
                autoit.control_click("[Class:#32770]", "Button1")
        else:
            break
    page.click("div[id='list_id_2_10']")
    page.click("div[id='list_id_2_10']",button="right")
    page.click("text=Install Extension VSIX")
    page.wait_for_timeout(5000)
