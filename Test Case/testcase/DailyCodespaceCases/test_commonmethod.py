import string
import json
import uuid
import pytest
import autoit
from playwright.async_api import Page, Playwright, Browser

def test_newtemplatepage(playwright: Playwright, pageurl: string)-> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cwayma")
    page = context.new_page()
    page.goto(pageurl)
    return page

def test_terminalcommand(page: Page, cmdline: string):
    terminaltextarea="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
    page.type(terminaltextarea, cmdline)
    page.keyboard.press("Enter")

def test_terminalothertemplatecommand(page: Page, cmdline: string, terminaltextarea: string,assertstr:string):
    if "fatal: not a git repository"!=assertstr:
        if page.locator('#list_id_1_0').get_attribute('aria-selected')=="false":
            bashselector="#list_id_1_0 > div > div > div.monaco-icon-label-container"
            page.locator(bashselector).click()
    page.type(terminaltextarea, cmdline)
    page.keyboard.press("Enter")

# @pytest.mark.getgithubuserrepo
def test_getgithubuserrepo(page: Page, reponame: string):
    page.goto(test_getgithubuser()+"/"+reponame)
    page.wait_for_timeout(5000)
    page.reload()
    # assert that a link exists on the page
    assert reponame in page.title()
    page.wait_for_timeout(3000)

def test_getgithubuser() -> string:
    github="https://github.com/"
    return github + test_getusenamefromcookiefile()


def test_getusenamefromcookiefile() -> string:
    # read cookies from the json file
    with open('cwayma', 'r') as f:
      cookies = json.load(f)
    # get a value from the cookies array by name
    for cookie in cookies["cookies"]:
      if cookie['name'] == 'dotcom_user':
        return cookie['value']

def test_create_ppe_codespace(page: Page, reponame: string):
    page.get_by_role("button", name="Select a repository").click()
    page.keyboard.type(reponame)
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

def test_upload_install_vsix(page: Page):
    for i in range(10):
        if ".vsix" not in page.locator("#workbench\.view\.explorer > div > div > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div.pane-body").inner_text():
            if not autoit.win_exists("[CLASS:#32770]"):
                page.mouse.click(x=150, y=500, delay=0, button="right")
                page.wait_for_timeout(1000)
                page.click("text=Upload...")
                page.wait_for_timeout(2000)
            else:
                autoit.control_send("[CLASS:#32770]", "Edit1", 'C:\\Users\\v-margema\\Downloads\\Extension\\codespaces-1.13.10.vsix')
                page.wait_for_timeout(3000)
                autoit.control_click("[Class:#32770]", "Button1")
                page.wait_for_timeout(2500)
        else:
            break
    page.click("div[id='list_id_2_10']")
    page.click("div[id='list_id_2_10']",button="right")
    if page.locator("text=Install Extension VSIX").count()<1:
        page.get_by_role("treeitem").filter(has_text="vsix").click()
        page.get_by_role("treeitem").filter(has_text="vsix").click(button="right")
    page.click("text=Install Extension VSIX")
    page.wait_for_timeout(5000)
    page.get_by_title("Reload Now").click()
    page.wait_for_timeout(15000)