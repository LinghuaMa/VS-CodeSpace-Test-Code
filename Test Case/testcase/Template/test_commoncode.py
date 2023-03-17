import string
import json
import uuid
import pytest
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

def test_terminalothertemplatecommand(page: Page, cmdline: string, terminaltextarea: string):
    
    page.type(terminaltextarea, cmdline)
    page.keyboard.press("Enter")

# @pytest.mark.getgithubuserrepo
def test_getgithubuserrepo(page: Page, reponame: string):
    page.goto(test_getgithubuser()+"/"+reponame)
    page.wait_for_timeout(2000)
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