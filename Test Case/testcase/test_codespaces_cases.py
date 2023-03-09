import string
import json
import uuid
from asyncio import sleep
from lib2to3.pgen2 import pgen
from multiprocessing import context
from pydoc import pager
from re import T
import pytest
from playwright.async_api import Page, expect, Playwright, Browser, BrowserContext

# @pytest.mark.usereacttemplatecreatecodespace
def test_use_react_template_create_codespace(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto("https://github.com/codespaces")
    assert 'Your codespaces' in page.text_content('h2')

    #see all template
    templatemaindiv="body > div.logged-in.env-production.page-responsive > div.application-main > main > div"
    showallbuttonselector=templatemaindiv+"> div.Layout-sidebar.p-2 > ul > li:nth-child(1) > nav-list > ul > li > ul > li:nth-child(2)"
    page.locator(showallbuttonselector).click()
    assert 'Choose a template' in page.text_content('h1')
    
    sleep(1500)
    reacttemplateselector=templatemaindiv+" > div.Layout-main > codespace-zero-config > ol > li:nth-child(3) > div > div:nth-child(3) > form > button"
    page.locator(reacttemplateselector).click()
    sleep(30000)
    page.wait_for_timeout(20000)

def test_newtemplatepage(playwright: Playwright, pageurl: string)-> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto(pageurl)
    return page

@pytest.mark.githubhaikusforcodespaces
def test_new_githubhaikuspage(playwright: Playwright):
    githubhaikusurl="https://github.com/github/haikus-for-codespaces"
    page=test_newtemplatepage(playwright,githubhaikusurl)
    assert page.title()=="github/haikus-for-codespaces"
    commonbuttonselector="#repo-content-pjax-container > div > div > div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div.Layout-main > div.file-navigation.mb-3.d-flex.flex-items-start > span:nth-child(8) > details"
    geenusethembuttonselector=commonbuttonselector+" > summary"
    page.locator(geenusethembuttonselector).click()
    openincodespbuttonselector=commonbuttonselector+" > div > ul > li:nth-child(3) > form > button"
    page.locator(openincodespbuttonselector).click()
    assert page.wait_for_event('popup')
    page.wait_for_timeout(2000)

@pytest.mark.reacttemplatecreatecodespace
def test_new_reacttemplatepage(playwright: Playwright):
    reacttempurl="https://github.com/codespaces/new?template=react"
    page=test_newtemplatepage(playwright,reacttempurl)
    assert 'Create a new codespace' in page.text_content('h2')
    page.wait_for_timeout(2000)

@pytest.mark.checkunpublishstatus
def test_checkunpublishstatus(playwright: Playwright):
    haikusforcodespacesurl="https://github.com/codespaces?unpublished=true"
    page=test_newtemplatepage(playwright,haikusforcodespacesurl)
    assert 'Your codespaces' in page.text_content('h2')
    # f="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > div > p"
    b="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(1) > div:nth-child(1) > div > p"
    # d="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(7) > div > div:nth-child(1) > div:nth-child(1) > div > p"
    # e="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(9) > div > div:nth-child(1) > div:nth-child(1) > div > p"
    assert "Created from" in page.locator(b).inner_text()
    page.wait_for_timeout(2000)

@pytest.mark.haikusforcodespacesopenpage
def test_new_haikusforcodespacespage(playwright: Playwright):
    haikusforcodespacesurl="https://github.com/codespaces/new?template_repository=github/haikus-for-codespaces"
    page=test_newtemplatepage(playwright,haikusforcodespacesurl)
    assert 'Create a new codespace' in page.text_content('h2')
    page.wait_for_timeout(2000)

@pytest.mark.blanktemplatecreatecodespace
def test_blank_template_create_codespace_(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="cway")
    page = context.new_page()
    page.goto("https://github.com/codespaces/new?template=blank")
    assert 'Create a new codespace' in page.text_content('h2')

    templatemaindiv="body > div.logged-in.env-production.page-responsive > div.application-main > main"
    blankbutton=templatemaindiv+" > new-codespace > div.js-codespaces-completable > div.Box.position-relative.container-sm > div > div > div:nth-child(3) > form > button"
    page.locator(blankbutton).click()
    new_page = page.wait_for_event('popup')

    terminaltextarea="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
    new_page.type(terminaltextarea,"git status")
    new_page.keyboard.press("Enter")
    commondactionselecter="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-decoration-container > div.codicon.error.terminal-command-decoration.xterm-decoration.codicon-terminal-decoration-error"
    new_page.locator(commondactionselecter).click()
    for i in range(3):
        new_page.keyboard.press("ArrowDown")
    new_page.keyboard.press("Enter")
    searchselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(2) > a"
    new_page.locator(searchselector).click()
    searchtextarea="#workbench\.view\.search > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body > div.search-view.actions-right > div.search-widgets-container > div.search-widget > div.search-container.input-box > div > div.monaco-scrollable-element > div.monaco-inputbox.idle > div > textarea"
    new_page.locator(searchtextarea).click()
    new_page.keyboard.press("Control+V")
    assert "fatal: not a git repository" in new_page.locator(searchtextarea).input_value()

    #create a new file named htmltest.html
    new_page.keyboard.press("Control+Shift+E")
    newfileactionselector="#workbench\.view\.explorer > div > div > div.monaco-scrollable-element > div.split-view-container > div:nth-child(1) > div > div.pane-header.expanded > div.actions > div > div > ul > li:nth-child(1)"
    new_page.locator(newfileactionselector).click()
    new_page.keyboard.type("htmltest.html")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(1500)
    new_page.keyboard.press("Enter")
    new_page.keyboard.type("<html>htmltest</html>")
    sourcecontrolselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(3) > a"
    new_page.locator(sourcecontrolselector).click()
    publishtogithubselector="#workbench\.view\.scm > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.welcome > div.welcome-view > div > div.welcome-view-content > div > a"
    new_page.locator(publishtogithubselector).click()
    
    #rename reponame
    reponameselector="#js-vscode-workbench-placeholder > div > div.quick-input-widget.show-file-icons > div.quick-input-header > div.quick-input-and-message > div.quick-input-filter > div.quick-input-box > div > div.monaco-inputbox.idle > div > input"
    oldreponame=new_page.locator(reponameselector).input_value()
    guid = uuid.uuid4().hex
    new_page.locator(reponameselector).fill(oldreponame+guid)
    new_page.wait_for_timeout(1000)
    new_page.keyboard.press("ArrowDown")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(1000)
    new_page.keyboard.press("Tab")
    new_page.keyboard.press("Enter")
    new_page.wait_for_timeout(3000)
    test_getgithubuserrepo(browser, oldreponame+guid)
    page.wait_for_timeout(3000)


@pytest.mark.getgithubuserrepo
def test_getgithubuserrepo(browser: Browser, reponame: string):
    page = browser.new_page()
    page.goto(test_getgithubuser()+"/"+reponame)
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
        


# def getnewpagebyclickusethistemplate(page) -> page:
#     new_page = page.wait_for_event('popup')
#     terminaltextarea="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
#     new_page.type(terminaltextarea,"git status")
#     new_page.keyboard.press("Enter")
#     commondactionselecter="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-decoration-container > div.codicon.error.terminal-command-decoration.xterm-decoration.codicon-terminal-decoration-error"
#     new_page.locator(commondactionselecter).click()
#     for i in range(3):
#         new_page.keyboard.press("ArrowDown")
#     new_page.keyboard.press("Enter")
#     searchselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(2) > a"
#     new_page.locator(searchselector).click()
#     searchtextarea="#workbench\.view\.search > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body > div.search-view.actions-right > div.search-widgets-container > div.search-widget > div.search-container.input-box > div > div.monaco-scrollable-element > div.monaco-inputbox.idle > div > textarea"
#     new_page.locator(searchtextarea).click()
#     new_page.keyboard.press("Control+V")
#     assert "fatal: not a git repository" in new_page.locator(searchtextarea).input_value() 
#     return new_page

@pytest.mark.forgotpassword01
def test_open_forgotpassword(page: Page) -> Page:
      page.goto("https://github.com/codespaces")
      # //a[contains(@href, "/password_reset")]
      # a[href*="/password_reset"]
      page.click("a[href*='/password_reset']")
      assert 'Reset your password' in page.text_content('h1')
    #   assert 'Reset your password' in page.inner_text('h1')
    #   page.wait_for_timeout(300)
    #   page.get_attribute("login_field").fill("v-margema@microsoft.com")
    #   page.get("password").fill("Extensibility123456")
      page.url
      new_page = page.wait_for_event('popup')
      newpagetitle=new_page.title()
      newpageurl=new_page.url()
      terminaltextarea="#terminal > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.shell-integration.integrated-terminal.wide > div.monaco-split-view2.horizontal > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div > div > div > div.xterm-screen > div.xterm-helpers > textarea"
      new_page.type(terminaltextarea,"git status")
      new_page.locator("")
      page.wait_for_timeout(3000)
