import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo

#region Repository Templates
@pytest.mark.blanktemplate
def test_blankRepositoryTemplates(playwright: Playwright):
    blankrepotemp="codespaces-blank"
    test_userepositorytemp(playwright, blankrepotemp)

@pytest.mark.railstemplate
def test_railsRepositoryTemplates(playwright: Playwright):
    railsrepotemp="codespaces-rails"
    test_userepositorytemp(playwright, railsrepotemp)

@pytest.mark.reacttemplate
def test_reactRepositoryTemplates(playwright: Playwright):
    reactrepotemp="codespaces-react"
    test_userepositorytemp(playwright, reactrepotemp)

@pytest.mark.jupytertemplate
def test_jupyterRepositoryTemplates(playwright: Playwright):
    jupyterrepotemp="codespaces-jupyter"
    test_userepositorytemp(playwright, jupyterrepotemp)

@pytest.mark.expresstemplate
def test_expressRepositoryTemplates(playwright: Playwright):
    expressrepotemp="codespaces-express"
    test_userepositorytemp(playwright, expressrepotemp)

@pytest.mark.djangotemplate
def test_djangoRepositoryTemplates(playwright: Playwright):
    djangorepotemp="codespaces-django"
    test_userepositorytemp(playwright, djangorepotemp)

@pytest.mark.nextjstemplate
def test_nextjsRepositoryTemplates(playwright: Playwright):
    nextjsrepotemp="codespaces-nextjs"
    test_userepositorytemp(playwright, nextjsrepotemp)

@pytest.mark.flasktemplate
def test_flaskRepositoryTemplates(playwright: Playwright):
    flaskrepotemp="codespaces-flask"
    test_userepositorytemp(playwright, flaskrepotemp)

@pytest.mark.preacttemplate
def test_preactRepositoryTemplates(playwright: Playwright):
    preactrepotemp="codespaces-preact"
    test_userepositorytemp(playwright, preactrepotemp)
    
def test_userepositorytemp(playwright: Playwright, repotemp: string):
    githuburl="https://github.com/github/"
    page=test_newtemplatepage(playwright, githuburl+repotemp)
    assert repotemp in page.title()
    commonbuttonselector="#repo-content-pjax-container > div > div > div.Layout.Layout--flowRow-until-md.Layout--sidebarPosition-end.Layout--sidebarPosition-flowRow-end > div.Layout-main > div.file-navigation.mb-3.d-flex.flex-items-start > span:nth-child(8) > details"
    geenusethembuttonselector=commonbuttonselector+" > summary"
    page.locator(geenusethembuttonselector).click()
    openincodespbuttonselector=commonbuttonselector+" > div > ul > li:nth-child(3) > form > button"
    page.locator(openincodespbuttonselector).click()
    codespace_page=page.wait_for_event('popup')
    page.close()

    test_terminalcommand(codespace_page, "git status")
    test_validatepublishbutton(codespace_page, repotemp)

def test_validatepublishbutton(codespace_page: Page, repotemp: string):
    codespace_page.wait_for_timeout(10000)
    sourcecontrolselector="#workbench\.parts\.activitybar > div > div.composite-bar > div > ul > li:nth-child(3) > a"
    codespace_page.locator(sourcecontrolselector).click()
    codespace_page.wait_for_load_state("networkidle")
    codespace_page.keyboard.press("Control+Shift+G")
    codespace_page.wait_for_timeout(10000)
    if "blank" in repotemp:
      assertselector="#workbench\.view\.scm > div > div > div.monaco-scrollable-element > div.split-view-container > div > div > div.pane-body.welcome > div.welcome-view > div > div.welcome-view-content > div > a"
    else:
      assertselector="#list_id_4_1 > div > div.monaco-tl-contents > div > a"
    assert codespace_page.is_visible(assertselector)
    codespace_page.wait_for_timeout(2000)
    codespace_page.close()
#endregion Repository Templates