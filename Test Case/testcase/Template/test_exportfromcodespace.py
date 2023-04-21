import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo

#region Export/Publish from /Codespaces
@pytest.mark.blanktemplate
def test_blanktemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 0, "blank")

@pytest.mark.reacttemplate
def test_reacttemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 2, "react")

@pytest.mark.railstemplate
def test_railstemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 1, "rails")

@pytest.mark.jupytertemplate
def test_jupytertemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 3, "jupyter")

@pytest.mark.expresstemplate
def test_expresstemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 4, "express")

@pytest.mark.nextjstemplate
def test_nextjstemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 5, "nextjs")

@pytest.mark.djangotemplate
def test_djangotemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 6, "django")

@pytest.mark.flasktemplate
def test_flasktemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 7, "flask")

@pytest.mark.preacttemplate
def test_preacttemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 8, "preact")

def test_repositorytempandexportcodespace(playwright: Playwright, nth: int, tempname: string):
    tempurl="https://github.com/codespaces/templates"
    page=test_newtemplatepage(playwright, tempurl)
    assert "Choose a template" in page.text_content('h1')

    page.get_by_label("VSCS target").click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert page.get_by_label("VSCS target").input_value()=="ppe"
    
    page.locator("button", has_text="Use this template").nth(nth).click()
    codespace_page=page.wait_for_event('popup')
    codespace_page.wait_for_timeout(120000)
    test_terminalcommand(codespace_page, "git status")
    test_validatepublishbutton(codespace_page, tempname)
    
    # Export/Publish from /Codespaces
    page.goto("https://github.com/codespaces?unpublished=true")
    page.get_by_role("button", name="Codespace configuration").nth(0).click()
    page.get_by_role("menuitem", name="Publish to a new repository").click()
    page.wait_for_timeout(1000)
    publishreponameselector="#publish-codespace-repo-name"
    guid = uuid.uuid4().hex
    page.query_selector_all(publishreponameselector)[0].fill(tempname+guid)
    page.locator("button", has_text="Create repository").click()
    page.wait_for_timeout(2000)
    test_getgithubuserrepo(page, tempname+guid)
    page.wait_for_timeout(3000)

def test_validatepublishbutton(codespace_page: Page, repotemp: string):
    codespace_page.wait_for_timeout(10000)
    codespace_page.keyboard.press("Control+Shift+G")
    codespace_page.wait_for_timeout(10000)
    if "blank" in repotemp:
      assert codespace_page.get_by_role("button",name="Publish to GitHub").is_visible()
    else:
      assert codespace_page.get_by_role("button",name="Publish Branch").is_visible()
    codespace_page.wait_for_timeout(2000)
    codespace_page.close()

#endregion Export/Publish from /Codespaces