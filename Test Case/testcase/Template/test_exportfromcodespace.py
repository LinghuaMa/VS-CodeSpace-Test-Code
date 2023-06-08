import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getgithubuserrepo

#region Export/Publish from /Codespaces
@pytest.mark.exporttemplate
@pytest.mark.blanktemplate
def test_blanktemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 0, "blank")

@pytest.mark.exporttemplate
@pytest.mark.reacttemplate
def test_reacttemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 2, "react")

@pytest.mark.exporttemplate
@pytest.mark.railstemplate
def test_railstemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 1, "rails")

@pytest.mark.exporttemplate
@pytest.mark.jupytertemplate
def test_jupytertemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 3, "jupyter")

@pytest.mark.exporttemplate
@pytest.mark.expresstemplate
def test_expresstemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 4, "express")

@pytest.mark.exporttemplate
@pytest.mark.nextjstemplate
def test_nextjstemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 5, "nextjs")

@pytest.mark.exporttemplate
@pytest.mark.djangotemplate
def test_djangotemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 6, "django")

@pytest.mark.exporttemplate
@pytest.mark.flasktemplate
def test_flasktemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 7, "flask")

@pytest.mark.exporttemplate
@pytest.mark.preacttemplate
def test_preacttemppublishcodespace(playwright: Playwright):
    test_repositorytempandexportcodespace(playwright, 8, "preact")

def test_repositorytempandexportcodespace(playwright: Playwright, nth: int, tempname: string):
    tempurl="https://github.com/codespaces/templates"
    page=test_newtemplatepage(playwright, tempurl)
    assert page.locator(".application-main", has_text="Choose a template").is_visible()

    page.get_by_label("VSCS target").click()
    page.keyboard.press("ArrowDown")
    page.keyboard.press("Enter")
    assert page.get_by_label("VSCS target").input_value()=="ppe"
    
    page.locator("button", has_text="Use this template").nth(nth).click()
    codespace_page=page.wait_for_event('popup')
    codespace_page.wait_for_timeout(120000)
    test_terminalcommand(codespace_page, "git status")
    test_addnewfileandnavigatetosoucontrol(codespace_page)
    
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
    page.wait_for_timeout(60000)
    page.locator("a", has_text="See repository").click()
    page.wait_for_timeout(2000)
    assert tempname+guid in page.title()
    page.wait_for_timeout(500)
    page.close()

def test_addnewfileandnavigatetosoucontrol(page:Page):
    page.keyboard.press("Control+Shift+E")
    page.wait_for_timeout(1000)
    page.mouse.click(x=150, y=500, delay=0, button="left")
    page.get_by_role("button",name="New File...").click()
    page.keyboard.type("htmltest.html")
    page.wait_for_timeout(300)
    page.keyboard.press("Enter")
    page.wait_for_timeout(8000)
    page.keyboard.press("Enter")
    page.keyboard.type("<html>htmltest</html>")
    page.keyboard.press("Control+Shift+G")
    page.wait_for_timeout(1000)

def test_validatepublishbutton(codespace_page: Page, repotemp: string):
    codespace_page.wait_for_timeout(8000)
    
    if "blank" in repotemp:
      assert codespace_page.get_by_role("button",name="Publish to GitHub").is_visible()
    else:
        codespace_page.get_by_label('Message (Ctrl+Enter to commit on "main")').fill("add a html file for test")
        codespace_page.get_by_role("treeitem", name="Changes" ).click()
        codespace_page.get_by_title("Stage All Changes").click()
        codespace_page.wait_for_timeout(1000)
        codespace_page.get_by_title('Commit Changes on "main"').click()
        codespace_page.wait_for_timeout(4000)
        assert codespace_page.get_by_role("button",name="Publish Branch").is_visible()
    codespace_page.wait_for_timeout(2000)
    codespace_page.close()

#endregion Export/Publish from /Codespaces