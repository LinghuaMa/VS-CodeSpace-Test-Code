import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo

#region Export/Publish from /Codespaces
@pytest.mark.blankrepositorytemp
def test_blanktemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(1) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "blank")

@pytest.mark.reactrepositorytemp
def test_reacttemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(3) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "react")

@pytest.mark.railsrepositorytemp
def test_railstemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(2) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "rails")

@pytest.mark.jupyterrepositorytemp
def test_jupytertemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(4) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "jupyter")

@pytest.mark.expressrepositorytemp
def test_expresstemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(5) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "express")

@pytest.mark.nextjsrepositorytemp
def test_nextjstemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(6) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "nextjs")

@pytest.mark.djangorepositorytemp
def test_djangotemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(7) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "django")

@pytest.mark.flaskrepositorytemp
def test_flasktemppublishcodespace(playwright: Playwright):
    usethistempbuttonselector="body > div.logged-in.env-production.page-responsive > div.application-main > main > div > div.Layout-main > codespace-zero-config > ol > li:nth-child(8) > div > div:nth-child(3) > form > button"
    test_repositorytempandexportcodespace(playwright, usethistempbuttonselector, "flask")

@pytest.mark.preactrepositorytemp
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
#endregion Export/Publish from /Codespaces