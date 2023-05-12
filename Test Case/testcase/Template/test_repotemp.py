import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage,test_terminalcommand,test_getusenamefromcookiefile

#region Repository Templates
@pytest.mark.blanktemplate
def test_blankOpenInCodespace(playwright: Playwright):
    blankrepotemp="codespaces-blank"
    test_open_in_codespace(playwright, blankrepotemp)

@pytest.mark.railstemplate
def test_railsOpenInCodespace(playwright: Playwright):
    railsrepotemp="codespaces-rails"
    test_open_in_codespace(playwright, railsrepotemp)

@pytest.mark.reacttemplate
def test_reactOpenInCodespace(playwright: Playwright):
    reactrepotemp="codespaces-react"
    test_open_in_codespace(playwright, reactrepotemp)

@pytest.mark.jupytertemplate
def test_jupyterOpenInCodespace(playwright: Playwright):
    jupyterrepotemp="codespaces-jupyter"
    test_open_in_codespace(playwright, jupyterrepotemp)

@pytest.mark.expresstemplate
def test_expressOpenInCodespace(playwright: Playwright):
    expressrepotemp="codespaces-express"
    test_open_in_codespace(playwright, expressrepotemp)

@pytest.mark.djangotemplate
def test_djangoOpenInCodespace(playwright: Playwright):
    djangorepotemp="codespaces-django"
    test_open_in_codespace(playwright, djangorepotemp)

@pytest.mark.nextjstemplate
def test_nextjsOpenInCodespace(playwright: Playwright):
    nextjsrepotemp="codespaces-nextjs"
    test_open_in_codespace(playwright, nextjsrepotemp)

@pytest.mark.flasktemplate
def test_flaskOpenInCodespace(playwright: Playwright):
    flaskrepotemp="codespaces-flask"
    test_open_in_codespace(playwright, flaskrepotemp)

@pytest.mark.preacttemplate
def test_preactOpenInCodespace(playwright: Playwright):
    preactrepotemp="codespaces-preact"
    test_open_in_codespace(playwright, preactrepotemp)
    
def test_open_in_codespace(playwright: Playwright, repotemp: string):
    githuburl="https://github.com/github/"
    page=test_newtemplatepage(playwright, githuburl+repotemp)
    assert repotemp in page.title()
    page.get_by_role("button", name="Use this template").click()
    page.locator("button", has_text="Open in a codespace").click()
    codespace_page=page.wait_for_event('popup')
    page.close()

    test_terminalcommand(codespace_page, "git status")
    test_validatepublishbutton(codespace_page, repotemp)

def test_validatepublishbutton(codespace_page: Page, repotemp: string):
    codespace_page.wait_for_timeout(10000)
    codespace_page.get_by_role("tab", name="Source Control").click()
    codespace_page.keyboard.press("Control+Shift+G")
    codespace_page.wait_for_timeout(10000)
    if "blank" in repotemp:
      assert codespace_page.get_by_role("button",name="Publish to GitHub").is_visible()
    else:
      assert codespace_page.get_by_role("button",name="Publish Branch").is_visible()
    codespace_page.wait_for_timeout(2000)
    codespace_page.close()
#endregion Repository Templates

#region User this template--create in a new repository
@pytest.mark.blanktemplate
def test_blankTemplates_create_repo(playwright: Playwright):
    blankrepotemp="codespaces-blank"
    test_create_new_repository(playwright, blankrepotemp)

@pytest.mark.railstemplate
def test_railsRepositoryTemplates(playwright: Playwright):
    railsrepotemp="codespaces-rails"
    test_create_new_repository(playwright, railsrepotemp)

@pytest.mark.reacttemplate
def test_reactRepositoryTemplates(playwright: Playwright):
    reactrepotemp="codespaces-react"
    test_create_new_repository(playwright, reactrepotemp)

@pytest.mark.jupytertemplate
def test_jupyterRepositoryTemplates(playwright: Playwright):
    jupyterrepotemp="codespaces-jupyter"
    test_create_new_repository(playwright, jupyterrepotemp)

@pytest.mark.expresstemplate
def test_expressRepositoryTemplates(playwright: Playwright):
    expressrepotemp="codespaces-express"
    test_create_new_repository(playwright, expressrepotemp)

@pytest.mark.djangotemplate
def test_djangoRepositoryTemplates(playwright: Playwright):
    djangorepotemp="codespaces-django"
    test_create_new_repository(playwright, djangorepotemp)

@pytest.mark.nextjstemplate
def test_nextjsRepositoryTemplates(playwright: Playwright):
    nextjsrepotemp="codespaces-nextjs"
    test_create_new_repository(playwright, nextjsrepotemp)

@pytest.mark.flasktemplate
def test_flaskRepositoryTemplates(playwright: Playwright):
    flaskrepotemp="codespaces-flask"
    test_create_new_repository(playwright, flaskrepotemp)

@pytest.mark.preacttemplate
def test_preactRepositoryTemplates(playwright: Playwright):
    preactrepotemp="codespaces-preact"
    test_create_new_repository(playwright, preactrepotemp)

def test_create_new_repository(playwright: Playwright, repotemp: string):
    githuburl="https://github.com/github/"
    page=test_newtemplatepage(playwright, githuburl+repotemp)
    assert repotemp in page.title()
    guid = uuid.uuid4().hex
    page.get_by_role("button", name="Use this template").click()
    page.locator("a", has_text="Create a new repository").click()
    page.get_by_role("button", name="Select an owner").click()
    page.keyboard.press("Tab")
    page.keyboard.press("Enter")
    page.locator("#new_repository_name").fill(repotemp+guid)
    page.locator("button", has_text="Create repository from template" ).click()
    page.wait_for_timeout(9999)
    assert "Latest commit" in page.text_content("h2")
    page.wait_for_timeout(3000)
#endregion