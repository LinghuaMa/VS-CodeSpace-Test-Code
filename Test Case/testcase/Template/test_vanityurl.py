import string
import json
import uuid
import pytest
from playwright.async_api import Page, Playwright, Browser
from test_commoncode import test_newtemplatepage

#region Vanity URLs
def test_change_option_create_ppe_codespace(playwright:Playwright, tempurl: string, machinetype: string):
    page=test_newtemplatepage(playwright,tempurl)
    page.wait_for_timeout(2000)
    if page.locator("a", has_text="Change options").is_visible():
        page.locator("a", has_text="Change options").click()
    else:
        if page.locator("a", has_text="Create a new one").is_visible():
            page.locator("a", has_text="Create a new one").click()
    page.wait_for_timeout(3000)
    assert page.locator("#js-global-screen-reader-notice", has_text="Create new codespace").is_visible()
    page.get_by_role("button", name="production").click()
    page.get_by_role("menuitemradio", name="pre-production").check()
    page.wait_for_timeout(1400)
    page.get_by_role("button", name="-core").click()
    page.wait_for_timeout(500)
    page.get_by_role("menuitemcheckbox", name=machinetype).click()
    page.wait_for_timeout(1200)
    page.get_by_role("button", name="Create codespace").click()

    page.wait_for_timeout(75000)
    if not "blank" in tempurl:
        for i in range(20):
            if not page.locator("a", has_text="bash").is_visible():
                page.wait_for_timeout(20000)
            else:
                break
        if page.locator("a", has_text="bash").is_visible():
            page.locator("a", has_text="bash").click()
            page.wait_for_timeout(100)
    assert page.get_by_label("Terminal 1, bash Run").is_visible()
    page.close()

@pytest.mark.vanityURLs
@pytest.mark.blanktemplate
def test_changeoptions_blankVanityURLs(playwright: Playwright):
    blanktempurl="https://github.com/codespaces/new?template=blank"
    test_change_option_create_ppe_codespace(playwright, blanktempurl, "16-core")

@pytest.mark.vanityURLs
@pytest.mark.reacttemplate
def test_changeoptions_reactVanityURLs(playwright: Playwright):
    reacttempurl="https://github.com/codespaces/new?template=react"
    test_change_option_create_ppe_codespace(playwright, reacttempurl, "8-core")

@pytest.mark.vanityURLs
@pytest.mark.railstemplate
def test_changeoptions_railsVanityURLs(playwright: Playwright):
    railstempurl="https://github.com/codespaces/new?template=rails"
    test_change_option_create_ppe_codespace(playwright, railstempurl, "4-core")

@pytest.mark.vanityURLs
@pytest.mark.jupytertemplate
def test_changeoptions_jupyterVanityURLs(playwright: Playwright):
    jupytertempurl="https://github.com/codespaces/new?template=jupyter"
    test_change_option_create_ppe_codespace(playwright, jupytertempurl, "4-core")

@pytest.mark.vanityURLs
@pytest.mark.expresstemplate
def test_changeoptions_expressVanityURLs(playwright: Playwright):
    expresstempurl="https://github.com/codespaces/new?template=express"
    test_change_option_create_ppe_codespace(playwright, expresstempurl, "4-core")

@pytest.mark.vanityURLs
@pytest.mark.nextjstemplate
def test_changeoptions_nextjsVanityURLs(playwright: Playwright):
    nextjstempurl="https://github.com/codespaces/new?template=nextjs"
    test_change_option_create_ppe_codespace(playwright, nextjstempurl, "4-core")

@pytest.mark.vanityURLs
@pytest.mark.djangotemplate
def test_changeoptions_djangoVanityURLs(playwright: Playwright):
    djangotempurl="https://github.com/codespaces/new?template=django"
    test_change_option_create_ppe_codespace(playwright, djangotempurl, "4-core")

@pytest.mark.vanityURLs
@pytest.mark.flasktemplate
def test_changeoptions_flaskVanityURLs(playwright: Playwright):
    flasktempurl="https://github.com/codespaces/new?template=flask"
    test_change_option_create_ppe_codespace(playwright, flasktempurl, "4-core")

