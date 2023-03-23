import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo

#region Export/Publish from /Codespaces
@pytest.mark.blanktemplate
def test_blanktemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(1) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "blank")

@pytest.mark.reacttemplate
def test_reacttemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(3) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "react")

@pytest.mark.railstemplate
def test_railstemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(2) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "rails")

@pytest.mark.jupytertemplate
def test_jupytertemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(4) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "jupyter")

@pytest.mark.expresstemplate
def test_expresstemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(5) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "express")

@pytest.mark.nextjstemplate
def test_nextjstemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(6) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "nextjs")

@pytest.mark.djangotemplate
def test_djangotemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(7) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "django")

@pytest.mark.flasktemplate
def test_flasktemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(8) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "flask")

@pytest.mark.preacttemplate
def test_preacttemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(9) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "preact")

def test_repositorytempandexportcodespace(playwright: Playwright, buttonselector: string, tempname: string):
    tempurl="https://github.com/codespaces/templates"
    page=test_newtemplatepage(playwright, tempurl)
    assert "Choose a template" in page.text_content('h1')

    ppeselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > div > div:nth-child(2) > div > select"
    page.locator(ppeselector).click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert page.locator(ppeselector).input_value()=="ppe"
    
    page.locator(buttonselector).click()
    codespace_page=page.wait_for_event('popup')
    codespace_page.wait_for_timeout(6000)
    test_terminalcommand(codespace_page, "git status")
    test_validatepublishbutton(codespace_page, tempname)
    
    # Export/Publish from /Codespaces
    page.goto("https://github.com/codespaces?unpublished=true")
    spaceconfig='body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div.Box-row > div > div:nth-child(2) > div > div.right-0.top-0.top-lg-auto.right-lg-auto.position-absolute.position-lg-relative > options-popover>details:nth-child(1)'
    summaryselector=spaceconfig+">summary"
    page.query_selector_all(summaryselector)[0].click()
    publishareposelector=spaceconfig+"> details-menu > button:nth-child(4) > span"
    page.query_selector_all(publishareposelector)[0].click()
    page.wait_for_timeout(1000)
    publishreponameselector="#publish-codespace-repo-name"
    guid = uuid.uuid4().hex
    page.query_selector_all(publishreponameselector)[0].fill(tempname+guid)
    button="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > div:nth-child(3) > div > div:nth-child(2) > div > div:nth-child(2) > div > div.right-0.top-0.top-lg-auto.right-lg-auto.position-absolute.position-lg-relative > options-popover > details:nth-child(3) > details-dialog>div:nth-child(3)>export-branch>div>form>button"
    page.query_selector_all(button)[0].click()
    test_getgithubuserrepo(page, tempname+guid)
    page.wait_for_timeout(3000)

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

#endregion Export/Publish from /Codespaces