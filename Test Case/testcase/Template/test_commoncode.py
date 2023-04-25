import string
import json
import uuid
import pytest
import getpass
from playwright.async_api import Page, Playwright, Browser

def test_newtemplatepage(playwright: Playwright, pageurl: string)-> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto(pageurl)
    return page

def test_open_page_sso(playwright: Playwright, pageurl: string)-> Page:
    context = playwright.chromium.launch_persistent_context(user_data_dir=f"c:\\User\\{getpass.getuser()}\\AppData\\Local\\Microsoft\\Edge\\User Data",
                                                accept_downloads=True,
                                                headless=False,
                                                bypass_csp=False,
                                                slow_mo=1000,
                                                channel="msedge")    
    page = context.new_page()
    page.storage_state="cway"
    page.goto(pageurl)
    if page.get_by_text("Single sign-on").is_visible():
        page.get_by_text("Single sign-on").click()
        page.get_by_role("button", name="Continue").click()
        page.wait_for_timeout(5000)
    return page

def test_terminalcommand(page: Page, cmdline: string):
    if page.get_by_text("bash").count()==1:
        page.get_by_text("bash").click()
    page.get_by_label("Terminal 1, bash Run").type(cmdline)
    page.keyboard.press("Enter")

def test_terminalothertemplatecommand(page: Page, cmdline: string,assertstr:string):
    if "fatal: not a git repository"!=assertstr and page.get_by_text("bash").count()==1:
        page.get_by_text("bash").click()
    page.keyboard.press("Enter")
    page.wait_for_timeout(1000)
    page.get_by_label("Terminal 1, bash Run").type(cmdline)
    # page.type(terminaltextarea, cmdline)
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
    with open('cway', 'r') as f:
      cookies = json.load(f)
    # get a value from the cookies array by name
    for cookie in cookies["cookies"]:
      if cookie['name'] == 'dotcom_user':
        return cookie['value']