@pytest.mark.vanityURLs
@pytest.mark.preacttemplate
def test_changeoptions_preactVanityURLs(playwright: Playwright):
    preacttempurl="https://github.com/codespaces/new?template=preact"
    test_change_option_create_ppe_codespace(playwright, preacttempurl, "8-core")

def test_create_production_codespace(playwright: Playwright, tempurl: string):
    page=test_newtemplatepage(playwright, tempurl)
    for i in range(10):
        if page.locator("a", has_text="Resume this codespace").is_visible():
            page.get_by_role("button", name="Codespace configuration").click()
            page.get_by_role("menuitem", name="Delete").click()
            page.on("dialog", lambda dialog: dialog.accept())
            page.keyboard.press("Enter")
            page.wait_for_timeout(3000)
            page.reload()
        else:
            break
    page.locator("button", has_text="Create new codespace").click()
    page.wait_for_timeout(75000)
    if not "blank" in tempurl:
        if page.locator("a", has_text="bash").is_visible():
            page.locator("a", has_text="bash").click()
            page.wait_for_timeout(100)
    assert page.get_by_label("Terminal 1, bash Run").is_visible()
    page.close()

@pytest.mark.vanityURLs
@pytest.mark.blanktemplate
def test_new_blankVanityURLs(playwright: Playwright):
    blanktempurl="https://github.com/codespaces/new?template=blank"
    test_create_production_codespace(playwright, blanktempurl)

@pytest.mark.vanityURLs
@pytest.mark.reacttemplate
def test_new_reactVanityURLs(playwright: Playwright):
    reacttempurl="https://github.com/codespaces/new?template=react"
    test_create_production_codespace(playwright, reacttempurl)

@pytest.mark.vanityURLs
@pytest.mark.railstemplate
def test_new_railsVanityURLs(playwright: Playwright):
    railstempurl="https://github.com/codespaces/new?template=rails"
    test_create_production_codespace(playwright, railstempurl)

@pytest.mark.vanityURLs
@pytest.mark.jupytertemplate
def test_new_jupyterVanityURLs(playwright: Playwright):
    jupytertempurl="https://github.com/codespaces/new?template=jupyter"
    test_create_production_codespace(playwright, jupytertempurl)

@pytest.mark.vanityURLs
@pytest.mark.expresstemplate
def test_new_expressVanityURLs(playwright: Playwright):
    expresstempurl="https://github.com/codespaces/new?template=express"
    test_create_production_codespace(playwright, expresstempurl)

@pytest.mark.vanityURLs
@pytest.mark.nextjstemplate
def test_new_nextjsVanityURLs(playwright: Playwright):
    nextjstempurl="https://github.com/codespaces/new?template=nextjs"
    test_create_production_codespace(playwright, nextjstempurl)

@pytest.mark.vanityURLs
@pytest.mark.djangotemplate
def test_new_djangoVanityURLs(playwright: Playwright):
    djangotempurl="https://github.com/codespaces/new?template=django"
    test_create_production_codespace(playwright, djangotempurl)

@pytest.mark.vanityURLs
@pytest.mark.flasktemplate
def test_new_flaskVanityURLs(playwright: Playwright):
    flasktempurl="https://github.com/codespaces/new?template=flask"
    test_create_production_codespace(playwright, flasktempurl)

@pytest.mark.vanityURLs
@pytest.mark.preacttemplate
def test_new_preactVanityURLs(playwright: Playwright):
    preacttempurl="https://github.com/codespaces/new?template=preact"
    test_create_production_codespace(playwright, preacttempurl)
#endregion Vanity URLs

#region Slightly-less-vanity URLs 
@pytest.mark.vanityURLs
def test_haikusSlightlylessvanityURLs(playwright: Playwright):
    codespacesurl="https://github.com/codespaces/new?template_repository=github/haikus-for-codespaces"
    test_change_option_create_ppe_codespace(playwright, codespacesurl, "4-core")

@pytest.mark.vanityURLs
def test_new_haikusSlightlylessvanityURLs(playwright: Playwright):
    tempurl="https://github.com/codespaces/new?template_repository=github/haikus-for-codespaces"
    test_create_production_codespace(playwright, tempurl) 
#endregion Slightly-less-vanity URLs 